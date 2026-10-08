# pt-client-programming

A Claude Code skill for clinicians who write and maintain home exercise programs. Built around a real physical therapist's workflow: one approved program per client, careful edits between visits, a polished handout at the end.

## What it fixes

If you have tried to do this with a chat assistant you know the failure modes: it can't tell you what it actually remembers about a client, it rewrites things you didn't ask it to touch, and a "small change" costs twenty minutes of checking. This skill addresses each one with a file, a rule, or a script:

| Problem | What this skill does |
|---------|----------------------|
| "Did it load the real program or a summary?" | Every task starts with a **retrieval report** that names the exact approved file and version it read. |
| Edits that bleed into unrelated rows | **PATCH** copies the approved file, applies only your change, then runs a diff and shows you a before/after table. Anything outside the request is a bug it must fix before showing you. |
| Current state vs. ideas vs. history | `approved/` holds the truth, `drafts/` holds proposals, `visits/` holds notes. `CURRENT_STATE.md` points to the one approved file. Nothing moves to approved without your explicit **APPROVE**. |
| Guessing doses | Gaps become `[[CONFIRM: …]]` markers. Approval refuses while any remain. |
| "Good text in chat, no usable document" | **EXPORT** builds a `.docx` with your header, footer and page numbers, embeds exercise photos, reads the file back and reports what's in it. Upload to Google Drive and it's a Google Doc. |
| Reusing exercises across clients | A `library/` of exercise descriptions and handout language, seeded from this skill, that grows as you approve new ones. Clients never read each other's folders. |

## Install

From the root of this repo:

```bash
./scripts/install-skill.sh pt-client-programming
~/.claude/skills/pt-client-programming/scripts/setup.sh
```

`setup.sh` installs two helpers (pandoc for document conversion, a small Python package for Word files), creates `~/PT-Programs/`, and copies the seed library and a `practice.conf` for you to fill in with your name, credentials, practice, and the links that go in your header and footer.

Then open Claude Code anywhere and say:

```
new client C-0001, first name Sam. Findings: ... Goals: ... Exercises I've chosen: ...
```

## Daily use

Say what you want in plain language. The skill maps it to one of these modes and tells you which:

| Mode | Example | Result |
|------|---------|--------|
| DISCUSS | "What would you progress next for C-0001's pulling ladder?" | Suggestions, labelled as such, nothing saved to the program |
| NEW CLIENT | "New client C-0002, first name Jo, …" | Folder + intake with gaps flagged |
| BUILD | "Build the first-visit handout for C-0002" | A draft file, section list, list of things to confirm |
| PATCH | "C-0001: add side-lying ER at 2×8–12 to Phase 2 and change wall slide to 2 sets. Nothing else." | A draft, a diff, a before/after table |
| EXPORT | "Export that draft so I can look at it" | A `.docx`, verified |
| APPROVE | "Approve draft_2026-10-14_b: progressed Phase 2" | New approved version, state updated, handout built |

Modifiers: `ROW PATCH ONLY`, `TABLE ONLY`, `TABLE ONLY — DOCX`, `PLAIN TEXT`. They restrict what you get back, never what gets edited.

Read [`SKILL.md`](SKILL.md) for the full rules and [`references/workflow-modes.md`](references/workflow-modes.md) for worked examples.

## Files

```
pt-client-programming/
├── SKILL.md                     the instructions Claude follows
├── README.md                    this file
├── references/
│   ├── program-structure.md     anatomy of a handout; the three patterns; exact table shapes
│   ├── style-guide.md           voice, dose grammar, how to write an exercise description
│   ├── workflow-modes.md        worked examples of each mode
│   ├── exercise-library.md      seed exercise descriptions (side-neutral)
│   └── language-blocks.md       reusable paragraphs and tables
├── templates/                   blank client files and the practice.conf example
└── scripts/
    ├── setup.sh                 one-time: tools, workspace, seed library
    ├── new_client.sh            create a client folder from templates
    ├── find_client.sh           code lookup by first name (searches profile.md only)
    ├── load_client.sh           the retrieval report
    ├── patch_check.py           diff + which sections changed + leftover markers
    ├── build_handout.py         markdown → .docx with header/footer, verified
    └── approve.sh               draft → approved vNNN, state + changelog updated
```

## Privacy

This matters more here than in most skills, so plainly:

- **Everything Claude reads is sent to Anthropic** to generate the response. That includes the client folder you load. Consumer Claude plans (Pro, Max) are not covered by a HIPAA Business Associate Agreement. Whether that is acceptable for your records is your call and your regulator's, not this skill's. If you need a BAA, that is available through enterprise arrangements, not through this setup.
- The skill minimises what goes in: client **codes** in folder and file names, first name only inside the client folder, no contact details, no third-party names. It loads one client at a time and never reads across clients.
- `~/PT-Programs/` lives on your Mac. It is not in this repo and `.gitignore` here refuses it. Back it up the way you back up any clinical record.
- Nothing in this repo contains real client data. The exercise library and language blocks are generic clinical writing.

## Requirements

- macOS with Homebrew (see the main guide, steps 1–5)
- Claude Code
- `pandoc` and Python 3 (installed by `setup.sh`)
