#!/usr/bin/env python3
"""
Executive Writing Critic — deterministic scoring for executive documents.

Analyzes text against an explicit executive writing bar and returns
line-level findings with an overall letter grade.

Usage:
    python3 critic.py < document.txt
    python3 critic.py --file document.txt
    python3 critic.py --json --file document.txt

No external dependencies. Pure Python stdlib.
"""

import argparse
import json
import math
import re
import statistics
import sys
import textwrap
from collections import Counter

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HEDGE_WORDS = [
    "might", "possibly", "somewhat", "arguably", "perhaps",
    "likely", "probably", "fairly", "rather", "quite",
]

HEDGE_PHRASES = [
    "it seems", "i think",
]

# Common passive auxiliaries paired with past-participle patterns.
PASSIVE_RE = re.compile(
    r"\b(is|are|was|were|been|being|be|get|gets|got|gotten)\s+"
    r"(\w+ly\s+)?(\w+ed|written|taken|made|done|seen|given|told|shown"
    r"|built|sent|found|held|known|left|run|set|read|kept|thought"
    r"|brought|bought|caught|taught|felt|lost|paid|met|put|cut)\b",
    re.IGNORECASE,
)

# POS-approximation: common adjectives that appear before nouns.
# We use a broad regex: word ending in -ful, -ous, -ive, -ble, -al, -ent,
# -ant, -ic, -less, -ary, or one of a short explicit list.
ADJ_SUFFIX_RE = re.compile(
    r"\b\w{3,}(?:ful|ous|ive|ble|ial|ual|ent|ant|tic|less|ary|ing)\b",
    re.IGNORECASE,
)
EXPLICIT_ADJECTIVES = {
    "good", "great", "big", "small", "new", "old", "long", "short",
    "high", "low", "best", "worst", "key", "clear", "fast", "slow",
    "hard", "soft", "deep", "wide", "real", "true", "false", "raw",
    "top", "main", "next", "last", "full", "free", "open", "flat",
    "rich", "poor", "safe", "dark", "bold", "lean", "sharp", "quick",
}

