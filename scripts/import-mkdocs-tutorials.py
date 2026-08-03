#!/usr/bin/env python3
"""Convert the existing MkDocs tutorial Markdown into Quarto pages.

The conversion keeps the original files untouched. It translates MkDocs
admonitions, adds consistent page metadata, removes duplicate H1 headings, and
copies the assets used by the interactive spectroscopy page.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PAGES = (
    {
        "source": "containers/updating-docker-apps.md",
        "target": "containers/updating-docker-apps.qmd",
        "title": "Updating a Docker Application Safely",
        "description": "Update a Docker Compose application without losing persistent data.",
        "categories": ["Containers", "Docker", "System administration"],
        "level": "Beginner",
        "estimated_time": "10 minutes",
        "date": "2025-12-29",
        "aliases": ["/my_tutorials/containers/updating-docker-apps/"],
        "overview": (
            "**Goal:** Update a Docker Compose application while preserving its data.\n\n"
            "**Audience:** Anyone maintaining a small Docker Compose deployment.\n\n"
            "**Time required:** About 10 minutes, excluding image download time.\n\n"
            "**Prerequisites:** Terminal access, a working Compose deployment, and persistent storage mounted from the host."
        ),
    },
    {
        "source": "data_management/downloading-large-datasets.md",
        "target": "data-management/downloading-large-datasets.qmd",
        "title": "Downloading Large Datasets from Zenodo",
        "description": "Generate file URLs, download large Zenodo records reliably, resume failures, and verify checksums.",
        "categories": ["Data management", "Zenodo", "HPC"],
        "level": "Beginner / Intermediate",
        "estimated_time": "10 minutes to prepare",
        "date": "2026-07-15",
        "aliases": ["/my_tutorials/data_management/downloading-large-datasets/"],
        "replacements": {
            "[Section 4.5](#45-the-403-forbidden-trap-two-causes)": "[Section 4.5](#sec-waf)",
            "## 4.5 The `403 Forbidden` Trap: Two Causes": "## 4.5 The `403 Forbidden` Trap: Two Causes {#sec-waf}",
        },
    },
    {
        "source": "emacs/e1.md",
        "target": "emacs/org-mode.qmd",
        "title": "Org mode notes",
        "description": "A placeholder for practical Org-mode notes.",
        "categories": ["Emacs", "Org mode"],
        "level": "Beginner",
        "estimated_time": "Coming soon",
        "date": "2025-12-24",
        "aliases": ["/my_tutorials/emacs/e1/"],
        "draft": True,
    },
    {
        "source": "physics/spectroscopy.md",
        "target": "physics/spectroscopy.qmd",
        "title": "Spectroscopic Notation Explorer",
        "description": "A compact reference and interactive calculator for atomic, meson, and baryon spectroscopic notation.",
        "categories": ["Physics", "Spectroscopy", "Interactive"],
        "level": "Intermediate",
        "estimated_time": "10 minutes",
        "date": "2026-04-12",
        "aliases": ["/my_tutorials/physics/spectroscopy/"],
        "clean_spectroscopy_html": True,
        "raw_html_from": '<div class="spectroscopy-section-heading">',
        "append": '\n\n<script src="spectroscopy.js"></script>\n',
        "extra_yaml": (
            "resources:\n"
            "  - spectroscopy.js\n"
            "format:\n"
            "  html:\n"
            "    css: spectroscopy.css\n"
        ),
    },
    {
        "source": "system/chezmoi-dotfiles.md",
        "target": "system/chezmoi-dotfiles.qmd",
        "title": "Managing Dotfiles Across Multiple Computers with chezmoi",
        "description": "Understand chezmoi's three layers and synchronize configuration safely across macOS and Linux.",
        "categories": ["System administration", "Dotfiles", "chezmoi"],
        "level": "Beginner / Intermediate",
        "estimated_time": "20 minutes",
        "date": "2026-07-28",
        "aliases": ["/my_tutorials/system/chezmoi-dotfiles/"],
    },
)


ADMONITION_TYPES = {
    "abstract": "note",
    "danger": "important",
    "example": "note",
    "failure": "caution",
    "info": "note",
    "note": "note",
    "question": "note",
    "success": "tip",
    "tip": "tip",
    "warning": "warning",
    "answer": "note",
}

CALLOUT_RE = re.compile(
    r'^(?P<indent>\s*)(?P<marker>!!!|\?\?\?)\s+(?P<kind>[\w-]+)(?:\s+"(?P<title>[^"]+)")?\s*$'
)


def quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def convert_callouts(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    index = 0

    while index < len(lines):
        match = CALLOUT_RE.match(lines[index])
        if match is None:
            output.append(lines[index])
            index += 1
            continue

        base_indent = len(match.group("indent"))
        kind = ADMONITION_TYPES.get(match.group("kind"), "note")
        title = match.group("title")
        attributes = f".callout-{kind}"
        if match.group("marker") == "???":
            attributes += ' collapse="true"'
        if title:
            attributes += f" title={quote(title)}"
        output.append(" " * base_indent + f"::: {{{attributes}}}")

        index += 1
        block: list[str] = []
        body_mode: str | None = None
        while index < len(lines):
            line = lines[index]
            if not line.strip():
                if body_mode == "flat":
                    break
                block.append("")
                index += 1
                continue
            indentation = len(line) - len(line.lstrip(" "))
            if body_mode is None:
                body_mode = "indented" if indentation > base_indent else "flat"
            if body_mode == "indented":
                if indentation <= base_indent:
                    break
                remove = min(base_indent + 4, indentation)
                block.append(line[remove:])
            else:
                if indentation < base_indent:
                    break
                block.append(line[base_indent:])
            index += 1

        while block and block[-1] == "":
            block.pop()
        output.extend(block)
        output.append(" " * base_indent + ":::")

    return "\n".join(output).rstrip() + "\n"


def convert_mermaid_fences(text: str) -> str:
    return re.sub(r"^```mermaid\s*$", "```{mermaid}", text, flags=re.MULTILINE)


def clean_spectroscopy_html(text: str) -> str:
    text = re.sub(r'<span class="arithmatex">(.*?)</span>', r"\1", text)
    text = text.replace(
        'class="md-button md-button--primary"',
        'class="spectroscopy-button spectroscopy-button--primary"',
    )
    return text.replace('class="md-button"', 'class="spectroscopy-button"')


def validate_conversion(text: str, source: Path) -> None:
    checks = {
        "unconverted MkDocs admonition": r"^(?:!!!|\?\?\?)\s+",
        "unconverted Mermaid fence": r"^```mermaid\s*$",
        "empty Quarto callout": r"^::: \{\.callout-[^}]+\}\n:::$",
    }
    for label, pattern in checks.items():
        if re.search(pattern, text, flags=re.MULTILINE):
            raise ValueError(f"{label} remains after converting {source}")


def strip_first_h1(text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        if line.startswith("# "):
            del lines[index]
        break
    return "\n".join(lines).lstrip()


def front_matter(page: dict[str, object]) -> str:
    categories = ", ".join(quote(str(item)) for item in page["categories"])
    values = [
        "---",
        f"title: {quote(str(page['title']))}",
        f"description: {quote(str(page['description']))}",
        f"categories: [{categories}]",
        f"level: {quote(str(page['level']))}",
        f"estimated-time: {quote(str(page['estimated_time']))}",
        f"date: {page['date']}",
    ]
    aliases = page.get("aliases")
    if aliases:
        values.append("aliases:")
        values.extend(f"  - {quote(str(alias))}" for alias in aliases)
    if page.get("draft"):
        values.append("draft: true")
    extra_yaml = page.get("extra_yaml")
    if extra_yaml:
        values.extend(str(extra_yaml).rstrip().splitlines())
    values.extend(("---", ""))
    return "\n".join(values)


def convert_page(source_root: Path, output_root: Path, page: dict[str, object]) -> None:
    source = source_root / str(page["source"])
    target = output_root / str(page["target"])
    text = strip_first_h1(source.read_text(encoding="utf-8"))
    text = convert_callouts(text)
    text = convert_mermaid_fences(text)

    for old, new in dict(page.get("replacements", {})).items():
        text = text.replace(str(old), str(new))
    if page.get("clean_spectroscopy_html"):
        text = clean_spectroscopy_html(text)

    overview = page.get("overview")
    if overview:
        text = f'::: {{.callout-note title="Overview"}}\n{overview}\n:::\n\n{text}'

    metadata = (
        "::: {.tutorial-meta}\n"
        f"**Level:** {page['level']} · **Working time:** {page['estimated_time']}\n"
        ":::\n\n"
    )
    text = metadata + text

    raw_html_from = page.get("raw_html_from")
    if raw_html_from:
        marker = str(raw_html_from)
        marker_index = text.find(marker)
        if marker_index == -1:
            raise ValueError(f"Raw HTML marker not found in {source}: {marker}")
        raw_fragment = text[marker_index:].rstrip()
        text = f"{text[:marker_index].rstrip()}\n\n```{{=html}}\n{raw_fragment}\n```\n"

    validate_conversion(text, source)
    append = str(page.get("append", ""))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(front_matter(page) + text.rstrip() + append, encoding="utf-8")


def copy_spectroscopy_assets(source_root: Path, output_root: Path) -> None:
    target = output_root / "physics"
    target.mkdir(parents=True, exist_ok=True)
    javascript = (source_root / "javascripts/spectroscopy-embed.js").read_text(encoding="utf-8")
    javascript = javascript.replace(
        'return `<span class="arithmatex">\\\\(${latex}\\\\)</span>`;',
        'return `\\\\(${latex}\\\\)`;',
    )
    (target / "spectroscopy.js").write_text(javascript, encoding="utf-8")

    css = (source_root / "stylesheets/spectroscopy.css").read_text(encoding="utf-8")
    replacements = {
        "var(--md-default-fg-color--lightest)": "var(--note-line)",
        "var(--md-default-fg-color--light)": "var(--note-muted)",
        "var(--md-default-fg-color)": "var(--note-text)",
        "var(--md-default-bg-color)": "var(--note-panel)",
        "var(--md-primary-fg-color)": "var(--note-accent)",
        "var(--md-accent-fg-color)": "var(--note-warm)",
        "var(--md-typeset-a-color)": "var(--note-warm)",
        "var(--md-code-bg-color)": "var(--note-accent-soft)",
        "color-mix(in srgb, white 94%, var(--note-panel))": "var(--note-panel)",
    }
    for old, new in replacements.items():
        css = css.replace(old, new)
    css += """

.spectroscopy-tool__actions button {
  border: 1px solid var(--note-accent);
  border-radius: 0.45rem;
  background: transparent;
  color: var(--note-accent);
  cursor: pointer;
  font: inherit;
  font-weight: 600;
  padding: 0.55rem 0.85rem;
}

.spectroscopy-tool__actions button:first-child {
  background: var(--note-accent);
  color: var(--note-paper);
}
"""
    (target / "spectroscopy.css").write_text(css, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Path to the MkDocs docs directory")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "tutorials",
        help="Quarto tutorials directory",
    )
    arguments = parser.parse_args()
    source_root = arguments.source.expanduser().resolve()
    output_root = arguments.output.expanduser().resolve()

    for page in PAGES:
        convert_page(source_root, output_root, page)
    copy_spectroscopy_assets(source_root, output_root)

    print(f"Converted {len(PAGES)} tutorial pages into {output_root}")


if __name__ == "__main__":
    main()
