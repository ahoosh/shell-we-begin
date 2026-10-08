# Program structure

Every handout is a markdown file that `build_handout.py` turns into a Word document. The markdown headings become Word headings; pipe tables become bordered tables; the practice header and footer are added automatically from `practice.conf`.

## The three patterns

| Pattern | When | Sections |
|---------|------|----------|
| **First visit** | Week 1, 3–5 exercises, nothing established yet | Title · Goal · Symptom guide · Adjusting challenge · Weekly plan (provisional) · Phase 1 · Phase 2 (what comes next) · Daily-life adjustments · Exercise menu |
| **Progressed** | Client seen several times; phases, ladders, return-to-activity | First-visit sections + ladders + return-to-activity table + optional tools/links + optional second region |
| **Complex** | Long-term client, multiple domains, other people involved (coach, family) | Numbered sections (1. Daily planning … 12. Weekly check-in), weekly check-in log, coach/family guide, and **adjunct** documents linked from the top |

Ask the clinician which pattern, or infer from how many visits and how many domains are involved, and say which you picked.

## Section anatomy (in order)

### 0. Front matter

```markdown
---
title: "Left Shoulder: Build Toward Overhead Reaching and Lifting"
subtitle: "Build comfortable motion, shoulder control, and load tolerance, one step at a time."
---
```

Title = region + goal, in the client's words where possible. Subtitle = one sentence of what the program builds. The practice line (clinician, practice, scheduling link) comes from `practice.conf`; don't write it in the body.

For the complex pattern, add adjunct links right under the title:

```markdown
> **Running adjunct:** running stages, practice drills, coach modifications. *(see adjuncts/running.md)*
```

### 1. Your goal (Heading 1)

Two to four sentences. What we're building; what the findings suggest (working impression language); what guides progression ("your symptoms and function will guide the program rather than the scan or calendar alone").

### 2. Symptom guide (Heading 1: "Use your response to choose the dose" or "Your symptom guide")

Three-row table. Two accepted shapes:

```markdown
| Zone | What you notice | Your next move |
|------|-----------------|----------------|
| **GREEN** | … | Continue. After 2–3 green sessions, progress one small variable. |
| **YELLOW** | … | Reduce range, resistance, repetitions, sets, speed, or time. … |
| **RED** | … | Stop that movement. Contact {{clinician_first_name}} or another healthcare provider. |
```

or the two-column form: `| GREEN — Continue or gradually progress | description |`. For athletes with nerve-type symptoms use the three-column "GREEN — Go as planned | YELLOW — Adjust | RED — Stop and get help" block from `language-blocks.md`, which has criteria rows and "your plan" rows.

Optional one-line note after the table, e.g. about noise: "A painless click with steady control may remain green; painful catching, slipping, or loss of function is red."

### 3. Adjusting challenge and recovery (Heading 1)

Three to five short paragraphs from `language-blocks.md` → "Adjust the dose", adapted: what counts as load for this client (work, hiking, chores, sport), one-variable rule, no doubling after a missed day, what to return to if range drops.

### 4. Weekly plan (Heading 1: "Weekly frequency" / "Your weekly plan" / "Weekly schedule")

```markdown
| Category | Days per week | How to use it |
|----------|---------------|---------------|
| Mobility and control | 4–6 | … |
| Strength | 2–3 | … |
| Active recovery | 1–3 as needed | … |
```

Then a "Scheduling notes" paragraph: categories can share a day; lower end when yellow/fatigued/busy; upper end only with stable green; don't double up.

Mark provisional ranges as provisional on a first visit: "These are provisional starting ranges because we have not yet established your home-exercise tolerance."

### 5. Phases (Heading 1 per phase: "Phase 1 — Comfortable motion and basic control")

One or two lead-in sentences (entry criterion, how many exercises to pick per day), then the phase table:

```markdown
| Exercise | Starting dose | Progression or regression |
|----------|---------------|---------------------------|
| Wall slide | 1–2 sets of 8–12 | Add a light band around the hands. Regress to a pinky-side slide or less height. |
```

Exact header text is `Exercise | Starting dose | Progression or regression`. For a phase that progresses an earlier phase's exercises, the middle column may be `Next dose`.

Optional note lines after a table start with a bold label: `**Rotation:** Isotonic means moving against resistance. If movement is yellow, …`

Routines inside a phase (A / B) are Heading 2: `## Routine A — Lower-body loading and carrying`.

### 6. Ladders (Heading 1: "Overhead pulling ladder", "Heel raise ladder")

Lead-in: where to start, what must be green first, what the clinician checks before the loaded steps.