# For paragraph-one specificity: named entities, numbers, concrete nouns.
NUMBER_RE = re.compile(r"\b\d[\d,.%$]*\b")
NAMED_ENTITY_RE = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b")
CONCRETE_NOUN_INDICATORS = re.compile(
    r"\b(?:team|product|customer|user|revenue|cost|quarter|year|week"
    r"|month|company|market|launch|release|system|server|app|tool"
    r"|budget|headcount|pipeline|roadmap|sprint|milestone|deadline"
    r"|API|SDK|dashboard|database|report|metric|KPI|OKR)\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Sentence and paragraph splitting
# ---------------------------------------------------------------------------

def split_sentences(text):
    """Split text into sentences. Handles common abbreviations."""
    # Protect common abbreviations from splitting.
    protected = text
    for abbr in ["Mr.", "Mrs.", "Dr.", "Jr.", "Sr.", "vs.", "e.g.", "i.e.", "etc."]:
        protected = protected.replace(abbr, abbr.replace(".", "<DOT>"))

    parts = re.split(r'(?<=[.!?])\s+', protected)
    sentences = []
    for p in parts:
        restored = p.replace("<DOT>", ".").strip()
        if restored:
            sentences.append(restored)
    return sentences


def split_paragraphs(text):
    """Split text into paragraphs on blank lines."""
    blocks = re.split(r'\n\s*\n', text.strip())
    return [b.strip() for b in blocks if b.strip()]

# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_hedges(sentences):
    """Flag hedge/weasel words with line-level detail."""
    findings = []
    total_hedges = 0
    for i, sent in enumerate(sentences, 1):
        lower = sent.lower()
        found = []
        for hw in HEDGE_WORDS:
            # Match whole word only.
            if re.search(rf"\b{re.escape(hw)}\b", lower):
                found.append(hw)
        for hp in HEDGE_PHRASES:
            if hp in lower:
                found.append(hp)
        if found:
            total_hedges += len(found)
            findings.append({
                "sentence": i,
                "text": sent,
                "hedges": found,
            })

    rate = total_hedges / max(len(sentences), 1)
    # Grade: 0 hedges = A, <5% = B, <10% = C, <20% = D, else F
    if rate == 0:
        grade = "A"
    elif rate < 0.05:
        grade = "B"
    elif rate < 0.10:
        grade = "C"
    elif rate < 0.20:
        grade = "D"
    else:
        grade = "F"

    return {
        "name": "Hedge / weasel words",
        "grade": grade,
        "hedge_count": total_hedges,
        "sentence_count": len(sentences),
        "rate": round(rate, 3),
        "findings": findings,
    }


def check_passive(sentences):
    """Estimate passive voice rate."""
    passive_count = 0
    findings = []
    for i, sent in enumerate(sentences, 1):
        if PASSIVE_RE.search(sent):
            passive_count += 1
            findings.append({
                "sentence": i,
                "text": sent,
            })

    rate = passive_count / max(len(sentences), 1)
    if rate < 0.10:
        grade = "A"
    elif rate < 0.20:
        grade = "B"
    elif rate < 0.30:
        grade = "C"
    elif rate < 0.45:
        grade = "D"
    else:
        grade = "F"

    return {
        "name": "Passive voice",
        "grade": grade,
        "passive_count": passive_count,
        "sentence_count": len(sentences),
        "rate": round(rate, 3),
        "findings": findings,
    }


def check_data_density(sentences):
    """Measure claims vs. supporting data.

    A 'data sentence' contains a number, percentage, dollar amount,
    or explicit metric. An 'assertion sentence' is one that doesn't.
    High assertion-to-data ratio means the writing is making claims
    without backing them up.
    """
    data_sents = 0
    assertion_sents = 0
    flagged = []
    for i, sent in enumerate(sentences, 1):
        if NUMBER_RE.search(sent):
            data_sents += 1
        else:
            assertion_sents += 1
            flagged.append({"sentence": i, "text": sent})

    if len(sentences) == 0:
        ratio = 0
    else:
        ratio = data_sents / len(sentences)

    # Grade on data density: >30% = A, >20% = B, >10% = C, >5% = D, else F
    if ratio > 0.30:
        grade = "A"
    elif ratio > 0.20:
        grade = "B"
    elif ratio > 0.10:
        grade = "C"
    elif ratio > 0.05:
        grade = "D"
    else:
        grade = "F"

    return {
        "name": "Data density",
        "grade": grade,
        "data_sentences": data_sents,
        "assertion_sentences": assertion_sents,
        "density": round(ratio, 3),
        "findings": flagged[:10],  # Cap at 10 to keep output readable.
    }


def count_adjectives(sent):
    """Approximate adjective count in a sentence."""
    count = 0
    words = re.findall(r"\b\w+\b", sent.lower())
    for w in words:
        if w in EXPLICIT_ADJECTIVES:
            count += 1
        elif ADJ_SUFFIX_RE.match(w) and w not in {"something", "nothing", "everything", "anything"}:
            count += 1
    return count


def check_adjective_bloat(sentences):
    """Flag sentences with excessive adjective density."""
    threshold = 3  # Adjectives per sentence.
    findings = []
    counts = []
    for i, sent in enumerate(sentences, 1):
        c = count_adjectives(sent)
        counts.append(c)
        if c >= threshold:
            findings.append({
                "sentence": i,
                "text": sent,
                "adjective_count": c,
            })

    avg = sum(counts) / max(len(counts), 1)
    if avg < 1.0:
        grade = "A"
    elif avg < 1.5:
        grade = "B"
    elif avg < 2.0:
        grade = "C"
    elif avg < 2.5:
        grade = "D"
    else:
        grade = "F"

    return {
        "name": "Adjective bloat",
        "grade": grade,
        "avg_adjectives_per_sentence": round(avg, 2),
        "threshold": threshold,
        "flagged_sentences": len(findings),
        "findings": findings,
    }


def check_sentence_variance(sentences):
    """Measure sentence length variance. Low variance = monotonous."""
    if len(sentences) < 3:
        return {
            "name": "Sentence length variance",
            "grade": "N/A",
            "note": "Too few sentences to assess.",
            "findings": [],
        }

    lengths = [len(s.split()) for s in sentences]
    avg = statistics.mean(lengths)
    stdev = statistics.stdev(lengths)
    cv = stdev / avg if avg > 0 else 0  # Coefficient of variation.

    # Grade on CV: >0.5 = A, >0.35 = B, >0.25 = C, >0.15 = D, else F
    if cv > 0.50:
        grade = "A"
    elif cv > 0.35:
        grade = "B"
    elif cv > 0.25:
        grade = "C"
    elif cv > 0.15:
        grade = "D"
    else:
        grade = "F"

    return {
        "name": "Sentence length variance",
        "grade": grade,
        "mean_words": round(avg, 1),
        "stdev_words": round(stdev, 1),
        "coefficient_of_variation": round(cv, 3),
        "sentence_lengths": lengths,
        "findings": [] if grade in ("A", "B") else [{
            "note": f"Sentences are too uniform. Mean {avg:.0f} words, "
                    f"stdev {stdev:.1f}. Mix in short punchy lines.",
        }],
    }


def check_buried_lede(paragraphs, sentences):
    """Check whether the first paragraph contains the key claim.

    Heuristic: the first paragraph should contain an imperative framing
    (a recommendation, a number, a named action) rather than pure background.
    """
    if not paragraphs:
        return {
            "name": "Buried lede",
            "grade": "N/A",
            "note": "No paragraphs found.",
            "findings": [],
        }

    first_para = paragraphs[0]
    first_lower = first_para.lower()

    # Positive signals: contains a recommendation verb or a number.
    action_verbs = [
        "recommend", "propose", "request", "ship", "launch", "build",
        "cut", "increase", "reduce", "approve", "invest", "hire",
        "cancel", "prioritize", "decide", "commit",
    ]
    has_action = any(v in first_lower for v in action_verbs)
    has_number = bool(NUMBER_RE.search(first_para))
    has_directive = any(
        first_lower.startswith(w)
        for w in ["we should", "i recommend", "the ask", "my recommendation",
                   "bottom line", "summary", "tldr", "tl;dr"]
    )

    score = sum([has_action, has_number, has_directive])

    if score >= 2:
        grade = "A"
    elif score == 1:
        grade = "B"
    else:
        # Check for pure background signals.
        background_starts = ["in recent", "over the past", "historically",
                             "as you know", "background", "context"]
        starts_with_bg = any(first_lower.startswith(b) for b in background_starts)
        grade = "F" if starts_with_bg else "C"

    findings = []
    if grade in ("C", "D", "F"):
        findings.append({
            "text": first_para[:200] + ("..." if len(first_para) > 200 else ""),
            "note": "First paragraph lacks a clear ask, recommendation, or number. "
                    "Lead with the point; add context after.",
        })

    return {
        "name": "Buried lede",
        "grade": grade,
        "has_action_verb": has_action,
        "has_number": has_number,
        "has_directive_opening": has_directive,
        "findings": findings,
    }


def check_opening_specificity(paragraphs):
    """Check whether the opening paragraph contains concrete detail."""
    if not paragraphs:
        return {
            "name": "Opening specificity",
            "grade": "N/A",
            "note": "No paragraphs found.",
            "findings": [],
        }

    first = paragraphs[0]
    has_number = bool(NUMBER_RE.search(first))
    has_entity = bool(NAMED_ENTITY_RE.search(first))
    has_concrete_noun = bool(CONCRETE_NOUN_INDICATORS.search(first))

    score = sum([has_number, has_entity, has_concrete_noun])
    if score >= 2:
        grade = "A"
    elif score == 1:
        grade = "B"
    else:
        grade = "D"

    findings = []
    if grade in ("C", "D", "F"):
        findings.append({
            "text": first[:200] + ("..." if len(first) > 200 else ""),
            "note": "Opening lacks concrete nouns, numbers, or named entities. "
                    "Anchor the reader with specifics.",
        })

    return {
        "name": "Opening specificity",
        "grade": grade,
        "has_number": has_number,
        "has_named_entity": has_entity,
        "has_concrete_noun": has_concrete_noun,
        "findings": findings,
    }

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

GRADE_VALUES = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}

