> **Terminal route.** This is the original, more technical version of the guide. The simpler desktop-app route is in the [main README](../../README.md). Both end up with the same skills.

# Step 0 · Before you start

**Time: 5 minutes.** Nothing to install yet. Just a checklist and two ideas.

## Checklist

- [ ] A Mac running macOS 13 (Ventura) or newer. Check: Apple menu  → **About This Mac**.
- [ ] A Claude account on the **Pro** or **Max** plan. The free plan does not include Claude Code. Sign up or upgrade at [claude.ai](https://claude.ai).
- [ ] Your Mac's login password. Installers will ask for it once or twice.
- [ ] About 90 minutes, ideally in one sitting. Steps 1 to 5 are the ones that need to happen together.
- [ ] Your phone nearby for [Step 7](07-phone-access.md).

## Idea 1: the terminal is just a chat window for your computer

Every app you use is a graphical skin over commands. The terminal lets you type those commands directly.

That sounds scary. It is actually simpler than a graphical app, because there is nothing to hunt for. You type a word, press **Enter**, the computer answers, and you get a new line to type on. That's the whole interface.

```
you type ──▶  ls                ◀── "list what's here"
Mac says  ──▶  Desktop  Documents  Downloads  Music
you type  ──▶  █                ◀── ready for the next command
```

The blinking block is called the **cursor**. The text before it (your name, a folder, a `%` or `$` sign) is called the **prompt**. The prompt means "I'm listening."

## Idea 2: Claude Code is a colleague sitting at your keyboard

Claude Code is an AI that lives in the terminal. You describe what you want in plain English. It looks at your files, decides what to do, and does it: creates documents, renames photos, builds a spreadsheet, writes a script, fixes something that broke.

Two rules it always follows:

1. It works inside the folder you start it in. It can't wander around your Mac.
2. It asks before changing anything, until you tell it you trust it.

So the terminal skills you need are small: open a terminal, move into a folder, start Claude. Everything else you can ask Claude to do, including explaining the terminal to you.

## How to copy and paste in this guide

Every command looks like this:

```bash
echo "hello"
```

Hover over the box and a **copy** button appears in the top-right corner. Click it, go to your terminal, press **⌘V**, then press **Enter**. Commands only run when you press Enter.

> [!NOTE]
> Don't type the `$` or `%` you might see at the start of a line in other tutorials. In this guide, the boxes contain exactly what you type.

## The three keys you'll use constantly

| Key | What it does |
|-----|--------------|
| **Enter** | Run the command you typed |
| **Tab** | Auto-complete a file or folder name (press it early and often) |
| **Ctrl + C** | "Stop whatever you're doing." Your panic button. Never harmful. |

Ready? → [Step 1: Meet the terminal and install Homebrew](01-terminal-and-homebrew.md)
