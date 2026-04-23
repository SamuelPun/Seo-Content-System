"""
match_internal_links.py — Find internal link opportunities for a draft against the page index.

Scores each indexed page by how well its title, headings, and keyphrases overlap
with the keyphrases extracted from the draft. Title matches are weighted 3x,
heading matches 2x, keyphrase matches 1x.

Usage:
    python match_internal_links.py --draft editorial/draft.md --page-index brand/page-index.json --out-dir data/

Dependencies:
    pip install yake
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yake
except ImportError:
    print("ERROR: yake not installed. Run: pip install yake", file=sys.stderr)
    sys.exit(1)


_kw_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.7, top=30, features=None)

# Single-word terms so common across the site they add no signal — loaded from page-index.json
_site_stopwords: set[str] = set()


def load_site_stopwords(page_index_path: Path):
    """Build a stopword set from terms that appear in 80%+ of indexed pages."""
    global _site_stopwords
    try:
        data = json.loads(page_index_path.read_text(encoding="utf-8"))
        pages = data.get("pages", [])
        if len(pages) < 5:
            return
        threshold = len(pages) * 0.8
        term_counts: dict[str, int] = {}
        for page in pages:
            seen = set()
            for phrase in page.get("keyphrases", []):
                for word in phrase.lower().split():
                    if word not in seen:
                        term_counts[word] = term_counts.get(word, 0) + 1
                        seen.add(word)
        _site_stopwords = {w for w, count in term_counts.items() if count >= threshold}
    except Exception:
        pass


def extract_keyphrases(text: str) -> list[str]:
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'^#+\s.*$', '', text, flags=re.MULTILINE)
    text = text.strip()
    if len(text) < 50:
        return []
    try:
        results = _kw_extractor.extract_keywords(text)
        phrases = [phrase.lower() for phrase, _score in results]
        # Drop phrases where every word is a site-wide stopword
        return [p for p in phrases if not all(w in _site_stopwords for w in p.split())]
    except Exception:
        return []


def phrase_hits(phrase: str, targets: list[str]) -> bool:
    """True if a multi-word phrase appears in (or shares words with) any target string."""
    words = phrase.split()
    if len(words) < 2:
        return False
    meaningful_words = set(words) - _site_stopwords
    if not meaningful_words:
        return False
    for target in targets:
        target_lower = target.lower()
        if phrase in target_lower:
            return True
        if meaningful_words & set(target_lower.split()):
            return True
    return False


def score_page(draft_phrases: list[str], page: dict) -> tuple[int, list[str]]:
    title    = [page.get("title", "").lower()]
    headings = [h.lower() for h in page.get("headings", [])]
    kws      = [k.lower() for k in page.get("keyphrases", [])]

    score = 0
    matched = []

    for phrase in draft_phrases:
        if phrase_hits(phrase, title):
            score += 3
            matched.append(phrase)
        elif phrase_hits(phrase, headings):
            score += 2
            matched.append(phrase)
        elif phrase_hits(phrase, kws):
            score += 1
            matched.append(phrase)

    return score, matched


def run(draft_path: Path, page_index_path: Path, out_dir: Path, top_n: int = 10) -> bool:
    if not draft_path.exists():
        print(f"ERROR: Draft not found: {draft_path}", file=sys.stderr)
        return False
    if not page_index_path.exists():
        print(f"ERROR: Page index not found: {page_index_path}", file=sys.stderr)
        return False

    out_dir.mkdir(parents=True, exist_ok=True)

    load_site_stopwords(page_index_path)

    draft_text = draft_path.read_text(encoding="utf-8")
    draft_phrases = extract_keyphrases(draft_text)

    index_data = json.loads(page_index_path.read_text(encoding="utf-8"))
    pages = index_data.get("pages", [])

    if not pages:
        print("WARN: page-index.json has no pages — run build_page_index.py first", file=sys.stderr)
        out_path = out_dir / "internal-link-candidates.json"
        out_path.write_text("[]", encoding="utf-8")
        return True

    scored = []
    for page in pages:
        s, matched = score_page(draft_phrases, page)
        if s > 0:
            scored.append({
                "url":             page["url"],
                "title":           page.get("title", ""),
                "relevance_score": s,
                "matched_phrases": list(dict.fromkeys(matched))[:5],
                "lastmod":         page.get("lastmod"),
            })

    scored.sort(key=lambda x: x["relevance_score"], reverse=True)
    top = scored[:top_n]

    out_path = out_dir / "internal-link-candidates.json"
    out_path.write_text(json.dumps(top, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK]   {out_path}")
    print(f"\n=== INTERNAL LINK CANDIDATES (top {top_n}) ===")
    for r in top:
        phrases = ", ".join(r["matched_phrases"])
        print(f"  [{r['relevance_score']:>3} pts]  {r['title'] or r['url']}")
        print(f"           {r['url']}")
        print(f"           matched: {phrases}")
    if not top:
        print("  No relevant pages found in the index.")
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft",      required=True)
    parser.add_argument("--page-index", required=True, help="Path to brand/page-index.json")
    parser.add_argument("--out-dir",    required=True)
    parser.add_argument("--top",        type=int, default=10)
    return parser.parse_args()


def main():
    args = parse_args()
    ok = run(Path(args.draft), Path(args.page_index), Path(args.out_dir), args.top)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
