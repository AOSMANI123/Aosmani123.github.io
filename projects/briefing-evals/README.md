# Briefing evals

**Does an AI briefing drafter invent facts, or flag what it doesn't know?**

I build AI systems that draft executive briefings. The failure I worry about most isn't a typo. It's a confident guess: a moderator who was never named, last year's date carried forward, "a big crowd" turned into "500 attendees." In a briefing, a guess is worse than a blank.

This is a small, open test suite for that one failure. It's independent work, and every case is fictional.

## How it works

- **12 cases** in `cases/`. Each is a made-up engagement request plus an answer key for nine briefing fields: event name, date, location, format, moderator, audience size, requestor name, requestor organization and the ask.
- **Each case sets one trap**: a missing moderator, a date that's only from last year, a forwarded email where the forwarder isn't the requestor, an audience given as a range, a format left open, and so on.
- **The drafter must return JSON.** Known fields get the value; missing fields get `UNKNOWN`.
- **The scorer** (`evals.py`) labels every field `correct`, `missed`, `wrong` or `fabricated`, and flags any number in the output that isn't in the source.

The two numbers that matter:

| Metric | What it means |
|---|---|
| Recall on known fields | Did it pull out what was actually there? |
| Fabrication rate | Of the fields that were missing, how many did it fill in anyway? |

## Run it

```bash
# Check the scorer works (no API key needed)
python3 -m unittest discover -s tests
python3 evals.py --drafter mock-faithful     # should score 100%, 0 fabrications
python3 evals.py --drafter mock-fabricator   # should be caught on all 12 gaps

# Test a real model
pip install anthropic
export ANTHROPIC_API_KEY=...
python3 evals.py --drafter anthropic --prompt prompts/naive.txt
python3 evals.py --drafter anthropic --prompt prompts/flag_gaps.txt
```

## The experiment

Two prompts, same cases:

- `prompts/naive.txt`: "fill in the briefing details."
- `prompts/flag_gaps.txt`: the rules I actually use. Only this event, `UNKNOWN` when it isn't stated, the requestor isn't the forwarder, copy numbers as written.

**Hypothesis:** the naive prompt fills in missing fields, and the explicit rules bring the fabrication rate close to zero without hurting recall.

## Results

| Drafter | Recall | Fabrication rate | Status |
|---|---|---|---|
| mock-faithful (scorer self-check) | 96/96 | 0/12 | Verified |
| mock-fabricator (scorer self-check) | 96/96 | 12/12 caught | Verified |
| Real model, naive prompt | | | Not yet run |
| Real model, flag-gaps prompt | | | Not yet run |

The mock rows only prove the scorer works. I'll add real model results here once they're run, including the cases each prompt still gets wrong.

## Limits

- Twelve cases is a starting set, not a benchmark. The next step is 50+ cases drawn from the patterns I see in real requests, rewritten with fictional details.
- Matching is simple: a known field counts as correct if the expected text appears in the output. It can't catch an invented venue added next to the right city.
- This checks the fact block, not the prose of the briefing.
