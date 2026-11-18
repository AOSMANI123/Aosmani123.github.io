# Cost and routing: can a cheaper model draft the easy briefings?

**Status:** Built and tested offline, November 2026. Every result below is from a **simulation**. No real model has run through the router yet, and no real users have used it. The real-run plan is at the end.
**Author:** Atif Osmani

---

## The question

Sending every briefing request to a strong model is the safe default, and the most expensive one. Most requests are simple. If I can tell the simple ones apart from the text alone, a cheaper model can draft those, and the strong model keeps the hard ones.

**Goal:** cut the cost per run without failing the pass gate. In a briefing, a guess is worse than a blank, so the gate on fabricated fields is the line I won't cross for savings.

## What I measure

| Metric | What it means |
|---|---|
| Cost per run | Tokens in and out for all 50 cases, priced per model |
| Latency | Median seconds per case |
| Pass rate | Share of requests whose whole briefing could go out as drafted, with no fabricated, wrong or missed field |
| Failure rate | Share of requests with no usable briefing: an API error, a refusal, a reply cut off, or unreadable output |
| Fabrication rate | Share of missing fields the drafter filled with a guess. This is the one the gate guards hardest |

## What I changed

1. **Failure tracking.** Before, a failed API call crashed the run, and a cut-off reply looked the same as bad output. Now each call is recorded as an API error, a refusal or a cut-off reply, and the run keeps going. I also raised the reply limit from 800 to 4,000 tokens, because newer models think before they answer and 800 could cut the JSON off.
2. **A router** (`router.py`). It reads only the request text and sends it one of three ways:
   - **Easy, to the cheap model:** nothing in the text matches a known trap.
   - **Hard, to the strong model:** a forward, last year's details, a "TBD", a vague number, two dates, or other people with roles.
   - **Flag for a person:** the request says a detail changed. The strong model drafts it, and a person checks it, because a briefing that keeps the old date looks right.
3. **Routed runs.** `--route` runs the suite through the router, prices each model separately and reports where each case went and what the flag caught.
4. **A cost estimate before any paid call.** `evals.py estimate` gives a floor cost from the text length.

## Before and after (simulated)

The simulated cheap model falls for a trap 22% of the time; the simulated strong model 6%. I chose those rates. They are assumptions, not measurements, so the table shows the harness working, not how any real model behaves. Prices are Anthropic's list prices as of November 2026 for Claude Haiku 5.5 (cheap) and Claude Sonnet 5.5 (strong), and token counts are estimated from text length. Ten runs each.

| Setup | Pass rate | Fabrication rate | Failure rate | Est. cost per run |
|---|---|---|---|---|
| Strong model for everything (baseline) | 82% | 5% | 0% | $0.10 |
| Cheap model for everything | 49% | 21% | 0% | $0.005 |
| Routed: 17 cases cheap, 33 strong | 70% | 12% | 0% | $0.07 |

**The routed setup fails the gate.** It cuts the estimated cost by about a third, and fabricated fields go from 2.6 to 5.9 a run, more than run-to-run noise explains (the gate allows 1.8). Under these assumptions, I wouldn't ship it.

Latency isn't in the table because a simulation has none. Real runs record the median seconds per case for each setup.

## Why it failed, and the tradeoffs

- **A keyword router can't see what's missing.** The most common trap is a field the request never mentions, like no moderator. Those requests read as plain, so the router sends them to the cheap model, which is exactly where the guessing happens. Five of the six missing-field cases went to the cheap model.
- **The flag is narrow.** It catches only requests that say something changed. It flagged 4 of 50 requests, and caught 1 of about 15 that had an error. A person checking every briefing still catches more.
- **The rules are tuned to this test set.** I wrote the keywords while reading these 50 cases, so their accuracy here is better than it would be on new requests.
- **Two models cost more to run well.** Each model has its own prompt cache, so routing gives up some cache savings, and there are two models to watch and test.
- **This test set is almost all traps.** 47 of 50 cases are built to trip a drafter. Real requests are mostly plain, so on real traffic more would go to the cheap model, and both the savings and the risk would be larger.

## What I'd try next

Route by what the draft says, not only by the request. The cheap model drafts first. Any field it filled goes to the strong model to check against the source, and any field it marked unknown stays blank. That targets the guess directly, and it costs one short check per briefing rather than a full strong-model draft.

## Real runs: the plan

`run_real.sh` runs all three setups for real, three times each over the 50 made-up cases, with Claude Sonnet 5.5 as the strong model and Claude Haiku 5.5 as the cheap one, both at low effort. It asks for the API key in the terminal without showing or saving it, and stops before any call once $1.95 has been spent. The expected cost is about $1. It writes `real-results.md` with cost per run, pass rate, failure rate, fabrication rate, latency and the gate result.

```
bash run_real.sh             # real, paid run
python3 real_run.py --dry-run  # same steps with the simulated models; free, no key
```

To run the setups by hand instead:

```
python3 evals.py estimate --runs 10 --price 2 10 --price 0.10 0.50
python3 evals.py --drafter anthropic --model claude-sonnet-5-5 --price-in 2 --price-out 10 \
    --effort low --runs 10 --max-spend 2 --out runs/all-strong.json
python3 evals.py --route --drafter anthropic \
    --cheap-model claude-haiku-5-5 --cheap-price 0.10 0.50 \
    --strong-model claude-sonnet-5-5 --strong-price 2 10 \
    --effort low --runs 10 --max-spend 2 --out runs/routed.json
python3 evals.py compare runs/all-strong.json runs/routed.json
```

The simulated results come from fixed seeds, so these rebuild the table above exactly:

```
python3 evals.py --drafter mock-strong --runs 10 --price-in 2 --price-out 10 --out runs/sim-strong.json
python3 evals.py --drafter mock-cheap --runs 10 --price-in 0.10 --price-out 0.50 --out runs/sim-cheap.json
python3 evals.py --route --cheap-drafter mock-cheap --cheap-price 0.10 0.50 \
    --strong-drafter mock-strong --strong-price 2 10 --runs 10 --out runs/sim-routed.json
python3 evals.py table runs/sim-*.json
```
