# ADR-001: Build the Evaluator, Not the Generator

## Status

Accepted

## Date

October 2026

## Context

A daily executive news brief has two halves: assembling the right stories, and writing them up. Most AI tools focus on the second half — summarizing articles into a polished brief. The question is whether to build a generator (which produces briefs) or an evaluator (which scores them).

## Decision

Build the evaluator. Score briefs against the available story universe rather than generating briefs.

## Rationale

### The generator is a commodity

Any large language model can summarize ten articles into a coherent brief. The tooling is mature, the quality is adequate, and the marginal improvement from a custom generator is small. Dozens of products already do this.

### The evaluator is the differentiator

No tool answers the question "did the brief cover what was available?" That requires:

1. Knowing what entities to track (roster definition)
2. Knowing what stories existed (source sweep)
3. Deduplicating syndicated/wire stories so coverage isn't inflated
4. Matching the brief's content against the available universe

This is a measurement problem, not a generation problem.

### Measurement enables improvement

Without a coverage score, brief quality is invisible. You can't track it over time, you can't compare team members, you can't measure the impact of adding a source or changing a roster. The evaluator makes all of those possible.

### The evaluator is generator-agnostic

It scores any brief — written by a person, an AI, or a mix. This makes it useful regardless of how the brief is produced and avoids coupling to a specific generation approach.

## Consequences

- The tool does not produce briefs. Users need a separate process or tool for generation.
- The tool's value depends on having a reasonably complete source list. A sweep that misses a major outlet will undercount available stories.
- The coverage score is relative to configured sources, not absolute. A score of 90 means "90% of what we could see," not "90% of everything that happened."

## Alternatives Considered

### Build both

More complete but doubles the scope and conflates two problems. The evaluator can be tested independently; coupling it with a generator makes both harder to validate.

### Build the generator only

Easier to demo ("look, it wrote a brief!") but doesn't answer the hard question. Generators already exist. The gap in the market is measurement.

### Build a real-time monitor

Different product category with different infrastructure requirements (streaming, alerting, uptime). The batch-evaluation model is simpler to build, test, and explain, and validates the core measurement idea before committing to infrastructure.
