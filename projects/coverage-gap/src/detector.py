#!/usr/bin/env python3
"""
Coverage Gap Detector for Executive News Briefs.

Evaluates whether a news brief adequately covered what was available
from public sources for a given roster of entities and time window.

Usage:
    python detector.py --roster ../sample-roster.json --brief brief.txt
    python detector.py --roster ../sample-roster.json --brief brief.txt --days 1
    python detector.py --roster ../sample-roster.json --sweep-only
"""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from typing import Optional
from urllib.request import urlopen, Request
from urllib.error import URLError

# ---------------------------------------------------------------------------
# Stage 1 — Roster loading
# ---------------------------------------------------------------------------

def load_roster(path: str) -> dict:
    """Load a roster JSON file. Returns the parsed dict."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    roster = data.get("roster", [])
    for entry in roster:
        if "aliases" not in entry:
            entry["aliases"] = []
        if "company" not in entry:
            entry["company"] = ""
    return data


def entity_names(roster: list[dict]) -> list[str]:
    """Return all matchable names (primary + aliases + companies)."""
    names = []
    for entry in roster:
        names.append(entry["name"])
        names.extend(entry.get("aliases", []))
        if entry.get("company"):
            names.append(entry["company"])
    return names


# ---------------------------------------------------------------------------
# Stage 2 — Source sweep (RSS)
# ---------------------------------------------------------------------------

def fetch_rss(url: str, timeout: int = 15) -> list[dict]:
    """
    Fetch and parse an RSS feed. Returns a list of headline dicts:
    [{"title": str, "link": str, "published": str, "source_url": str}]

    Uses feedparser if available, otherwise falls back to stdlib XML parsing.
    """
    try:
        import feedparser
        return _fetch_with_feedparser(url, timeout)
    except ImportError:
        return _fetch_with_stdlib(url, timeout)


def _fetch_with_feedparser(url: str, timeout: int) -> list[dict]:
    import feedparser
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries:
        items.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "source_url": url,
        })
    return items


def _fetch_with_stdlib(url: str, timeout: int) -> list[dict]:
    """Parse RSS XML with stdlib. Handles both RSS 2.0 and Atom."""
    req = Request(url, headers={"User-Agent": "CoverageGapDetector/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except (URLError, OSError) as e:
        print(f"  Warning: could not fetch {url}: {e}", file=sys.stderr)
        return []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        print(f"  Warning: could not parse XML from {url}", file=sys.stderr)
        return []

    items = []
    # RSS 2.0: channel/item
    for item in root.iter("item"):
        title = _xml_text(item, "title")
        link = _xml_text(item, "link")
        pub = _xml_text(item, "pubDate")
        items.append({
            "title": title,
            "link": link,
            "published": pub,
            "source_url": url,
        })
    # Atom: entry
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
        title = _xml_text(entry, "{http://www.w3.org/2005/Atom}title")
        link_el = entry.find("{http://www.w3.org/2005/Atom}link")
        link = link_el.get("href", "") if link_el is not None else ""
        pub = _xml_text(entry, "{http://www.w3.org/2005/Atom}published") or \
              _xml_text(entry, "{http://www.w3.org/2005/Atom}updated")
        items.append({
            "title": title,
            "link": link,
            "published": pub,
            "source_url": url,
        })
    return items


def _xml_text(parent, tag: str) -> str:
    el = parent.find(tag)
    return (el.text or "").strip() if el is not None else ""


def sweep_sources(
    roster: list[dict],
    sources: list[dict],
    days: int = 1,
) -> list[dict]:
    """
    Sweep all RSS sources and filter to headlines mentioning rostered entities.
    Returns list of headline dicts with an added 'matched_entities' field.
    """
    all_names = entity_names(roster)
    # Build case-insensitive patterns
    patterns = []
    for name in all_names:
        # Match whole words/phrases
        patterns.append((name, re.compile(re.escape(name), re.IGNORECASE)))

    all_headlines = []
    for source in sources:
        url = source.get("rss_url", "")
        source_name = source.get("name", url)
        if not url:
            continue
        print(f"  Fetching {source_name}...", file=sys.stderr)
        items = fetch_rss(url)
        print(f"    Got {len(items)} items", file=sys.stderr)
        for item in items:
            item["source_name"] = source_name
        all_headlines.extend(items)

    # Filter to entity-relevant headlines
    relevant = []
    for h in all_headlines:
        title = h.get("title", "")
        matched = []
        for name, pattern in patterns:
            if pattern.search(title):
                matched.append(name)
        if matched:
            h["matched_entities"] = matched
            relevant.append(h)

    return relevant


# ---------------------------------------------------------------------------
# Stage 3 — Syndication deduplication
# ---------------------------------------------------------------------------

SIMILARITY_THRESHOLD = 0.75


def deduplicate(headlines: list[dict], threshold: float = SIMILARITY_THRESHOLD) -> list[dict]:
    """
    Cluster near-identical headlines. Returns a list of unique story dicts,
    each with a 'cluster' field listing all source headlines.
    """
    clusters: list[dict] = []

    for h in headlines:
        title = h.get("title", "")
        placed = False
        for cluster in clusters:
            rep_title = cluster["title"]
            sim = SequenceMatcher(None, _normalize(title), _normalize(rep_title)).ratio()
            if sim >= threshold:
                cluster["cluster"].append(h)
                # Merge matched entities
                for ent in h.get("matched_entities", []):
                    if ent not in cluster["matched_entities"]:
                        cluster["matched_entities"].append(ent)
                placed = True
                break
        if not placed:
            clusters.append({
                "title": title,
                "matched_entities": list(h.get("matched_entities", [])),
                "cluster": [h],
                "source_count": 1,
            })

    # Update source counts
    for c in clusters:
        source_names = set()
        for item in c["cluster"]:
            source_names.add(item.get("source_name", item.get("source_url", "")))
        c["source_count"] = len(source_names)
        c["sources"] = sorted(source_names)

    return clusters


def _normalize(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# Stage 4 — Brief evaluation
# ---------------------------------------------------------------------------

def evaluate_brief(
    brief_text: str,
    unique_stories: list[dict],
    roster: list[dict],
    consensus_threshold: int = 2,
) -> dict:
    """
    Score a brief against the available story universe.

    Returns:
        {
            "coverage_score": float (0-100),
            "entity_coverage": {entity_name: {"available": int, "covered": int}},
            "total_available": int,
            "total_covered": int,
            "missed_consensus": [story dicts where source_count >= threshold],
            "dedup_stats": {"raw_headlines": int, "unique_stories": int},
        }
    """
    brief_lower = brief_text.lower()

    # Map roster entries to their matchable names
    entity_map = {}
    for entry in roster:
        primary = entry["name"]
        all_names_for_entity = [primary] + entry.get("aliases", [])
        if entry.get("company"):
            all_names_for_entity.append(entry["company"])
        entity_map[primary] = all_names_for_entity

    # Check which stories the brief covers
    covered_stories = []
    missed_stories = []

    for story in unique_stories:
        story_title_lower = _normalize(story["title"])
        # A story is "covered" if the brief mentions enough of its key terms
        # We check: does the brief mention any of the story's matched entities
        # AND contain words distinctive to the headline?
        is_covered = _story_in_brief(story, brief_lower)
        if is_covered:
            covered_stories.append(story)
        else:
            missed_stories.append(story)

    # Entity coverage breakdown
    entity_coverage = {}
    for primary, names in entity_map.items():
        available = 0
        covered = 0
        for story in unique_stories:
            story_entities = story.get("matched_entities", [])
            if any(n in story_entities for n in names):
                available += 1
                if story in covered_stories:
                    covered += 1
        entity_coverage[primary] = {"available": available, "covered": covered}

    # Missed consensus stories (carried by 2+ sources but not in the brief)
    missed_consensus = [
        s for s in missed_stories
        if s.get("source_count", 1) >= consensus_threshold
    ]

    # Coverage score
    total_available = len(unique_stories)
    total_covered = len(covered_stories)
    coverage_score = (total_covered / total_available * 100) if total_available > 0 else 100.0

    # Dedup stats
    raw_count = sum(len(s.get("cluster", [s])) for s in unique_stories)

    return {
        "coverage_score": round(coverage_score, 1),
        "entity_coverage": entity_coverage,
        "total_available": total_available,
        "total_covered": total_covered,
        "missed_consensus": missed_consensus,
        "dedup_stats": {
            "raw_headlines": raw_count,
            "unique_stories": total_available,
        },
    }


def _story_in_brief(story: dict, brief_lower: str) -> bool:
    """
    Determine whether a story is covered by the brief text.
    A story is considered covered if the brief mentions at least one of its
    matched entities AND contains at least 2 distinctive words from the headline.
    """
    # Check entity mention
    entities = story.get("matched_entities", [])
    entity_mentioned = any(e.lower() in brief_lower for e in entities)
    if not entity_mentioned:
        return False

    # Check for distinctive headline words in the brief
    title_words = set(_normalize(story["title"]).split())
    # Remove common stopwords
    stopwords = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
        "has", "have", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "shall", "its", "it", "that", "this",
        "as", "not", "no", "new", "says", "said", "also", "more", "than",
        "over", "after", "up", "out", "about",
    }
    distinctive = title_words - stopwords
    # Also remove entity names from distinctive words (they're already matched)
    for e in entities:
        for word in e.lower().split():
            distinctive.discard(word)

    if not distinctive:
        return entity_mentioned

    brief_normalized = set(_normalize(brief_lower).split())
    overlap = distinctive & brief_normalized
    return len(overlap) >= min(2, len(distinctive))


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def format_report(result: dict) -> str:
    """Format the evaluation result as a human-readable report."""
    lines = []
    lines.append("=" * 60)
    lines.append("COVERAGE GAP REPORT")
    lines.append("=" * 60)
    lines.append("")

    score = result["coverage_score"]
    lines.append(f"Coverage score: {score}/100")
    lines.append(f"Stories available: {result['total_available']}")
    lines.append(f"Stories covered:  {result['total_covered']}")
    lines.append("")

    dedup = result["dedup_stats"]
    lines.append(f"Dedup: {dedup['raw_headlines']} raw headlines → "
                 f"{dedup['unique_stories']} unique stories")
    lines.append("")

    # Entity breakdown
    lines.append("-" * 40)
    lines.append("ENTITY COVERAGE")
    lines.append("-" * 40)
    for entity, stats in result["entity_coverage"].items():
        avail = stats["available"]
        cov = stats["covered"]
        pct = (cov / avail * 100) if avail > 0 else 0
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        lines.append(f"  {entity:<25} {cov}/{avail} {bar} {pct:.0f}%")
    lines.append("")

    # Missed consensus
    missed = result["missed_consensus"]
    lines.append("-" * 40)
    lines.append(f"MISSED CONSENSUS STORIES ({len(missed)})")
    lines.append("-" * 40)
    if missed:
        for story in missed:
            sources = ", ".join(story.get("sources", []))
            lines.append(f"  [{story['source_count']} sources] {story['title']}")
            lines.append(f"    Sources: {sources}")
            lines.append(f"    Entities: {', '.join(story['matched_entities'])}")
            lines.append("")
    else:
        lines.append("  None — the brief covered all consensus stories.")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Coverage Gap Detector for Executive News Briefs"
    )
    parser.add_argument(
        "--roster", required=True,
        help="Path to roster JSON file"
    )
    parser.add_argument(
        "--brief",
        help="Path to brief text file to evaluate"
    )
    parser.add_argument(
        "--days", type=int, default=1,
        help="Number of days back to sweep (default: 1)"
    )
    parser.add_argument(
        "--sweep-only", action="store_true",
        help="Only sweep sources and report available stories (no brief evaluation)"
    )
    parser.add_argument(
        "--consensus-threshold", type=int, default=2,
        help="Minimum sources for a story to count as 'consensus' (default: 2)"
    )
    parser.add_argument(
        "--output-json", action="store_true",
        help="Output results as JSON instead of formatted report"
    )

    args = parser.parse_args()

    # Load roster
    print("Loading roster...", file=sys.stderr)
    data = load_roster(args.roster)
    roster = data["roster"]
    sources = data.get("sources", [])
    print(f"  {len(roster)} entities, {len(sources)} sources", file=sys.stderr)

    # Sweep sources
    print("\nSweeping sources...", file=sys.stderr)
    headlines = sweep_sources(roster, sources, days=args.days)
    print(f"\n  {len(headlines)} relevant headlines found", file=sys.stderr)

    # Deduplicate
    print("Deduplicating...", file=sys.stderr)
    unique_stories = deduplicate(headlines)
    print(f"  {len(unique_stories)} unique stories", file=sys.stderr)

    if args.sweep_only:
        print("\n--- Available stories ---")
        for i, story in enumerate(unique_stories, 1):
            print(f"\n{i}. [{story['source_count']} source(s)] {story['title']}")
            print(f"   Entities: {', '.join(story['matched_entities'])}")
            print(f"   Sources: {', '.join(story.get('sources', []))}")
        return

    # Load brief
    if not args.brief:
        print("Error: --brief is required unless --sweep-only is set", file=sys.stderr)
        sys.exit(1)

    with open(args.brief, "r", encoding="utf-8") as f:
        brief_text = f.read()

    # Evaluate
    print("Evaluating brief...", file=sys.stderr)
    result = evaluate_brief(
        brief_text, unique_stories, roster,
        consensus_threshold=args.consensus_threshold,
    )

    if args.output_json:
        # Make JSON-serializable (remove cluster details)
        output = {**result}
        output["missed_consensus"] = [
            {"title": s["title"], "source_count": s["source_count"],
             "sources": s.get("sources", []), "matched_entities": s["matched_entities"]}
            for s in output["missed_consensus"]
        ]
        print(json.dumps(output, indent=2))
    else:
        print("\n" + format_report(result))


if __name__ == "__main__":
    main()
