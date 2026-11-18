# Notes for AI tools that edit this site

Read this and [README.md](README.md) before changing anything.

This is Atif Osmani's portfolio, published with GitHub Pages from `main`.
It is read by hiring managers for product and product marketing roles in
health tech and AI. Every change goes public as soon as it is pushed.

## Rules that always hold

- **No named executives.** Don't name the executives Atif has supported,
  and don't use titles like "Office of the CEO" or "CVP". Employer names
  (Microsoft, Amazon) are fine. Job titles stay as they appear on the site.
- **Nothing internal or confidential from any employer.** No internal tool
  names beyond what the site already shows, no internal project details,
  no unpublished numbers. If you are unsure, leave it out and ask.
- **Fictional names in sample data.** Example people and companies in
  demos and tests are made up, or are public figures used only as
  public examples.
- **Don't edit `Atif_Osmani_Resume.pdf`.** Atif replaces it himself.
- **Facts come from Atif.** Titles, dates and results come from the resume
  or from what he tells you. Don't add claims you can't point to.
- **Writing goes live only after Atif reads it.** Draft new posts and
  teardowns for his review first.

## How the site is built

- Plain HTML and CSS. No framework and no build step.
- The homepage keeps its styles inline. Project pages share
  `assets/project.css`. Both use the same color tokens on `:root`, with
  dark mode under `prefers-color-scheme` and `data-theme`. Reuse the
  tokens instead of adding new colors.
- Type: Young Serif for headings, Public Sans for body, DM Mono for labels.
- Each project lives in `projects/<name>/` with an `index.html`, a
  `README.md` and a `CHANGELOG.md`. Add a CHANGELOG entry when a project
  changes.
- Voice: first person, plain words, short sentences. Lead with the
  decision or result, then how.

## Check a change before you push

```
python3 .github/scripts/check_site.py
```

This checks every internal link, image and anchor. On GitHub, the
**Site check** workflow also opens every page at phone and desktop widths
and fails if an image breaks, a page scrolls sideways or the console shows
an error. Its screenshots are saved with each run.
