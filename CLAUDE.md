# sbilmis.github.io

A Quarto static site published to `sbilmis.org` — Selçuk's public notebook:
physics, computing, and research workflows. Built with `quarto render`,
deployed via GitHub Pages (see `.github/`).

## Section map

Four content sections, organized by what the content *is*, not by subject
matter. Physics, HPC, Linux, Emacs, QCD, AI, research workflow, etc. are
`categories:` tags, never folders.

> Learn it → Tutorials · Read it → Blog · Use it → Tools · Explore research
> data → Scientometrics

All four are flat on disk — no subject subfolders like `tutorials/emacs/`,
`blog/reference/`, or `tools/interactive/`. The one narrow exception is a
genuine multi-part course (see below). This is a deliberate simplification:
the priority is a structure that's still easy to remember five years from
now, not a precise taxonomy today.

### `tutorials/*.qmd` — teach how to do something

Reproducible steps, from a short procedure to a large multi-part course.

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
`tutorials/chezmoi-dotfiles.qmd` as the canonical example.

A genuine multi-part course (e.g. Linux/HPC from zero to hero) is the one
exception to "flat": give it its own `tutorials/<course>/` subfolder. This
isn't subject-based foldering — it's one course with real sequential
parts, not a category. To keep the course's chapters from flooding the
main Tutorials listing and the homepage's Latest feed:

- Number the chapter files (`00-basic-linux.qmd`, `01-modules.qmd`, ...)
  and give them ordinary Tutorials frontmatter.
- `tutorials/<course>/index.qmd` is the course landing page. Give it its
  *own* `listing:` scoped to just that folder
  (`contents: ["*.qmd", "!index.qmd"]`) so chapters are only browsable
  from inside the course.
- Do **not** add a recursive `**/*.qmd` pattern anywhere. The top-level
  `tutorials/index.qmd` and the homepage's Latest listing both use this
  two-tier pattern instead, so a course contributes exactly **one** entry
  (its `index.qmd`) to each, never its individual chapters:
  ```yaml
  contents:
    - "tutorials/*.qmd"        # ordinary single-page tutorials
    - "!tutorials/index.qmd"
    - "tutorials/*/index.qmd"  # one entry per course, not its chapters
  ```
  (the homepage version prefixes each pattern with the section name, as
  above; `tutorials/index.qmd`'s own version omits the `tutorials/`
  prefix since it's already rooted there). Publishing or editing a course
  chapter therefore never bumps that course's Latest entry unless
  `index.qmd` itself changes — expected, since the course's `date:` is
  what represents it there.

### `blog/*.qmd` — explain, discuss, reflect, or collect

The broad publishing/writing area: physics explainers (a W-boson mass
article), reactions to papers or scientific developments, HPC/computing
commentary, personal or research reflections, curated resource lists,
conference notes, longer technical articles. If its primary purpose is to
be *read* rather than followed as a procedure or used as a tool, it's
here — regardless of length or how reference-like it is. There is no
separate "Notes"/"Reference"/"Writing" section; this is that section.

Frontmatter is loose; pick what fits:
```yaml
title: "..."
description: "..."
date: YYYY-MM-DD
categories: [tag, tag]
author: "Selçuk Bilmiş"    # optional
toc: true                  # optional, useful for long curated lists
date-modified: YYYY-MM-DD  # optional, bump when a curated list changes
```
No tutorial-meta bar, no Overview callout, no mandated structure — plain
prose, or a curated list with light commentary. See
`blog/why-public-notes.qmd` (essay) and
`blog/starter-pack-for-particle-physicists.qmd` (curated list) as the two
ends of what belongs here. A few files carry
`*Migrated from an earlier Org-mode note.*` — keep that note only when
further migrating an old list, drop it for anything new.

### `tools/*.qmd` — built to be used, not read

Anything built that a reader *uses* rather than reads: small utilities,
interactive calculators, browser-only widgets, Emacs helpers, Python
packages, full software projects — with or without a separate GitHub
repository. Project size and "does it have its own repo" do not decide
this section; use is what decides it (`Spectroscopic Notation Explorer`,
a page-only calculator, lives here next to `Zotero Project Manager`, a
full Python/plugin project).

Frontmatter: `title`, `description`, `categories`, `date`, `toc: true`
for a project page; a calculator/widget instead adds whatever
`resources:`/`format: html: css:` its JS/CSS needs (see
`tools/spectroscopy.qmd`). Body for a standalone project: one or two
intro paragraphs, a `## What it is for` bullet list, then trailing link
buttons:
```markdown
[View the repository](https://github.com/...){.btn .btn-primary}
[Download the latest release](https://github.com/.../releases/latest){.btn .btn-outline-primary}
```
See `tools/copy-for-llm.qmd`.

### `publications/*.qmd` — not one of the four types

`publications/index.qmd` is a pure redirect stub to an INSPIRE-HEP search,
kept only so `/publications.html` (an old CV-site URL) still resolves.
Not in the navbar; linked from `about.qmd`. Leave it alone unless
explicitly asked to change how publications are presented.

### Scientometrics — not a Quarto section

`archive/legacy-site/scientometrics/` is static HTML/JS (echarts
dashboards), copied into the built site by `scripts/preserve-legacy.py`
and linked directly in the navbar as `/scientometrics/`. Research-data
dashboards (publication counts, TRUBA/HPC acknowledgment stats,
institute-level bibliometrics) go here, in that existing structure — not
as `.qmd` files, and outside this section map entirely.

## Deciding where new content goes

| New content is... | Goes to |
| --- | --- |
| Reproducible steps someone else follows, short or a full course | `tutorials/` |
| A personal essay, reflection, reaction, or curated resource list | `blog/` |
| Something built that a reader uses (widget, calculator, script, full project) | `tools/` |
| Research-infrastructure/publication-count dashboards | `archive/legacy-site/scientometrics/` |

Subject matter never decides the folder — only `categories:` tags do.
When genuinely unsure between two of the four, prefer whichever is
lighter-weight to be wrong about: moving a page later is one `git mv`
plus an `aliases:` entry for the old URL.

## Listing pages auto-populate

Each section's `index.qmd` uses Quarto's `listing:` directive
(`contents: "*.qmd"`). A new file just needs to exist in the right
folder — **do not** hand-edit an `index.qmd` to add a link to a new post.

Filter UI and category sidebars are deliberately turned off across
`tutorials/`, `blog/`, and `tools/` while each holds only a handful of
pages — a search box over one item is clutter, not a feature. Turn them
back on, or add generated category-listing pages, once a section actually
has enough content to justify it; that's a frontmatter change on the
section's `index.qmd`, not a URL change, since categories already live in
each page's frontmatter today.

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
3. Adapt the draft to match — correct frontmatter shape, reuse existing
   categories.
4. Place the finished `.qmd` directly in `tutorials/`, `blog/`, or
   `tools/` — flat, no subfolder.
5. Delete the consumed file from `_drafts/`.
6. Stop and show what changed. Do not `git commit` or `git push` unless
   explicitly asked to.
