# Seven-Agent System for Executive Engagement Operations

> Independent work. Not affiliated with any employer.

## Problem

A CEO's office receives hundreds of engagement requests — speaking invitations, customer meetings, events, media inquiries. These flow in through email, forms and forwarded messages, and each one requires intake processing, priority assessment, scheduling checks, briefing preparation and follow-up. At scale, manual processing breaks down: requests get lost, briefings get assembled from scratch every time, and there is no systematic way to evaluate whether a briefing actually covered what the executive needed.

## Why now

The emergence of reliable language models makes it possible to build AI agents that handle structured reading, extraction and drafting tasks with high accuracy — while keeping humans in the decision loop. The three-workflow automation I built previously proved the pattern at a smaller scale. The jump to 200+ items demanded decomposition into specialized agents.

## What it does

Seven AI agents, each with a single responsibility, coordinated by an orchestrator:

1. **Intake Agent** — Reads incoming requests and extracts structured fields (event name, date, organization, requestor, format, audience, summary)
2. **Triage Agent** — Scores and categorizes each request by priority using an explicit, auditable rubric
3. **Scheduling Agent** — Checks calendar conflicts and logistics; proposes but never books
4. **Briefing Drafter** — Assembles preparation documents from the knowledge base, with every claim sourced
5. **Coverage Evaluator** — Measures what the briefing missed, not just what it got right
6. **Knowledge Retrieval Agent** — Maintains and searches the reference corpus; serves every other agent
7. **Orchestrator** — Routes work between agents, handles retries and failures, tracks state

## How I measure success

| Metric | Target | Why it matters |
|--------|--------|----------------|
| Items managed | 200+ concurrent | Proves the system handles real volume |
| Briefing assembly time | 60%+ reduction | The main time cost in the old workflow |
| Coverage score | Established and tracked | First systematic measure of briefing completeness |
| Auto-sent communications | Zero | The core safety constraint: humans send everything |

## Results from real use

- **200+ engagement items** managed through the system
- **~60% reduction** in briefing assembly time
- **Coverage evaluation metric** established for the first time — measuring what briefings miss, not just what they include
- **Zero auto-sent communications** — every output reviewed by a human before sending

## What I chose not to build

- **Fully autonomous system.** Kept humans in the loop at every decision point. Executive communications are too consequential for unsupervised AI
- **Custom LLM.** Used the platform's existing models. The differentiation is in the agent architecture, not the underlying model
- **New UI.** Agents run behind existing tools. No new interface to learn, no adoption friction

## What I'd build next

- **Cross-engagement pattern detection.** An agent that spots recurring themes and seasonal patterns across the full history
- **Briefing quality feedback loop.** Capture which parts the executive actually used and feed relevance data back into the drafter
- **Agent portability.** Package agent definitions for cross-platform orchestration
