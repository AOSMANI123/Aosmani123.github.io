#!/usr/bin/env python3
"""
Unit tests for the coverage gap detector's core scoring logic.

Tests the deduplication, entity matching, and brief evaluation stages
WITHOUT any network calls. All test data is synthetic.
"""

import os
import sys
import unittest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from detector import (
    deduplicate,
    entity_names,
    evaluate_brief,
    load_roster,
    _normalize,
    _story_in_brief,
)


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

SAMPLE_ROSTER = [
    {"name": "Tim Cook", "aliases": ["Timothy Cook"], "company": "Apple"},
    {"name": "Satya Nadella", "aliases": [], "company": "Microsoft"},
    {"name": "Jensen Huang", "aliases": [], "company": "NVIDIA"},
]

def make_story(title, entities, source_count=1, sources=None):
    """Helper to build a story dict for testing."""
    return {
        "title": title,
        "matched_entities": entities,
        "cluster": [{"title": title}] * source_count,
        "source_count": source_count,
        "sources": sources or [f"Source{i}" for i in range(source_count)],
    }


# ---------------------------------------------------------------------------
# Tests: Normalization
# ---------------------------------------------------------------------------

class TestNormalize(unittest.TestCase):
    def test_lowercase(self):
        self.assertEqual(_normalize("Hello World"), "hello world")

    def test_strip_punctuation(self):
        self.assertEqual(_normalize("CEO's plan: buy $100M"), "ceos plan buy 100m")

    def test_collapse_whitespace(self):
        self.assertEqual(_normalize("too   many   spaces"), "too many spaces")

    def test_empty_string(self):
        self.assertEqual(_normalize(""), "")


# ---------------------------------------------------------------------------
# Tests: Entity name extraction
# ---------------------------------------------------------------------------

class TestEntityNames(unittest.TestCase):
    def test_includes_primary_names(self):
        names = entity_names(SAMPLE_ROSTER)
        self.assertIn("Tim Cook", names)
        self.assertIn("Satya Nadella", names)

    def test_includes_aliases(self):
        names = entity_names(SAMPLE_ROSTER)
        self.assertIn("Timothy Cook", names)

    def test_includes_companies(self):
        names = entity_names(SAMPLE_ROSTER)
        self.assertIn("Apple", names)
        self.assertIn("Microsoft", names)


# ---------------------------------------------------------------------------
# Tests: Deduplication
# ---------------------------------------------------------------------------

class TestDedup(unittest.TestCase):
    def test_identical_headlines_cluster(self):
        headlines = [
            {"title": "Apple announces new iPhone", "matched_entities": ["Apple"],
             "source_name": "Reuters"},
            {"title": "Apple announces new iPhone", "matched_entities": ["Apple"],
             "source_name": "AP"},
        ]
        clusters = deduplicate(headlines)
        self.assertEqual(len(clusters), 1)
        self.assertEqual(clusters[0]["source_count"], 2)

    def test_similar_headlines_cluster(self):
        headlines = [
            {"title": "Apple announces new iPhone 16 at event",
             "matched_entities": ["Apple"], "source_name": "Reuters"},
            {"title": "Apple announces new iPhone 16 at annual event",
             "matched_entities": ["Apple"], "source_name": "CNBC"},
        ]
        clusters = deduplicate(headlines)
        self.assertEqual(len(clusters), 1)

    def test_different_headlines_stay_separate(self):
        headlines = [
            {"title": "Apple announces new iPhone", "matched_entities": ["Apple"],
             "source_name": "Reuters"},
            {"title": "Microsoft launches new cloud service",
             "matched_entities": ["Microsoft"], "source_name": "Reuters"},
        ]
        clusters = deduplicate(headlines)
        self.assertEqual(len(clusters), 2)

    def test_entity_merging_in_clusters(self):
        headlines = [
            {"title": "Apple and Microsoft partner on AI",
             "matched_entities": ["Apple"], "source_name": "Reuters"},
            {"title": "Apple and Microsoft partner on AI project",
             "matched_entities": ["Apple", "Microsoft"], "source_name": "CNBC"},
        ]
        clusters = deduplicate(headlines)
        self.assertEqual(len(clusters), 1)
        self.assertIn("Apple", clusters[0]["matched_entities"])
        self.assertIn("Microsoft", clusters[0]["matched_entities"])

    def test_empty_input(self):
        self.assertEqual(deduplicate([]), [])

    def test_custom_threshold(self):
        headlines = [
            {"title": "Apple stock rises sharply today",
             "matched_entities": ["Apple"], "source_name": "A"},
            {"title": "Apple stock rises modestly today",
             "matched_entities": ["Apple"], "source_name": "B"},
        ]
        # High threshold should keep them separate
        clusters_strict = deduplicate(headlines, threshold=0.95)
        self.assertEqual(len(clusters_strict), 2)
        # Low threshold should merge them
        clusters_loose = deduplicate(headlines, threshold=0.5)
        self.assertEqual(len(clusters_loose), 1)


# ---------------------------------------------------------------------------
# Tests: Story-in-brief matching
# ---------------------------------------------------------------------------

