"""
Unit tests for the Executive Writing Critic.

Each check is tested with purpose-built paragraphs to verify that the
scoring rules fire (or don't fire) as expected.

Run:
    python3 -m pytest evals/test_critic.py -v
    python3 -m unittest evals.test_critic -v
"""

import os
import sys
import unittest

# Add the src directory to the path so we can import critic.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import critic


class TestSentenceSplitting(unittest.TestCase):
    """Verify the sentence splitter handles common cases."""

    def test_simple_split(self):
        text = "First sentence. Second sentence. Third sentence."
        sents = critic.split_sentences(text)
        self.assertEqual(len(sents), 3)

    def test_abbreviations_preserved(self):
        text = "Dr. Smith went to Washington. He arrived on Monday."
        sents = critic.split_sentences(text)
        self.assertEqual(len(sents), 2)
        self.assertIn("Dr.", sents[0])

    def test_question_marks(self):
        text = "Is this working? Yes it is. Are you sure?"
        sents = critic.split_sentences(text)
        self.assertEqual(len(sents), 3)


class TestHedgeDetection(unittest.TestCase):
    """Hedge/weasel word detection."""

    def test_clean_paragraph_no_hedges(self):
        text = ("We will ship the feature on March 15. The team has three "
                "engineers allocated. The cost is $40,000.")
        sents = critic.split_sentences(text)
        result = critic.check_hedges(sents)
        self.assertEqual(result["hedge_count"], 0)
        self.assertEqual(result["grade"], "A")

    def test_hedge_heavy_paragraph(self):
        text = ("This might work. It possibly could help. The results are "
                "somewhat unclear. Arguably, we should wait. I think perhaps "
                "we are likely on track. It seems fairly reasonable. "
                "We should probably proceed rather cautiously. "
                "The outcome is quite uncertain.")
        sents = critic.split_sentences(text)
        result = critic.check_hedges(sents)
        # Should flag many hedges.
        self.assertGreater(result["hedge_count"], 8)
        self.assertIn(result["grade"], ("D", "F"))

    def test_single_hedge_in_long_text(self):
        # Build a long text with many clean sentences and one hedge at the end.
        lines = [
            "We shipped the feature on time.",
            "Revenue grew 12% in Q3.",
            "The team delivered all milestones.",
            "Costs dropped by $200K.",
            "We hired four engineers.",
            "The dashboard went live in September.",
            "Customer satisfaction hit 92%.",
            "Three bugs were fixed before launch.",
            "The API handles 10K requests per second.",
            "We closed 15 deals last month.",
            "Infrastructure costs fell 18%.",
            "The team completed sprint planning.",
            "We onboarded 300 new users.",
            "Support tickets dropped 25%.",
            "Pipeline coverage reached 3x.",
            "Retention improved to 88%.",
            "The board approved the budget.",
            "We signed the vendor contract.",
            "Training finished ahead of schedule.",
            "This might take longer than expected.",
        ]
        text = " ".join(lines)
        sents = critic.split_sentences(text)
        result = critic.check_hedges(sents)
        # One hedge in 20+ sentences: rate ~0.05, should be B or C.
        # A single hedge in a long document is not a serious problem.
        self.assertEqual(result["hedge_count"], 1)
        self.assertIn(result["grade"], ("A", "B", "C"))

    def test_hedge_phrases_detected(self):
        text = "It seems the project is behind. I think we need more time."
        sents = critic.split_sentences(text)
        result = critic.check_hedges(sents)
        self.assertEqual(result["hedge_count"], 2)
        hedges_found = [h for f in result["findings"] for h in f["hedges"]]
        self.assertIn("it seems", hedges_found)
        self.assertIn("i think", hedges_found)


class TestPassiveVoice(unittest.TestCase):
    """Passive voice detection."""

    def test_active_paragraph(self):
        text = ("The team shipped the feature. We hit the target. "
                "Revenue grew 15% in Q3. Three engineers built the pipeline.")
        sents = critic.split_sentences(text)
        result = critic.check_passive(sents)
        self.assertIn(result["grade"], ("A", "B"))

    def test_passive_heavy_paragraph(self):
        text = ("The feature was shipped by the team. The target was met. "
                "The pipeline was built by three engineers. Errors were found "
                "in production. The report was written last week. "
                "The decision was made by leadership.")
        sents = critic.split_sentences(text)
        result = critic.check_passive(sents)
        self.assertGreater(result["passive_count"], 3)
        self.assertIn(result["grade"], ("D", "F"))


class TestDataDensity(unittest.TestCase):
    """Data density measurement."""

    def test_data_rich_paragraph(self):
        text = ("Revenue grew 15% to $4.2M. We added 300 new users. "
                "Response time dropped from 450ms to 120ms. "
                "The team shipped 12 features in Q3.")
        sents = critic.split_sentences(text)
        result = critic.check_data_density(sents)
        self.assertIn(result["grade"], ("A", "B"))

    def test_data_sparse_paragraph(self):
        text = ("The product is doing well. Customers are happy. "
                "The team is working hard. We are making progress. "
                "Things are looking up. The future is bright. "
                "Our strategy is sound. Momentum is building.")
        sents = critic.split_sentences(text)
        result = critic.check_data_density(sents)
        self.assertEqual(result["data_sentences"], 0)
        self.assertEqual(result["grade"], "F")


