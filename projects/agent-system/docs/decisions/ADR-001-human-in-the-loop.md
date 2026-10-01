# ADR-001: Human in the loop at every decision point

## Status

Accepted

## Date

2025

## Context

The seven-agent system processes 200+ executive engagement items across intake, triage, scheduling, briefing production and knowledge retrieval. At each stage, the system could either (a) take action autonomously or (b) stage outputs for human review before anything is sent or committed.

Executive communications carry high stakes. A mis-triaged request, a scheduling conflict, an inaccurate briefing or an inappropriate response can damage relationships and reputation in ways that are difficult to reverse. The failure cost of a single autonomous mistake outweighs the efficiency gained from removing human review.

## Decision

**The human is always the final sender.** Every agent stages its output for human review. No agent sends communications, books calendar slots, or publishes briefings without a person approving the output first.

Specifically:

- **Intake Agent** extracts structured fields and presents them for verification. A human confirms the extraction before the record enters the system
- **Triage Agent** proposes a priority score and category. A human reviews and can override
- **Scheduling Agent** checks conflicts and proposes slots. A human books the meeting
- **Briefing Drafter** assembles a draft document. A human edits and finalizes
- **Coverage Evaluator** flags gaps. A human decides which gaps to address
- **Knowledge Retrieval** surfaces relevant documents. A human decides what to include
- **Orchestrator** routes work between agents. Error handling escalates to a human rather than auto-retrying indefinitely

## Consequences

### Positive

- Zero auto-sent communications — the core safety guarantee
- Errors caught before they reach external parties
- Team trust in the system, because it augments rather than replaces their judgment
- Regulatory and reputational risk minimized

### Negative

- Throughput is bounded by human review capacity. The system can process faster than humans can review
- Some latency added to every workflow — outputs queue until reviewed
- Risk of "rubber-stamping" if review volume is high and reviewers stop reading carefully

### Mitigations for negative consequences

- Coverage Evaluator provides an independent check on briefing quality, reducing reliance on manual review alone
- Triage Agent's priority scoring helps reviewers focus on the highest-stakes items first
- The system's structured outputs are designed to be scannable — key fields surfaced, diffs highlighted — to make review fast without making it superficial

## Alternatives considered

1. **Full autonomy for low-risk items.** Auto-send decline responses for clearly out-of-scope requests. Rejected because the definition of "clearly out-of-scope" drifts over time, and a single auto-sent decline to the wrong person is worse than a few minutes of human review
2. **Approval only for high-priority items.** Let low-priority items flow through without review. Rejected for the same reason — priority is a judgment call, and the cost of getting it wrong is asymmetric
3. **Post-hoc review (send first, review later).** Rejected outright. Executive communications cannot be recalled

## Related

- This decision carries forward from the earlier automation system built at Microsoft, where the same constraint ("the human is always the final sender") governed a three-workflow pipeline
