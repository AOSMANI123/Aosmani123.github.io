# Prompts

Generic versions of the three AI Builder prompts. Replace the bracketed parts with your office's details.

## 1. Extraction (Flow 1)

```
Read the email thread below. It is a request for [Executive Title] to take part in an event.

Return JSON with these keys:
event_name, event_date, requestor_name, requestor_email, requestor_org, industry, summary, next_step

Rules:
- Use only what the thread states about this event.
- If a value is not stated, return an empty string. Do not guess, and do not use dates from past events.
- The requestor is the person asking on behalf of the event, not someone who forwarded the email.
- industry must be one of: [list your 8-10 choices].
- summary: two or three plain sentences saying what is being asked, by whom, and by when.
- next_step: one suggested action for the team. It is a suggestion; a person decides.

Email thread:
[Body]
```

## 2. Digest summary line (Flow 2)

```
Write one line (under 25 words) for a weekly digest, from these fields:
[Title], [Event Date], [Requestor Org], [AI Summary]
Lead with the ask. No adjectives about the event's importance.
```

## 3. Decline draft (Flow 3)

```
Draft a short, warm reply declining this request on behalf of [Executive Name]'s office.

- Thank the requestor by name for thinking of [Executive Name].
- Say that [Executive Name] is not able to take part this time. Do not give a reason unless one is in the Decision Notes.
- Do not suggest a substitute speaker or a future date unless the Decision Notes say to.
- Under 90 words. Sign off as [Team Name].

Requestor: [Requestor Name], [Requestor Org]
Event: [Title], [Event Date]
Decision Notes: [Decision Notes]
```

The draft lands in the Drafts folder. Someone on the team reads it, edits it and sends it.