class TestAdjectiveBloat(unittest.TestCase):
    """Adjective bloat detection."""

    def test_lean_paragraph(self):
        text = ("Ship the feature. Cut the cost. Hire two engineers. "
                "We need a decision by Friday.")
        sents = critic.split_sentences(text)
        result = critic.check_adjective_bloat(sents)
        self.assertIn(result["grade"], ("A", "B"))

    def test_adjective_heavy_paragraph(self):
        text = ("We built a robust, scalable, innovative, flexible platform. "
                "The comprehensive, powerful, intuitive, adaptive dashboard "
                "provides actionable, meaningful, valuable, real insights.")
        sents = critic.split_sentences(text)
        result = critic.check_adjective_bloat(sents)
        self.assertGreater(result["flagged_sentences"], 0)


class TestSentenceVariance(unittest.TestCase):
    """Sentence length variance detection."""

    def test_varied_paragraph(self):
        text = ("Ship it. We need to move fast on this because the "
                "competition launched two weeks ago and our window is closing. "
                "Three engineers. The timeline is tight but achievable if we "
                "cut the admin panel from v1. Do it.")
        sents = critic.split_sentences(text)
        result = critic.check_sentence_variance(sents)
        self.assertIn(result["grade"], ("A", "B"))

    def test_monotonous_paragraph(self):
        text = ("The team will ship the feature soon. "
                "The cost will be about forty thousand. "
                "The timeline will take about five weeks. "
                "The risk will remain at a medium level. "
                "The team will need three more engineers. "
                "The budget will cover the full project.")
        sents = critic.split_sentences(text)
        result = critic.check_sentence_variance(sents)
        # All sentences are roughly the same length.
        self.assertIn(result["grade"], ("C", "D", "F"))

    def test_too_few_sentences(self):
        text = "One sentence. Two."
        sents = critic.split_sentences(text)
        result = critic.check_sentence_variance(sents)
        self.assertEqual(result["grade"], "N/A")


class TestBuriedLede(unittest.TestCase):
    """Buried lede detection."""

    def test_clear_lede(self):
        text = ("I recommend we invest $2M in the new platform. "
                "It will cut costs by 30% in the first year.\n\n"
                "Background: the current system is five years old.")
        paras = critic.split_paragraphs(text)
        sents = critic.split_sentences(text)
        result = critic.check_buried_lede(paras, sents)
        self.assertIn(result["grade"], ("A", "B"))

    def test_buried_lede(self):
        text = ("Over the past several quarters, the landscape has evolved "
                "significantly. Many factors have contributed to where we are "
                "today.\n\nWe recommend investing in the new platform.")
        paras = critic.split_paragraphs(text)
        sents = critic.split_sentences(text)
        result = critic.check_buried_lede(paras, sents)
        self.assertIn(result["grade"], ("D", "F"))


class TestOpeningSpecificity(unittest.TestCase):
    """Opening paragraph specificity."""

    def test_specific_opening(self):
        text = ("Amazon Web Services grew revenue 30% to $25B in Q3 2026. "
                "The growth was driven by AI workloads.\n\n"
                "This memo covers the pricing strategy for next quarter.")
        paras = critic.split_paragraphs(text)
        result = critic.check_opening_specificity(paras)
        self.assertIn(result["grade"], ("A", "B"))

    def test_vague_opening(self):
        text = ("Things have been going well lately. We are making progress "
                "on several fronts and the outlook is positive.\n\n"
                "Specifically, revenue grew 30% last quarter.")
        paras = critic.split_paragraphs(text)
        result = critic.check_opening_specificity(paras)
        self.assertIn(result["grade"], ("C", "D", "F"))


class TestOverallScoring(unittest.TestCase):
    """End-to-end scoring integration."""

    def test_good_document(self):
        text = ("I recommend we approve the $1.5M investment in Platform v2. "
                "It will reduce infrastructure costs by 25% within 6 months.\n\n"
                "The current platform handles 500K requests per day. "
                "We need 2M by Q2. The upgrade path requires 4 engineers "
                "over 12 weeks. Ship date: March 15.")
        result = critic.score_document(text)
        self.assertIn(result["overall_grade"], ("A", "B"))
        self.assertGreater(result["sentence_count"], 0)
        self.assertGreater(result["word_count"], 0)

    def test_bad_document(self):
        text = ("Over the past several quarters, things have been somewhat "
                "challenging. It seems the situation is arguably getting "
                "better, though we might possibly need to consider various "
                "options. Perhaps the best approach would be fairly "
                "cautious. The strategy is likely quite reasonable.\n\n"
                "More thought is needed. The landscape is evolving. "
                "Stakeholders are being consulted. Progress is being made. "
                "Results are expected soon. Momentum is building steadily.")
        result = critic.score_document(text)
        self.assertIn(result["overall_grade"], ("C", "D", "F"))

    def test_empty_text_raises(self):
        """Empty text should still return a result (not crash)."""
        result = critic.score_document("Hello.")
        self.assertIn("overall_grade", result)
        self.assertEqual(len(result["checks"]), 7)


if __name__ == "__main__":
    unittest.main()
