# Coverage Gap Detector

## Press Release (PRFAQ Format)

### Headline

Coverage Gap Detector measures whether executive news briefs actually covered what was available.

### Subheadline

A Python evaluation tool that sweeps public news sources for a roster of entities, deduplicates syndicated stories, and scores any candidate brief on what it caught and what it missed.

### Problem

Teams that produce daily executive news briefs have no way to measure completeness. A brief can be well-written, accurately sourced, and still miss the most important story of the day. Current quality checks verify what's *in* the brief (are the facts right? are the links live?) but not what's *missing* from the brief (did we miss a story that four outlets carried?). Without a measurement, coverage quality is invisible and unimprovable.

### Solution

The Coverage Gap Detector takes a roster of tracked entities (people, companies) and a time window, sweeps public RSS feeds, deduplicates syndicated and wire stories, and builds a universe of what was available. Any candidate brief can then be evaluated against that universe. The output is a coverage score (0–100), entity-by-entity breakdown, and a missed-consensus report listing stories that multiple sources carried but the brief omitted.

### How It Works

1. **Roster definition.** A JSON file lists entities to track — names, aliases, and associated companies.
2. **Source sweep.** The tool fetches headlines from configured RSS feeds and filters to entity-relevant stories.
3. **Deduplication.** Near-identical headlines (syndicated/wire stories) are clustered using title similarity so one AP story in 12 outlets counts once.
4. **Evaluation.** A brief text is scored against the available story universe. Entity mentions and distinctive headline words determine whether a story was covered.

### Key Metrics

| Metric | Description |
|--------|-------------|
| Coverage score | Percentage of available consensus stories mentioned in the brief (0–100) |
| Entity coverage | Per-entity breakdown of available vs. covered stories |
| Syndication dedup ratio | Raw headlines to unique stories (measures source diversity) |
| Missed-consensus count | Stories from 2+ sources that the brief omitted |

### Getting Started

```bash
# Sweep sources and see what's available
python src/detector.py --roster sample-roster.json --sweep-only

# Evaluate a brief
python src/detector.py --roster sample-roster.json --brief path/to/brief.txt

# JSON output for downstream processing
python src/detector.py --roster sample-roster.json --brief brief.txt --output-json
```

### FAQ

**Q: Does this generate briefs?**
A: No. It evaluates them. The evaluator is the interesting half — any LLM can summarize articles, but knowing whether the right articles were selected is a measurement problem.

**Q: What sources does it use?**
A: Public RSS feeds configured in the roster JSON file. The sample uses Reuters, AP, CNBC, and Google News results for Bloomberg and WSJ.

**Q: How does deduplication work?**
A: Title similarity using Python's `SequenceMatcher`. Headlines above a 0.75 similarity threshold are clustered as the same story. This catches wire stories syndicated across outlets with minor editorial changes.

**Q: What counts as a "consensus" story?**
A: A story carried by 2 or more sources (configurable via `--consensus-threshold`). The logic: if multiple independent outlets covered it, it was probably worth including.

**Q: Can I use a news API instead of RSS?**
A: The architecture separates source sweeping from evaluation. You can replace the RSS sweep with any API that returns headlines, without touching the scoring logic.

**Q: Is this affiliated with any company?**
A: No. This is independent work using public data only. The sample roster uses S&P 100 CEO names as a demonstration.

### Architecture Decision Records

- [ADR-001: Evaluator, not generator](docs/decisions/ADR-001-evaluator-not-generator.md)

### Project Structure

```
coverage-gap/
├── index.html              # Project page
├── sample-roster.json      # Sample roster (10 S&P 100 CEOs)
├── README.md               # This file
├── CHANGELOG.md            # Version history
├── src/
│   └── detector.py         # Core detection and evaluation logic
├── evals/
│   └── test_detector.py    # Unit tests for scoring logic
└── docs/
    ├── metrics.md           # Metric definitions
    └── decisions/
        └── ADR-001-evaluator-not-generator.md
```
