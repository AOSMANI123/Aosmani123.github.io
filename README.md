# Atif Osmani · Product portfolio

**Live site: [aosmani123.github.io](https://aosmani123.github.io)**

I build AI systems and operating models for executive teams. I've spent five years supporting senior executives at Amazon and Microsoft, and I came to tech through Microsoft's ACE rotation program in product marketing and product research. I start by talking to the people doing the work, find the real constraint, and build around it.

This repo is my personal site and the projects on it.

## Projects

### Shipped at work
| Project | What it is |
|---|---|
| [Seven-agent system](https://aosmani123.github.io/projects/agent-system/) · [code](https://github.com/AOSMANI123/engagement-agents) | Multi-agent orchestration managing 200+ executive engagement items across intake, triage, briefing production and knowledge retrieval. The code link is a runnable public version with a review queue and no send step. |
| [AI-powered engagement automation](https://aosmani123.github.io/projects/engagement-automation/) | Rebuilt an executive's engagement workflow from three manual processes into one AI-assisted pipeline. ~80% less processing time. |
| [Engagement tracker template](https://aosmani123.github.io/projects/engagement-triage/) | A generalized version of that system any office can set up, with a free step-by-step [template](projects/engagement-triage/template). |

### Measuring AI quality
| Project | What it is |
|---|---|
| [Briefing evals: model readiness](https://aosmani123.github.io/projects/briefing-evals/) · [code](https://github.com/AOSMANI123/briefing-evals) | Tests whether an AI briefing drafter invents facts: 50 trap cases, repeated runs, a noise-calibrated pass gate, multi-provider runs, and an answer-key agreement check. In v1, a gap-flagging prompt cut real fabrications from 3 of 12 cases to 1. |
| [Coverage gap detector](https://aosmani123.github.io/projects/coverage-gap/) · [code](https://github.com/AOSMANI123/coverage-gap) | Scores a news brief on what it missed, not just what it included. Coverage score, entity breakdown, missed-consensus report. |
| [Executive writing critic](https://aosmani123.github.io/projects/writing-critic/) · [code](https://github.com/AOSMANI123/writing-critic) | Seven deterministic checks against an executive writing bar. CLI + web scorer. Python stdlib, no dependencies. |

### Product judgment
| Project | What it is |
|---|---|
| [AI product teardowns](https://aosmani123.github.io/projects/ai-teardowns/) | ChatGPT, Copilot, Notion AI, Midjourney, Grammarly: metrics tree, funnel, a feature to kill, a feature to build, what data would change my mind. |
| [Sign-up lists for WhatsApp Communities](https://aosmani123.github.io/projects/whatsapp-signups/) | A teardown of how Communities handles events, three options, a spec and a metrics plan. |

Anything that hasn't been tested with users or run against a real model is labeled that way.

## How I work

1. Talk to the users first.
2. Find the real constraint.
3. Ship something that works.
4. Check whether it moved.

One rule runs through every AI system I build: **the human is always the final sender.** AI drafts, sorts and retrieves. A person decides.

## Repo layout

```
index.html                     personal site
assets/project.css             shared styles for project pages
projects/
  # shipped at work
  agent-system/                seven-agent system architecture
  engagement-automation/       AI engagement automation case study
  engagement-triage/           engagement tracker template + setup guide
  # measuring AI quality
  briefing-evals/              model-readiness evals, 50 cases, gate, tests
  coverage-gap/                coverage gap detector for news briefs
  writing-critic/              executive writing scorer: CLI + web demo
  # product judgment
  ai-teardowns/                five AI product teardowns
  whatsapp-signups/            teardown + spec
```

## Contact

[LinkedIn](https://linkedin.com/in/azosmani) · atifzosmani@gmail.com · [Resume (PDF)](https://aosmani123.github.io/Atif_Osmani_Resume.pdf)
