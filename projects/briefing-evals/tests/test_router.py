"""Checks the router's rules and the routed suite.
Run: python3 -m unittest discover -s tests
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import evals  # noqa: E402
import router  # noqa: E402

HERE = Path(__file__).resolve().parents[1]


class RouterRuleTests(unittest.TestCase):
    def test_plain_request_is_easy(self):
        r = router.route("Please join our panel on March 3 in Denver. About 200 guests. - Ana, Acme")
        self.assertEqual(r.tier, "easy")  # "About 200" is a number, not a vague one
        self.assertEqual(r.model_tier, "cheap")

    def test_trap_patterns_are_hard(self):
        for text in ["Fwd: speaking request", "Last year we hosted 900 people.",
                     "The moderator is TBD.", "We expect hundreds of founders.",
                     "Our dean will introduce the speaker."]:
            with self.subTest(text=text):
                self.assertEqual(router.route(text).tier, "hard")

    def test_changed_details_are_flagged_for_a_person(self):
        r = router.route("Quick update: the forum has moved to May 13.")
        self.assertEqual(r.tier, "review")
        self.assertTrue(r.needs_human)
        self.assertEqual(r.model_tier, "strong")

    def test_two_different_dates_are_hard(self):
        self.assertIn("two_dates", router.route("Join us May 6. Our gala is June 2.").reasons)
        self.assertNotIn("two_dates", router.route("May 6, and again, May 6.").reasons)

    def test_router_never_reads_the_answer_key(self):
        """Same text, different answer key and category: same route."""
        c = evals.load_cases()[0]
        self.assertEqual(router.route(c.source), router.route(str(c.source)))


class RouterCoverageTests(unittest.TestCase):
    """Offline check against the case categories. The rules were written while reading
    these cases, so this agreement is optimistic for new requests."""

    def setUp(self):
        self.cases = evals.load_cases()

    def test_controls_go_to_the_cheap_model(self):
        for c in self.cases:
            if c.category == "control":
                self.assertEqual(router.route(c.source).tier, "easy", c.id)

    def test_every_correction_is_flagged(self):
        for c in self.cases:
            if c.category == "correction":
                self.assertEqual(router.route(c.source).tier, "review", c.id)


class RoutedSuiteTests(unittest.TestCase):
    def test_routed_suite_sends_each_case_one_way_and_prices_each_tier(self):
        rec = evals.run_routed(("mock-faithful", None), ("mock-faithful", None),
                               str(HERE / "prompts" / "flag_gaps.txt"))
        s = rec["runs"][0]["summary"]
        self.assertEqual(s["to_cheap"] + s["to_strong"], 50)
        self.assertEqual(s["bad_cases"], 0)          # a perfect drafter makes no errors either way
        self.assertEqual(s["fabrication_rate"], 0.0)
        self.assertEqual(s["pass_rate"], 1.0)

    def test_routing_cost_uses_each_tiers_price(self):
        rec = evals.run_routed(("mock-cheap", None), ("mock-strong", None),
                               str(HERE / "prompts" / "flag_gaps.txt"),
                               cheap_price=(1.0, 0.0), strong_price=(0.0, 0.0))
        u = rec["runs"][0]["usage"]
        self.assertAlmostEqual(u["cost_usd"], u["by_tier"]["cheap"][0] / 1_000_000)
        self.assertTrue(rec["estimated_tokens"])

    def test_no_price_means_no_cost(self):
        rec = evals.run_routed(("mock-cheap", None), ("mock-strong", None),
                               str(HERE / "prompts" / "flag_gaps.txt"), cheap_price=(1.0, 1.0))
        self.assertIsNone(rec["runs"][0]["usage"]["cost_usd"])

    def test_simulated_tiers_are_repeatable(self):
        c = evals.load_cases()[5]
        self.assertEqual(evals.mock_cheap(c, "", 3), evals.mock_cheap(c, "", 3))


class EstimateTests(unittest.TestCase):
    def test_estimate_makes_no_calls_and_scales_with_runs(self):
        tin, tout = evals.main(["estimate", "--runs", "2", "--price", "1", "1"])
        self.assertGreater(tin, 0)
        self.assertEqual(tout, 50 * 150)