```markdown
| Step and exercise | Starting dose | Progression or regression |
|-------------------|---------------|---------------------------|
| 1 High-anchor pulldown | 1 set of 6–8 | … |
| 2 Overhead pulldown | 2 sets of 8–12 | … |
```

Then two bold-labelled paragraphs: `**Stop signals:**` and `**Progression:**` (advance after three green sessions; what stays for later review).

An alternative ladder shape used for a single-joint progression with a plan row:

```markdown
| Progression | Exercise and starting dose | Progression or regression |
|-------------|----------------------------|---------------------------|
| Plan and baseline | … | … |
| Weekly dose | … | … |
| 1 Two-leg floor heel raise | … | … |
```

### 7. Return to activity (Heading 1: "Return to sport", "Running return", "Return to lifting")

```markdown
| Stage | Activity A (e.g. gym) | Activity B (e.g. field sport) |
|-------|-----------------------|-------------------------------|
| 1 Technique | … | … |
```

or for a single activity:

```markdown
| Stage | Run plan | Ready to move up when… |
|-------|----------|------------------------|
| 1 | 30 sec jog / 90 sec walk × 6–8 | Two green sessions; symptoms same or better later and next morning. |
```

Follow with `**Activity response:**` paragraph.

### 8. Daily-life adjustments (Heading 1: "Helpful day-to-day adjustments" / "Adjust daily activities while symptoms settle")

Short paragraphs with a bold lead word: `**Sleep:** …`, `**Work and transfers:** …`, `**Recreation:** …`.

### 9. Tools and links (optional)

A short list of equipment with links the clinician supplies. Links are `[text](url)`. Never invent a URL.

### 10. Exercise menu (Heading 1: "Exercise menu")

Lead-in: "Use only the exercises and versions currently assigned. Sets, repetitions, and progression appear in the program tables above." Then:

```markdown
| Exercise | How to do it |
|----------|--------------|
| Supine shoulder flexion | Lie on your back with the working arm by your side … |
```

Every exercise named in any phase/ladder table **must** have a row here, with the same name. `patch_check.py` warns when a phase exercise is missing from the menu.

Images: a row's description can end with an image on the next line inside the cell is not supported; instead put images after the table as `![Supine shoulder flexion](images/supine-flexion.jpg){width=2.5in}` with the exercise name as the caption, in menu order. Or make a separate "Exercise photos" Heading 1 with one image per exercise.

### 11. Complex-pattern extras

- **Weekly check-in & updates** (Heading 1 near the top): dated paragraph addressed to the client, what changed since last time, upcoming appointments (dates only if the clinician includes them).
- **Daily checkpoints** table: `When | Ask | What it means`.
- **When a flare starts** table: `Time | Use this plan`.
- **Build the week** table: `Part of the week | Dose | Guardrails` and an example-week table (MON…SUN).
- **Team warm-up swaps**: `Team drill | Use this version`.
- **One-week check-in log**: the 7-row table from `language-blocks.md`.
- **Coach / family quick guide**: five bullets.

All of these exist as blocks in `language-blocks.md`. Adapt, don't retype.

### 12. Adjunct documents

Separate files in `adjuncts/`, built from `templates/adjunct.md`. They open with the "ADJUNCT REFERENCE" box: use with the master program; the master chooses today's colour; if instructions conflict, follow the clinician's newest guidance. They hold sport-specific stages, warm-ups, terrain ladders, drill swaps, a practice check-in, and a "share with coaches" list. Export them separately; link them from the master document.

## Table rules

- Pipe tables only. Header row, separator row, body rows. No merged cells, no nested lists inside cells. Separate sentences inside a cell with a period and a space; for a forced break use `<br>`.
- Numbers: `8–12` (en dash), `2 sets of 8–12`, `3 × 20–40 sec` is acceptable in athlete programs, `45°` or `45 degrees` consistently within one document.
- Steps and stages are numbered inside the first cell: `1 High-anchor pulldown`.
- Keep columns to three. Four only for check-in logs and side-by-side activity staging.

## File naming

| Thing | Name |
|-------|------|
| Draft | `drafts/draft_2026-10-14_a.md` (letter increments within a day) |
| Approved | `approved/v003_2026-10-14.md` and `approved/v003_2026-10-14.docx` |
| Client copy of the handout | `approved/C-0427_Left-Shoulder_v003.docx` |
| Review export of a draft | `drafts/draft_2026-10-14_a_REVIEW.docx` |
| Table-only export | `exports/2026-10-14_phase2-table.md` / `.docx` |
| Adjunct | `adjuncts/running.md` (+ versioned approved copies in `approved/adjunct_running_v002_2026-10-14.md`) |
| Visit note | `visits/2026-10-14.md` |
