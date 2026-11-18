"""Model routing for the briefing drafter: decide, from the request text alone, which
model should draft it and whether a person should check the result.

Three routes:
    easy   -> the cheap model. Nothing in the text looks like a known trap.
    hard   -> the strong model. The text has a pattern the evals show tempts a drafter
              (a forward, last year's details, a "TBD", a vague number, a second event).
    review -> the strong model drafts it, and the briefing is flagged for a person,
              because the request says a detail changed. A briefing that keeps the old
              value looks right and can get signed.

The router only reads the request. It never sees the answer key or the case's category,
because in real use neither exists. The categories are used only offline, to check how
often the router's guesses line up with what each case is actually testing.

These are keyword rules, not a model. They are cheap, fast and easy to read, and they
miss things a model would catch. That tradeoff is the point of writing them down.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# Each signal: name, the pattern, and the route it pushes toward.
# Patterns are matched case-insensitively against the whole request.
REVIEW_SIGNALS = [
    ("correction", r"\b(correction|corrected|update[sd]?:|quick update|change of plans?)\b"),
    ("moved", r"\b(moved|rescheduled|postponed|pushed (back|to)|now (fully )?(virtual|online|in person))\b"),
    ("replaced", r"\b(instead of|no longer|will now|replac(e|es|ed|ing)|taking over from|stepping in for)\b"),
]
HARD_SIGNALS = [
    ("forwarded", r"(\bfwd?:|\bforward(ed|ing)\b|-{3,}\s*original message|begin forwarded message)"),
    ("past_event", r"\b(last year|last time|previous(ly)?|in the past|past years?|prior year|our \d{4} (event|gala|forum|summit))\b"),
    ("not_set", r"\b(tbd|tbc|tba|to be (confirmed|determined|announced|decided)|pending|not yet (set|confirmed|final)|still (being )?(decid|confirm|finaliz|work))"),
    ("options", r"\b(shortlist|either\b.{0,40}\bor\b|one of (two|three)|deciding between)"),
    ("vague_number", r"\b(hundreds|thousands|dozens|a (big|large|full|packed) (crowd|house|room)|capacity|registrations?|roughly|approximately|about \d|around \d|\d+\s*(-|to|–)\s*\d+ (people|attendees|guests))\b"),
    ("other_people", r"\b(introduce|introduction|open the (evening|event)|welcome remarks|panelists?|co-?host|point of contact|logistics contact|on behalf of|suggested (i|we) reach out|passed (along|your name)|left the (organization|company))\b"),
    ("other_event", r"\b(also (hosting|holding|running)|separately|another event|our (gala|dinner|series)|monthly|declined|next (month|year)'?s?)\b"),
]
DATE = re.compile(
    r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.? \d{1,2}(st|nd|rd|th)?\b", re.I)


@dataclass
class Route:
    tier: str                       # easy | hard | review
    reasons: list[str] = field(default_factory=list)

    @property
    def model_tier(self) -> str:
        """Which model drafts it: the cheap one only for easy requests."""
        return "cheap" if self.tier == "easy" else "strong"

    @property
    def needs_human(self) -> bool:
        return self.tier == "review"


def route(source: str) -> Route:
    text = source.lower()
    review = [name for name, pat in REVIEW_SIGNALS if re.search(pat, text)]
    hard = [name for name, pat in HARD_SIGNALS if re.search(pat, text)]
    if len({m.group(0).lower() for m in DATE.finditer(source)}) >= 2:
        hard.append("two_dates")
    if review:
        return Route("review", review + hard)
    if hard:
        return Route("hard", hard)
    return Route("easy", [])
