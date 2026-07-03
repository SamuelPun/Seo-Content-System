---
name: output
description: "Steps 9-10 — generates meta.json, schema.json, final.html, and publish checklist."
---

# Skill: Output
*Steps 9–10 of the SEO Content System*

---

## Your job

You are a technical content publisher. Review the final output package — meta tags, schema markup, and the assembled HTML — and confirm everything is correct and publish-ready.

You do not rewrite the article. You verify, fix issues, and produce a publish checklist.

---

## Inputs — read all of these

| File | What it contains |
|---|---|
| `PUBLISH_DIR/final.html` | The assembled publish-ready HTML file |
| `DATA_DIR/meta.json` | SEO title and meta description — validated by `validate_meta.py` |
| `DATA_DIR/schema.json` | Structured data markup (Article / FAQ / HowTo) |
| `EDITORIAL_DIR/draft.md` | The final approved draft — use as reference for accuracy checks |
| `EDITORIAL_DIR/outline.md` | Original outline — confirm final HTML reflects approved structure |
| `DATA_DIR/keyword.json` | Target keyword — confirm it appears correctly in meta and content |
| `DATA_DIR/serp-urls.json` | Competitor titles — cross-check that meta title is not duplicated |

---

## Step 1 — Verify meta tags

Read `DATA_DIR/meta.json`. Check:

**SEO title:**
- [ ] Contains the target keyword
- [ ] Under 65 characters
- [ ] Not duplicated from a competitor title (cross-check `serp-urls.json`)
- [ ] Matches the chosen headline or is a clear SEO variant of it
- [ ] No clickbait or misleading framing

**Meta description:**
- [ ] Between 140–160 characters
- [ ] Contains the target keyword naturally
- [ ] Describes what the reader will get — not generic ("Read our guide to...")
- [ ] Has a clear value proposition

If either fails, write the corrected version directly into `DATA_DIR/meta.json` and note what you changed.

---

## Step 2 — Verify schema markup

Read `DATA_DIR/schema.json`. Check:

**Article schema (always present):**
- [ ] `headline` matches the SEO title
- [ ] `datePublished` is present and ISO 8601 formatted
- [ ] `author` is present with a `name` field
- [ ] `publisher` is present with `name` and `logo`
- [ ] `description` matches the meta description

**FAQ schema (if present):**
- [ ] Every question corresponds to a PAA question or H3 in the article
- [ ] Every answer is a direct, factual response — not a teaser or redirect
- [ ] Answers are under 300 characters where possible

**HowTo schema (if present):**
- [ ] Steps match the article content exactly
- [ ] Each step has a `name` and `text`
- [ ] Steps are in logical order

Flag any issues with: `[SCHEMA ISSUE: description]`

---

## Step 3 — Verify the HTML

Read `PUBLISH_DIR/final.html`. Check:

**Structure:**
- [ ] H1 matches the chosen headline exactly (only one H1)
- [ ] H2s match the outline section headings
- [ ] No heading tags used for non-heading content
- [ ] `<title>` and `<meta name="description">` inside `<head>` match `meta.json`
- [ ] Schema JSON-LD block is present in `<head>` and is valid JSON

**Content integrity:**
- [ ] All sections from `draft.md` are present — nothing truncated or missing
- [ ] All source citations are present and correctly linked
- [ ] No `[SOURCE NEEDED]` placeholders left in the content

**Technical:**
- [ ] No broken image `src` attributes
- [ ] No empty `href` values
- [ ] HTML is well-formed (tags closed, no malformed markup)

---

## Step 4 — Write the publish checklist

Write `publish-checklist.md` to PUBLISH_DIR:

```markdown
# Publish Checklist — [keyword]
*Generated: [today's date]*

## Ready to publish
- [x] Meta title: [title] ([N chars])
- [x] Meta description: [description] ([N chars])
- [x] Schema: Article [+ FAQ if present] [+ HowTo if present]
- [x] final.html: clean and complete

## Issues to resolve before publishing
- [ ] [Issue and what to do — or delete this section if none]

## WordPress upload steps
1. Create new post in WordPress
2. Paste content from final.html into the HTML editor (not visual editor)
3. Set SEO title in Yoast: [exact title]
4. Set meta description in Yoast: [exact description]
5. Add the schema JSON-LD block to the post header (via Yoast or custom field)
6. Set publish date, category, and featured image
7. Preview — check H1, formatting, all links
8. Publish
```

---

## End of session

> **Output verified. Ready for publish.**
>
> Issues found: [N — or "None"]
> [List any issues briefly]
>
> Open `publish-checklist.md` for the full WordPress upload guide.
> All files are in your workspace folder: [workspace path]
