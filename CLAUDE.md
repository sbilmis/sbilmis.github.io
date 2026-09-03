# sbilmis.github.io

A Quarto static site published to `sbilmis.org` — Selçuk's public notebook:
physics, computing, and research workflows. Built with `quarto render`,
deployed via GitHub Pages (see `.github/`).

## Section map

Four content sections, each with a different frontmatter shape. Pick the
one that matches what you're writing — don't invent a fifth.

### `Tutorials/<topic>/*.qmd` — step-by-step guides

Frontmatter:
```yaml
title: "..."
description: "..."
categories: ["...", "..."]
level: "Beginner" | "Beginner / Intermediate" | "Intermediate" | ...
estimated-time: "10 minutes"
date: YYYY-MM-DD
aliases:            # optional, only when migrating a URL
  - "/old/path/"
```

Body opens with two fixed blocks, then numbered sections:

```markdown
::: {.tutorial-meta}
**Level:** Beginner · **Working time:** 10 minutes
:::

::: {.callout-note title="Overview"}
* **Goal:** ...
* **Audience:** ...
* **Outcome:** ...
* **Time required:** ...
* **Skill level:** ...
* **Prerequisites:** ...
* **Example:** ...
:::

## 1. First Section Title
...
---
## 2. Next Section Title
...
```

Use tables for command/purpose maps, `.callout-tip` / `.callout-warning` /
`.callout-important` for asides, ` ```{mermaid} flowchart ``` ` for process
diagrams, and close with `## References` linking primary sources. See
`Tutorials/system/chezmoi-dotfiles.qmd` as the canonical example.

### `writing/posts/*.qmd` — the blog: essays, reflections, reactions

Frontmatter:
```yaml
title: "..."
description: "..."
date: YYYY-MM-DD
categories: [tag, tag]
author: "Selçuk Bilmiş"
draft: false
```
Then plain prose. No tutorial-meta bar, no Overview callout. See
`writing/posts/why-public-notes.qmd`. This is the home for personal essays,
historical/outreach reflections, and reactions to something read or studied
(a paper, someone else's blog post, a recent result) — the durable version
of what might otherwise only be a LinkedIn post.

### `writing/reference/*.qmd` — curated link collections

Frontmatter: `title`, `description`, `date`, `date-modified` (bump on
updates), `categories`, `toc: true`. Body is a curated list of external
links/resources with light commentary, not original prose. See
`writing/reference/starter-pack-for-particle-physicists.qmd`. Several
existing files are annotated `*Migrated from an earlier Org-mode note.*` —
keep that note if further migrating an old list, drop it for anything new.

### `writing/tools/*.qmd` — friction you hit, fix you found or built

For the "someone already solved this, I just needed to notice" pattern —
short write-ups of a workflow friction and the tool (someone else's, or a
quick one of your own not worth a full `software/` release) that removed
it. Frontmatter is the same shape as `writing/posts/*.qmd`. Mirror the
structure that already works on LinkedIn: the friction in plain terms, the
tool + link, the before/after workflow, why it matters. Not yet populated —
first candidate is a write-up of `clipssh`.

### `writing/interactive/*.qmd` — self-built widgets, calculators, sims

For an original interactive piece that lives only as a page — a
calculator, an explorable diagram, a small simulation — as opposed to
`software/`, which is for a standalone project with its own repo and
releases. Frontmatter: `title`, `description`, `categories`, `date`, plus
whatever `resources:`/`format: html: css:` the page's JS/CSS needs. No
tutorial-meta bar or `level`/`estimated-time` — those are Tutorials-only.
See `writing/interactive/spectroscopy.qmd` (moved here from
`Tutorials/physics/` — it was never a procedure, just a reference tool).
A future example: a double-pendulum animation.

### `software/*.qmd` — a project/tool page

Frontmatter: `title`, `description`, `categories`, `date`, `toc: true`.
Body: one or two intro paragraphs, a `## What it is for` bullet list, then
trailing link buttons:
```markdown
[View the repository](https://github.com/...){.btn .btn-primary}
[Download the latest release](https://github.com/.../releases/latest){.btn .btn-outline-primary}
```
See `software/copy-for-llm.qmd`.

### `publications/*.qmd`

Not yet documented here — check existing files in that folder before adding
one, same as above.

## Deciding where new content goes

Route new content by what it *is*, not by subject matter — physics and
computing both show up in several sections below:

| New content is... | Goes to |
| --- | --- |
| Reproducible steps someone else follows | `Tutorials/<topic>/` |
| A big multi-part course (e.g. Linux/HPC from zero to hero) | Still `Tutorials/<topic>/`, as several ordered pages under one topic folder — no new section needed. Number filenames (`00-`, `01-`, ...) or order them explicitly in that topic's `index.qmd` |
| A personal essay, reflection, or reaction to something read/studied | `writing/posts/` |
| A curated list of external links/resources | `writing/reference/` |
| A friction you hit + a fix you found or quickly built | `writing/tools/` |
| A self-built interactive widget/calculator/sim living only as a page | `writing/interactive/` |
| A full standalone project with its own repo and releases | `software/` |

When genuinely unsure, prefer the lighter-weight section — moving a page
later is one `git mv` plus an `aliases:` entry for the old URL, so getting
it exactly right up front matters less than not stalling on the decision.

## Listing pages auto-populate

Each section's `index.qmd` uses Quarto's `listing:` directive
(`contents: "*.qmd"` or a subfolder list). A new file just needs to exist
in the right folder — **do not** hand-edit an `index.qmd` to add a link to
a new post.

## Categories already in use

Reuse one of these where it fits rather than inventing a near-duplicate
(e.g. don't add "Sysadmin" next to the existing "System administration"):

Containers, Docker, System administration, Data management, Zenodo, HPC,
Emacs, Org mode, publishing, workflow, Physics, Spectroscopy, Interactive,
Dotfiles, chezmoi, macOS, Finder, LLM, Swift, notebook, Reference,
Particle physics, Research workflow, Events, Literature search, Zotero,
Python.

## The `_drafts/` workflow

`_drafts/*.md` are raw, unstyled notes dropped by the `draft-note` skill
from other sessions — see `_drafts/README.md`. When asked to integrate
them:

1. Read each draft and its suggested target section.
2. Look at 1–2 existing files in that section for exact current style
   (things drift; this file is a summary, the files are ground truth).
3. Adapt the draft to match — correct frontmatter shape, correct
   structural blocks, reuse existing categories.
4. Place the finished `.qmd` in the right folder.
5. Delete the consumed file from `_drafts/`.
6. Stop and show what changed. Do not `git commit` or `git push` unless
   explicitly asked to.

## Known issue, unfixed

`_quarto.yml`'s render list has `"tutorials/**/*.qmd"` (lowercase) but the
actual folder is `Tutorials/` (capital T). This works on case-insensitive
local filesystems (macOS) but may silently fail to render on a
case-sensitive Linux CI runner. Worth checking whether the deployed site
actually includes the Tutorials section — not fixed here since it's outside
whatever task brought you to this file.
