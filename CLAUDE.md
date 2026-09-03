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

### `writing/posts/*.qmd` — shorter notes, no mandated structure

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
`writing/posts/why-public-notes.qmd`.

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
