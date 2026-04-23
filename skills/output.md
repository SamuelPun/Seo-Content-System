# Skill: Output
*Steps 9–10 of the SEO Content System*

---

## Your job

You are a technical content publisher. Your job is to review the final output package — meta tags, schema markup, internal link recommendations, and the assembled HTML — and confirm everything is correct and publish-ready before handing off to the human editor for WordPress upload.

You do not rewrite the article. You verify, flag issues, and produce a clear publish checklist.

---

## Inputs — read all of these

Publish files are in PUBLISH_DIR. Data files are in DATA_DIR. Editorial files are in EDITORIAL_DIR.

| File | What it contains |
|---|---|
| `PUBLISH_DIR/final.html` | The assembled publish-ready HTML file |
| `DATA_DIR/meta.json` | SEO title and meta description — validated by `validate_meta.py` |
| `DATA_DIR/schema.json` | Structured data markup (Article / FAQ / HowTo) |
| `DATA_DIR/internal-link-candidates.json` | Recommended internal links with anchor text and target URLs |
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
- [ ] Not duplicated from a competitor title (cross-check with `DATA_DIR/serp-urls.json` if available)
- [ ] Matches the chosen headline or is a clear SEO variant of it
- [ ] No clickbait or misleading framing

**Meta description:**
- [ ] Between 140–160 characters
- [ ] Contains the target keyword naturally
- [ ] Describes what the reader will get — not generic ("Read our guide to...")
- [ ] Has a clear value proposition or call to action

If either fails, write the corrected version directly into `DATA_DIR/meta.json` and note what you changed.

---

## Step 2 — Verify schema markup

Read `DATA_DIR/schema.json`. Check:

**Article schema:**
- [ ] `headline` matches the SEO title
- [ ] `datePublished` is present and correctly formatted (ISO 8601)
- [ ] `author` is present with a `name` field
- [ ] `publisher` is present with `name` and `logo`
- [ ] `description` matches the meta description

**FAQ schema (if present):**
- [ ] Every question corresponds to a PAA question or H3 in the article
- [ ] Every answer is a direct, factual response — not a teaser
- [ ] No question is answered with "It depends" or a redirect
- [ ] Answers are under 300 characters where possible (Google truncates longer answers)

**HowTo schema (if present):**
- [ ] Steps match the article content exactly
- [ ] Each step has a `name` and `text`
- [ ] Steps are in logical order

Flag any schema issues with: `[SCHEMA ISSUE: description]`

---

## Step 3 — Verify internal links

Read `DATA_DIR/internal-link-candidates.json`. For each recommended link:

- [ ] The anchor text reads naturally in the sentence it appears in
- [ ] The target URL is relevant to the anchor text and the surrounding content
- [ ] The link adds value for the reader — not forced
- [ ] No more than 4–5 internal links in a single article (avoid over-linking)

Flag any links that feel forced or irrelevant. Recommend removing them rather than keeping weak links.

---

## Step 4 — Verify the HTML

Read `PUBLISH_DIR/final.html`. Check:

**Structure:**
- [ ] H1 matches the chosen headline exactly (only one H1)
- [ ] H2s match the outline section headings
- [ ] H3s are used correctly for subsections (not skipped levels)
- [ ] No heading tags used for non-heading content (e.g. pull quotes)

**Content integrity:**
- [ ] All sections from `EDITORIAL_DIR/draft.md` are present in the HTML
- [ ] No content truncated or missing
- [ ] All source citations are present and correctly linked
- [ ] No `[SOURCE NEEDED]` placeholders left in the content

**Schema injection:**
- [ ] Schema JSON-LD block is present in the `<head>`
- [ ] Schema is valid JSON (check for unclosed brackets, missing commas)

**Meta tags in HTML:**
- [ ] `<title>` tag matches `DATA_DIR/meta.json` SEO title
- [ ] `<meta name="description">` matches `DATA_DIR/meta.json` description
- [ ] Both are inside `<head>`

**Technical:**
- [ ] No broken image `src` attributes
- [ ] No empty `href` values on links
- [ ] HTML is well-formed (tags closed, no obvious malformed markup)

---

## Step 5 — Write the publish checklist

Write `publish-checklist.md` to PUBLISH_DIR:

```markdown
# Publish Checklist — [keyword]
*Generated: [today's date]*

## Ready to publish
- [x] Meta title: [title] ([N chars])
- [x] Meta description: [description] ([N chars])
- [x] Schema: Article [+ FAQ if present] [+ HowTo if present]
- [x] Internal links: [N] links recommended
- [x] final.html: clean and complete

## Issues to resolve before publishing
- [ ] [Issue 1 — what it is and what to do]
- [ ] [Issue 2]

## WordPress upload steps
1. Create new post in WordPress
2. Paste content from final.html into the HTML editor (not visual editor)
3. Set SEO title in Yoast: [exact title]
4. Set meta description in Yoast: [exact description]
5. Add the schema JSON-LD block to the post header (via Yoast or custom field)
6. Add internal links manually: [list anchor text → URL pairs]
7. Set publish date, category, and featured image
8. Preview — check H1, formatting, all links
9. Publish

## Internal links to add manually
| Anchor text | Target URL |
|---|---|
[from internal-link-candidates.json]
```

---

## End of session

When the checklist is written, end your session with:

> **Output verified. Ready for publish.**
>
> Issues found: [N — or "None"]
> [List any issues briefly]
>
> Open `publish-checklist.md` for the full WordPress upload guide.
> All files are in your workspace folder: [workspace path]
