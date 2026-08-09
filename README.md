# sbilmis.org

The site is authored with Quarto. Quarto source files are the source of truth; generated HTML is written to `_site/` and is not committed.

## Preview

```bash
quarto preview
```

## Build

```bash
quarto render
```

Generated files are written to `_site/` and are ignored by Git.

## Add a tutorial

Copy the tutorial template into the appropriate subject folder:

```bash
cp templates/tutorial.qmd.template tutorials/topic/my-tutorial.qmd
```

Fill in the metadata and the sections that help the reader. Remove `draft: true` when the page is ready. The standard sequence is Overview, Why this matters, Mental model, Before you start, Procedure, Verify, Troubleshooting, Quick reference, and References. It is guidance rather than a requirement to pad short notes.

A minimal `.qmd` or `.md` page also works if it has:

```yaml
---
title: "Tutorial title"
description: "A short description."
categories: [topic]
---
```

The Tutorials page discovers it automatically.

## Add a note

Put longer writing and imported LinkedIn posts in `writing/posts/`. Put curated reference collections in `writing/reference/`. Both appear automatically under Notes.

## Re-import the MkDocs tutorials

The original files remain in `my_tutorials`. To repeat the mechanical conversion, run:

```bash
python3 scripts/import-mkdocs-tutorials.py /Users/sbilmis/developer/projects/my_tutorials/docs
```

The import script overwrites the five mapped converted pages. New edits should normally be made directly in the Quarto pages.

## Legacy archive

The previous static site is preserved in `archive/legacy-site/`. The old capitalized `Tutorials/` tree is archive-only; the Quarto tutorials are now canonical. The post-render script republishes the archived scientometrics dashboards at their original URLs. Converted blog pages use Quarto redirects from their old addresses.

## Static tools

Standalone tools that should remain live outside the Quarto page graph live at the repository root. The TRUBA assistant is maintained in `truba-assistant/` and copied to `_site/truba-assistant/` after render, while remaining hidden from the homepage and navbar.

## Publishing

`.github/workflows/publish.yml` renders and deploys the site with GitHub Pages. Before the first deployment, set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**. The custom domain remains defined by `CNAME`.
