---
name: de-ai-writing
description: >
  Use this skill when the user wants to make AI-generated or AI-assisted content
  sound more human. Triggers include: "de-AI this", "make this sound less like AI",
  "humanise this content", "remove AI patterns", "this sounds too robotic", "audit
  for AI writing", or any request to review content for AI tells before publishing.
  Also triggers when building a standing De-AI guideline document for a content team.
  Produces two things: (1) a real-time audit and rewrite of submitted content, and
  (2) optionally a standing De-AI Style Guide (.md) for use in future writing prompts.
  This skill addresses four levels of AI detection: vocabulary, sentence structure,
  structural patterns, and absence of human signals. Word-level fixes alone are not
  enough — all four levels must be addressed.
---

# De-AI Writing Skill

## Why word lists alone are not enough

Research as of 2025 is clear on this: removing overused AI vocabulary reduces
detection time but does not make content undetectable. GPTZero and similar tools
detect AI writing through four distinct signals — vocabulary frequency, sentence
rhythm predictability, structural patterns, and the absence of human signals
(opinion, imprecision, specificity, personal experience). A piece can have zero
banned words and still read as AI if the structure and rhythm are mechanical.

This skill addresses all four levels. Do not treat it as a find-and-replace exercise.

---

## The Four Levels of AI Detection

### Level 1 — Vocabulary (the surface layer)

AI models overuse certain words and phrases because their training data skews toward
formal, SEO-optimised, and academic writing. These words are not wrong — they're just
statistically over-represented in AI output compared to human writing.

**High-frequency AI vocabulary — avoid or strictly limit:**

*Adjectives that signal AI formality:*
comprehensive, crucial, vital, pivotal, robust, innovative, dynamic, holistic,
multifaceted, nuanced, granular, cutting-edge, groundbreaking, seamless, impactful,
actionable, invaluable, paramount, commendable, exemplary, enlightening, captivating,
burgeoning, esteemed, fundamental, essential, notable, significant, considerable

*Verbs AI reaches for:*
delve, delve into, embark, leverage, foster, facilitate, elevate, empower, enable,
enhance, amplify, optimize, maximize, navigate, harness, underscore, exemplify,
demonstrate, illuminate, explore, unpack, craft, augment, bolster, spearhead, drive

*Nouns and noun phrases AI inflates:*
landscape, realm, space, ecosystem, paradigm, paradigm shift, framework, synergy,
linchpin, epicenter, game-changer, cornerstone, best practices, key takeaways,
pain point, deep dive, bandwidth, deliverables, stakeholders, offerings, trajectory,
kaleidoscope, tapestry, journey (used metaphorically)

*Transitions AI overuses:*
furthermore, moreover, additionally, consequently, accordingly, nevertheless,
notwithstanding, herein, heretofore, hence, thus, as such, in essence, in summary,
in conclusion, moving forward, going forward, it is worth noting that,
it is important to note that, it's important to consider, based on the information provided

*Opening phrases that mark AI:*
"In today's rapidly evolving...", "In the dynamic world of...", "In the realm of...",
"In today's fast-paced...", "At its core...", "When it comes to...",
"Whether you're a beginner or an expert...", "Let's dive into...",
"Without further ado...", "In light of this..."

*Closing phrases that mark AI:*
"In conclusion, it is clear that...", "To summarise, we have explored...",
"As we have seen throughout this article...", "The journey doesn't end here..."

**The rule of three trap:**
AI defaults to grouping things in threes: "efficient, scalable, and sustainable."
This is not wrong, but it's so consistent in AI output that it reads as mechanical.
Vary list lengths — two items, four items, one item with elaboration.

---

### Level 2 — Sentence rhythm (the cadence layer)

AI writing has what researchers call low "burstiness" — sentences tend toward similar
lengths and similar structures. Human writing has high burstiness: a short sentence
lands hard. Then a longer one unpacks the idea, adds a qualification, brings in an
example. Then another short one.

**What AI rhythm looks like:**
- Every sentence is 15–25 words
- Every paragraph is 3–4 sentences
- Paragraphs all follow: topic sentence → supporting point → supporting point → summary
- Transitions appear between every paragraph
- Nothing is one sentence. Nothing is one word.

**What to do instead:**
- Vary sentence length deliberately. Short sentences are not a sign of poor writing.
  They are emphasis. Use them.
- Let some paragraphs be two sentences. Let some be one.
- Cut transitional sentences that exist only to connect, not to say anything.
- Ask: does this sentence do something, or is it just holding space?
- Read the draft aloud. Where you pause unnaturally, the rhythm is AI.

**The em dash problem:**
Em dashes are one of the strongest AI detection signals. Use zero em dashes in
published content. Every em dash must be resolved before a draft can be finalised.

