# Step 5 · Claude Code

**Time: 15 minutes.** The reason you did the first four steps.

## 1. Install

In Ghostty:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

The command shows nothing while it downloads. Wait for **Claude Code successfully installed!** Then **close Ghostty completely (⌘Q) and reopen it**, so it learns where the new program lives.

Verify:

```bash
claude --version
```

You should see a version number like `2.1.285 (Claude Code)`.

<details>
<summary>If you see <code>command not found: claude</code></summary>

Run these two lines, then quit and reopen Ghostty:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```
</details>

## 2. Make a home for your projects

Claude works inside the folder you start it from. Give it a dedicated place so it never touches anything else:

```bash
mkdir -p ~/Projects/first-project
cd ~/Projects/first-project
```

## 3. Start it and sign in

```bash
claude
```

The first run:

1. It asks you to pick a color theme. Arrow keys, Enter.
2. It asks how to sign in. Choose **Claude account with subscription**. A browser window opens; sign in with the same account you use at claude.ai; click **Authorize**. Come back to the terminal.
3. It asks if you trust this folder. Press Enter for **Yes**. (It asks once per folder.)

You now see a text box with a `>` prompt. This is Claude. Say hi.

## 4. Your first job

Type this and press Enter:

```
create a file called hello.md with a short friendly note explaining what this folder is for
```

Claude will think for a moment, then show you the file it wants to create and ask permission. Press Enter to say **Yes**. Then:

```
open the folder in Finder so I can see it
```

It runs `open .` for you. That's the pattern: say what you want, approve, look at the result.

Try something real:

```
look at the files on my Desktop and tell me which ones are screenshots older than 30 days
```

(It will ask permission to read outside this folder. Say yes. It's only reading.)

## 5. The things to know

| What | How |
|------|-----|
| Stop Claude mid-task | **Esc** |
| New line without sending | **Shift Enter** (if it sends instead, type `/terminal-setup` once and follow the instruction) |
| Mention a file | Type `@` and start typing its name; pick from the list |
| Paste an image | Copy it, then **Ctrl V** (yes, Ctrl, not ⌘) in the Claude prompt |
| Drag a file in | Drag from Finder into the window; its path appears |
| See all commands | `/help` |
| Start fresh | `/clear` |
| Leave | `/exit` or **Ctrl D** |
| Come back later | In the same folder: `claude -c` (continue) or `claude -r` (pick from a list) |
| Change model | `/model` |
| Permissions | **Shift Tab** cycles between *ask every time*, *auto-accept edits*, and *plan only* |

## 6. Tell it who you are (optional, 2 minutes)

Inside Claude type:

```
/init
```

It writes a file called `CLAUDE.md` in this folder. Anything you put in that file, Claude reads at the start of every session. Open it and add a few lines in plain English:

```
I'm a physical therapist, not a programmer. Explain things simply.
Always show me what changed before and after.
Write in the same tone as my existing documents.
```

Every folder can have its own `CLAUDE.md`. There's also a personal one at `~/.claude/CLAUDE.md` that applies everywhere.

## 7. Good ways to ask

Claude is better the more you treat it like a careful colleague, not a search box.

- **Say the goal, not just the step.** "I want a one-page handout my clients can read on their phone" beats "make a document."
- **Point at examples.** "Do it in the style of @examples/last-week.docx."
- **Ask it to check its work.** "Before you finish, re-read the file and confirm nothing else changed."
- **Ask it to explain.** "What did that command do?" It's patient.

## 8. Where things live

| Path | What's there |
|------|--------------|
| `~/.claude/` | Claude's settings, memory, and your personal skills |
| `~/.claude/skills/` | Skills (Step 8) |
| `<project>/CLAUDE.md` | Instructions for this project |
| `<project>/.claude/` | Project-specific settings |

→ [Step 6: Herdr, sessions that don't die](06-herdr.md)
