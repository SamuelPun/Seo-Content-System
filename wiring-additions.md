# Wiring — work-log.md and writer-notes.md
*Drop-in additions for skills/writing.md, skills/audit.md, skills/revision.md, and run_workflow.py*

---

## 1. skills/writing.md — add this section

Add after the inputs table, before the process begins.

---

### Live capture during writing

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
- The intro is doing something against the SERP grain — and it's working
- A device landed well or failed — either is useful for system improvement
- A structural decision went against the outline (and why)
- A claim feels overstated relative to the source it rests on
- Anything the editor should read with extra attention

Do not write a note to confirm the draft is done, to summarise what was written, or to log anything the audit scripts will catch (banned phrases, rhythm, em dashes).

---

## 2. skills/audit.md — add this section

Add after the audit scripts are run, before audit-flags.json is written.

---

### Audit observations

After running all audit scripts and reviewing the outputs, write one entry to **work-log.md**:

```
---
step: audit | [timestamp] | status: [complete | partial | error]
---
[HIGH severity flags: count and brief description. MEDIUM severity flags: count. Rhythm: burstiness score, em dash count. Any flags that require human judgment rather than mechanical fix. Overall assessment in one sentence.]
```

**writer-notes.md** — write only for qualitative observations the scripts cannot catch:

- A passage that passes all script checks but still reads as AI to a human reader
- A structural issue that is technically compliant but feels wrong — thin section, misplaced emphasis, a device that didn't land
- A place where the content is technically sourced but the claim feels overstated
- Anything that needs editorial judgment, not just rule application

Do not duplicate what is already in audit-flags.json or rhythm-analysis.json. If the script caught it, the script recorded it. Writer notes are for what falls through.

---

## 3. skills/revision.md — add this section

Add at the very top of the process, before anything else happens.

---

### Before you begin revision: read these two files

**1. Read work-log.md in full.**
Scan every entry from `init` through `audit`. You are looking for:
- Steps that ran partial or with errors — what data might be degraded or missing
- Workarounds that were used — decisions that may need to be revisited
- Human gate decisions — what the editor approved or changed and why

**2. Read writer-notes.md in full.**
These are observations from the writing and audit sessions. Some will be directly actionable (a flagged section to tighten, a claim to verify). Some will be context (why a structural decision was made). Some will be signals for the human editor rather than for you.

Act on notes that fall within the revision skill's remit. Pass the rest to the human via revision-notes.md.

**After revision, write one entry to work-log.md:**

```
---
step: revision | [timestamp] | status: complete
---
[What changed and why. Sections tightened, claims adjusted, structural moves made. Any writer notes that were actioned. Any writer notes passed to human in revision-notes.md.]
```

Do not write to writer-notes.md during revision. That file's writing phase is closed.

---

## 4. run_workflow.py — add this to the article initialisation block

Find the section that creates the article workspace directory and initialises log.json. Add the following immediately after:

```python
import datetime

def init_article_files(slug, workspace_path):
    """Initialise work-log.md and writer-notes.md for a new article."""

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # work-log.md
    work_log_path = workspace_path / "work-log.md"
    if not work_log_path.exists():
        work_log_content = f"""# Work Log — {slug}
*Append-only. Written by every skill step and the orchestrator. Never edited — only added to.*
*Read by: human editor at any gate, revision skill before final pass.*

---
step: init | {timestamp} | status: complete
---
Workspace created for {slug}. work-log.md and writer-notes.md initialised.

"""
        work_log_path.write_text(work_log_content)

    # writer-notes.md
    writer_notes_path = workspace_path / "writer-notes.md"
    if not writer_notes_path.exists():
        writer_notes_content = f"""# Writer Notes — {slug}
*Append-only. Written on instinct — not on a schedule. Short, unpolished, honest.*
*Written by: writing skill, audit skill, human editor (at revision gate).*
*Read by: revision skill before final pass. Human editor after the run for system improvement.*

---

"""
        writer_notes_path.write_text(writer_notes_content)
```

**Call `init_article_files(slug, workspace_path)` in the same place you call the log.json initialisation.**

---

### Orchestrator work-log entries

For each step the orchestrator runs, append a start entry before invoking the Claude Code session, and a completion entry after:

```python
def log_step_start(slug, workspace_path, step_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"""---
step: {step_name} | {timestamp} | status: running
---
Orchestrator started {step_name} step.

"""
    work_log_path = workspace_path / "work-log.md"
    with open(work_log_path, "a") as f:
        f.write(entry)


def log_step_end(slug, workspace_path, step_name, status, note=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    note_line = f"\n{note}" if note else ""
    entry = f"""---
step: {step_name} | {timestamp} | status: {status}
---
Orchestrator completed {step_name} step.{note_line}

"""
    work_log_path = workspace_path / "work-log.md"
    with open(work_log_path, "a") as f:
        f.write(entry)
```

**Usage in run_workflow.py step runner:**

```python
log_step_start(slug, workspace_path, step_name)
try:
    run_claude_session(step_name, ...)  # your existing call
    log_step_end(slug, workspace_path, step_name, "complete")
except Exception as e:
    log_step_end(slug, workspace_path, step_name, "error", note=str(e))
    raise
```

For human gates, log the pause and the resume separately:

```python
# Before gate
log_step_end(slug, workspace_path, step_name, "complete",
    note="Human gate: review [file] before continuing.")

# After gate (when --from is used to resume)
log_step_start(slug, workspace_path, next_step_name)
```

---

## Folder structure update

Add to the workspace layout in the handoff doc:

```
workspace/article/[slug]/
    log.json                   ← machine-readable step completion tracker
    work-log.md                ← ✓ human-readable technical record (append-only)
    writer-notes.md            ← ✓ writer's real-time observations (append-only)
    ...
```