When rewriting an em dash, identify what it is doing in the sentence and restructure
accordingly — do not simply swap in a comma or colon:

- **Parenthetical aside** (`X — detail — continues`): Ask whether the aside earns its
  place. If yes, restructure as a relative clause (`X, which [detail], continues`) or
  pull it out as its own sentence. If no, cut it.
- **Dramatic pause or contrast** (`claim — punchline`): Split into two sentences. Let
  the second carry the weight on its own.
- **Inline definition** (`term — what it means`): Rephrase as a subordinate clause:
  `term, which means...`
- **Clarification after a quote** (`"quote" — explanation`): Start a new sentence.
  `"Quote." The explanation follows.`

The rewritten sentence must read naturally with no punctuation patch. If it still
feels awkward, rewrite the whole sentence from scratch.

---

### Level 3 — Structural patterns (the architecture layer)

This is the level most audits miss. Even with varied vocabulary and rhythm, AI
writing follows predictable structural templates that experienced readers recognise.

**AI structural tells:**

*The symmetrical article:*
Every section is the same length. Every H2 has three H3s beneath it. Every section
ends with a summary sentence. Human writing is asymmetric — some ideas need more
space, others need less.

*The definition-first opening:*
AI often opens articles by defining the topic. "Cryptocurrency is a digital form of
currency that..." Human experts don't open by defining things everyone already knows.
They open with the thing that surprised them, the problem they ran into, or the
question nobody is asking.

*The balanced conclusion:*
AI conclusions summarise, acknowledge complexity, and call for nuance — then end
with a forward-looking statement about the future. They are structurally identical
across articles. Human conclusions take a position, make a recommendation, or
admit what they still don't know.

*The fake balance:*
AI adds counter-arguments not because they're worth engaging with, but because it
was trained to appear balanced. If a counter-argument isn't strong enough to change
a reader's mind, don't include it. Its presence just makes the piece feel hedged.

*The listicle default:*
AI converts everything into bullet points. It's more comfortable in lists than in
prose. If the content has narrative logic — if one idea causes or leads to another —
write it as prose. Lists are for genuinely discrete, parallel items.

*The padding paragraph:*
AI fills space with sentences that restate what was just said in different words,
or that announce what's about to be said. Cut any sentence that could be removed
without the reader noticing anything is missing.

---

### Level 4 — Absence of human signals (the authenticity layer)

This is the deepest level and the hardest to fix by rule. AI writing is confident
but impersonal. It covers topics without inhabiting them. Human writing has:

**Specificity over generality:**
AI says: "Many businesses have seen significant improvements in efficiency."
Human says: "When we switched from weekly reports to a shared live dashboard,
our Monday morning meeting dropped from 90 minutes to 20."
Specifics are not always available — but when they are, use them. When they're
not, acknowledge the lack of data instead of covering it with vague claims.

**Opinion and position:**
AI hedges. It presents multiple perspectives and lets the reader decide. Expert human
writing takes a position. It says what it thinks and why. If you're not saying anything
that could be disagreed with, you're probably not saying anything worth reading.

**Appropriate imprecision:**
Human experts acknowledge uncertainty. They say "I'm not sure this holds across all
markets" or "we don't have enough data yet to be confident about X." AI presents
everything with the same level of confident precision regardless of how well-established
it actually is. Appropriate hedging — hedging that reflects genuine uncertainty, not
political caution — is a human signal.

**Personal or organisational experience:**
What has your brand actually done, seen, or learned? Even one sentence grounded in
real experience ("we tried X and it didn't work because Y") is worth more than three
paragraphs of general advice. AI cannot generate this. It must come from the human.

**Friction and contradiction:**
Real expertise includes the awareness that things are messier than they appear.
AI smooths complexity into clean frameworks. Human writing sometimes says: "this
contradicts what I said earlier, and I haven't fully resolved it." That tension is
credible. It signals a real mind engaging with a real problem.

---

## How to Run a De-AI Audit

### When given content to audit and rewrite:

**Step 1 — Read the full piece without editing.**
Before touching anything, read it through. Form an overall impression: does this
feel like a person wrote it, or like a capable summarising machine? Note the specific
moments where it shifts from one to the other.

**Step 2 — Run the four-level check.**

