# Metrics Definition

## Primary Metrics

### Coverage Score (0–100)

The percentage of available unique stories that appear in the evaluated brief.

**Formula:**
```
coverage_score = (stories_covered / stories_available) * 100
```

- `stories_available`: Unique stories (after deduplication) that mention a rostered entity, found across all configured sources within the time window.
- `stories_covered`: Stories from the available set that the brief mentions, determined by entity mention + distinctive headline word overlap.

**Interpretation:**
- 100: The brief mentioned every available story. (Rare in practice — some stories are minor.)
- 80–99: Strong coverage with a few misses worth reviewing.
- 50–79: Significant gaps. The missed-consensus report will show what was dropped.
- Below 50: The brief missed more than it caught. Likely a source or roster configuration issue.

**Edge case:** If no stories are available (empty sweep), the score defaults to 100 — you can't miss what doesn't exist.

### Entity Coverage Breakdown

Per-entity ratio of available stories to covered stories.

**Format:**
```
{entity_name: {available: int, covered: int}}
```

**Use:** Identifies which entities are well-covered and which are blind spots. An entity with 5 available stories and 0 covered indicates a systematic miss, not a one-off.

### Missed-Consensus Count

The number of stories carried by N or more sources (default N=2) that the brief omitted.

**Why "consensus":** A story in one niche outlet might be skippable. A story in Reuters, CNBC, and the Wall Street Journal probably isn't. The consensus threshold separates signal from noise.

**Configurable:** The `--consensus-threshold` flag adjusts N. Higher values produce fewer, more confident misses.

## Secondary Metrics

### Syndication Dedup Ratio

```
dedup_ratio = raw_headlines / unique_stories
```

**Interpretation:**
- Ratio near 1.0: Most headlines are unique. Either sources have little overlap or stories are niche.
- Ratio of 3–5: Healthy syndication — major stories are picked up by multiple outlets.
- Ratio above 10: Wire-service dominance. One AP story appearing in 10+ outlets. Not a problem, but means the "source count" metric is measuring syndication breadth, not editorial consensus.

### Story-in-Brief Match Quality

A story is considered "covered" when:
1. At least one of the story's matched entities appears in the brief text (case-insensitive).
2. At least 2 distinctive words from the headline appear in the brief (stopwords and entity names excluded).

**Why both conditions:** Entity mention alone produces false positives (the brief mentions Apple in a different context). Headline words alone miss paraphrased coverage. Both together balance precision and recall.

## Limitations

- **Coverage score is relative to configured sources.** A score of 100 means the brief caught everything the tool could see, not everything that happened.
- **Story matching is heuristic.** A brief that deeply paraphrases a story without using any headline words may register as a miss. Semantic similarity (embeddings) would improve this but adds a dependency.
- **No importance weighting.** All consensus stories count equally. A CEO resignation and a minor product update both count as one story. Source-quality weighting is a planned extension.
- **English only.** Headlines and brief text are matched in English. Non-English sources require separate handling.
