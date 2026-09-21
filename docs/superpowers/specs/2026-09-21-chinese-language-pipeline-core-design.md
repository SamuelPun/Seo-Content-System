# Design: Chinese-language pipeline core (zh-HK)

## Problem

The pipeline only knows how to produce English content — `content-standards.md`'s
numeric rules (word count, sentence length) are word-counted, which is meaningless
for Chinese (no whitespace between words); `scan_banned_phrases.py`'s HIGH-severity
gate is an English phrase list that will never fire on Chinese text, silently
disabling the AI-tell gate for a Chinese client; `analyse_rhythm.py` computes
sentence length via `len(s.split())`, which returns ~1 for an entire unspaced
Chinese sentence; and `generate_checklist.py`'s meta title/description char
thresholds (30–65 / 140–160) are sized for Latin-character pixel width, roughly 2x
too generous for CJK glyphs at the same render width.

This is sub-project 1 of a two-part effort (see prior chat decomposition):
onboarding a new Chinese client (`onboard/*.py` — site scraping, brand-voice
extraction) is a separate follow-up spec. This spec assumes a client's
`brand/` files already exist (hand-authored for the first Chinese client, to
unblock testing the pipeline core independently of onboarding automation).

Scope is a single language variant: **Traditional Chinese, Hong Kong (zh-HK)**.
Language is a per-client setting, not per-article — a client is one language,
always (confirmed with user; no client currently needs mixed English/Chinese
articles).

## Design

### Config contract

`profile.md` gains a `**Language:**` field next to the existing
`**Search market:**` (e.g. `**Language:** zh-HK`). Missing field defaults to
`en`, mirroring how `**Search market:**` already defaults to `us`.

`config.py` gets `load_client_language(client_dir) -> str`, same shape as the
existing `load_client_market()`.

`RunContext` (`steps.py`) gains `lang: str = "en"`, populated in
`cli/workflow.py` alongside the existing `market=load_client_market(client_dir)`
line.

This is the shared contract sub-project 2 (onboarding) must also write to.

### Header plumbing (`runner.py::run_claude_skill`)

Two new header lines, resolved from `lang`:

```
WRITE_LANGUAGE: Traditional Chinese (Hong Kong)     # "English" for lang == "en"
CONTENT_STANDARDS_PATH: <repo>/skills/zh-hk/content-standards.md   # or skills/content-standards.md for en
```

This doubles as a bugfix: `writing.md` and `polish.md` currently reference
`skills/content-standards.md` as a bare relative path, but the Claude subprocess's
cwd is the workspace, not the repo — that reference cannot resolve today. Both
skill files change from the literal path string to "the file at
`CONTENT_STANDARDS_PATH`", fixing resolution for English too and getting
language-switching for free. `run_claude_skill` gains a `lang` parameter, threaded
from `ctx.lang` at every `step_*` call site.

`lang` not `en` and `skills/zh-hk/content-standards.md` missing → hard fail before
launching the subprocess. No silent fallback to English standards.

### The one forked skill file

`skills/zh-hk/content-standards.md` — full replacement of the numeric section only,
same structure as the English file so `writing.md`/`polish.md`'s references stay
valid unedited. Everything non-numeric (headings, links, CTA rules, structure) is
copied verbatim — not language-specific. Figures below are sourced from
Traditional-Chinese SEO industry sources and WCAG CJK readability guidance (see
research log); the meta-description figure is an extrapolation, flagged below.