```
LEVEL 1 — VOCABULARY
□ Search for banned/flagged vocabulary (use the list above as a reference)
□ Note which ones appear and how often
□ Flag any sentence where the vocabulary choice feels chosen for formality
  rather than for accuracy

LEVEL 2 — RHYTHM
□ Highlight every sentence. Note the length distribution.
□ Flag any sequence of more than 3 sentences that are similar in length
□ Count em dashes — any em dash is a flag (zero tolerance)
□ Flag transitional sentences that exist only to connect, not to say something

LEVEL 3 — STRUCTURE
□ Are all sections roughly the same length?
□ Does the introduction open with a definition or a scene-setting statement?
□ Does the conclusion summarise and end with a forward-looking statement?
□ Are there bullet lists where prose would be more natural?
□ Are there counter-arguments that feel obligatory rather than genuine?
□ Are there padding sentences (restate, announce, summarise unnecessarily)?

LEVEL 4 — HUMAN SIGNALS
□ Does the piece take a clear position on anything?
□ Is there any specificity that only this brand/author could have provided?
□ Is there any acknowledgment of uncertainty where uncertainty is genuine?
□ Is there any friction, contradiction, or unresolved tension?
□ Could this article have been written by any competent writer on this topic,
  or does it require knowledge of this brand's actual experience?
```

**Step 3 — Rewrite, level by level.**

Do not rewrite everything at once. Work through the levels in order:
1. Vocabulary substitutions (fastest, lowest impact alone)
2. Rhythm interventions (break up uniform sentence lengths, cut transitions)
3. Structural surgery (reshape introduction and conclusion, collapse padding,
   convert lists to prose where appropriate)
4. Human signal injection (add specificity, position, and appropriate uncertainty —
   flag any place where real experience or data from the brand is needed and
   cannot be fabricated)

**Step 4 — Flag what only the human can fix.**

After your rewrite, produce a short list of places where the content still reads
as generic because you did not have access to the real information needed. Format:

```
HUMAN INPUT NEEDED

[Section / paragraph reference]
What's missing: [e.g. "a specific example of a campaign that worked or failed"]
Why it matters: [e.g. "this claim is currently unsupported and reads as AI filler"]
Suggested fix: [e.g. "Replace with a real case from your own experience, or
remove the claim entirely"]
```

---

## Standing De-AI Style Guide Format

When producing a De-AI Style Guide for a content team (rather than auditing a
specific piece), produce the following document. Tailor the banned vocabulary
section to the brand's specific risk areas based on their existing content.

```markdown
# [Brand] De-AI Writing Style Guide
Version: [date]

## Purpose
This guide exists to prevent AI writing patterns from appearing in our content —
whether the content was generated by AI, assisted by AI, or written by a human
who has absorbed AI writing habits. It is not an anti-AI policy. It is a
quality standard.

## The four things that make content sound like AI
1. Overused vocabulary that AI statistically favours
2. Uniform sentence rhythm with low variation in length
3. Predictable structural templates (definition → points → summary → future)
4. Absence of specificity, opinion, and genuine uncertainty

Fixing only #1 is not enough. All four must be addressed.

## Banned vocabulary (check every draft)
[Insert full tailored list — pull from master list above, add brand-specific
terms identified during brand voice research]

## Banned structural moves
- Opening an article by defining the topic
- Closing with a summary of what was just said, followed by a forward-looking
  statement about the industry
- Bullet-pointing content that has a logical flow (if A leads to B leads to C,
  write it as prose)
- Adding a counter-argument to appear balanced when the counter-argument is not
  genuinely strong
- Writing a transitional sentence between every section

## Required human signals (at least two per article)
- A specific example, data point, or case that only we could provide
- A clear position or recommendation — something that could be disagreed with
- At least one acknowledgment of genuine uncertainty or a limit to our knowledge

## Rhythm rules
- No more than 3 consecutive sentences of similar length
- At least one paragraph of 1–2 sentences per article
- Em dashes: maximum 2 per article
- Transitional words (furthermore, moreover, additionally): maximum 1 per article,
  or zero

## The self-check question
Before submitting any draft, ask: "Could this have been written by a competent
AI given a brief about our topic, or does it require knowledge that only we have?"
If the honest answer is the former, it needs more work.
```

---

## What This Skill Cannot Do

This skill can identify and fix AI writing patterns. It cannot inject the human
experience, opinion, and specificity that only the brand can provide. Every audit
will produce a "human input needed" section. Those gaps are not failures of the
skill — they are the work that no AI can do on behalf of the brand.

The goal is not to make AI content undetectable by tools. Detection tool accuracy
is unreliable (false positive rates are significant, and tools update constantly).
The goal is to produce content that reads as genuinely expert and human to a
knowledgeable reader — which is a higher standard than fooling a detector, and
the standard that actually matters for trust and SEO authority.

---

## Skill Maintenance Notes

The vocabulary list above should be reviewed every 6 months. AI models update their
writing patterns as they are fine-tuned on human feedback — words that are currently
strong AI signals may become less so, and new patterns emerge. Check GPTZero's
AI Vocabulary tool (gptzero.me/ai-vocabulary) for current frequency data when
refreshing the list.

Structural and authenticity patterns change more slowly. The four-level framework
is unlikely to need significant revision within a 12-month period.
