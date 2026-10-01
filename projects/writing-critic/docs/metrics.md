# Metrics — Executive Writing Critic

## Primary metric

**Precision**: what percentage of flags the tool raises are real issues a writer should fix.

- Definition: (true positives) / (true positives + false positives), measured against human-labeled ground truth.
- Target: >80%
- Baseline: TBD — requires first round of user testing with labeled documents.
- Why this is primary: a tool that cries wolf loses trust fast. Precision-over-recall means every flag is worth reading.

## Guardrail metric

**Recall**: what percentage of real structural issues the tool catches.

- Definition: (true positives) / (true positives + false negatives), measured against the same labeled set.
- Target: >60% (with a decision trigger at 85% for the LLM layer — see ADR-001).
- Baseline: TBD
- Why this is a guardrail: a tool that misses everything isn't useful either. But we'd rather miss an issue than flag a non-issue.

## Driver metrics

**Time to first useful feedback**: how long from paste/submit to scorecard display.

- Target: <2 seconds (CLI), <1 second (web).
- Current: ~10ms (deterministic, no network). Already met.

**Adoption**: number of unique documents scored per week.

- Target: 10+ documents/week in first month (personal use + shared usage).
- Baseline: 0

## Outcome metric

**User satisfaction**: "Did this improve your document?" (yes/no) asked after scoring.

- Target: >70% yes
- Baseline: TBD — requires instrumentation in the web demo.

## How we'll measure

1. Assemble a labeled set of 50+ executive documents, each scored by two raters on the seven check dimensions.
2. Run the tool against the labeled set. Compute precision and recall per check and overall.
3. Track web demo usage via lightweight analytics (page loads, score button clicks).
4. User satisfaction via an optional one-question prompt after scoring.

## Current status

Instrumentation designed but not yet deployed. First measurement pass planned after one week of real usage.
