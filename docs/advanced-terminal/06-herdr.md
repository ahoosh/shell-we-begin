# Step 6 · Herdr, sessions that keep running

**Time: 10 minutes.**

## The problem Herdr solves

Right now, if you close the Ghostty window while Claude is in the middle of a 20-minute job, the job dies. If you want two Claude sessions on two different projects, you juggle windows and lose track of which one needs you.

[Herdr](https://herdr.dev) fixes both. It's a small program that keeps your terminal sessions alive in the background, so you can close the window, reopen it hours later, and everything is exactly where you left it. It also shows a sidebar with every Claude session you have running and whether each one is **working**, **blocked** (waiting for you), or **done**.

It's the piece that makes [Step 7, phone access](07-phone-access.md), reliable: Claude keeps running on your Mac even when you're not looking at it.

## 1. Install

```bash
brew install herdr
```

## 2. Start it

Go to a project folder and run it:

```bash
cd ~/Projects/first-project
herdr
```

The screen changes: a sidebar on the left, a terminal on the right. The terminal pane is a normal shell. Herdr noticed you were in `first-project` and made a **workspace** for it.

Now start Claude inside that pane:

```bash
claude
```

Look at the sidebar. Herdr detected Claude and shows its status. Give Claude something slow to do, for example *"write a detailed 2000-word guide to stretching after running, as a markdown file"*, and watch the sidebar say **working**.

## 3. The magic trick: detach

While Claude is still working, press **Ctrl B**, release, then press **q**.

You're back in your plain shell. Claude is still running in the background. Close Ghostty completely if you like.

Now reopen Ghostty and type:

```bash
herdr
```

Everything is back. Claude probably finished while you were gone.

> [!NOTE]
> **Ctrl B** is the "prefix." Every Herdr shortcut is: press Ctrl B, let go, then press one more key. It's how Herdr tells your keystrokes apart from Claude's. (Claude Code itself uses Ctrl B to push a task into the background. If you ever need that, press Ctrl B twice, or change Herdr's prefix in its config.)

## 4. The shortcuts you'll use

Everything also works with the mouse: click panes, drag borders, right-click for a menu. Keyboard is just faster.

| Shortcut (after Ctrl B) | What it does |
|-------------------------|--------------|
| **q** | Detach. Everything keeps running. |
| **v** | Split right (a second terminal beside this one) |
| **-** (minus) | Split down |
| **h j k l** | Move focus left / down / up / right |
| **z** | Zoom: make the current pane full-screen, again to undo |
| **x** | Close the current pane |
| **c** | New tab inside this workspace |
| **n / p** | Next / previous tab |
| **Shift N** | New workspace (a second project) |
| **w** | Jump between workspaces |
| **g** | "Go to" picker: jump to any agent or terminal |
| **b** | Hide / show the sidebar |
| **?** | Show every shortcut |

## 5. A typical layout

Two projects, each with Claude running, and a spare shell for `ls` and `open .`:

```
┌──────────────┬──────────────────────────────────────┐
│ ▸ clients    │  claude  (working)                   │
│    claude ●  │                                      │
│    shell     ├──────────────────────────────────────┤
│ ▸ website    │  $ ls                                │
│    claude ●  │  $ open .                            │
└──────────────┴──────────────────────────────────────┘
```

Make it: `herdr` in the first project, `claude`, then **Ctrl B** `-` to split and have a shell underneath. **Ctrl B** `Shift N` for the second project.

## 6. Optional: tighter Claude integration

```bash
herdr integration install claude
```

This lets Herdr restore Claude sessions natively after a reboot. It edits Claude's settings file to add a small hook; it's safe, and `herdr integration status` shows what it did.

## 7. Stopping everything

Detaching is the normal way to walk away. If you truly want to shut everything down:

```bash
herdr server stop
```

## 8. Updating

Herdr moves fast. Every couple of weeks:

```bash
brew upgrade herdr
```

→ [Step 7: Use it from your phone](07-phone-access.md)
