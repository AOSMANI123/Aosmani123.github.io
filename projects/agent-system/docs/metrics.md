# Metrics Definition: Seven-Agent Engagement System

> Independent work. Not affiliated with any employer.

## Primary metrics

### 1. Engagement items managed

- **Definition:** Count of distinct engagement requests processed through the system (intake through disposition)
- **Target:** 200+
- **Measurement:** Count of records in the engagement tracker with a completed status
- **Why it matters:** Demonstrates the system handles real operational volume, not a prototype workload

### 2. Briefing assembly time reduction

- **Definition:** Percentage reduction in time from "engagement accepted" to "briefing draft ready for review," compared to the manual baseline
- **Target:** 60% reduction
- **Baseline:** Manual briefing assembly time measured before the system was deployed
- **Measurement:** Timestamp delta between acceptance and draft-ready, averaged across engagements
- **Why it matters:** Briefing assembly was the largest single time cost in the old workflow. This is where the system delivers the most direct value

### 3. Coverage evaluation score

- **Definition:** Percentage of expected briefing sections that contain sourced, relevant content, as assessed by the Coverage Evaluator agent
- **Target:** Establish the metric and track trend (no fixed target for v1 — the point is having a measurement that didn't exist before)
- **Measurement:** Coverage Evaluator output for each briefing, tracked over time
- **Components:**
  - Section completeness: did the brief address each expected topic?
  - Source coverage: is every factual claim backed by a document in the knowledge base?
  - Gap identification: what did the brief miss?
- **Why it matters:** Before this system, there was no systematic way to know whether a briefing was complete. The metric exists to catch the failure mode where a drafter produces confident-sounding text without adequate sourcing

### 4. Auto-sent communications

- **Definition:** Count of communications sent to external parties without human review
- **Target:** Zero
- **Measurement:** Audit log of all outbound communications, flagged if no human-review timestamp precedes the send timestamp
- **Why it matters:** This is the system's core safety constraint. See ADR-001

## Secondary metrics

### 5. Intake extraction accuracy

- **Definition:** Percentage of structured fields correctly extracted by the Intake Agent, as verified by human reviewers
- **Measurement:** Sample-based — reviewers flag extraction errors during their normal review pass; error rate calculated weekly
- **Why it matters:** Garbage in, garbage out. If intake extraction is inaccurate, every downstream agent works from bad data

### 6. Triage override rate

- **Definition:** Percentage of engagements where a human reviewer changes the Triage Agent's recommended priority or category
- **Measurement:** Compare Triage Agent output to final human-set values
- **Why it matters:** A high override rate signals the scoring rubric needs recalibration. A very low rate may signal rubber-stamping (see ADR-001 consequences)

### 7. Knowledge retrieval relevance

- **Definition:** Percentage of documents surfaced by the Knowledge Retrieval Agent that the Briefing Drafter actually uses
- **Measurement:** Compare retrieved document set to documents cited in the final briefing
- **Why it matters:** If the retrieval agent surfaces too many irrelevant documents, it slows down the drafter. If it misses key documents, the briefing has gaps

## Metrics not tracked (and why)

- **End-to-end processing time:** Not tracked as a target because speed is bounded by human review capacity (by design). Optimizing for speed would create pressure to reduce review thoroughness
- **Engagement acceptance rate:** Not a system metric — acceptance/decline is a leadership decision, not a system outcome
- **User satisfaction score:** Not formally tracked in v1. The team's continued use of the system is the primary signal
