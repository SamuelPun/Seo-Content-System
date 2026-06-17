"""
Generate a publish checklist from the assembled output files.

Runs mechanical validation checks on meta.json, schema.json,
internal-link-candidates.json, and final.html — then writes
publish-checklist.md to the publish directory.

Replaces the output.md Claude skill: all checks here are mechanical
and do not require judgment. The human reviews the checklist before
publishing and resolves any flagged issues.

Usage:
    python3 generate_checklist.py --workspace /path/to/article/workspace
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

# ---------------------------------------------------------------------------
# HTML parser
# ---------------------------------------------------------------------------

class _HTMLChecker(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1_texts:       list[str] = []
        self.title_text:     str       = ""
        self.meta_desc:      str       = ""
        self.jsonld_blocks:  list[str] = []
        self.empty_hrefs:    int       = 0

        self._in_h1           = False
        self._in_title        = False
        self._in_jsonld       = False
        self._jsonld_buf:     list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        d = dict(attrs)
        if tag == "h1":
            self._in_h1 = True
        elif tag == "title":
            self._in_title = True
        elif tag == "script" and d.get("type") == "application/ld+json":
            self._in_jsonld = True
            self._jsonld_buf = []
        elif tag == "a":
            href = d.get("href")
            if href == "" or href is None:
                self.empty_hrefs += 1
        elif tag == "meta" and d.get("name") == "description":
            self.meta_desc = d.get("content", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self._in_h1 = False
        elif tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.jsonld_blocks.append("".join(self._jsonld_buf))

    def handle_data(self, data: str) -> None:
        if self._in_h1:
            self.h1_texts.append(data.strip())
        elif self._in_title:
            self.title_text += data
        elif self._in_jsonld:
            self._jsonld_buf.append(data)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _check(ok: bool, label: str, detail: str = "") -> tuple[bool, str]:
    mark = "✓" if ok else "✗"
    line = f"- [{mark}] {label}"
    if detail:
        line += f" — {detail}"
    return ok, line


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def _generate(workspace: Path) -> None:
    data_dir    = workspace / "data"
    publish_dir = workspace / "publish"
    publish_dir.mkdir(parents=True, exist_ok=True)

    today        = date.today().isoformat()
    issues:  list[str] = []
    checks:  list[str] = []

    # keyword (for presence checks)
    keyword = ""
    kw_path = data_dir / "keyword.json"
    if kw_path.exists():
        keyword = json.loads(kw_path.read_text(encoding="utf-8")).get("keyword", "").lower()

    # competitor titles (for duplication check)
    competitor_titles: list[str] = []
    serp_path = data_dir / "serp-urls.json"
    if serp_path.exists():
        competitor_titles = [
            e.get("title", "").lower().strip()
            for e in json.loads(serp_path.read_text(encoding="utf-8"))
            if e.get("title")
        ]

    # ---- meta.json ----
    meta_title = ""
    meta_desc  = ""
    meta_path  = data_dir / "meta.json"
    if not meta_path.exists():
        issues.append("meta.json not found — run validate_meta.py first")
        checks.append("- [✗] meta.json — file missing")
    else:
        meta       = json.loads(meta_path.read_text(encoding="utf-8"))
        meta_title = meta.get("title", "")
        meta_desc  = meta.get("description", "")
        title_len  = len(meta_title)
        desc_len   = len(meta_desc)

        ok, line = _check(30 <= title_len <= 65, f"Meta title {title_len} chars", meta_title)
        checks.append(line)
        if not ok:
            issues.append(f"Meta title is {title_len} chars (target 30–65): {meta_title!r}")

        if keyword:
            ok, line = _check(keyword in meta_title.lower(), "Keyword in meta title")
            checks.append(line)
            if not ok:
                issues.append(f"Keyword {keyword!r} not found in meta title")

        ok, line = _check(meta_title.lower() not in competitor_titles, "Meta title not duplicated from SERP")
        checks.append(line)
        if not ok:
            issues.append("Meta title matches a competitor title — rewrite it")

        ok, line = _check(140 <= desc_len <= 160, f"Meta description {desc_len} chars")
        checks.append(line)
        if not ok:
            issues.append(f"Meta description is {desc_len} chars (target 140–160)")

        if keyword:
            ok, line = _check(keyword in meta_desc.lower(), "Keyword in meta description")
            checks.append(line)
            if not ok:
                issues.append(f"Keyword {keyword!r} not found in meta description")

    # ---- schema.json ----
    schema_type = ""
    schema_path = data_dir / "schema.json"
    if not schema_path.exists():
        issues.append("schema.json not found — run generate_schema.py first")
        checks.append("- [✗] schema.json — file missing")
    else:
        try:
            schema      = json.loads(schema_path.read_text(encoding="utf-8"))
            schema_type = schema.get("@type", "unknown")
            required    = ["headline", "datePublished", "author", "publisher", "description"]
            missing     = [f for f in required if not schema.get(f)]
            ok, line    = _check(
                not missing,
                f"Schema ({schema_type}) required fields",
                f"missing: {', '.join(missing)}" if missing else "all present",
            )
            checks.append(line)
            if not ok:
                issues.append(f"Schema ({schema_type}) missing fields: {', '.join(missing)}")
        except json.JSONDecodeError as exc:
            checks.append(f"- [✗] schema.json — invalid JSON: {exc}")
            issues.append("schema.json is not valid JSON")

    # ---- internal-link-candidates.json ----
    link_candidates: list[dict] = []
    links_path = data_dir / "internal-link-candidates.json"
    if not links_path.exists():
        checks.append("- [?] internal-link-candidates.json — missing (links step may not have run yet)")
    else:
        link_candidates = json.loads(links_path.read_text(encoding="utf-8"))
        checks.append(f"- [✓] Internal link candidates: {len(link_candidates)} suggested (add 4–5 manually)")

    # ---- final.html ----
    html_path = publish_dir / "final.html"
    if not html_path.exists():
        issues.append("final.html not found — run build_output.py first")
        checks.append("- [✗] final.html — file missing")
    else:
        html_text = html_path.read_text(encoding="utf-8")
        parser    = _HTMLChecker()
        parser.feed(html_text)

        h1_texts = [t for t in parser.h1_texts if t]

        ok, line = _check(len(h1_texts) == 1, f"Single H1: {h1_texts[0]!r}" if h1_texts else "H1 missing")
        checks.append(line)
        if not ok:
            issues.append(f"Expected 1 H1, found {len(h1_texts)}: {h1_texts}")

        title_tag = parser.title_text.strip()
        titles_match = (not meta_title) or (title_tag == meta_title)
        ok, line = _check(bool(title_tag) and titles_match, "<title> matches meta.json")
        checks.append(line)
        if not ok:
            issues.append(f"<title> ({title_tag!r}) does not match meta.json ({meta_title!r})")

        valid_jsonld = any(
            _is_valid_json(b) for b in parser.jsonld_blocks
        )
        ok, line = _check(valid_jsonld, "JSON-LD block present and valid")
        checks.append(line)
        if not ok:
            issues.append("JSON-LD schema block missing or invalid in final.html")

        ok, line = _check(parser.empty_hrefs == 0, f"No empty href values ({parser.empty_hrefs} found)")
        checks.append(line)
        if not ok:
            issues.append(f"{parser.empty_hrefs} empty href attribute(s) in final.html")

    # ---- Build checklist ----
    passed = sum(1 for c in checks if "[✓]" in c)
    total  = sum(1 for c in checks if "[✓]" in c or "[✗]" in c)

    out: list[str] = [
        f"# Publish Checklist — {keyword or 'article'}",
        f"*Generated: {today}*",
        "",
        f"**Checks passed: {passed}/{total}**",
        "",
        "## Validation",
        "",
        *checks,
    ]

    if issues:
        out += ["", "## Issues to resolve before publishing", ""]
        out += [f"- [ ] {i}" for i in issues]
    else:
        out += ["", "## Issues to resolve before publishing", "", "None — ready to publish."]

    out += [
        "",
        "## WordPress upload steps",
        "",
        "1. Create new post in WordPress",
        "2. Paste content from `final.html` into the HTML editor (not the visual editor)",
        f"3. Set SEO title in Yoast: {meta_title}",
        f"4. Set meta description in Yoast: {meta_desc}",
        "5. Add the schema JSON-LD block to the post header (via Yoast or custom field)",
        "6. Add internal links manually — see table below",
        "7. Set publish date, category, and featured image",
        "8. Preview — check H1, formatting, all links work",
        "9. Publish",
    ]

    if link_candidates:
        out += ["", "## Internal links to add manually", "", "| Page title | URL |", "|---|---|"]
        for c in link_candidates[:8]:
            url   = c.get("url", "")
            title = c.get("title", url)
            out.append(f"| {title} | {url} |")

    out_path = publish_dir / "publish-checklist.md"
    out_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    status_label = "READY" if not issues else f"{len(issues)} issue(s)"
    print(f"[generate_checklist] {status_label} — {out_path.name}")


def _is_valid_json(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except (json.JSONDecodeError, ValueError):
        return False


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate publish checklist from assembled output files.")
    ap.add_argument("--workspace", required=True, help="Path to article workspace directory")
    args = ap.parse_args()
    _generate(Path(args.workspace))


if __name__ == "__main__":
    main()
