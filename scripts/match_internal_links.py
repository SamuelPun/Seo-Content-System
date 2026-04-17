import argparse
import json
import re
import sys
from pathlib import Path


def extract_keywords(text):
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()
    stopwords = {
        'the','a','an','and','or','but','in','on','at','to','for','of','with',
        'by','from','is','are','was','were','be','been','being','have','has',
        'had','do','does','did','will','would','could','should','may','might',
        'this','that','these','those','it','its','as','if','so','not','no',
        'us','can','we','our','your','their','you','i','he','she','they',
        'all','more','also','about','up','out','than','into','when','how',
    }
    return {w for w in words if w not in stopwords and len(w) > 3}


def slug_to_keywords(url):
    slug = url.rstrip('/').split('/')[-1]
    slug = re.sub(r'[^a-z0-9]+', ' ', slug.lower())
    return set(slug.split())


def run(draft_path, candidates_path, out_dir, top_n=10):
    if not draft_path.exists():
        print(f"ERROR: Draft not found: {draft_path}", file=sys.stderr)
        return False
    if not candidates_path.exists():
        print(f"ERROR: Candidates not found: {candidates_path}", file=sys.stderr)
        return False

    out_dir.mkdir(parents=True, exist_ok=True)

    draft_text = draft_path.read_text(encoding="utf-8")
    candidates = json.loads(candidates_path.read_text(encoding="utf-8"))
    draft_keywords = extract_keywords(draft_text)

    scored = []
    for entry in candidates:
        url = entry.get("url", "")
        slug_kws = slug_to_keywords(url)
        overlap = draft_keywords & slug_kws
        if overlap:
            scored.append({
                "url":             url,
                "lastmod":         entry.get("lastmod"),
                "overlap_score":   len(overlap),
                "matched_keywords": sorted(overlap),
            })

    scored.sort(key=lambda x: x["overlap_score"], reverse=True)
    top = scored[:top_n]

    out_path = out_dir / "internal-link-candidates.json"
    out_path.write_text(json.dumps(top, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK]   {out_path}")
    print(f"\n=== INTERNAL LINK CANDIDATES (top {top_n}) ===")
    for r in top:
        kws = ", ".join(r["matched_keywords"][:5])
        print(f"  [{r['overlap_score']:>2} matches]  {r['url']}")
        print(f"            keywords: {kws}")
    if not top:
        print("  No keyword overlap found with sitemap candidates.")
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft",      required=True)
    parser.add_argument("--candidates", required=True, help="Path to sitemap-candidates.json")
    parser.add_argument("--out-dir",    required=True)
    parser.add_argument("--top",        type=int, default=10)
    return parser.parse_args()


def main():
    args = parse_args()
    ok = run(Path(args.draft), Path(args.candidates), Path(args.out_dir), args.top)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
