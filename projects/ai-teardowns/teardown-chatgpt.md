# ChatGPT

**One-liner:** A general-purpose conversational AI that lets anyone ask questions, write text, analyze data, and generate code through a chat interface.

---

## Metrics tree

```
Primary metric
└── Monthly active users (MAU)
    ├── New user acquisition
    │   ├── Organic sign-ups (word of mouth, search)
    │   ├── Paid acquisition (partnerships, ads)
    │   └── Viral loops (shared conversations, GPTs)
    ├── Activation rate (% who complete a meaningful first session)
    │   ├── Time to first query (< 30 seconds target)
    │   ├── First-session query count (>= 3 signals value found)
    │   └── First-session satisfaction (response rated helpful)
    └── Retention (W1, W4, W12 cohort retention)
        ├── Weekly query volume per active user
        ├── Use case breadth (categories of queries per user)
        ├── Paid conversion rate (free → Plus/Team)
        └── Query success rate (user didn't rephrase or abandon)
```

**Why this tree matters:** OpenAI reports MAU because it's large and growing. But MAU alone hides the question that determines the business: are people coming back? A product with 200M MAU and 15% W4 retention is a revolving door. The tree exposes that retention, not acquisition, is the metric that needs to move.

---

## Hypothesized funnel

| Stage | Estimated conversion | Where users drop and why |
|-------|---------------------|--------------------------|
| **Awareness** | Very high (90%+ of internet users in target markets have heard of it) | Not a bottleneck. ChatGPT has near-universal awareness in its target demographics. |
| **Sign-up** | ~60% of those who visit the landing page | The sign-up wall is a real gate. Users who arrive from a shared conversation link and hit a login screen bounce. Google sign-in mitigates but doesn't eliminate this. |
| **First query** | ~70% of sign-ups | **This is the biggest drop.** The empty prompt box is the product's original sin. New users face a blank text field and no structured guidance on what ChatGPT is good at. The suggested prompts are generic and don't match the user's actual context. ~30% of new sign-ups never submit a meaningful query. |
| **First valuable session** | ~50% of first-query users | The user asks something, gets a response, but doesn't experience the "aha" moment. Common failure: the first query is too vague ("tell me something interesting") and the response is generic. Or the first query is too specific and domain-expert, and the response is confidently wrong. |
| **Habit formation (weekly use)** | ~25% of activated users | This is where the funnel collapses. Users who had one good session don't come back because they don't have a mental model of when to use ChatGPT. It's not tied to a workflow. There's no trigger. The product waits passively for the user to remember it exists. |
| **Paid conversion** | ~5-8% of weekly active users | Plus conversion is gated on power use. Users who hit rate limits or want GPT-4 access convert. But the free tier is generous enough that most weekly users never feel the constraint. |
| **Retention (W12)** | ~15-20% of paid users churn per quarter | Paid users churn when a new model release doesn't noticeably improve their use case, or when a competitor (Claude, Gemini) offers comparable quality for less friction. |

**The core problem:** ChatGPT acquires users effortlessly but retains them poorly. The funnel is widest at the top and narrows fastest at the habit-formation stage because the product has no opinion about what you should use it for.

---

## The one feature I would kill

**Custom GPTs (the GPT Store)**

The GPT Store is OpenAI's attempt to build a platform play: let creators build specialized versions of ChatGPT, distribute them through a marketplace, and earn revenue share. It's hurting the product in three ways:

1. **It fragments the user experience.** A new user who discovers a custom GPT has a worse first experience than using base ChatGPT, because most custom GPTs are poorly built wrappers with bad system prompts. The median GPT in the store adds negative value.

2. **It dilutes product focus.** Engineering and design resources spent on GPT creation tools, the store's discovery UI, the revenue-share infrastructure, and creator tooling are resources not spent on making the core chat experience sticky. The platform bet is premature when the core product hasn't solved retention.

3. **It creates a lemons problem.** Without quality control, the store fills with low-effort GPTs that erode trust in the concept. Users who try two bad GPTs stop browsing the store entirely.

**What data would make me keep it:** If GPT Store users have W4 retention 2x higher than non-store users (controlling for power-user bias), the store is driving habit formation and I'm wrong. If >10% of new users discover ChatGPT through a shared custom GPT link and activate at a higher rate than organic sign-ups, the store is a genuine acquisition channel.

---

## The one feature I would build

**Workflow triggers: proactive nudges tied to the user's actual tools**

**The user problem:** People forget ChatGPT exists between sessions. The product sits in a browser tab and waits. There's no integration into the moments where AI would actually help.

**The solution:** Deep integrations into calendar, email, and browser that create natural triggers. Not a full agent that acts on your behalf, but a notification layer: "You have a meeting with [person] in 30 minutes — want a briefing on the last three emails from them?" or "You just copied a block of text — want to clean it up?" or "You bookmarked five articles on [topic] this week — want a synthesis?"

**Target metric:** W1 retention. The hypothesis is that users who receive 3+ contextual triggers per week have 2x the W1 retention of users who rely on self-initiated sessions.

**What would have to be true:**
- Users grant the necessary permissions (calendar, email) at a rate above 30% when prompted during onboarding
- The trigger suggestions are relevant at least 60% of the time (below that, users disable notifications)
- The triggers lead to completed sessions, not just opened-and-abandoned tabs
- Privacy concerns don't create a backlash that outweighs the retention benefit

---

## What data would change my mind

1. **If ChatGPT's W4 retention among free users is above 40%.** That would mean the empty-prompt-box problem is less severe than hypothesized, and the product's retention is actually healthy for a general-purpose tool. The feature recommendations would shift from "create triggers" to "optimize conversion."

2. **If users who create or regularly use custom GPTs retain at 3x the base rate, even after controlling for overall engagement level.** That would mean the GPT Store is the retention solution, not the problem, and the right move is to invest more in store quality rather than kill it.

3. **If the average ChatGPT session starts from the ChatGPT app/site directly (not from a workflow integration or link) for retained users.** That would mean habitual users have already built their own mental triggers, and the product doesn't need to create them artificially.
