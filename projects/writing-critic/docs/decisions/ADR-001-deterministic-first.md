# ADR-001: Deterministic rules before LLM layer

## Status

Accepted — October 2026

## Context

Executive writing has structural problems that are detectable at the text level: hedge words, passive voice, low data density, monotonous sentence rhythm, buried ledes. The question is whether to check these with deterministic pattern matching (regex, heuristics, thresholds) or with an LLM that can also assess semantic quality (tone, argument structure, logical coherence).

We need the tool to be:
- **Fast**: feedback in under 2 seconds, no network round-trip.
- **Free to run**: no API costs per scoring call.
- **Reproducible**: same input always produces the same output.
- **Auditable**: every flag traces to a readable rule, not a black-box probability.
- **Dependency-free**: runs anywhere Python runs, no pip install, no API key.

## Options considered

### Option A: Deterministic rules only (chosen)

Regex patterns for hedge words and passive voice. Counting heuristics for data density, adjective bloat, and sentence variance. First-paragraph analysis for buried ledes and opening specificity. All stdlib Python.

- **Pros**: Fast (~10ms), free, reproducible, auditable, zero dependencies.
- **Cons**: Cannot assess tone, argument quality, or logical gaps. Regex-based passive voice detection has false positives. Adjective detection without a real POS tagger is approximate.

### Option B: LLM-only scoring

Send the full document to an LLM with a structured prompt. Parse the response into a scorecard.

- **Pros**: Can assess semantic quality. Handles nuance better.
- **Cons**: Costs money per call. Non-deterministic. Latency measured in seconds. Requires an API key. Hard to debug bad flags. Users can't inspect the rule that triggered a finding.

### Option C: Hybrid — rules first, LLM second

Ship deterministic rules as v1. Measure precision and recall. Add an LLM layer only if rules miss more than 15% of real issues.

- **Pros**: Gets the free, fast, auditable checks into users' hands now. Defers cost and complexity until there's evidence it's needed.
- **Cons**: Two codepaths to maintain if the LLM layer ships.

## Decision

**Option C, starting with the deterministic layer (Option A).** The LLM layer ships only if the decision criterion is met.

## Decision criterion

Add an LLM scoring layer if and only if: deterministic rules alone have recall below 85% on structural writing issues, measured against a manually labeled set of 50+ executive documents scored by at least two human raters.

## What this costs us

- False positives on passive voice detection (regex approximation, not a real parser).
- False positives on adjective detection (suffix matching, not POS tagging).
- Inability to flag tone problems, weak arguments, or logical gaps in v1.
- Users may expect AI-powered analysis and find regex-based checks underwhelming.

## How we'd know this is wrong

- Precision drops below 70% (too many false flags; users stop trusting the tool).
- Users consistently report that the tool misses the issues they care about most, and those issues are semantic, not structural.
- Recall on structural issues is already below 85% in the first round of user testing, triggering the LLM criterion.
