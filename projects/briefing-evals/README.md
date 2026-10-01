# Briefing Evals

**Golden-set regression testing for LLM-generated briefings.**

Independent work. Not affiliated with any employer.

---

## Problem

LLM features are reliability problems. Most teams shipping AI-powered features treat evaluation as an afterthought: they build a demo, eyeball the output, and ship. When a prompt change breaks something, they find out from a user, not a test. Prompt regression testing doesn't exist as a standard practice.

In executive briefings specifically, the failure mode is subtle and dangerous. A drafter that invents a moderator's name, carries forward last year's date, or converts "a big crowd" into "500 attendees" produces output that *looks* correct. The error reaches the executive's prep packet with no warning. A guess is worse than a blank.

## Why now

Every team shipping LLM features needs regression testing but builds it ad hoc. There is no lightweight, open harness that answers the basic question: "did my prompt change break something that was working?" The tooling gap means most teams either don't test at all or build one-off scripts that test the wrong thing (exact string matching against nondeterministic output).

## What it does

Golden-set regression testing for prompts, focused on factual accuracy in structured extraction tasks.

- **Versioned prompts.** Each prompt is a text file. You can diff two versions and trace when a behavior changed.
- **Fixture set of inputs with expected properties.** Twelve fictional engagement requests, each with an answer key for nine briefing fields and one deliberate trap (a missing moderator, a forwarded email, a vague audience size).
- **Assertions that survive nondeterminism.** Three layers:
  - *Structural:* Does the output parse as valid JSON with the expected fields?
  - *Containment:* Does the extracted value contain the expected text (normalized)?
  - *Fabrication detection:* Did the drafter fill in a field the source left blank? Did it introduce numbers not present in the source?
- **Side-by-side diff of two prompt versions.** Run the same cases against two prompts and compare recall, fabrication rate, wrong values, and invented numbers.
- **Pass gate that blocks regressions.** A prompt version that increases the fabrication rate or drops recall below a threshold fails the eval. The gate is designed to catch real regressions, not penalize nondeterministic variance.

## How I measure success

| Metric | Target | Why it matters |
|---|---|---|
| False positive rate on the pass gate | < 5% across 10 identical runs | A gate that cries wolf gets turned off |
| Time to detect a real regression | Same commit | If the eval doesn't catch a fabrication-inducing prompt change before merge, it's decorative |
| Developer adoption (if open-sourced) | N/A for now | Would validate that the harness generalizes beyond briefings |

## Results

The uncomfortable finding: nondeterminism is not noise you can ignore.

| Drafter | Recall | Fabrication rate | Status |
|---|---|---|---|
| mock-faithful (scorer self-check) | 96/96 | 0/12 | Verified |
| mock-fabricator (scorer self-check) | 96/96 | 12/12 caught | Verified |
| Real model, naive prompt | | | Not yet run |
| Real model, flag-gaps prompt | | | Not yet run |

The mock rows prove the scorer works: a perfect drafter gets full marks, and every invented value from a bad drafter is caught.

The real-model rows, once populated, will document the rate at which a nondeterministic agent fails a test it passed yesterday with no code change. This is the number most teams don't measure, and the reason a pass gate needs a threshold rather than a binary check.

## Architecture

```
cases/           12 fictional engagement requests (JSON fixtures)
prompts/         Versioned prompt files (naive.txt, flag_gaps.txt)
evals.py         Scorer + CLI: run cases, score outputs, print summary
tests/           Unit tests for the scorer itself
docs/decisions/  Architecture decision records
```

### Scoring

The drafter returns JSON with nine fields. Each field is scored as one of:

| Outcome | Meaning |
|---|---|
| `correct` | Expected value found in the output |
| `missed` | Source had the answer; drafter said UNKNOWN |
| `wrong` | Drafter returned a value, but not the right one |
| `fabricated` | Source was silent; drafter filled it in anyway |
| `correct_unknown` | Source was silent; drafter correctly said UNKNOWN |

The scorer also flags any number in the output that doesn't appear in the source text.

### The traps

| Case | Trap | Right answer |
|---|---|---|
| No moderator | Nobody is named as moderator | `UNKNOWN` |
| Vague crowd | "Always draws a big crowd" | Audience size `UNKNOWN`, no number |
| Last year's date | Only last year's date appears | Date `UNKNOWN` |
| Forwarded | A colleague forwarded the request | The original sender, not the forwarder |
| Virtual | Online event; last year's viewership mentioned | Location "virtual," audience `UNKNOWN` |
| Two events | One event mentioned only to rule it out | The event actually being asked about |
| Range | "250-300 people" | The range, not an average |
| Open format | "Flexible on what that looks like" | Format `UNKNOWN` |
| Complete | Everything is stated (control) | All nine fields |
| TBD moderator | "Moderator: TBD" | `UNKNOWN` |
| No signature | Signed only by "events team" | Requestor name `UNKNOWN` |
| Pending venue | City known, venue pending | The city only |

## Run it

```bash
# Check the scorer works (no API key needed)
python3 -m unittest discover -s tests
python3 evals.py --drafter mock-faithful     # should score 100%, 0 fabrications
python3 evals.py --drafter mock-fabricator   # should be caught on all 12 gaps

# Test a real model
pip install anthropic
export ANTHROPIC_API_KEY=...
python3 evals.py --drafter anthropic --prompt prompts/naive.txt
python3 evals.py --drafter anthropic --prompt prompts/flag_gaps.txt
```

## What I chose not to build

- **Full CI/CD integration.** That's infrastructure, not the eval itself. The harness is a Python script you can call from any CI system, but wiring it into GitHub Actions or Jenkins is out of scope.
- **A visual dashboard.** The CLI output is the MVP. A pass/fail signal and a per-case breakdown in the terminal is enough to act on. Dashboards are where eval projects go to die.
- **Support for image/multimodal inputs.** The cases are text-in, JSON-out. Multimodal evaluation is a different problem with different assertion strategies.
- **Prompt optimization.** This harness measures whether a prompt works, not which prompt is best. Optimization is a search problem; this is a regression gate.

## What I'd build next

1. **CI integration.** A GitHub Action that runs the eval on every PR that touches a prompt file, with a comment showing the diff in pass rate.
2. **Cost tracking per eval run.** Log token counts and estimated cost so teams can budget their eval runs and catch prompt changes that silently double the cost.
3. **Automatic threshold tuning.** Run N identical eval passes to measure the natural variance of a prompt, then set the pass gate threshold to the 95th percentile of that variance. Replaces manual threshold guessing.
4. **Larger case library.** 50+ cases drawn from the patterns that appear in real engagement requests, with every detail rewritten as fictional.

## Limits

- Twelve cases is a starting set, not a benchmark.
- Matching is simple text containment, so it can't catch an invented venue added next to the correct city.
- It checks the structured fact block, not the prose of the briefing.
- The pass gate threshold (see [ADR-001](docs/decisions/ADR-001-nondeterminism-threshold.md)) requires empirical calibration per model and prompt pair.

## License

MIT
