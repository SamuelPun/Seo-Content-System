import pathlib
import re

# ── 1. skills/writing.md ─────────────────────────────────────────────────────

writing_addition = '''
---

## Live capture during writing

**work-log.md** — write one entry when the draft is complete:

```
---
step: writing | [timestamp] | status: [complete | partial | error]
---
[What happened. Word count of draft.md. Any sections that deviated from outline.md and why. Any data gaps that affected the writing. If partial or error, what was saved and what needs to be redone.]
```

**writer-notes.md** — write only when a genuine instinct fires during drafting. Ask before each potential entry: "Would a thoughtful editor want to know this before doing the final pass?" If no, don't write it.

Write a note when:
- A section feels thin despite being structurally sound
- The intro is doing something against the SERP grain — and it is working
- A device landed well or failed — either is useful for system improvement
- A structural decision went against the outline (and why)
- A claim feels overstated relative to the source it rests on
- Anything the editor should read with extra attention

Do not write a note to confirm the draft is done, to summarise what was written, or to log anything the audit scripts will catch (banned phrases, rhythm, em dashes).

---
'''

path = pathlib.Path("skills/writing.md")
content = path.read_text()
marker = "Do not begin writing until you have read all of the above."
assert marker in content, "FAIL: marker not found in writing.md"
path.write_text(content.replace(marker, marker + "\n" + writing_addition, 1))
print("OK: skills/writing.md")


# ── 2. skills/audit.md ───────────────────────────────────────────────────────

audit_addition = '''
---

## Audit observations

After running all audit scripts and reviewing the outputs, write one entry to **work-log.md**:

```
---
step: audit | [timestamp] | status: [complete | partial | error]
---
[HIGH severity flags: count and brief description. MEDIUM severity flags: count. Rhythm: burstiness score, em dash count. Any flags that require human judgment rather than mechanical fix. Overall assessment in one sentence.]
```

**writer-notes.md** — write only for qualitative observations the scripts cannot catch:

- A passage that passes all script checks but still reads as AI to a human reader
- A structural issue that is technically compliant but feels wrong — thin section, misplaced emphasis, a device that did not land
- A place where the content is technically sourced but the claim feels overstated
- Anything that needs editorial judgment, not just rule application

Do not duplicate what is already in audit-flags.json or rhythm-analysis.json. If the script caught it, the script recorded it. Writer notes are for what falls through.

---
'''

path = pathlib.Path("skills/audit.md")
content = path.read_text()
marker = "## End of session"
assert marker in content, "FAIL: '## End of session' marker not found in audit.md"
path.write_text(content.replace(marker, audit_addition + "\n## End of session", 1))
print("OK: skills/audit.md")


# ── 3. skills/revision.md ────────────────────────────────────────────────────

revision_addition = '''## Before you begin revision: read these two files

**1. Read work-log.md in full.**
Scan every entry from `init` through `audit`. You are looking for:
- Steps that ran partial or with errors — what data might be degraded or missing
- Workarounds that were used — decisions that may need to be revisited
- Human gate decisions — what the editor approved or changed and why

**2. Read writer-notes.md in full.**
These are observations from the writing and audit sessions. Some will be directly actionable (a flagged section to tighten, a claim to verify). Some will be context (why a structural decision was made). Some will be signals for the human editor rather than for you.

Act on notes that fall within the revision skill\'s remit. Pass the rest to the human via revision-notes.md.

**After revision, write one entry to work-log.md:**

```
---
step: revision | [timestamp] | status: complete
---
[What changed and why. Sections tightened, claims adjusted, structural moves made. Any writer notes that were actioned. Any writer notes passed to human in revision-notes.md.]
```

Do not write to writer-notes.md during revision. That file\'s writing phase is closed.

---

'''

path = pathlib.Path("skills/revision.md")
content = path.read_text()
marker = "## Your job"
assert marker in content, "FAIL: '## Your job' marker not found in revision.md"
path.write_text(content.replace(marker, revision_addition + "## Your job", 1))
print("OK: skills/revision.md")


# ── 4. run_workflow.py ────────────────────────────────────────────────────────

orchestrator_addition = '''
import datetime


def init_article_files(slug, workspace_path):
    """Initialise work-log.md and writer-notes.md for a new article."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    work_log_path = workspace_path / "work-log.md"
    if not work_log_path.exists():
        work_log_path.write_text(
            f"# Work Log — {slug}\\n"
            "*Append-only. Written by every skill step and the orchestrator. Never edited — only added to.*\\n"
            "*Read by: human editor at any gate, revision skill before final pass.*\\n\\n"
            f"---\\nstep: init | {timestamp} | status: complete\\n---\\n"
            f"Workspace created for {slug}. work-log.md and writer-notes.md initialised.\\n\\n"
        )

    writer_notes_path = workspace_path / "writer-notes.md"
    if not writer_notes_path.exists():
        writer_notes_path.write_text(
            f"# Writer Notes — {slug}\\n"
            "*Append-only. Written on instinct — not on a schedule. Short, unpolished, honest.*\\n"
            "*Written by: writing skill, audit skill, human editor (at revision gate).*\\n"
            "*Read by: revision skill before final pass. Human editor after the run for system improvement.*\\n\\n"
            "---\\n\\n"
        )


def log_step_start(slug, workspace_path, step_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"---\\nstep: {step_name} | {timestamp} | status: running\\n---\\n"
        f"Orchestrator started {step_name} step.\\n\\n"
    )
    with open(workspace_path / "work-log.md", "a") as f:
        f.write(entry)


def log_step_end(slug, workspace_path, step_name, status, note=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    note_line = f"\\n{note}" if note else ""
    entry = (
        f"---\\nstep: {step_name} | {timestamp} | status: {status}\\n---\\n"
        f"Orchestrator completed {step_name} step.{note_line}\\n\\n"
    )
    with open(workspace_path / "work-log.md", "a") as f:
        f.write(entry)

'''

path = pathlib.Path("run_workflow.py")
content = path.read_text()
last_import = list(re.finditer(r'^(?:import |from )', content, re.MULTILINE))
assert last_import, "FAIL: no import lines found in run_workflow.py"
insert_pos = content.index("\n", last_import[-1].start()) + 1
path.write_text(content[:insert_pos] + orchestrator_addition + content[insert_pos:])
print("OK: run_workflow.py")

print("\nAll done. Now run:")
print("  git add -A && git commit -m 'wire work-log and writer-notes into skills and orchestrator'")
