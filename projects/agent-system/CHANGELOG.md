# Changelog

All notable changes to the seven-agent engagement system.

> Independent work. Not affiliated with any employer.

## [1.0.0] — 2025

### Added

- Seven-agent architecture: Intake, Triage, Scheduling, Briefing Drafter, Coverage Evaluator, Knowledge Retrieval, Orchestrator
- Human-in-the-loop review at every decision point (see ADR-001)
- Structured intake extraction: event name, date, organization, requestor, format, audience, summary
- Priority scoring with explicit, auditable rubric
- Calendar conflict checking (read-only access, propose but never book)
- Briefing drafting from knowledge base with source citations
- Coverage evaluation metric — first systematic measurement of briefing completeness
- Knowledge retrieval as a shared service across all agents
- Orchestrator with stateless routing, retry logic and failure escalation

### Design constraints

- Zero auto-sent communications
- All agents stage outputs for human review
- Orchestrator escalates errors to humans rather than auto-retrying indefinitely
- Knowledge Retrieval Agent serves as the single source for all background context

### Measured results

- 200+ engagement items managed
- ~60% reduction in briefing assembly time
- Coverage evaluation metric established for the first time
- Zero auto-sent communications