def letter_from_gpa(gpa):
    """Convert a GPA-style float to a letter grade."""
    if gpa >= 3.5:
        return "A"
    elif gpa >= 2.5:
        return "B"
    elif gpa >= 1.5:
        return "C"
    elif gpa >= 0.5:
        return "D"
    else:
        return "F"


def score_document(text):
    """Run all checks and return a full scorecard."""
    sentences = split_sentences(text)
    paragraphs = split_paragraphs(text)

    checks = [
        check_hedges(sentences),
        check_passive(sentences),
        check_data_density(sentences),
        check_adjective_bloat(sentences),
        check_sentence_variance(sentences),
        check_buried_lede(paragraphs, sentences),
        check_opening_specificity(paragraphs),
    ]

    # Compute overall grade as GPA of individual check grades.
    graded = [c for c in checks if c["grade"] != "N/A"]
    if graded:
        gpa = sum(GRADE_VALUES[c["grade"]] for c in graded) / len(graded)
        overall = letter_from_gpa(gpa)
    else:
        gpa = 0
        overall = "N/A"

    return {
        "overall_grade": overall,
        "gpa": round(gpa, 2),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "word_count": len(text.split()),
        "checks": checks,
    }

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

GRADE_COLOR = {
    "A": "\033[32m",  # Green
    "B": "\033[36m",  # Cyan
    "C": "\033[33m",  # Yellow
    "D": "\033[33m",  # Yellow
    "F": "\033[31m",  # Red
    "N/A": "\033[90m",  # Gray
}
RESET = "\033[0m"


