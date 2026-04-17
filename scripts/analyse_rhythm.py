import argparse
import json
import re
import sys
from pathlib import Path


def split_sentences(text):
    text = re.sub(r'\s+', ' ', text)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if len(s.split()) >= 3]


def burstiness(lengths):
    if len(lengths) < 2:
        return 0.0
    mean = sum(lengths) / len(lengths)
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    std = variance ** 0.5
    if mean == 0:
        return 0.0
    return round(std / mean, 3)


def run(draft_path, out_dir):
    if not draft_path.exists():
        print(f"ERROR: Draft not found: {draft_path}", file=sys.stderr)
        return False

    out_dir.mkdir(parents=True, exist_ok=True)
    text = draft_path.read_text(encoding="utf-8")

    # Strip markdown headings and code blocks for cleaner analysis
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'^#+\s.*$', '', text, flags=re.MULTILINE)

    sentences = split_sentences(text)
    lengths = [len(s.split()) for s in sentences]
    em_dash_count = text.count('—')

    if not lengths:
        print("ERROR: No sentences found in draft.", file=sys.stderr)
        return False

    mean_len   = round(sum(lengths) / len(lengths), 1)
    min_len    = min(lengths)
    max_len    = max(lengths)
    burst      = burstiness(lengths)

    # Flag sequences of 3+ sentences with similar length (within 5 words of each other)
    uniform_runs = []
    run_start = 0
    for i in range(1, len(lengths)):
        if abs(lengths[i] - lengths[i-1]) <= 5:
            if i - run_start >= 2:
                uniform_runs.append({
                    "start_sentence": run_start + 1,
                    "end_sentence":   i + 1,
                    "lengths":        lengths[run_start:i+1],
                })
        else:
            run_start = i

    # Distribution buckets
    distribution = {
        "1_to_10":  sum(1 for l in lengths if l <= 10),
        "11_to_20": sum(1 for l in lengths if 11 <= l <= 20),
        "21_to_30": sum(1 for l in lengths if 21 <= l <= 30),
        "31_plus":  sum(1 for l in lengths if l > 30),
    }

    result = {
        "sentence_count":   len(sentences),
        "mean_length":      mean_len,
        "min_length":       min_len,
        "max_length":       max_len,
        "burstiness_score": burst,
        "em_dash_count":    em_dash_count,
        "distribution":     distribution,
        "uniform_runs":     uniform_runs[:10],  # cap at 10 for readability
        "flags": {
            "low_burstiness":    burst < 0.4,
            "em_dash_overuse":   em_dash_count > 2,
            "no_short_sentences": distribution["1_to_10"] == 0,
        }
    }

    out_path = out_dir / "rhythm-analysis.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"[OK]   {out_path}")
    print(f"\n=== RHYTHM ANALYSIS ===")
    print(f"  Sentences:      {result['sentence_count']}")
    print(f"  Mean length:    {result['mean_length']} words")
    print(f"  Range:          {result['min_length']}–{result['max_length']} words")
    print(f"  Burstiness:     {result['burstiness_score']}  {'⚠ LOW — uniform rhythm' if result['flags']['low_burstiness'] else '✓ OK'}")
    print(f"  Em dashes:      {result['em_dash_count']}  {'⚠ OVERUSE' if result['flags']['em_dash_overuse'] else '✓ OK'}")
    print(f"  Short sentences (≤10w): {distribution['1_to_10']}  {'⚠ NONE — add short sentences' if result['flags']['no_short_sentences'] else '✓ OK'}")
    if uniform_runs:
        print(f"  Uniform runs:   {len(uniform_runs)} sequence(s) of similar-length sentences")
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
