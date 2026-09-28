# Engagement Tracker Template

A free, step-by-step template for tracking requests for a leader's time: speaking invitations, meetings, interviews, panels, school visits, video messages. It's written for someone who has never built an automation before.

I built the original for a senior executive's office at Microsoft, where it cut the time to update each request by 80%. This version is generic. It contains no company data. The full story is in the [case study](https://aosmani123.github.io/projects/engagement-triage/).

## What it does

1. Requests arrive by email.
2. AI reads each one and fills a row in a shared list: event, date, who's asking, their organization, a short summary.
3. Every Monday, your team gets one email with everything that needs a decision.
4. When the answer is no, a polite decline is drafted for a person to review and send.
5. When the answer is yes, the details are poured into your briefing template.

**The one rule:** the human is always the final sender. AI reads, sorts and drafts. A person decides and sends. Nothing goes out automatically.

## Who it's for

Any team that manages requests on someone else's behalf: executive and chief of staff offices, university presidents' and deans' offices, nonprofit leadership, civic offices, speakers bureaus. If you get more than a handful of requests a week and more than one person touches them, it's worth it.

## What you need

| Tool | What it is | Do you have it? |
|---|---|---|
| Outlook | Email, with a shared inbox for requests | Most Microsoft 365 workplaces |
| SharePoint Lists | A shared, spreadsheet-like list | Most Microsoft 365 workplaces |
| Power Automate | "When this happens, do that" automation, no coding | Most Microsoft 365 workplaces |
| AI Builder | Lets Power Automate send text to an AI model | May need an add-on or credits. Ask your IT admin |
| Word | For your briefing template | Most Microsoft 365 workplaces |

**Not on Microsoft 365?** The same design works with Google Sheets or Airtable for the list, Zapier or Make for the automations, and any AI step those tools offer.

**No AI access yet?** Build steps 1 to 3 below anyway. A shared list and a Monday email fix most of the problem on their own. Add AI later.

## Files in this folder

| File | What's in it |
|---|---|
| `list-schema.csv` | The columns to create in your list, what each one is for, and whether AI or a person fills it in |
| `prompts.md` | The instructions to give the AI: one for reading requests, one for the Monday summary lines, one for decline drafts |

## Build it in this order

Each step works on its own, so you get value before the whole thing is done.

**Step 1. Create the list (30 minutes).** Make a new SharePoint List and add the columns in `list-schema.csv`. Set up the Status choices first (New, Needs decision, Accepted, Decline, Scheduled, Closed), because the automations key off them. For now, add a few requests by hand.

**Step 2. Add views (15 minutes).** Views are saved filters, so each person sees only what they need:

| View | For | Filter |
|---|---|---|
| Triage | Whoever makes the first call | Status is New or Needs decision |
| Schedule | Scheduler or assistant | Status is Accepted or Scheduled, sorted by date |
| Leadership | Chief of staff or team lead | Status is Needs decision |
| Production | Whoever writes briefings | Status is Accepted |
| All requests | Anyone | Everything, including declines and why |

**Step 3. Send the Monday email (1 hour).** In Power Automate, create a scheduled flow that runs Monday morning, gets every item where Status is New or Needs decision, and emails the team a table. Send it only to yourself for two weeks before adding anyone else.

**Step 4. Let AI read new requests (2 to 3 hours).** Create a flow that runs when a new email arrives in the shared inbox. It sends the email text to AI Builder with the "Reading a request" instructions in `prompts.md`, then creates a list row from what comes back. Before connecting it to the live inbox, run it on ten old requests and check every field by hand.

**Step 5. Draft declines (1 hour).** Create a flow that runs when Status changes to Decline. It sends the details to AI Builder with the "Drafting a decline" instructions and saves the result as a draft in the shared inbox. It never sends. A person does.

**Step 6. Fill in briefings (optional).** For accepted requests, map list fields into a Word briefing template so prep starts mostly filled in.

## Tips

- Write your acceptance criteria down, even if it's five bullets. The tracker makes decisions faster, but it can't tell you what "yes" should mean.
- Keep the Industry choices to eight or ten. Short lists make AI sorting more reliable.
- Save why each request was accepted or declined in Decision Notes. Over a year, that becomes your record of what you say yes to.
- Log the AI's answer next to any correction a person makes. That log shows you where the AI goes wrong, and becomes a test set like my [briefing evals](../../briefing-evals/).

## Words you'll see

| Term | Meaning |
|---|---|
| Engagement | Any request for a leader's time |
| Flow | One automation in Power Automate ("when X happens, do Y") |
| Trigger | The event that starts a flow, such as a new email arriving |
| Prompt | The written instructions you give the AI |
| View | A saved filter on the list |
| Triage | Sorting new requests so the right ones get a decision first |
