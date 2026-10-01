# Grammarly

**One-liner:** A writing assistant that checks grammar, spelling, tone, and clarity across every text field on the web, now expanding into full-text AI generation and rewriting.

---

## Metrics tree

```
Primary metric
└── Annual recurring revenue (ARR)
    ├── Individual subscribers (Free → Premium $12/mo → Pro $15/mo)
    │   ├── Free-to-Premium conversion rate
    │   │   ├── Weekly corrections delivered (value demonstration)
    │   │   ├── Premium feature gate hits (tone, clarity, full rewrites)
    │   │   └── Competitor-free retention (no substitute discovered)
    │   └── Premium retention rate
    │       ├── Corrections accepted rate (user trusts the suggestions)
    │       ├── Documents checked per week
    │       └── Cross-platform usage (desktop, browser, mobile)
    ├── Business accounts (per-seat, team features)
    │   ├── Seat count growth
    │   ├── Style guide adoption rate
    │   └── Enterprise security/compliance feature usage
    └── AI feature revenue (Pro tier and enterprise AI add-ons)
        ├── AI generation sessions per user
        ├── AI rewrite acceptance rate
        └── AI-to-core feature cannibalization rate
```

**The dangerous metric in this tree:** AI-to-core feature cannibalization rate. Grammarly's business was built on catching errors in text the user wrote. AI generation and rewriting produce text the user didn't write. If AI-generated text still flows through the correction engine, the correction engine catches fewer errors (because the AI doesn't make spelling mistakes), which makes the correction engine look less valuable, which weakens the case for Premium. The AI features risk hollowing out the product that pays the bills.

---

## Hypothesized funnel

| Stage | Estimated conversion | Where users drop and why |
|-------|---------------------|--------------------------|
| **Awareness** | Very high (~85% of English-language internet users in target markets) | Grammarly has spent heavily on brand advertising. Awareness is a solved problem. |
| **Install** | ~30% of aware users install the browser extension | The install rate is healthy but constrained by two factors: (1) users who write primarily on mobile, where the extension doesn't work as well, and (2) enterprise environments where IT policies block browser extensions. |
| **First correction accepted** | ~80% of installs | Grammarly's activation is best-in-class. The extension starts working immediately in whatever text field the user types in next. No setup, no configuration, no learning curve. The red underline is universally understood. This is the product's most defensible asset. |
| **Weekly active use** | ~55% of activated users | Grammarly retains well because it's ambient — it works in the background across every site. Users don't have to remember to open it. Drop-off is from users who write infrequently or who find the suggestions too aggressive (flagging stylistic choices as errors). |
| **Premium conversion** | ~8-10% of weekly active free users | **The conversion gate is well-designed but narrowing.** Free users see Premium suggestions grayed out (tone detection, clarity rewrites, vocabulary enhancement). The conversion trigger is hitting the gate repeatedly in a single writing session. The problem: as the free tier gets more capable (competitive pressure from free AI tools), the perceived gap between free and Premium shrinks. |
| **Premium retention** | ~80% annual | Premium churn is driven by: (1) users who upgraded for a specific project (job application, thesis) and don't need it ongoing, (2) users who discover that ChatGPT or Claude can do the same rewrites for free, and (3) users whose writing improved enough from Grammarly's corrections that they no longer need Premium-level help. The third reason is the "graduation problem" — the better the product works, the less the user needs it. |

**The core problem:** Grammarly built a trust-based product. Users trust the red underline because it catches real errors in their own writing. The AI generation and rewriting features break that trust model in a subtle way: when Grammarly writes text for you, you lose the ability to judge whether the correction engine is adding value. You can't tell if the AI wrote "affect" and the correction engine caught it, or if the AI wrote "effect" correctly on its own. The correction layer becomes invisible, which makes it feel unnecessary.

---

## The one feature I would kill

**Full-text AI generation ("Write for me")**

Grammarly now offers a feature where you describe what you want to write and it generates a complete draft. This directly competes with ChatGPT, Claude, and every other AI writing tool, and it does so from a position of weakness.

**Why it hurts:**

1. **It puts Grammarly in a fight it can't win.** Full-text generation is a commodity capability. Every LLM can do it. Grammarly's underlying models are not differentiated on generation quality. Users who want AI-generated text already have better tools (ChatGPT, Claude) that produce higher-quality output with more control. Grammarly's "write for me" is a worse version of something the user already has.

2. **It undermines the product's positioning.** Grammarly's brand is "make your writing better." The implicit promise is that the writing is yours, and Grammarly helps you improve it. "Write for me" turns Grammarly into "replace your writing," which is a fundamentally different value proposition. Users who came to Grammarly to improve their skills don't want a ghostwriter. Users who want a ghostwriter already use general-purpose AI tools.

3. **It degrades the correction feedback loop.** When a user writes and Grammarly corrects, the user learns. Over hundreds of corrections, they internalize rules: "it's 'fewer,' not 'less'" or "this sentence is too long." When Grammarly generates the text, there's nothing to learn. The educational flywheel — the thing that made users feel Grammarly was worth paying for — stops spinning.

**What data would make me keep it:** If "Write for me" users have Premium conversion rates 2x higher than correction-only users, the feature is driving revenue regardless of its strategic risk. If users who generate text with Grammarly use it in contexts where they wouldn't use ChatGPT (inline in a Gmail compose window, for instance), the feature has a distribution advantage that compensates for its quality disadvantage.

---

## The one feature I would build

**Writing fingerprint: a personal style model that makes corrections context-aware**

**The user problem:** Grammarly applies the same rules to everyone. A legal brief and a marketing email get the same suggestions. A user who deliberately writes in short, punchy fragments gets flagged for incomplete sentences every time. Over months of use, users train themselves to ignore certain categories of Grammarly suggestions, which erodes trust in all suggestions.

**The solution:** A user-specific style model built from the corrections they accept and reject. After 1,000+ interactions, Grammarly knows: this user always rejects sentence-length suggestions (they prefer short sentences), always accepts comma corrections (they're genuinely unsure about commas), and never changes "impact" to "affect" (they've decided "impact" as a verb is acceptable in their register). The correction engine then stops making suggestions the user consistently rejects and increases confidence on suggestions the user consistently accepts.

Beyond suppression, the style model enables positive features: "Your last 50 emails averaged 12 words per sentence. This draft averages 28. Want to break some up?" That's a correction no generic rule can make — it's grounded in the user's own established style.

**Target metric:** Correction acceptance rate. The hypothesis is that personalized suggestions increase acceptance rate from ~45% to ~65%, which directly correlates with perceived product value and Premium retention.

**What would have to be true:**
- 1,000 accept/reject interactions is enough signal to model preferences reliably (too few and the model overfits to noise)
- Users experience the personalization as "Grammarly gets me" rather than "Grammarly stopped catching things" (framing matters: the feature needs to be visible, not silent)
- The style model doesn't inadvertently suppress genuine errors by over-learning from a user who rejected a correct suggestion a few times
- Privacy: the style model stays local or encrypted, and the user can see, edit, and delete their style profile

---

## What data would change my mind

1. **If "Write for me" accounts for >20% of all AI-feature sessions and those users retain at rates equal to or better than correction-only users.** That would mean generation is a real use case for the Grammarly audience, not a distraction, and I'm underestimating the demand for AI generation inside existing writing contexts.

2. **If Grammarly's overall correction acceptance rate is already above 60% without personalization.** That would mean the generic rules are well-calibrated enough that user-specific tuning has limited room to improve, and the engineering cost of building style models isn't justified by the marginal quality gain.

3. **If the primary churn driver is price sensitivity, not perceived value.** If exit surveys show that churning users believe Grammarly is valuable but $12/month is too much, the product's problem is pricing or packaging, not the feature set. The right response would be a cheaper tier, not a new feature.
