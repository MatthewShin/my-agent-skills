#!/usr/bin/env python3
"""Generate a standalone HTML project structure and relationship report."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".cache",
    ".next",
    ".nuxt",
    ".parcel-cache",
    ".turbo",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "bower_components",
    "dist",
    "build",
    "coverage",
    "target",
    "out",
}

TEXT_EXTS = {
    ".cjs",
    ".css",
    ".html",
    ".htm",
    ".js",
    ".jsx",
    ".mjs",
    ".mts",
    ".py",
    ".tsx",
    ".ts",
    ".vue",
    ".svelte",
}

FOCUS_EXTS = {
    ".cjs",
    ".css",
    ".html",
    ".htm",
    ".js",
    ".jsx",
    ".mjs",
    ".mts",
    ".tsx",
    ".ts",
    ".vue",
    ".svelte",
}

JS_RE = re.compile(
    r"""(?:import\s+(?:[^'"]+\s+from\s+)?|export\s+[^'"]+\s+from\s+|require\(|import\()\s*['"]([^'"]+)['"]""",
    re.MULTILINE,
)
CSS_RE = re.compile(r"""@import\s+(?:url\()?['"]?([^'")]+)['"]?\)?""")
HTML_RE = re.compile(r"""(?:src|href)=["']([^"']+)["']""", re.IGNORECASE)
PY_IMPORT_RE = re.compile(r"""^\s*(?:from\s+([.\w]+)\s+import|import\s+([.\w]+))""", re.MULTILINE)


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str


def run_git(root: Path, args: list[str]) -> list[str] | None:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return [line for line in proc.stdout.splitlines() if line.strip()]


def discover_files(root: Path, include_hidden: bool, max_files: int) -> list[Path]:
    tracked = run_git(root, ["ls-files"])
    others = run_git(root, ["ls-files", "--others", "--exclude-standard"])
    rels: list[str]

    if tracked is not None:
        rels = tracked + (others or [])
    else:
        rels = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [
                d
                for d in dirnames
                if d not in SKIP_DIRS and (include_hidden or not d.startswith("."))
            ]
            base = Path(dirpath)
            for name in filenames:
                if not include_hidden and name.startswith("."):
                    continue
                rels.append(str((base / name).relative_to(root)))

    files: list[Path] = []
    seen: set[str] = set()
    for rel in rels:
        path = root / rel
        if rel in seen or not path.is_file():
            continue
        parts = Path(rel).parts
        if any(part in SKIP_DIRS for part in parts):
            continue
        if not include_hidden and any(part.startswith(".") for part in parts):
            continue
        seen.add(rel)
        files.append(Path(rel))
        if len(files) >= max_files:
            break
    return sorted(files)


def read_text(path: Path, limit: int = 500_000) -> str | None:
    try:
        if path.stat().st_size > limit:
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def possible_targets(importer: Path, spec: str, root: Path, files: set[str]) -> str | None:
    if spec.startswith(("http://", "https://", "mailto:", "#")):
        return None
    if not (spec.startswith(".") or spec.startswith("/")):
        return None

    base = (root / spec.lstrip("/")) if spec.startswith("/") else (root / importer.parent / spec)
    candidates = [base]
    for ext in [".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".css", ".html", ".json"]:
        candidates.append(base.with_suffix(ext) if base.suffix == "" else base)
    for ext in [".ts", ".tsx", ".js", ".jsx", ".py", ".css", ".html"]:
        candidates.append(base / f"index{ext}")

    for candidate in candidates:
        try:
            rel = str(candidate.resolve().relative_to(root.resolve()))
        except ValueError:
            continue
        if rel in files:
            return rel
    return None


def python_module_target(importer: Path, module: str, root: Path, files: set[str]) -> str | None:
    if not module.startswith("."):
        return None
    dots = len(module) - len(module.lstrip("."))
    tail = module[dots:].replace(".", "/")
    base = root / importer.parent
    for _ in range(max(dots - 1, 0)):
        base = base.parent
    if tail:
        base = base / tail
    for candidate in [base.with_suffix(".py"), base / "__init__.py"]:
        try:
            rel = str(candidate.resolve().relative_to(root.resolve()))
        except ValueError:
            continue
        if rel in files:
            return rel
    return None


def extract_edges(root: Path, rel_files: list[Path]) -> list[Edge]:
    file_set = {str(path) for path in rel_files}
    edges: set[Edge] = set()
    for rel in rel_files:
        if rel.suffix.lower() not in TEXT_EXTS:
            continue
        text = read_text(root / rel)
        if text is None:
            continue
        if rel.suffix.lower() in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".vue", ".svelte"}:
            for spec in JS_RE.findall(text):
                target = possible_targets(rel, spec, root, file_set)
                if target:
                    edges.add(Edge(str(rel), target, "import"))
        if rel.suffix.lower() == ".css":
            for spec in CSS_RE.findall(text):
                target = possible_targets(rel, spec, root, file_set)
                if target:
                    edges.add(Edge(str(rel), target, "css"))
        if rel.suffix.lower() in {".html", ".htm"}:
            for spec in HTML_RE.findall(text):
                target = possible_targets(rel, spec, root, file_set)
                if target:
                    edges.add(Edge(str(rel), target, "html"))
        if rel.suffix.lower() == ".py":
            for from_mod, import_mod in PY_IMPORT_RE.findall(text):
                module = from_mod or import_mod
                target = python_module_target(rel, module, root, file_set)
                if target:
                    edges.add(Edge(str(rel), target, "python"))
    return sorted(edges, key=lambda e: (e.source, e.target, e.kind))


def dir_name(path: str) -> str:
    parent = str(Path(path).parent)
    return "." if parent == "." else parent


def build_tree(paths: list[Path]) -> dict:
    root: dict = {}
    for path in paths:
        cursor = root
        for part in path.parts:
            cursor = cursor.setdefault(part, {})
    return root


def render_tree(node: dict, depth: int = 0) -> str:
    rows = []
    for name, child in sorted(node.items(), key=lambda item: (not bool(item[1]), item[0].lower())):
        safe = html.escape(name)
        if child:
            rows.append(f"<details open><summary>{safe}/</summary>{render_tree(child, depth + 1)}</details>")
        else:
            rows.append(f"<div class=\"file\">{safe}</div>")
    return "\n".join(rows)


def top_source_root(path: Path) -> str:
    return path.parts[0] if len(path.parts) > 1 else "."


def supported_source_files(rel_files: list[Path]) -> list[Path]:
    return [path for path in rel_files if path.suffix.lower() in FOCUS_EXTS]


def split_focus_dirs(value: str) -> list[str]:
    cleaned = [item.strip().strip("/") for item in re.split(r"[,:\n]", value) if item.strip().strip("/")]
    return list(dict.fromkeys(cleaned))


def dir_contains(path: Path | str, focus_dir: str) -> bool:
    if focus_dir == ".":
        return True
    parts = Path(path).parts
    focus_parts = Path(focus_dir).parts
    return bool(focus_parts) and parts[: len(focus_parts)] == focus_parts


def detect_focus_dirs(rel_files: list[Path], edges: list[Edge], requested: str) -> list[str]:
    explicit = split_focus_dirs(requested)
    if explicit and explicit != ["auto"]:
        return explicit

    source_files = supported_source_files(rel_files)
    if not source_files:
        return []

    top_counts = Counter(top_source_root(path) for path in source_files)
    edge_counts = Counter()
    for edge in edges:
        edge_counts[top_source_root(Path(edge.source))] += 1
        edge_counts[top_source_root(Path(edge.target))] += 1

    top_roots = [
        name
        for name, count in top_counts.items()
        if name != "." and (count >= 2 or edge_counts[name] > 0 or (Path(name) / "package.json") in rel_files)
    ]
    if len(top_roots) >= 2:
        return sorted(top_roots, key=lambda name: (-top_counts[name], name))

    conventional = []
    for candidate in ["src", "app", "lib", "server", "client"]:
        if any(dir_contains(path, candidate) for path in source_files):
            conventional.append(candidate)
    if conventional:
        return conventional

    if top_roots:
        return top_roots

    return ["."]


def render_graph(dir_edges: Counter[tuple[str, str]], dir_counts: Counter[str]) -> str:
    nodes = sorted({n for edge in dir_edges for n in edge} | set(dir_counts))
    if not nodes:
        return "<p class=\"muted\">No static relative relationships found.</p>"
    nodes = sorted(nodes, key=lambda name: (Path(name).parts if name != "." else (), name))[:48]
    node_set = set(nodes)

    levels: dict[int, list[str]] = {}
    for node in nodes:
        depth = 0 if node == "." else len(Path(node).parts)
        levels.setdefault(depth, []).append(node)
    for depth in levels:
        levels[depth].sort(key=lambda name: (-dir_counts[name], name))

    col_w, row_h = 250, 112
    margin_x, margin_y = 58, 40
    max_rows = max(len(items) for items in levels.values())
    width = max(860, margin_x * 2 + len(levels) * col_w)
    height = max(360, margin_y * 2 + max_rows * row_h)
    points: dict[str, tuple[float, float]] = {}
    for col, depth in enumerate(sorted(levels)):
        items = levels[depth]
        column_height = (len(items) - 1) * row_h
        start_y = (height - column_height) / 2
        for row, node in enumerate(items):
            points[node] = (margin_x + col * col_w, start_y + row * row_h)

    marker = (
        '<defs><marker id="dir-arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" '
        'orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" '
        'fill="#315990" /></marker></defs>'
    )
    lines: list[str] = []
    for (source, target), count in dir_edges.most_common(120):
        if source not in node_set or target not in node_set or source == target:
            continue
        x1, y1 = points[source]
        x2, y2 = points[target]
        start_x, start_y = x1 + 172, y1 + 32
        end_x, end_y = x2, y2 + 32
        mid_x = (start_x + end_x) / 2
        label_x, label_y = (start_x + end_x) / 2, (start_y + end_y) / 2 - 8
        lines.append(
            f'<path d="M {start_x:.1f} {start_y:.1f} C {mid_x:.1f} {start_y:.1f}, '
            f'{mid_x:.1f} {end_y:.1f}, {end_x:.1f} {end_y:.1f}" class="dir-edge" '
            f'marker-end="url(#dir-arrow)"><title>{html.escape(source)} -> '
            f'{html.escape(target)} ({count})</title></path>'
            f'<text x="{label_x:.1f}" y="{label_y:.1f}" class="dir-edge-label">{count}</text>'
        )
    labels: list[str] = []
    for node, (x, y) in points.items():
        node_class = "dir-node root-dir" if node == "." else "dir-node"
        labels.append(f'<g class="{node_class}">')
        labels.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="172" height="64" rx="7" />')
        labels.append(
            f'<text x="{x + 14:.1f}" y="{y + 25:.1f}" class="dir-node-title">'
            f'{html.escape(shorten(node, 24))}</text>'
        )
        labels.append(
            f'<text x="{x + 14:.1f}" y="{y + 47:.1f}" class="dir-node-meta">'
            f'{dir_counts[node]} files</text><title>{html.escape(node)}</title></g>'
        )
    return f'<svg class="dir-graph" viewBox="0 0 {width} {height}" role="img">{marker}{"".join(lines + labels)}</svg>'


def in_focus(path: Path | str, focus_dirs: list[str]) -> bool:
    return any(dir_contains(path, focus_dir) for focus_dir in focus_dirs)


def is_focus_file(path: Path, focus_dirs: list[str]) -> bool:
    return in_focus(path, focus_dirs) and path.suffix.lower() in FOCUS_EXTS


def file_label(path: str, focus_dirs: list[str]) -> str:
    for focus_dir in focus_dirs:
        if focus_dir != "." and dir_contains(path, focus_dir):
            return str(Path(path).relative_to(focus_dir))
    return path


def ext_class(path: str) -> str:
    ext = Path(path).suffix.lower().lstrip(".") or "none"
    return re.sub(r"[^a-z0-9_-]", "-", ext)


def render_file_graph(focus_files: list[Path], focus_edges: list[Edge], focus_dirs: list[str]) -> str:
    if not focus_files:
        return (
            f'<p class="muted">Focus directories <code>{html.escape(", ".join(focus_dirs) or "auto")}</code> were not found '
            "or has no supported source files.</p>"
        )

    nodes = [str(path) for path in focus_files]
    cols = min(4, max(1, int(len(nodes) ** 0.5 + 0.999)))
    rows = (len(nodes) + cols - 1) // cols
    cell_w, cell_h = 260, 116
    width = max(760, cols * cell_w + 80)
    height = max(280, rows * cell_h + 80)
    positions: dict[str, tuple[float, float]] = {}
    for index, node in enumerate(nodes):
        col = index % cols
        row = index // cols
        positions[node] = (50 + col * cell_w, 45 + row * cell_h)

    marker = (
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" '
        'orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" '
        'fill="#64748b" /></marker></defs>'
    )
    edge_lines = []
    edge_kind_class = {"import": "edge-import", "css": "edge-css", "html": "edge-html", "python": "edge-python"}
    for edge in focus_edges:
        if edge.source not in positions or edge.target not in positions or edge.source == edge.target:
            continue
        x1, y1 = positions[edge.source]
        x2, y2 = positions[edge.target]
        start_x, start_y = x1 + 210, y1 + 34
        end_x, end_y = x2, y2 + 34
        mid_x = (start_x + end_x) / 2
        cls = edge_kind_class.get(edge.kind, "edge-import")
        edge_lines.append(
            f'<path d="M {start_x:.1f} {start_y:.1f} C {mid_x:.1f} {start_y:.1f}, '
            f'{mid_x:.1f} {end_y:.1f}, {end_x:.1f} {end_y:.1f}" class="file-edge {cls}" '
            f'marker-end="url(#arrow)"><title>{html.escape(edge.source)} -> '
            f'{html.escape(edge.target)} ({html.escape(edge.kind)})</title></path>'
        )

    node_boxes = []
    incoming = Counter(edge.target for edge in focus_edges)
    outgoing = Counter(edge.source for edge in focus_edges)
    for node in nodes:
        x, y = positions[node]
        label = file_label(node, focus_dirs)
        ext = Path(node).suffix.lower() or "[none]"
        node_boxes.append(
            f'<g class="file-node ext-{ext_class(node)}">'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="210" height="68" rx="7" />'
            f'<text x="{x + 12:.1f}" y="{y + 24:.1f}" class="file-node-title">'
            f'{html.escape(shorten(label, 34))}</text>'
            f'<text x="{x + 12:.1f}" y="{y + 47:.1f}" class="file-node-meta">'
            f'{html.escape(ext)} · out {outgoing[node]} · in {incoming[node]}</text>'
            f'<title>{html.escape(node)}</title></g>'
        )

    return (
        f'<div class="graph-scroll"><svg class="file-graph" viewBox="0 0 {width} {height}" '
        f'role="img">{marker}{"".join(edge_lines + node_boxes)}</svg></div>'
    )


def shorten(value: str, limit: int) -> str:
    return value if len(value) <= limit else value[: limit - 1] + "..."


def generate_html(root: Path, rel_files: list[Path], edges: list[Edge], focus_dirs: list[str]) -> str:
    ext_counts = Counter(path.suffix.lower() or "[none]" for path in rel_files)
    dir_counts = Counter(dir_name(str(path)) for path in rel_files)
    dir_edges = Counter((dir_name(edge.source), dir_name(edge.target)) for edge in edges)
    total_bytes = sum((root / path).stat().st_size for path in rel_files if (root / path).exists())
    focus_files = [path for path in rel_files if is_focus_file(path, focus_dirs)]
    focus_edges = [edge for edge in edges if in_focus(edge.source, focus_dirs) and in_focus(edge.target, focus_dirs)]

    edge_rows = "\n".join(
        f"<tr><td>{html.escape(edge.kind)}</td><td>{html.escape(edge.source)}</td><td>{html.escape(edge.target)}</td></tr>"
        for edge in edges[:500]
    ) or '<tr><td colspan="3" class="muted">No relationships found.</td></tr>'
    file_rows = "\n".join(
        f"<tr><td>{html.escape(str(path))}</td><td>{html.escape(path.suffix or '[none]')}</td><td>{(root / path).stat().st_size:,}</td></tr>"
        for path in rel_files
    )
    ext_json = html.escape(json.dumps(ext_counts.most_common(12), ensure_ascii=False))
    top_dirs = "".join(
        f"<li><span>{html.escape(name)}</span><strong>{count}</strong></li>"
        for name, count in dir_counts.most_common(12)
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Project Structure Report - {html.escape(root.name)}</title>
  <style>
    :root {{ color-scheme: light; --ink:#172026; --muted:#5e6b73; --line:#d8dee4; --bg:#f6f8fa; --panel:#ffffff; --accent:#0f766e; --accent2:#7c3aed; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color:var(--ink); background:var(--bg); }}
    header {{ padding:28px 32px 18px; background:#ffffff; border-bottom:1px solid var(--line); }}
    h1 {{ margin:0 0 6px; font-size:28px; letter-spacing:0; }}
    h2 {{ margin:0 0 14px; font-size:18px; letter-spacing:0; }}
    main {{ max-width:1280px; margin:0 auto; padding:24px 24px 48px; display:grid; gap:20px; }}
    section {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:18px; }}
    .muted {{ color:var(--muted); }}
    .stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:12px; }}
    .stat {{ background:#eef6f5; border:1px solid #c9e4df; border-radius:8px; padding:14px; }}
    .stat strong {{ display:block; font-size:24px; }}
    .grid {{ display:grid; grid-template-columns:minmax(280px,0.8fr) minmax(360px,1.2fr); gap:20px; align-items:start; }}
    .tree {{ max-height:620px; overflow:auto; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:13px; }}
    details {{ margin-left:14px; }}
    summary {{ cursor:pointer; font-weight:650; color:#0f513f; }}
    .file {{ margin-left:30px; color:#334155; white-space:nowrap; }}
    svg {{ width:100%; min-height:360px; border:1px solid var(--line); border-radius:8px; background:#fbfcfd; }}
    .dir-graph {{ min-height:390px; }}
    .dir-edge {{ fill:none; stroke:#315990; stroke-width:1.5; stroke-dasharray:4 4; opacity:.72; }}
    .dir-edge-label {{ font-size:11px; font-weight:700; fill:#244a7f; paint-order:stroke; stroke:#fbfcfd; stroke-width:5px; }}
    .dir-node rect {{ fill:#4a98c9; stroke:#ffffff; stroke-width:1.4; }}
    .root-dir rect {{ fill:#ffffff; stroke:#244a7f; stroke-width:2.5; }}
    .dir-node-title {{ font-size:13px; font-weight:750; fill:#ffffff; }}
    .root-dir .dir-node-title {{ fill:#244a7f; }}
    .dir-node-meta {{ font-size:11px; font-weight:650; fill:#d9eef9; }}
    .root-dir .dir-node-meta {{ fill:#5e6b73; }}
    .graph-scroll {{ width:100%; overflow:auto; }}
    .file-graph {{ min-width:760px; min-height:320px; }}
    .file-edge {{ fill:none; stroke:#64748b; stroke-width:1.5; opacity:.78; }}
    .edge-css {{ stroke:#0f766e; stroke-dasharray:5 4; }}
    .edge-html {{ stroke:#7c3aed; }}
    .edge-python {{ stroke:#b45309; stroke-dasharray:2 4; }}
    .file-node rect {{ fill:#ffffff; stroke:#cbd5e1; stroke-width:1.2; }}
    .file-node-title {{ font-size:12px; font-weight:700; fill:#172026; }}
    .file-node-meta {{ font-size:11px; fill:#5e6b73; }}
    .ext-ts rect, .ext-tsx rect {{ stroke:#2563eb; fill:#eff6ff; }}
    .ext-js rect, .ext-jsx rect, .ext-mjs rect, .ext-cjs rect {{ stroke:#ca8a04; fill:#fefce8; }}
    .ext-css rect {{ stroke:#0f766e; fill:#ecfdf5; }}
    .ext-html rect, .ext-htm rect {{ stroke:#7c3aed; fill:#f5f3ff; }}
    .ext-vue rect, .ext-svelte rect {{ stroke:#db2777; fill:#fdf2f8; }}
    text {{ font-size:11px; fill:#1f2937; }}
    table {{ width:100%; border-collapse:collapse; }}
    th, td {{ border-bottom:1px solid var(--line); padding:8px 10px; text-align:left; vertical-align:top; }}
    th {{ background:#f2f5f7; font-size:12px; text-transform:uppercase; color:#46525c; }}
    td {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:12px; overflow-wrap:anywhere; }}
    ul {{ margin:0; padding:0; list-style:none; display:grid; gap:6px; }}
    li {{ display:flex; justify-content:space-between; gap:12px; border-bottom:1px solid var(--line); padding:5px 0; }}
    code {{ background:#eef2f6; padding:2px 5px; border-radius:4px; }}
    @media (max-width: 860px) {{ header {{ padding:22px 18px 14px; }} main {{ padding:16px; }} .grid {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(root.name)} Project Structure</h1>
    <div class="muted">Generated {html.escape(datetime.now().isoformat(timespec="seconds"))} from <code>{html.escape(str(root))}</code></div>
  </header>
  <main>
    <section class="stats">
      <div class="stat"><span>Files</span><strong>{len(rel_files):,}</strong></div>
      <div class="stat"><span>Directories</span><strong>{len(dir_counts):,}</strong></div>
      <div class="stat"><span>Relationships</span><strong>{len(edges):,}</strong></div>
      <div class="stat"><span>Total Size</span><strong>{total_bytes:,}</strong></div>
    </section>
    <section class="grid">
      <div>
        <h2>File Tree</h2>
        <div class="tree">{render_tree(build_tree(rel_files))}</div>
      </div>
      <div>
        <h2>Directory Relationships</h2>
        {render_graph(dir_edges, dir_counts)}
        <p class="muted">Static relative imports and file links only. Top extensions: <code>{ext_json}</code></p>
      </div>
    </section>
    <section>
      <h2>Source File Relationships</h2>
      {render_file_graph(focus_files, focus_edges, focus_dirs)}
      <p class="muted">Focus: <code>{html.escape(", ".join(focus_dirs) or "auto")}</code>. Showing {len(focus_files):,} source files and {len(focus_edges):,} static relationships. Dynamic imports, aliases, and runtime-generated asset paths may not be linked.</p>
    </section>
    <section>
      <h2>Top Directories</h2>
      <ul>{top_dirs}</ul>
    </section>
    <section>
      <h2>File Relationships</h2>
      <table><thead><tr><th>Kind</th><th>Source</th><th>Target</th></tr></thead><tbody>{edge_rows}</tbody></table>
    </section>
    <section>
      <h2>File Inventory</h2>
      <table><thead><tr><th>Path</th><th>Type</th><th>Bytes</th></tr></thead><tbody>{file_rows}</tbody></table>
    </section>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Project root to inspect")
    parser.add_argument("--output", "-o", default="structure.html", help="HTML output path")
    parser.add_argument("--max-files", type=int, default=2000, help="Maximum files to include")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files and directories")
    parser.add_argument("--focus-dir", default="auto", help="Directory or comma-separated directories for the detailed file graph; default auto-detects source roots")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"error: root is not a directory: {root}", file=sys.stderr)
        return 2
    if args.max_files < 1:
        print("error: --max-files must be positive", file=sys.stderr)
        return 2

    rel_files = discover_files(root, args.include_hidden, args.max_files)
    edges = extract_edges(root, rel_files)
    focus_dirs = detect_focus_dirs(rel_files, edges, args.focus_dir)
    output = Path(args.output).expanduser()
    if not output.is_absolute():
        output = root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generate_html(root, rel_files, edges, focus_dirs), encoding="utf-8")
    print(f"wrote {output} ({len(rel_files)} files, {len(edges)} relationships, focus: {', '.join(focus_dirs) or 'none'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
