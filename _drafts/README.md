# Drafts inbox

This folder is a staging area, not published content. Quarto ignores it
because it's underscore-prefixed (like `_site`, `_freeze`) and its files
aren't `.qmd`, so nothing here ever renders by accident.

## How a file gets here

Run the `draft-note` skill from any Claude Code session, anywhere, whenever
something is worth keeping — a fix, a tool, a workflow, a tutorial-shaped
explanation. It writes a single `.md` file here with a suggested `target`
section and rough frontmatter. It never touches anything else in this repo.

## How a file leaves here

Open a session rooted in this repo and ask it to integrate the drafts. It
should read `CLAUDE.md` for the exact conventions per section, adapt each
draft to match its target section's siblings, place the finished `.qmd`,
and delete the consumed draft from here. It should stop for your review
before committing or pushing — integration is deliberate, not automatic.
