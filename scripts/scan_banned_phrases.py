import argparse
import json
import re
import sys
from pathlib import Path

BANNED = [
    ("—", "HIGH"),
    ("delve", "HIGH"),
    ("delve into", "HIGH"),
    ("embark", "HIGH"),
    ("leverage", "HIGH"),
    ("foster", "HIGH"),
    ("facilitate", "HIGH"),
    ("elevate", "HIGH"),
    ("empower", "HIGH"),
    ("harness", "HIGH"),
    ("underscore", "HIGH"),
    ("spearhead", "HIGH"),
    ("paradigm shift", "HIGH"),
    ("game-changer", "HIGH"),
    ("game changer", "HIGH"),
    ("it is worth noting that", "HIGH"),
    ("it is important to note that", "HIGH"),
    ("it's important to consider", "HIGH"),
    ("based on the information provided", "HIGH"),
    ("in today's rapidly evolving", "HIGH"),
    ("in the dynamic world of", "HIGH"),
    ("in the realm of", "HIGH"),
    ("in today's fast-paced", "HIGH"),
    ("let's dive into", "HIGH"),
    ("without further ado", "HIGH"),
    ("in conclusion, it is clear that", "HIGH"),
    ("to summarise, we have explored", "HIGH"),
    ("as we have seen throughout this article", "HIGH"),
    ("the journey doesn't end here", "HIGH"),
    ("kaleidoscope", "HIGH"),
    ("tapestry", "HIGH"),
    ("synergy", "HIGH"),
    ("linchpin", "HIGH"),
    ("epicenter", "HIGH"),
    ("at its core", "HIGH"),
    ("moving forward", "HIGH"),
    ("going forward", "HIGH"),
    # Consultant-jargon / AI-cluster vocabulary — genuinely rare in ordinary human
    # writing about mundane topics, disproportionately common in AI-generated
    # marketing copy. Kept at MEDIUM.
    ("comprehensive", "MEDIUM"),
    ("robust", "MEDIUM"),
    ("innovative", "MEDIUM"),
    ("dynamic", "MEDIUM"),
    ("holistic", "MEDIUM"),
    ("multifaceted", "MEDIUM"),
    ("nuanced", "MEDIUM"),
    ("granular", "MEDIUM"),
    ("cutting-edge", "MEDIUM"),
    ("groundbreaking", "MEDIUM"),
    ("seamless", "MEDIUM"),
    ("impactful", "MEDIUM"),
    ("actionable", "MEDIUM"),
    ("invaluable", "MEDIUM"),
    ("paramount", "MEDIUM"),
    ("commendable", "MEDIUM"),
    ("exemplary", "MEDIUM"),
    ("enlightening", "MEDIUM"),
    ("captivating", "MEDIUM"),
    ("burgeoning", "MEDIUM"),
    ("esteemed", "MEDIUM"),
    ("amplify", "MEDIUM"),
    ("bolster", "MEDIUM"),
    ("augment", "MEDIUM"),
    ("illuminate", "MEDIUM"),
    ("unpack", "MEDIUM"),
    ("landscape", "MEDIUM"),
    ("realm", "MEDIUM"),
    ("ecosystem", "MEDIUM"),
    ("paradigm", "MEDIUM"),
    ("framework", "MEDIUM"),
    ("best practices", "MEDIUM"),
    ("key takeaways", "MEDIUM"),
    ("pain point", "MEDIUM"),
    ("deep dive", "MEDIUM"),
    ("bandwidth", "MEDIUM"),
    ("deliverables", "MEDIUM"),
    ("stakeholders", "MEDIUM"),
    ("trajectory", "MEDIUM"),
    ("notwithstanding", "MEDIUM"),
    ("herein", "MEDIUM"),
    ("heretofore", "MEDIUM"),
    ("in essence", "MEDIUM"),
    ("whether you're a beginner or an expert", "MEDIUM"),
    ("in light of this", "MEDIUM"),
    # Removed from this list on review: essential, significant, crucial, vital,
    # pivotal, fundamental, notable, considerable, enable, enhance, drive, craft,
    # explore, navigate, optimize, maximise/maximize, furthermore, moreover,
    # additionally, consequently, accordingly, nevertheless, hence, as such, in
    # summary, in conclusion, when it comes to, journey. These are ordinary
    # workhorse words and formal connectives used constantly in normal human
    # writing (news, textbooks, this tool's own SEO-content domain) — not a
    # distinctive AI tell, just noise that gets "corrected" out of otherwise fine
    # prose during polish.
]

BANNED_SORTED = sorted(BANNED, key=lambda x: len(x[0]), reverse=True)


def scan(text):
    lines = text.splitlines()
    hits = []
    for line_num, line in enumerate(lines, start=1):
        line_lower = line.lower()
        matched_in_line = set()
        for phrase, severity in BANNED_SORTED:
            if phrase in matched_in_line:
                continue
            if " " in phrase:
                if phrase in line_lower:
                    hits.append({"phrase": phrase, "severity": severity, "line_number": line_num, "line_text": line.strip()})
                    matched_in_line.add(phrase)
            elif not any(c.isalnum() for c in phrase):
                # Non-alphanumeric patterns (e.g. em dash) — direct match on original line
                if phrase in line:
                    hits.append({"phrase": phrase, "severity": severity, "line_number": line_num, "line_text": line.strip()})
                    matched_in_line.add(phrase)
            else:
                pattern = r"\b" + re.escape(phrase) + r"\b"
                if re.search(pattern, line_lower):
                    hits.append({"phrase": phrase, "severity": severity, "line_number": line_num, "line_text": line.strip()})
                    matched_in_line.add(phrase)
    return hits


def run(draft_path, out_dir):
    if not draft_path.exists():
        print(f"ERROR: Draft not found: {draft_path}", file=sys.stderr)
        return False
    out_dir.mkdir(parents=True, exist_ok=True)
    text = draft_path.read_text(encoding="utf-8")
    hits = scan(text)
    out_path = out_dir / "audit-flags.json"
    out_path.write_text(json.dumps(hits, indent=2, ensure_ascii=False), encoding="utf-8")
    high   = [h for h in hits if h["severity"] == "HIGH"]
    medium = [h for h in hits if h["severity"] == "MEDIUM"]
    print(f"[OK]   {out_path}")
    print("\n=== BANNED PHRASE SCAN ===")
    print(f"  HIGH severity:   {len(high)}")
    print(f"  MEDIUM severity: {len(medium)}")
    print(f"  Total hits:      {len(hits)}")
    if high:
        print("\n--- HIGH severity hits ---")
        for h in high:
            print(f"  Line {h['line_number']:>4}: [{h['phrase']}]  {h['line_text'][:80]}")
    if medium:
        print("\n--- MEDIUM severity hits ---")
        for h in medium:
            print(f"  Line {h['line_number']:>4}: [{h['phrase']}]  {h['line_text'][:80]}")
    return True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft",   required=True)
    parser.add_argument("--out-dir", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    ok = run(Path(args.draft), Path(args.out_dir))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
