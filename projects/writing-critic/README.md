# Executive Writing Critic

## Problem

People who write executive documents — strategy briefs, decision memos, launch reviews — get feedback that's either too vague ("make it crisper") or too late (after the meeting). There's no fast, concrete way to check whether a document meets the bar before it goes out. The cost is wasted review cycles, buried asks that don't get funded, and memos that executives stop reading halfway through.

## Why now

LLMs made everyone focus on AI-generated writing feedback, but that feedback is non-deterministic and hard to audit. Meanwhile, the simplest structural problems in executive writing — hedge words, passive voice, missing data, buried ledes — are fully detectable with pattern matching. No one has packaged those checks into a fast, free, dependency-free scorer that gives line-level findings. The gap between "writing advice exists" and "writing is automatically checked before send" is closable right now with stdlib Python.

## What it does

The tool runs seven deterministic checks against pasted text and returns a letter grade (A through F) with line-level findings for each check. It catches hedge words, passive voice, low data density, adjective bloat, monotonous sentence rhythm, buried ledes, and vague openings. There's a CLI (`python3 src/critic.py < doc.txt`) and a [web demo](https://aosmani123.github.io/projects/writing-critic/) that runs the same rules client-side in the browser.

## How I measure success

| Metric | Type | Target | Baseline |
|--------|------|--------|----------|
| Precision — what % of flags are real issues a writer should fix | Primary | >80% | TBD via user testing |
| Recall — what % of real structural issues the tool catches | Guardrail | >60% | TBD via user testing |
| Time to first useful feedback | Driver | <2 seconds | N/A (no prior tool) |
| User satisfaction — "Did this improve your document?" | Outcome | >70% yes | TBD |

## Results from real use

Instrumentation in place. First usage data after week 1.

## What I chose not to build, and why

**An LLM scoring layer.** Tone, argument structure, and logical coherence matter for executive writing, and an LLM could assess them. But LLMs are expensive per call, non-deterministic (same input, different flags), and impossible to debug when they produce a bad flag. Deterministic rules go first because they're fast, free, reproducible, and auditable. Every flag traces to a specific regex or threshold you can read in the source. The LLM layer is the next version, not the first one.

**Grammar and spell checking.** Grammarly and Word already do this. This tool targets the layer above grammar: is the writing shaped for the executive audience?

## What I'd build next, and what would have to be true first

An LLM layer for semantic analysis — tone detection, argument quality scoring, logical gap identification. But only if deterministic rules alone miss more than 15% of real structural issues in user testing. If rules get 85%+ recall on their own, the LLM cost isn't justified. The decision framework is in [ADR-001](docs/decisions/ADR-001-deterministic-first.md).

## Run it

```bash
# Score from stdin
python3 src/critic.py < your-document.txt

# Score from a file
python3 src/critic.py --file your-document.txt

# JSON output for downstream tooling
python3 src/critic.py --json --file your-document.txt
```

No dependencies beyond Python 3.6+ standard library.

## Try it

[Web demo](https://aosmani123.github.io/projects/writing-critic/) — paste text, click Score, see the scorecard. Same rules, runs client-side.

## Run tests

```bash
python3 -m pytest evals/test_critic.py -v
# or
python3 -m unittest evals.test_critic -v
```
