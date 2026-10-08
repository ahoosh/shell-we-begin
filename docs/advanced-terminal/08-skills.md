# Step 8 · Skills: teaching Claude a job it does the same way every time

**Time: 10 minutes.**

## What a skill is

A skill is a folder with a file called `SKILL.md` inside. The file is written in plain English and says: *here's a job, here's how I want it done, here are the rules.* Claude reads it automatically whenever your request matches, or when you type `/skill-name`.

A skill can also bring along templates, reference material, and small scripts. Think of it as a very detailed standard operating procedure that Claude actually follows.

```
~/.claude/skills/
└── pt-client-programming/
    ├── SKILL.md           ← the instructions (Claude reads this)
    ├── README.md          ← for humans
    ├── references/        ← style guide, document structure, exercise library
    ├── templates/         ← blank client files
    └── scripts/           ← helpers (build the Word doc, check a patch, …)
```

Personal skills live in `~/.claude/skills/` and work in every folder on your Mac.

## Install a skill from this repo

First, get this repo onto your Mac (once):

```bash
cd ~/Projects
git clone https://github.com/ahoosh/shell-we-begin.git
cd shell-we-begin
```

Then install any skill by name:

```bash
./scripts/install-skill.sh pt-client-programming
```

It copies the skill into `~/.claude/skills/`. Start (or restart) Claude Code and type `/` to see it in the list.

## Update a skill later

```bash
cd ~/Projects/shell-we-begin
git pull
./scripts/install-skill.sh pt-client-programming
```

`git pull` fetches the latest version of this repo. The install script overwrites the old copy of the skill (your own data is never inside the skill folder, so nothing of yours is lost).

## Skills available

| Skill | What it's for | Setup guide |
|-------|---------------|-------------|
| `pt-client-programming` | Clinicians who write and update client exercise programs. Approved versions, surgical patches, before/after review, Word/Google Docs + PDF + phone-friendly HTML export. | [How to use](../../skills/pt-client-programming/HOW-TO-USE.md) · [README](../../skills/pt-client-programming/README.md) |

## Make your own

The easiest way: ask Claude.

```
I do the same task every Monday: <describe it>. Turn it into a skill called
weekly-report in ~/.claude/skills, with a SKILL.md that explains the steps,
the rules, and the output format. Ask me questions first.
```

Claude knows the format. Give it an example of a finished output and it will write the skill around it.

For the full specification, see [Anthropic's skills documentation](https://code.claude.com/docs/en/skills).

---

**You're done with the setup.** Keep the [cheat sheet](cheat-sheet.md) handy.
