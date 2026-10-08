# Workflow modes, worked examples

Client code `C-0427`, first name "Sam" (fictional), left shoulder, progressed pattern. All paths relative to `~/PT-Programs/clients/C-0427/`.

## The retrieval report (every task)

`load_client.sh C-0427` prints something like:

```
RETRIEVAL REPORT — C-0427 (Sam)
approved:   v003_2026-10-01.md   (2026-10-01)  ← authoritative
            docx: present
drafts:     none
visits:     latest 2026-10-01.md (3 notes total)
adjuncts:   none
images:     4 files
markers:    0 in approved
status:     active — next visit 2026-10-15 (from CURRENT_STATE)
```

Paste it. Then one sentence: "I have the full approved v003 loaded, not a summary." If `approved:` says `none`, say so: "There is no approved program yet; anything I produce is a first draft."

## DISCUSS

> **Clinician:** Sam's overhead pulldowns were yellow for two sessions. Thoughts?

You answer in prose. Options with reasoning, labelled `Suggestion:`. You may quote the approved ladder rows to anchor the discussion. You do not write to `drafts/` or `approved/`. If asked to note it: append to `visits/2026-10-07.md` under `## Discussed, not adopted`.

## BUILD (first visit)

> **Clinician:** New client C-0511, first name Jo. Right shoulder, findings suggest rotator cuff irritation, possible biceps tendon involvement. Goal reaching and lifting at home. Four exercises: supine shoulder flexion, side-lying ER, supported IR/ER at 45°, isometric abduction at wall. No weights yet. Weekly: mobility 4–6, strength 2–3, active recovery 1–3. Precaution: don't push through anterior pinch; neck symptoms stop the exercise.

Steps:
1. `new_client.sh C-0511 "Jo"`; fill `intake.md` with the above.
2. Draft from `templates/program.md`, first-visit pattern. Pull the four descriptions from `library/exercises.md`, adapt to the right side ("Lie on your left side… your right elbow").
3. Doses the clinician didn't give get markers: `| Supine shoulder flexion | [[CONFIRM: starting dose]] | … |`.
4. Save `drafts/draft_2026-10-07_a.md`. Report:

```
Saved drafts/draft_2026-10-07_a.md (first-visit pattern)
Sections: Your goal · Your symptom guide · Adjusting challenge and recovery · Your weekly plan ·
          Phase 1 · Phase 2 · Adjust daily activities · Return to everyday reaching · Exercise menu
Markers (3):
  [[CONFIRM: starting dose for supine shoulder flexion]]
  [[CONFIRM: starting dose for side-lying external rotation]]
  [[CONFIRM: hold time for isometric abduction]]
Say "export the draft" to get a review .docx, or give me the doses and I'll patch them in.
```

## PATCH

> **Clinician:** C-0427: in Phase 2 add "Standing band row, 2 sets of 8–12, progress low to higher elbows as assigned; reduce resistance or angle" after Reverse fly. Change Wall slide in Phase 1 to 2 sets of 8–12. Nothing else.

Steps:
1. `cp approved/v003_2026-10-01.md drafts/draft_2026-10-07_a.md`
2. Edit exactly two things: insert one row; change one cell.
3. Add the Standing band row description to the Exercise menu **only if** the clinician asked or the menu rule requires it. The rule requires it (every phase exercise has a menu row), so add it from the library and say so explicitly: "Also added the menu row for Standing band row, required by the menu rule. Tell me if you'd rather leave it out."
4. `patch_check.py approved/v003_2026-10-01.md drafts/draft_2026-10-07_a.md` →

```
PATCH CHECK
baseline: approved/v003_2026-10-01.md   draft: drafts/draft_2026-10-07_a.md
lines: +2  -1  ~1   (added / removed / changed)
sections touched: Phase 1 Comfortable motion and basic control · Phase 2 Strength and weight bearing control · Exercise menu
markers in draft: 0
menu check: all phase exercises present in Exercise menu
```

5. Before / after:

| Where | Before | After |
|-------|--------|-------|
| Phase 1 › Wall slide › Starting dose | 1–2 sets of 8–12 | 2 sets of 8–12 |
| Phase 2 › after Reverse fly | (none) | **Standing band row** · 2 sets of 8–12 · Progress low to higher elbows as assigned. Reduce resistance or angle. |
| Exercise menu › after Reverse fly | (none) | **Standing band row** · (library description, adapted to left side) |

6. "Draft saved. Not exported, not approved."

If `patch_check.py` shows a section you didn't intend (say, a stray reflow of a paragraph), you fix the draft and re-run before showing anything.

### ROW PATCH ONLY

Same steps; the chat output is only the changed rows as a markdown table, plus the path of the saved draft.

### TABLE ONLY — DOCX

> **Clinician:** TABLE ONLY — DOCX: the Phase 2 table from Sam's approved program, I'll paste it into last week's Doc.

Write `exports/2026-10-07_phase2-table.md` containing just that table (with its header row), run `build_handout.py exports/2026-10-07_phase2-table.md --out exports/2026-10-07_phase2-table.docx --table-only`. No header/footer. Report the path.

## EXPORT

> **Clinician:** Export the draft for review.

`build_handout.py drafts/draft_2026-10-07_a.md --out drafts/draft_2026-10-07_a_REVIEW.docx` →

```
BUILD REPORT
source:   drafts/draft_2026-10-07_a.md
output:   drafts/draft_2026-10-07_a_REVIEW.docx  (84 KB)
title:    Left Shoulder: Build Toward Overhead Reaching and Lifting
headings: 11 (H1) · 3 (H2)
tables:   9   rows: 61
images:   4 embedded, 0 missing
header:   "Schedule your next session" link + page numbers
footer:   practice contact line
markers:  0
```

Paste it. Add: "To review in Google Docs: upload to Drive, right-click, Open with → Google Docs."

The script exits non-zero and lists missing images or unresolved markers; fix or report, don't hand over a broken file.

## APPROVE

> **Clinician:** Approve draft_2026-10-07_a: progressed wall slide, added band row.

Check markers = 0 (refuse otherwise). `approve.sh C-0427 drafts/draft_2026-10-07_a.md "Progressed wall slide to 2 sets; added Standing band row to Phase 2"` →

```
APPROVED — C-0427
new version:  approved/v004_2026-10-07.md
handout:      approved/v004_2026-10-07.docx   (build report above)
client copy:  approved/C-0427_Left-Shoulder_v004.docx
CURRENT_STATE.md updated (approved_version: v004, approved_date: 2026-10-07)
CHANGELOG.md appended
draft archived: drafts/archive/draft_2026-10-07_a.md
```

Next visit, the retrieval report shows v004. That's the whole continuity mechanism: a file, not a memory.

## Mixed request

> **Clinician:** Add the band row (2×8–12) to Phase 2, and do you think they're ready for step 3 of the pulling ladder?

Answer in two labelled parts:

**PATCH** (done as above, with the check and the before/after).
**DISCUSS** (prose, labelled suggestion, nothing written to the draft about ladder steps).

Never fold the suggestion into the draft.