| Rule | English (existing) | zh-HK (new) |
|---|---|---|
| Article floor | 1,200 words | 1,000 characters |
| Article target | from `keyword.json` SERP-derived range | same mechanism — already measures competitor content directly, self-corrects per keyword regardless of language |
| Article ceiling | 3,500 words | 3,500 characters |
| Sentence soft target | 16–20 words | 15–25 characters |
| Sentence hard cap | 35 words | 45 characters (anchored to WCAG 1.4.8's 40-char CJK line-readability guideline, plus headroom) |
| Short-sentence rule | ≥15% under 10 words | ≥15% under 8 characters |
| Paragraph length | 2–4 sentences | unchanged — not language-specific |
| Intro length | 120–180 words, keyword in first 100 words | 150–250 characters, keyword in first 150 characters |

Everything else under `skills/` (advisor frame, angle/editor/reader-check
rubrics, process) stays the single shared copy — no new files there. If a real
Chinese draft surfaces an English-only example baked into another skill file
(e.g. `content-devices.md`), that's a small follow-up fork of just that file,
not a sign this design is wrong.

### `scan_banned_phrases.py`

Gains `--lang` (default `en`) and a second list, `BANNED_ZH_HK`, built from
deep research into *why* each English category exists and whether an
analogous, independently-evidenced problem exists in Chinese — not a
translation of the English list. Verdicts:

- **Punctuation tell** (English: em-dash only, HIGH) → **kept, expanded to 3**:
  colon (：), em-dash (——), and double quotation marks (""). Two independent
  sources converge on this set. The quote-mark entry is stronger than a
  statistical AI tell — formal Chinese/HK typography uses corner brackets
  「」/『』, not "", so "" is arguably wrong punctuation for the language,
  not just an AI-frequency signal. 「」 is the prescribed replacement.
- **LLM-cluster buzzwords** (English: leverage/delve/robust/..., MEDIUM) →
  **excluded**. Checked the obvious Chinese candidate — Mainland tech jargon
  (赋能/抓手/闭环/颗粒度) — and found it's pre-existing corporate jargon mocked
  since well before the LLM era, not a demonstrated AI-distinctive tell, and
  Mainland-internet-register specific, so it would read as foreign in HK
  content regardless of AI-origin. No genuine single-word buzzword-cluster
  equivalent was found for Chinese.
- **Formulaic discourse markers** (English: throat-clearing, temporal clichés,
  stock openers/closers, HIGH) → **kept, ~30 items**, well-evidenced across 3
  independent sources. Covers filler connectors (说白了/本质上/换句话说),
  summary clichés (综上所述/总而言之), enumeration transitions
  (首先...其次...最后/第一...第二...第三), AI marker phrases
  (值得注意的是/不难发现/显而易见), era platitudes (在当今...的时代/随着...的快速发展),
  empty generalizations, false emphasis, and pseudo-colloquialisms. Source list
  is Simplified-authored ([stop-slop-zh](https://github.com/pencil20388-eng/stop-slop-zh)) —
  convert to Traditional characters before shipping.
- **Purple-prose metaphors** (English: kaleidoscope/tapestry/linchpin, HIGH) →
  **deferred**. The concept is confirmed as a real Chinese AI-writing flaw
  (堆砌華麗辭藻) but no source itemizes concrete words the way English does.
  Skip at launch; build this sub-list empirically from real flagged drafts
  during the pilot run rather than guessing.
- **"Sounds human" colloquial replacements** (说真的/踩过坑/挺猛的, from the
  same source's recommended-phrases list) → **excluded**. Mainland Mandarin
  internet-colloquial register, no dialect validation, doesn't match HK
  written Chinese. If HK needs a "sound human" nudge, that's a per-client
  `brand-voice-card.md` decision, same as English doesn't hardcode casualness
  system-wide either.

Implementation note: the existing `\b`-regex match path (used for single-word,
no-space, alphanumeric English entries) assumes whitespace-tokenized words.
Python's `\b` between two CJK characters frequently won't fire where expected —
Chinese has no word-boundary concept, so `\b综上所述\b` can silently fail to
match when the phrase is directly adjacent to other CJK characters. `BANNED_ZH_HK`
entries route through the same direct substring-in-line check already used for
punctuation-only English entries (no regex, no `\b`), never the `\b` path.

Structural AI tells (numbered-list addiction, bullet-heavy listicles, rigid
总分总 structure, comparison-table overuse) are independently well-documented for
Chinese but have no English-list equivalent at all — English's scanner is purely
phrase-based, this needs multi-line pattern/frequency detection. **Out of scope
for this spec** — flagged as a distinct follow-on, not silently dropped.

### `analyse_rhythm.py`

CJK branch (keyed on `lang`): sentence splitting on 。！？ instead of `.!?`;
sentence "length" becomes character count (`len(s)`) instead of whitespace word
count (`len(s.split())`, which is broken for Chinese today, not just imprecise).
Burstiness calculation, uniform-run detection, and distribution buckets are pure
math over the `lengths` array — reused unchanged, with bucket boundaries scaled to
the zh-HK soft-target/hard-cap numbers above. Punctuation-tell counting
(colon/em-dash/quotes) stays owned by `scan_banned_phrases.py` only — not
duplicated here.

### `generate_checklist.py`

The hardcoded `30 ≤ title_len ≤ 65` / `140 ≤ desc_len ≤ 160` thresholds become
lang-keyed constants: zh-HK gets `15–33` chars (title, ~25–30 target, converged
from both a Traditional-Chinese-sourced figure and the general CJK pixel-width
ratio) and `60–85` chars (description, ~70–80 target). **The description figure
is my extrapolation from the pixel-width ratio, not a sourced number** — worth
revisiting once real Chinese SERP snippets are available to eyeball truncation.

### Out of scope / unchanged

- `config.normalise_slug()` — article identifiers stay ASCII slugs regardless of
  content language (already the existing CLI convention — articles are named by
  project codename, not derived from the headline). No change.
- `fetch_serp.py` — already takes a `--country` code with no language param;
  passing a Chinese keyword with `--country hk` already returns Chinese-language
  SERP results via Ahrefs. No change needed.
- Onboarding (`onboard/*.py`) — sub-project 2, separate spec.

## Testing

Unit tests for each new branch, following the repo's existing per-script
`tests/test_*.py` pattern: `BANNED_ZH_HK` matching (including the substring-not-`\b`
path), CJK sentence splitting/character counts in `analyse_rhythm.py`, lang-keyed
thresholds in `generate_checklist.py`, and `load_client_language()`.

No automated way to test skill-file *output quality* — that's validated by a
manual pilot: hand-write a minimal Chinese `brand/` folder for a test client, run
one real Chinese keyword through `angle → output`, and read the draft against the
new standards and banned-phrase gate. This pilot is also where the deferred
purple-prose category gets built empirically instead of guessed, and where any
English-only example baked into an untouched skill file would surface.

## Files

- New: `skills/zh-hk/content-standards.md`
- Changed: `config.py` (`load_client_language`), `cli/workflow.py` (`lang=` wiring),
  `steps.py` (`RunContext.lang`, `lang` threaded into every `run_claude_skill` call),
  `runner.py` (`run_claude_skill` header + `lang` param), `skills/writing.md` +
  `skills/polish.md` (content-standards reference → `CONTENT_STANDARDS_PATH`),
  `scripts/scan_banned_phrases.py` (`--lang`, `BANNED_ZH_HK`), `scripts/analyse_rhythm.py`
  (CJK branch), `scripts/generate_checklist.py` (lang-keyed thresholds)
- Test additions (all files already exist): `tests/test_scan_banned_phrases.py`,
  `tests/test_analyse_rhythm.py`, `tests/test_generate_checklist.py`, and
  `tests/test_config.py` for `load_client_language`
