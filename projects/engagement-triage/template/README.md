# Engagement triage template

A reusable version of the engagement tracker I built at Microsoft for a Corporate Vice President's office. It runs on tools most Microsoft 365 teams already have: Power Automate, AI Builder, SharePoint Lists and Outlook. Nothing here is specific to Microsoft's internal data. The list schema and prompts are rewritten as generic starting points.

The rule the whole design follows: **the human is always the final sender.** AI reads, extracts, summarizes and drafts. A person decides and sends.

## The pipeline

```
Shared mailbox ──> Flow 1: Intake ──> SharePoint List ──> Flow 2: Monday digest ──> Decision
                   (AI Builder                              (open requests +          │
                    extraction)                              decline queue)            │
                                                                                      ▼
                                          Flow 4: Brief ◄── Accepted     Declined ──> Flow 3: Draft decline
                                          (list fields → Word template)               (to Drafts folder; a
                                                                                       person edits and sends)
```

| Flow | Trigger | What it does |
|---|---|---|
| 1. Intake | New email in the shared mailbox | Runs the extraction prompt, writes one list item per request with the AI summary and a suggested next step |
| 2. Monday digest | Weekly, Monday morning | Email 1: open requests that need a decision, each with its summary. Email 2: the decline queue, so low-fit asks clear in one review |
| 3. Draft decline | Status set to Decline | Runs the decline prompt and saves a draft reply in the Drafts folder. Staff edit if needed and send from their own mailbox |
| 4. Brief | Status set to Accepted | Maps list fields into a Word brief template (Microsoft Syntex in my version) and drafts a speaker-context section for review |

## Views

One list, several filtered views for different readers: **Triage** (open requests), **Schedule**, **Chief of Staff view**, **Production tracker** and **All items**. Each reader gets the slice they need without a separate report.

## Files

- `list-schema.csv`: columns for the SharePoint List
- `prompts.md`: the extraction, summary and decline prompts

## Setup order

1. Create the list from `list-schema.csv`. Add the Status choices first; the flows key off them.
2. Build Flow 1 and run it on ten old requests before connecting the live mailbox. Check every extracted field by hand.
3. Add the views, then Flow 2. Send the digest to yourself for two weeks before adding anyone else.
4. Add Flows 3 and 4 last. They're the ones that produce text other people will read.

## If you build this

- The digest needs only a list and a filter, so it can ship before any AI step does.
- Log every AI-extracted field next to the human-corrected value from day one. That log becomes your eval set (see [briefing evals](../../briefing-evals/)).
