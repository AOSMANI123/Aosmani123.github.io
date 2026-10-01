# Changelog

All notable changes to the Coverage Gap Detector are documented here.

## [0.1.0] — October 2026

### Added
- Core detection pipeline: roster loading, RSS source sweep, syndication deduplication, brief evaluation.
- Coverage scoring (0–100) based on available-story universe.
- Entity coverage breakdown showing per-entity available vs. covered counts.
- Missed-consensus report identifying stories from 2+ sources that the brief omitted.
- Syndication deduplication using title similarity (SequenceMatcher, 0.75 threshold).
- CLI interface with `--roster`, `--brief`, `--sweep-only`, `--output-json`, `--consensus-threshold`, and `--days` flags.
- RSS fetching with feedparser (optional) or stdlib XML fallback.
- Sample roster with 10 S&P 100 CEO names and 5 public RSS sources.
- Unit test suite for core scoring logic (deduplication, entity matching, evaluation).
- Project page, README (PRFAQ format), metrics documentation, and ADR-001.
