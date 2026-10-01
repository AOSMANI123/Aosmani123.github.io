# Midjourney

**One-liner:** An AI image generation tool that turns text prompts into high-quality images, originally distributed through Discord and now expanding to a web application.

---

## Metrics tree

```
Primary metric
└── Monthly recurring revenue (MRR)
    ├── Subscriber count
    │   ├── New subscriber acquisition
    │   │   ├── Discord-native discovery (seeing others' generations)
    │   │   ├── Social media virality (shared images with attribution)
    │   │   └── Web app organic search and direct traffic
    │   ├── Plan tier mix (Basic $10 / Standard $30 / Pro $60 / Mega $120)
    │   │   ├── Upgrade rate from Basic to Standard (GPU hours as constraint)
    │   │   └── Pro/Mega adoption (commercial use, high volume)
    │   └── Churn rate
    │       ├── GPU hour exhaustion frustration
    │       ├── Prompt-to-output quality satisfaction
    │       └── Competitive switching (DALL-E, Stable Diffusion, Flux)
    └── Revenue per subscriber (ARPS)
        └── Tier distribution × pricing
```

**What's unusual about this tree:** Unlike most AI products, Midjourney's primary acquisition channel (Discord) doubles as its engagement engine. Users generate images in public channels, see what others create, learn prompting techniques from the community, and discover use cases they hadn't considered. The acquisition and engagement loops are the same loop. That's a strength until the company tries to leave Discord.

---

## Hypothesized funnel

| Stage | Estimated conversion | Where users drop and why |
|-------|---------------------|--------------------------|
| **Awareness** | High in creative communities (~70%), low in mainstream (~20%) | Midjourney images circulate widely on social media but are often shared without attribution. Many people see AI-generated images daily without knowing Midjourney made them. The brand awareness gap between creative professionals and general consumers is a strategic choice, not a failure. |
| **Discord join** | ~35% of aware users join the Discord server | **First major drop.** Requiring Discord is a filter. Users who don't already have Discord must download a new app, create an account, and navigate an unfamiliar interface to use an image generation tool. For non-gamers and non-technical users, this is a hard stop. The web app is changing this, but as of late 2026, Discord remains the primary onramp. |
| **First generation** | ~60% of Discord joiners | Users who make it to the server face a chaotic experience: thousands of messages scrolling in public channels, slash commands they've never used, and their generated images mixed in with hundreds of others. The learning curve for prompting is steep and largely undocumented. Users who generate their first image in a public channel often can't find it again. |
| **Paid subscription** | ~40% of first-generation users | This conversion rate is high relative to most freemium products because Midjourney's free tier is extremely limited (25 generations). The aggressive gate works because users who have seen one impressive generation are emotionally invested. But it also means the product has very little time to demonstrate value before asking for money. |
| **Monthly retention** | ~65% month-over-month | The users who churn fall into two buckets: (1) hobbyists who generated all the images they wanted in month one and have no ongoing need, and (2) power users who hit GPU-hour limits and switch to Stable Diffusion for unlimited local generation. The first bucket is a use-case problem. The second is a pricing problem. |
| **Tier upgrade** | ~20% of Basic subscribers upgrade within 6 months | GPU hours are the constraint that drives upgrades. Users who hit the Basic limit and value the output quality enough to pay more will upgrade. Users who hit the limit and find "good enough" alternatives elsewhere churn instead. |

**The core problem:** Midjourney's Discord-native distribution was brilliant for early growth — the public channels created a viral, social, learn-by-watching experience that no competitor matched. But the same distribution model is now a ceiling. Every non-Discord user is a lost potential subscriber. The web app transition isn't just a UX improvement; it's an existential migration.

---

## The one feature I would kill

**Public generation channels on Discord**

Public channels — where your generations appear alongside thousands of others — were the original Midjourney experience and the engine of its virality. I'd sunset them for new users and move all generation to DMs or the web app.

**Why they hurt now:**

1. **Privacy is a dealbreaker for commercial users.** Designers, marketers, and brand teams won't use a tool where their creative explorations are visible to the entire server. Every competitor offers private generation by default. Public channels signal "this is a toy," not "this is a professional tool."

2. **The noise destroys usability.** In a busy public channel, your four generated images scroll off screen within seconds. Finding, upscaling, and iterating on your generations requires either slash commands or scrolling through hundreds of other people's images. This is the worst UX of any mainstream creative tool.

3. **They create a false impression of the product.** New users see the chaotic public channels and think that's the product. The actual product — private generation with upscaling, variation, and parameter control — is hidden behind the noise. Public channels are now an anti-demo.

**What data would make me keep them:** If users who start in public channels have W4 retention 1.5x higher than users who start in DMs or the web app, the social discovery effect is still driving engagement more than the friction costs. If >25% of new subscribers cite "seeing what others create" as their primary reason for subscribing, public channels are still the acquisition engine and removing them would cut the viral loop.

---

## The one feature I would build

**Style memory: a persistent creative identity per user**

**The user problem:** Every Midjourney session starts from zero. A designer who has spent three months developing a specific visual style — warm analog tones, particular composition preferences, consistent lighting — has to reconstruct that style from scratch in every prompt. The prompt engineering knowledge lives in the user's head (or in a messy text file of saved prompts), not in the product. Style references (`--sref`) help but require the user to manage reference images externally.

**The solution:** A "style profile" that Midjourney learns from your generation history. After 50+ generations, the product identifies your aesthetic patterns: color palettes you upscale most, composition types you prefer, styles you consistently reject. The style profile becomes a persistent parameter. You can say "generate in my style" and get output that's consistent with your established preferences, or "generate in [saved style name]" to switch between multiple style identities.

**Target metric:** Monthly generation volume per subscriber. The hypothesis is that style memory reduces prompt iteration time by 40% (fewer attempts to recreate a look) and increases monthly generation volume by 25%, which directly drives GPU-hour consumption and tier upgrades.

**What would have to be true:**
- 50 generations is enough data to extract meaningful style preferences (too few and the profile is noise; too many and users churn before the feature activates)
- Style extraction can run on generation metadata and upscale choices without requiring users to explicitly label preferences (implicit signal only)
- The style profile produces noticeably consistent output — users should be able to tell their images apart from generic Midjourney output
- Saving and switching between multiple style profiles doesn't add complexity that overwhelms casual users

---

## What data would change my mind

1. **If the web app's organic acquisition rate exceeds Discord's within 6 months of launch, without cannibalizing Discord subscriptions.** That would mean the Discord-to-web transition is proceeding successfully and the public-channel problem is solving itself without needing to be forced.

2. **If commercial/enterprise users (agencies, brand teams) already make up >30% of Pro and Mega subscribers.** That would mean the privacy concern is less of a barrier than hypothesized — commercial users are finding ways to work within the current system.

3. **If generation volume per user is already growing quarter-over-quarter without style features.** That would mean the prompt-iteration friction is less of a bottleneck than I'm estimating, and the product's growth constraint is elsewhere (acquisition, not engagement depth).