def format_grade(grade):
    """Color a letter grade for terminal output."""
    color = GRADE_COLOR.get(grade, "")
    return f"{color}{grade}{RESET}"


def print_scorecard(result):
    """Print a human-readable scorecard to stdout."""
    print()
    print("=" * 60)
    print(f"  EXECUTIVE WRITING CRITIC — Overall: {format_grade(result['overall_grade'])} (GPA {result['gpa']:.2f})")
    print(f"  {result['word_count']} words, {result['sentence_count']} sentences, "
          f"{result['paragraph_count']} paragraphs")
    print("=" * 60)

    for check in result["checks"]:
        grade = check["grade"]
        name = check["name"]
        print(f"\n  {format_grade(grade)}  {name}")

        # Print key metrics for each check.
        skip_keys = {"name", "grade", "findings"}
        for k, v in check.items():
            if k in skip_keys:
                continue
            label = k.replace("_", " ").capitalize()
            print(f"     {label}: {v}")

        # Print findings.
        findings = check.get("findings", [])
        if findings:
            shown = findings[:5]
            for f in shown:
                if "text" in f:
                    snippet = f["text"][:80] + ("..." if len(f["text"]) > 80 else "")
                    detail = ""
                    if "hedges" in f:
                        detail = f" — hedges: {', '.join(f['hedges'])}"
                    elif "adjective_count" in f:
                        detail = f" — {f['adjective_count']} adjectives"
                    elif "note" in f:
                        detail = f" — {f['note']}"
                    print(f"     >> S{f.get('sentence', '?')}: {snippet}{detail}")
                elif "note" in f:
                    print(f"     >> {f['note']}")
            if len(findings) > 5:
                print(f"     ... and {len(findings) - 5} more")

    print()
    print("-" * 60)
    print("  Precision-over-recall: only high-confidence findings shown.")
    print("  Run with --json for machine-readable output.")
    print()

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Score a document against an executive writing bar."
    )
    parser.add_argument(
        "--file", "-f",
        help="Path to a text file. If omitted, reads from stdin.",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        dest="json_output",
        help="Output the scorecard as JSON instead of the formatted report.",
    )
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                text = fh.read()
        except FileNotFoundError:
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("Error: no text provided.", file=sys.stderr)
        sys.exit(1)

    result = score_document(text)

    if args.json_output:
        print(json.dumps(result, indent=2))
    else:
        print_scorecard(result)


if __name__ == "__main__":
    main()
