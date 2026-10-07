---
name: tomato-project-structure-html
description: Generate a standalone HTML report that visualizes a local project's folder structure, important files, and code relationships. Use when the user asks to show, map, document, inspect, or export a project directory's structure, file tree, dependencies, imports, links, or module relationships as an HTML result.
---

# Project Structure HTML

## Overview

Create a self-contained HTML report for a local project. Prefer the bundled script because it handles file discovery, relationship extraction, escaping, and report layout deterministically.

## Quick Start

Resolve `scripts/project_structure_html.py` relative to this `SKILL.md` as `SKILL_SCRIPT`, then run it from the project root unless the user names another directory:

```bash
python3 "$SKILL_SCRIPT" . --output structure.html
```

For a larger repository, keep the report readable by limiting the file count:

```bash
python3 "$SKILL_SCRIPT" . --output structure.html --max-files 1200
```

The report automatically detects source roots for the detailed file relationship graph. In split projects, roots such as `client` and `server` can both be shown. To focus one or more directories explicitly:

```bash
python3 "$SKILL_SCRIPT" . --output structure.html --focus-dir app
python3 "$SKILL_SCRIPT" . --output structure.html --focus-dir client,server
```

## Workflow

1. Resolve the target project directory. Do not scan outside the requested project unless the user explicitly asks.
2. Use the script to generate the HTML report.
3. Verify that the output file exists and is non-empty.
4. Report the output path and summarize any limits used, such as `--max-files`.

## Script Behavior

The script:

- Prefer `git ls-files` plus untracked non-ignored files when the target is a Git repository.
- Fall back to filesystem walking when Git is unavailable or the directory is not a repository.
- Skip common generated or vendor directories such as `.git`, `node_modules`, `dist`, `build`, `.next`, `coverage`, and virtual environments.
- Parse relative relationships in JavaScript, TypeScript, JSX, TSX, Python, CSS, and HTML files.
- Emit a standalone HTML file containing summary metrics, a collapsible file tree, an ordered directory relationship SVG, focused source file relationship SVG, file relationship table, and file inventory.
- Auto-detect source roots for the detailed graph by looking for supported source files, static relationships, common source directories, and split entry points such as `client` and `server`.
- Show every supported file inside the detected or requested focus directories as a node, including isolated files with no detected imports.

## Output Guidance

Use the project-local output path `structure.html` by default. If writing outside the project or using a different filename, get user confirmation first.

If the graph omits relationships, explain that only statically discoverable relative imports and links are included. Dynamic imports, framework aliases, generated routing, runtime dependency injection, runtime-generated asset paths, and external packages may need manual follow-up.
