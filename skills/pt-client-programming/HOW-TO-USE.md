# How to use pt-client-programming

A plain-language guide for the clinician. No terminal needed: everything happens in the Claude desktop app's **Code** tab (see the [main guide](../../README.md), steps 1 and 2).

## What you get

For every client, one folder on your Mac that holds the **approved** program, every past version, your visit notes, and the handouts. Every time you approve a change, four files are produced from one source:

| File | Who it's for | How it's used |
|------|--------------|---------------|
| `.docx` | You | Upload to Google Drive → right-click → **Open with Google Docs** to edit, or open in Word/Pages. Header with your scheduling link, page numbers, footer with your contact line. |
| `.pdf` | The client | Email it, text it, print it. Looks identical to the .docx. |
| `.html` | The client, on a phone | A single file that opens in any browser with big readable tables and colour-coded green/yellow/red rows. Good for texting. |
| `.md` | The record | The plain-text source of truth. You never need to open it, but it's what the next visit builds on. |

You also get, at every approval, a short **changes** file listing exactly what differs from the previous version, so you can write a "what's new this visit" note in seconds.

## One-time setup (10 minutes)

Follow [Step 2 of the main guide](../../docs/02-install-a-skill.md): you paste one prompt into the Code tab and Claude downloads this repo, installs the skill, and runs its setup. The setup installs the document tools (and, with `--with-pdf`, LibreOffice, a large download used only to make PDFs), creates `~/PT-Programs/`, and opens a file called `practice.conf` in TextEdit.

Fill in your name, credentials, practice name, phone, email, website and scheduling link. Save. That's what goes in every header and footer.

## Day to day

Open the desktop app, Code tab, any session on your `Projects` folder, and talk. Claude knows where the client files live.

### New client

> New client **C-0001**, first name **Sam**. Right shoulder. Findings suggest a sensitive rotator cuff. Goal: reaching and lifting at home. Exercises: supine flexion, side-lying ER, supported IR/ER at 45°, isometric abduction at wall. No weights yet. Mobility 4–6 days, strength 2–3, active recovery as needed. Precaution: no pushing through anterior pinch. First-visit pattern.

Claude creates the folder, writes the intake, and tells you anything it's missing (doses, for example). Give it the missing pieces, then:

> Build the handout.

It writes a draft and lists every spot it wasn't sure about as `[[CONFIRM: …]]`. It will not approve anything with those in it.

> Export the draft so I can read it.

You get a `.docx` and `.pdf` marked REVIEW. Read it. Then either ask for changes or:

> Approve draft_2026-10-07_a: first-visit program.

Now there is a version 1, and the client copies are in the client's `approved/` folder. Claude tells you the exact file names.

### Next visit: a change

> **C-0001**: in Phase 2 add Standing band row, 2 sets of 8–12, progress low to higher elbows; reduce resistance or angle. Change wall slide to 2 sets of 8–12. Nothing else.

Claude copies the approved program, makes exactly those two changes, runs a check that shows which sections were touched, and shows you a before/after table. Everything else stays identical, and it proves that with a diff. Then:

> Approve draft_2026-10-14_a: progressed Phase 1 and 2.

Version 2 exists; version 1 is kept. The retrieval report at the next visit will name version 2.

### Just thinking

> Sam's pulldowns were yellow twice. What would you consider next?

That's DISCUSS. Claude talks through options, labelled as suggestions, and writes nothing to the program. Say "note that in today's visit" if you want it recorded.

### Pasting into an existing Google Doc

> TABLE ONLY — DOCX: the Phase 2 table from Sam's approved program.

You get a small `.docx` with just that table, no header or footer, ready to copy into whatever document you already have.

### From your phone

If you set up [phone access](../../docs/03-phone.md), all of this works from the Claude app. Take a photo of a new exercise set-up, attach it, and say "add this photo to C-0001's images as band-row.jpg and reference it in the Exercise menu." Claude saves it on your Mac and patches the draft.

## Where everything lives

```
~/PT-Programs/
├── practice.conf                 your header/footer details
├── library/
│   ├── exercises.md              reusable exercise descriptions (grows as you approve new ones)
│   ├── language.md               reusable paragraphs: symptom guides, flare plan, coach notes…
│   └── images/                   exercise photos shared across clients
└── clients/
    └── C-0001/
        ├── CURRENT_STATE.md      which version is approved, status, open flags
        ├── profile.md            first name only
        ├── intake.md             findings, goals, precautions, exercise choices
        ├── CHANGELOG.md          one line per approved version
        ├── visits/               your notes by date
        ├── drafts/               proposals, never sent to clients
        ├── approved/             v001…, each with .docx .pdf .html and a changes file
        ├── adjuncts/             sport- or role-specific companion documents
        ├── images/               this client's photos
        └── exports/              table-only and other partial exports
```

Back up `~/PT-Programs` the way you back up any clinical record. It is never part of the public repo. To open it in Finder, say "open my PT-Programs folder in Finder."

## Things to know

- **Client codes, not names, in folder names.** The first name lives in `profile.md` and in the handout text. Nothing else about a person belongs in these files unless you put it there deliberately.
- **Claude never approves.** Only your explicit "approve draft_…" does. If it ever claims something is approved without that, something is wrong; check `CURRENT_STATE.md`.
- **The retrieval report is your safety check.** Every task starts with it. If it says "approved: NONE" or "FILE NOT FOUND", stop and sort that out before editing.
- **Exercises reused across clients come from the library**, never from another client's folder.
- **Privacy.** Everything Claude reads is sent to Anthropic to generate the response. Consumer plans carry no HIPAA agreement. Keep identifiers minimal; decide for yourself what belongs in these folders.

## If something breaks

Paste the error into Claude and say "fix this." Most problems are one of: setup not run yet, `practice.conf` not filled in, or a missing image file. The build report always says which.