class TestStoryInBrief(unittest.TestCase):
    def test_covered_story(self):
        story = make_story(
            "Tim Cook announces Apple Vision Pro sales numbers",
            ["Tim Cook", "Apple"]
        )
        brief = "Tim Cook shared Apple Vision Pro sales numbers at the event."
        self.assertTrue(_story_in_brief(story, brief.lower()))

    def test_missed_story_no_entity(self):
        story = make_story(
            "Tim Cook announces Apple Vision Pro sales numbers",
            ["Tim Cook", "Apple"]
        )
        brief = "The weather was nice today."
        self.assertFalse(_story_in_brief(story, brief.lower()))

    def test_entity_present_but_different_topic(self):
        story = make_story(
            "Tim Cook discusses privacy legislation in Europe",
            ["Tim Cook"]
        )
        brief = "Tim Cook announced new iPhone features at the keynote."
        # Entity is present but distinctive words (privacy, legislation, europe) are not
        self.assertFalse(_story_in_brief(story, brief.lower()))

    def test_case_insensitive_matching(self):
        story = make_story(
            "NVIDIA Reports Record Revenue",
            ["NVIDIA"]
        )
        brief = "nvidia reported record revenue in the latest quarter."
        self.assertTrue(_story_in_brief(story, brief.lower()))


# ---------------------------------------------------------------------------
# Tests: Full brief evaluation
# ---------------------------------------------------------------------------

class TestEvaluateBrief(unittest.TestCase):
    def setUp(self):
        self.stories = [
            make_story("Tim Cook announces Apple Vision Pro sales",
                       ["Tim Cook", "Apple"], source_count=3),
            make_story("Satya Nadella keynotes Microsoft Build conference",
                       ["Satya Nadella", "Microsoft"], source_count=2),
            make_story("Jensen Huang reveals NVIDIA next-gen GPU",
                       ["Jensen Huang", "NVIDIA"], source_count=4),
        ]

    def test_full_coverage(self):
        brief = (
            "Tim Cook announced Apple Vision Pro sales figures today. "
            "Satya Nadella keynotes Microsoft Build conference. "
            "Jensen Huang reveals NVIDIA next-gen GPU architecture."
        )
        result = evaluate_brief(brief, self.stories, SAMPLE_ROSTER)
        self.assertEqual(result["coverage_score"], 100.0)
        self.assertEqual(result["total_covered"], 3)
        self.assertEqual(len(result["missed_consensus"]), 0)

    def test_partial_coverage(self):
        brief = (
            "Tim Cook announced Apple Vision Pro sales figures today. "
            "Nothing else happened in tech."
        )
        result = evaluate_brief(brief, self.stories, SAMPLE_ROSTER)
        self.assertLess(result["coverage_score"], 100)
        self.assertGreater(result["coverage_score"], 0)
        self.assertEqual(result["total_covered"], 1)
        # Two missed consensus stories (both have source_count >= 2)
        self.assertEqual(len(result["missed_consensus"]), 2)

    def test_zero_coverage(self):
        brief = "Today's weather forecast calls for sun."
        result = evaluate_brief(brief, self.stories, SAMPLE_ROSTER)
        self.assertEqual(result["coverage_score"], 0.0)
        self.assertEqual(result["total_covered"], 0)
        self.assertEqual(len(result["missed_consensus"]), 3)

    def test_empty_stories(self):
        result = evaluate_brief("Any brief text", [], SAMPLE_ROSTER)
        self.assertEqual(result["coverage_score"], 100.0)
        self.assertEqual(result["total_available"], 0)

    def test_entity_coverage_breakdown(self):
        brief = (
            "Tim Cook announced Apple Vision Pro sales figures today."
        )
        result = evaluate_brief(brief, self.stories, SAMPLE_ROSTER)
        ec = result["entity_coverage"]
        self.assertEqual(ec["Tim Cook"]["available"], 1)
        self.assertEqual(ec["Tim Cook"]["covered"], 1)
        self.assertEqual(ec["Satya Nadella"]["available"], 1)
        self.assertEqual(ec["Satya Nadella"]["covered"], 0)

    def test_dedup_stats(self):
        result = evaluate_brief("anything", self.stories, SAMPLE_ROSTER)
        # 3+2+4 = 9 raw headlines across all clusters
        self.assertEqual(result["dedup_stats"]["raw_headlines"], 9)
        self.assertEqual(result["dedup_stats"]["unique_stories"], 3)

    def test_consensus_threshold(self):
        brief = "Today's weather forecast calls for sun."
        # With threshold=5, only the NVIDIA story (4 sources) is below,
        # so no story meets consensus
        result = evaluate_brief(brief, self.stories, SAMPLE_ROSTER,
                                consensus_threshold=5)
        self.assertEqual(len(result["missed_consensus"]), 0)

        # With threshold=3, Apple (3) and NVIDIA (4) stories are consensus
        result = evaluate_brief(brief, self.stories, SAMPLE_ROSTER,
                                consensus_threshold=3)
        self.assertEqual(len(result["missed_consensus"]), 2)


# ---------------------------------------------------------------------------
# Tests: Roster loading
# ---------------------------------------------------------------------------

class TestRosterLoading(unittest.TestCase):
    def test_load_sample_roster(self):
        roster_path = os.path.join(
            os.path.dirname(__file__), "..", "sample-roster.json"
        )
        if os.path.exists(roster_path):
            data = load_roster(roster_path)
            self.assertIn("roster", data)
            self.assertEqual(len(data["roster"]), 10)
            # Check structure
            for entry in data["roster"]:
                self.assertIn("name", entry)
                self.assertIn("aliases", entry)
                self.assertIn("company", entry)


if __name__ == "__main__":
    unittest.main()
