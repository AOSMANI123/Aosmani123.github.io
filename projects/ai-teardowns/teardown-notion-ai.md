# Notion AI

**One-liner:** AI writing, summarization, and Q&A features embedded directly into Notion's workspace product, available as a per-seat add-on.

---

## Metrics tree

```
Primary metric
└── AI add-on revenue (seats × $8-10/mo per member)
    ├── AI add-on attach rate (% of Notion seats that add AI)
    │   ├── In-product AI trial starts
    │   ├── Trial-to-paid conversion
    │   └── Team-level adoption (one user tries → team buys)
    ├── AI feature usage frequency (actions per user per week)
    │   ├── Write/edit actions (drafting, rewriting, tone changes)
    │   ├── Summarization actions (page summaries, meeting notes)
    │   ├── Q&A actions (asking questions about workspace content)
    │   └── Autofill actions (database property generation)
    └── AI-driven retention uplift (does AI reduce Notion churn?)
        ├── Engagement lift for AI users vs. non-AI users
        └── Workspace content volume growth (AI users create more?)
```

**The tension in this tree:** Notion AI has to serve two masters. It needs to generate enough standalone revenue to justify its cost (inference is expensive at scale). But it also needs to make the core Notion product stickier. These goals conflict when AI usage replaces manual engagement with the workspace.

---

## Hypothesized funnel

| Stage | Estimated conversion | Where users drop and why |
|-------|---------------------|--------------------------|
| **Awareness** | ~85% of active Notion users | Notion promotes AI heavily in-product: the sparkle icon, the slash command menu, inline prompts. Hard to miss. |
| **First use** | ~50% of aware users try AI at least once | The slash-command trigger (`/ai`) makes first use nearly frictionless. Drop-off is from users who don't write long-form content in Notion (project managers who use it for task boards, not documents). |
| **Repeated use** | ~20% of first-use users become weekly AI users | **This is where the funnel breaks.** The problem is quality variance. AI writing assistance works well for generic content (meeting notes, status updates) but poorly for anything requiring domain knowledge, brand voice, or specific context. Users try it three times, get two mediocre outputs, and revert to typing. |
| **Paid conversion** | ~15% of Notion workspaces purchase the add-on | The per-seat pricing model is the conversion killer for teams. At $8-10/seat/month, a 50-person team pays $400-500/month for AI features that only 5-10 people use regularly. The buyer (usually an admin or team lead) can't justify per-seat pricing when usage is concentrated in a few power users. |
| **Retention** | ~70% annual retention for AI add-on | Teams that bought the add-on churn when they realize usage plateaued after month two. The initial excitement fades, usage concentrates in 2-3 use cases (summarize this page, help me start this doc), and the admin questions whether $400/month is worth what is functionally a summarization tool. |

**The core problem:** Notion AI has a usage-concentration problem. It's bought per-seat but used by a minority of seats. The features that work well (summarization, first-draft generation) are infrequent needs, not daily habits. And the features that could be daily habits (Q&A across the workspace) aren't reliable enough to trust.

---

## The one feature I would kill

**AI tone/style rewriting ("make more professional," "make shorter," "make more casual")**

**Why it hurts:**

1. **It trains users to distrust AI output.** The workflow is: AI generates text → user reads it → user asks AI to rewrite it → user reads it again → user manually edits anyway. The rewrite step adds a round-trip that rarely produces text the user accepts without further editing. It's a polite way of telling the user "I couldn't get it right the first time."

2. **It cannibalizes the core editing experience.** Every minute a user spends cycling through AI tone options is a minute they're not writing in Notion's editor. The block editor is Notion's core product strength. AI rewriting pulls users out of the composing mindset and into a "prompt and evaluate" loop that is slower for anyone who can type at a reasonable speed.

3. **It commoditizes the AI offering.** Every AI writing tool offers tone rewriting. It's table stakes, not differentiation. Notion's unique advantage is that it has the user's entire workspace as context — their meeting notes, project docs, wikis, databases. Tone rewriting uses none of that context. It treats each text block as isolated content.

**What data would make me keep it:** If users who use tone rewriting have 30%+ higher weekly engagement with Notion (not just with AI features) than users who don't, the feature is driving overall product stickiness, not just AI usage. If tone rewriting is the top-cited reason in surveys for purchasing the AI add-on, removing it would directly hurt conversion.

---

## The one feature I would build

**Workspace-native Q&A that actually works as institutional memory**

**The user problem:** Teams put years of decisions, context, and rationale into Notion pages. Six months later, nobody can find the page where the team decided to deprecate a feature or why the pricing changed. The information exists but it's buried. Search returns pages, not answers.

**The solution:** A Q&A system that answers questions by citing specific Notion pages and blocks. Not "here's a summary of what I found" but "the team decided X on [date] in [this page], and the reasoning was [quoted block]." The answer includes a confidence score: high confidence when it found a single clear source, low confidence when it's synthesizing across multiple pages, and "I don't know" when the workspace doesn't contain the answer.

The key difference from current Notion AI Q&A: source attribution at the block level (not page level), explicit confidence indicators, and the ability to say "this isn't in your workspace" instead of generating a plausible-sounding answer from general knowledge.

**Target metric:** AI Q&A weekly active users as a percentage of workspace members. The hypothesis is that reliable, well-cited Q&A converts AI from a writing tool (used by content creators) to a knowledge tool (used by everyone on the team, including those who never write long-form content).

**What would have to be true:**
- Answer accuracy with correct source citation exceeds 80% for questions whose answers exist in the workspace
- The system reliably says "I don't know" when the answer isn't in the workspace (false-answer rate below 5%)
- Non-writer personas (PMs, engineers, designers who use Notion for task management) adopt Q&A at rates comparable to writers
- Latency is under 5 seconds for most queries (slow answers break the "just check Notion" habit)

---

## What data would change my mind

1. **If AI add-on retention at 12 months is above 85%.** That would mean the usage-concentration problem is less severe than hypothesized — either more users adopt than I expect, or the users who do adopt find it valuable enough that team leads don't question the cost.

2. **If tone rewriting is used in >40% of AI sessions and users who rewrite accept the output without further manual editing >60% of the time.** That would mean the feature is delivering real value, not just giving users a polished illusion of productivity.

3. **If the primary competitor threat comes from standalone AI writing tools (Jasper, Copy.ai) rather than from workspace competitors adding AI (Coda, Confluence).** That would mean Notion's AI challenge is feature quality, not platform strategy, and the right move is to improve the writing tools rather than pivot to knowledge management.
