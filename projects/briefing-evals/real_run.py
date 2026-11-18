"""One real run of the cost and routing comparison, capped at a fixed spend.

Run it through run_real.sh, which sets up Python and asks for your key without saving it.
It reads the key only from the ANTHROPIC_API_KEY environment variable and never prints,
logs or writes it. Only the 50 made-up cases in cases/ are sent.

Three setups, each run RUNS times over all 50 cases:
  1. strong model for everything (the baseline)
  2. cheap model for everything
  3. routed: router.py sends easy requests to the cheap model, the rest to the strong one

It stops before any call that would start once MAX_SPEND has been spent, and writes
real-results.md: cost per run, pass rate, failure rate, fabrication rate and latency.
That file holds no key and nothing private, so it's safe to paste back or commit.

    python3 real_run.py            # real, paid run
    python3 real_run.py --dry-run  # same steps with the simulated models; free, no key
"""
from __future__ import annotations

import contextlib
import datetime
import io
import json
import os
import sys
from pathlib import Path

import evals

HERE = Path(__file__).parent
# Anthropic list prices, USD per million tokens (input, output), November 2026.
STRONG = ("claude-sonnet-5-5", (2.00, 10.00))
CHEAP = ("claude-haiku-5-5", (0.10, 0.50))
EFFORT = "low"     # field extraction doesn't need deep thinking; keeps output tokens down
RUNS = 3           # 3 per setup keeps the total near $1; the gate is sharper with more
MAX_SPEND = 1.95   # USD, across all three setups; one call can go past it by a few cents at most
PROMPT = HERE / "prompts" / "flag_gaps.txt"


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    if not dry and not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY isn't set. Start this with run_real.sh, which asks for it.")
    drafter = {"strong": "mock-strong", "cheap": "mock-cheap"} if dry else {"strong": "anthropic", "cheap": "anthropic"}
    evals.EFFORT = EFFORT
    evals.MAX_SPEND = None if dry else MAX_SPEND
    evals.PRICES.update({STRONG[0]: STRONG[1], CHEAP[0]: CHEAP[1]})
    out_dir = HERE / "runs"
    out_dir.mkdir(exist_ok=True)
    cases = evals.load_cases()

    plan = [
        ("all-strong", lambda: evals.run_suite(drafter["strong"], str(PROMPT), STRONG[0], RUNS, cases, *STRONG[1])),
        ("all-cheap", lambda: evals.run_suite(drafter["cheap"], str(PROMPT), CHEAP[0], RUNS, cases, *CHEAP[1])),
        ("routed", lambda: evals.run_routed((drafter["cheap"], CHEAP[0]), (drafter["strong"], STRONG[0]),
                                            str(PROMPT), RUNS, cases, CHEAP[1], STRONG[1])),
    ]
    records, stopped = {}, None
    for name, run in plan:
        print(f"Running {name} ({RUNS} runs of {len(cases)} cases)...", flush=True)
        try:
            records[name] = run()
        except evals.SpendCapReached as e:
            stopped = f"Stopped at {name}: {e}."
            print(stopped)
            break
        (out_dir / f"{'sim' if dry else 'real'}-{name}.json").write_text(json.dumps(records[name], indent=1))
        print(f"  done; about ${evals.SPENT:.2f} spent so far", flush=True)

    report = render(records, dry, stopped)
    path = HERE / ("dry-run-results.md" if dry else "real-results.md")
    path.write_text(report)
    print("\n" + report)
    print(f"Saved to {path}")
    return 0


def render(records: dict, dry: bool, stopped: str | None) -> str:
    def capture(fn, *a):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            fn(*a)
        return buf.getvalue().strip()

    cases = evals.load_cases()
    lines = [f"# Briefing evals: {'DRY RUN (simulated, not real)' if dry else 'real run'}",
             "",
             f"- Date: {datetime.date.today():%B %-d, %Y}",
             f"- Strong model: {STRONG[0]} (${STRONG[1][0]:g} in / ${STRONG[1][1]:g} out per million tokens)",
             f"- Cheap model: {CHEAP[0]} (${CHEAP[1][0]:g} in / ${CHEAP[1][1]:g} out per million tokens)",
             f"- Effort: {EFFORT}; prompt: {PROMPT.name}; {RUNS} runs per setup; 50 made-up cases",
             f"- Total spent: about ${evals.SPENT:.2f} (cap ${MAX_SPEND:.2f})",
             ""]
    if stopped:
        lines += [f"**{stopped}**", ""]
    if records:
        lines += [capture(evals.print_table, list(records.values())), ""]
    if "routed" in records:
        s = records["routed"]["runs"][-1]["summary"]
        lines += [f"Routing: {s['to_cheap']} cases to the cheap model, {s['to_strong']} to the strong one, "
                  f"{s['flagged']} flagged for a person.", ""]
        for name in ("all-strong",):
            if name in records:
                cmp = capture(evals.print_compare, records[name], records["routed"], cases)
                cmp = cmp.split("\nFlaky")[0].strip()  # keep the gate and the clear failures; flaky ones need more runs
                rows = cmp.splitlines()
                if len(rows) > 45:  # keep it short enough to paste; the full list is in runs/
                    cmp = "\n".join(rows[:45] + [f"... {len(rows) - 45} more lines in runs/real-*.json"])
                lines += ["## Strong for everything vs. routed", "", "```", cmp, "```", ""]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
