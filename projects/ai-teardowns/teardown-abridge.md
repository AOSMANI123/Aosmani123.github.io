# Abridge

**One-liner:** Ambient AI that listens to a patient visit, drafts the clinical note, and links each sentence back to the moment in the conversation it came from.

**Thesis:** Abridge sells seats, but it keeps customers on frequency. Most clinicians don't use an AI scribe often enough to feel the benefit, and Epic now offers a built-in option that is "good enough" and already in the chart.

*Written November 2026 from public sources, listed at the end. Independent work, not affiliated with any employer.*

---

## Metrics tree

```
Primary metric
└── Contracted annual recurring revenue
    ├── Health systems under contract (300+ live, June 2026, per Fortune)
    ├── Licensed clinicians per system
    └── Renewal and expansion at each system
        ├── Clinicians who record most of their visits   <- the metric that matters
        ├── Note time saved per clinician (minutes per day)
        └── Products beyond the note (coding, revenue cycle)
```

**Secondary metric (the one that actually matters):** the share of licensed clinicians who record at least half of their visits. A large study in JAMA (April 1, 2026; five hospitals, about 1,800 scribe users) found those clinicians saved about twice the EHR time and three times the documentation time of everyone else. Only 32% of users got there. On average, the savings were modest: about 16 minutes less documentation per day, and no change in after-hours EHR time.

**Why this distinction matters:** it makes the licensed seat count a vanity metric. A health system that pays for 1,000 seats and sees 320 heavy users will ask why it's paying for the other 680, especially once Epic's own tool is an option.

---

## Hypothesized funnel

These are my hypotheses, stated so they can be tested. Only the regular-use figure comes from published data.

1. **System signs:** strong. Abridge has the brand, the Best in KLAS rating for revenue cycle, and large names like Kaiser Permanente and the VA.
2. **Clinician gets a license:** high, because rollout is top-down.
3. **First recorded visit:** I'd guess 70 to 85% of licensed clinicians try it within a month.
4. **Regular use (half of visits or more):** about 32%, per the JAMA study across five hospitals. This is the biggest drop.
5. **Signs the note with light edits:** unknown. No public study measures edit time, including the Kansas study of Abridge itself.
6. **System renews and expands:** depends on step 4 more than any other.

---

## The one feature I would kill

**Checking the note outside the chart.** Linked Evidence is Abridge's best trust feature: highlight a sentence and it shows, and plays, the part of the visit it came from. But Abridge's own help page describes doing this in its separate web editor. If a clinician has to leave the record to check a sentence, most won't, and the feature that builds trust goes unused. I'd move that check into the note inside the EHR and stop sending people to a second screen.

**What would make me keep it:** data showing most Linked Evidence use already happens inside the EHR, or that clinicians who use the web editor are the heaviest users.

---

## The one feature I would build

**A frequency coach for light users.**

**The user problem:** most licensed clinicians use the scribe for a minority of visits, so they never feel the time saved and their system never sees the return.

**The solution:** each week, show a light user their own minutes saved on recorded visits against the visits they didn't record. Then offer to start recording by default for the visit types where they already use it.

**Target metric:** the share of licensed clinicians recording at least half of their visits, from a 32% baseline.

**What would have to be true:**
- Light use comes from habit and friction, not distrust of the notes.
- Recording by default still respects each patient's consent.

---

## What data would change my mind

1. **If Abridge's own customers reach regular use well above 32%.** Then the funnel problem belongs to other vendors, and the risk is Epic, not frequency.

2. **If systems that turn on Epic's AI Charting keep renewing Abridge at the same rate.** Then the built-in threat is overstated, and specialty depth is the moat.

3. **If light users edit far more per note than heavy users.** Then the problem is note quality, and I'd build for accuracy instead of habit.

---

## Sources

- [JAMA study coverage, April 1, 2026](https://www.news-medical.net/news/20260401/AI-scribes-modestly-reduce-clinician-documentation-time-and-EHR-use.aspx): five hospitals, about 1,800 users, 32% heavy use.
- [University of Kansas study of Abridge, JAMIA Open, February 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11843214/): self-reported burnout and after-hours time; no edit or quality measures.
- [Epic's AI Charting launch, HIT Consultant, February 5, 2026](https://hitconsultant.net/2026/02/05/epic-releases-ai-charting-ambient-ai-market-implications/)
- [Abridge help page on Linked Evidence](https://support.abridge.com/hc/en-us/articles/30235128433811-Verify-a-Note-With-Linked-Evidence)
- [Funding, customers and the KLAS rating, summarized by Value Add VC](https://valueaddvc.com/blog/abridge-valuation-2026-5-3b-100m-arr-and-how-the-ai-scribe-beat-nuance-and-ambience): a secondary source citing Fortune and Abridge releases.
