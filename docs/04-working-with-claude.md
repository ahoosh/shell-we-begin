# Step 4 · Make Claude work the way you do

**Time: 10 minutes of reading.**

## How to ask

Treat Claude like a careful colleague, not a search box.

- **Say the goal, not just the step.** "I want a one-page handout my clients can read on their phone" beats "make a document."
- **Point at examples.** Drag in last week's document: "Do it in this style."
- **Ask it to check its work.** "Before you finish, re-read the file and confirm nothing else changed."
- **Ask it to explain.** "What did that command do?" It's patient, and it never minds.
- **Say no.** Reject a change in the diff view, or just type "no, keep the old wording" and press Enter.

## Where things live

| Place | What's there |
|-------|--------------|
| `~/Projects/` | Your project folders. You pick one when you start a session. |
| `~/Projects/shell-we-begin/` | This repo, with the skills' source. Claude updates it for you. |
| `~/.claude/skills/` | Installed skills. Hidden folder; you never need to open it. |
| `~/PT-Programs/` (for the clinical skill) | Your clients' files. Yours. Back it up like any record. |
| `CLAUDE.md` inside a project folder | Standing instructions Claude reads at the start of every session in that folder. |

`~` means your home folder, the one with your name on it. Folders starting with a dot are hidden; that's where tools keep settings.

## Standing instructions

Tell Claude once, in a session on your `Projects` folder:

```
Create a CLAUDE.md here that says: I'm a physical therapist, not a programmer. Explain things simply. Always show me what changed before and after. Match the tone of my existing documents. Use client codes, never client names, in file names.
```

From then on every session in that folder starts with those rules. There's also a personal one that applies everywhere; ask Claude to "put that in my global CLAUDE.md too."

## Permission modes

| Mode | When |
|------|------|
| **Manual** | You're new, or the task touches something important. Claude proposes, you accept. |
| **Accept edits** | Routine work. File edits auto-apply; you can review them in the diff view. |
| **Auto** | Long jobs. A background safety check blocks risky actions. |
| **Plan** | "Tell me how you'd do this before you do it." Nothing changes. |

Switch any time with the selector next to the send button.

## Make your own skill

The fastest way: describe the job and ask.

```
I do the same task every Monday: <describe it, with an example of the finished result attached>. Turn it into a skill called weekly-report in ~/.claude/skills: a SKILL.md with the steps, the rules, and the output format. Ask me questions first.
```

Claude knows the format. For the full specification, see [Anthropic's skills documentation](https://code.claude.com/docs/en/skills). Once it works, send it my way and it can join this repo for others.

## Parallel sessions, side chats, cloud

- **New session** in the sidebar runs a second task at the same time.
- **Side chat** asks a question without derailing the main task.
- **Cloud** sessions run on Anthropic's computers and keep going when you close the app, but they don't see your Mac's files. Local is what you want for your own documents.

---

**You're set up.** Keep the [cheat sheet](cheat-sheet.md) handy.
