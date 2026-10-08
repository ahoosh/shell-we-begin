# Troubleshooting

The ten things that actually go wrong.

## `command not found: brew` / `claude` / `herdr`

Your terminal doesn't know where the program was installed. Nearly always fixed by quitting the terminal completely (**⌘Q**) and reopening it.

If that doesn't help, for Homebrew on Apple Silicon:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

For Claude Code:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## The password prompt shows nothing when I type

Normal. The terminal hides passwords completely, not even dots. Type it and press Enter.

## The install command printed HTML or `syntax error near unexpected token '<'`

The download returned a web page instead of the installer, usually a network hiccup or a region block. Try again. If it keeps happening, install with Homebrew instead:

```bash
brew install --cask claude-code
```

## Icons show as boxes or question marks

Nerd Font isn't active. Check `~/.config/ghostty/config` has exactly:

```ini
font-family = JetBrainsMono Nerd Font
```

Then **⌘ Shift ,** or restart Ghostty. Confirm the font is installed:

```bash
ghostty +list-fonts | grep -i nerd
```

## Claude says I need a subscription

Claude Code needs **Pro or Max**. Free accounts can't use it. Also make sure you signed in with the same account in the browser that has the subscription. To switch accounts: `/login` inside Claude.

## Shift+Enter sends the message instead of adding a line

Inside Claude type `/terminal-setup` and follow the instructions. Or type `\` then Enter for a new line.

## My phone can't see the session

In order:

1. Is the Mac awake and online? ([Step 7, section 5](07-phone-access.md#5-keep-your-mac-awake))
2. Is `/rc active` shown in the session's status line? If not, type `/rc`.
3. Same account on phone and Mac? Check `/status` on the Mac and the account page in the app.
4. Session dropped after >10 minutes offline? On the Mac: `claude -c`, then `/rc`.

## I closed the window and lost my Claude session

If you weren't using Herdr: go back to the same folder and run `claude -c`. Your conversation is saved; only the live process ended.

If you were using Herdr: run `herdr`. It's all still there.

## Claude asks permission for everything

Press **Shift Tab** to switch to *accept edits* mode for this session. For a folder you fully trust, you can go further, but read what it says first.

## I ran `rm` and I want the file back

If you used `rm`, it's gone. If you installed `trash` and used that, check the macOS Trash. Going forward: `brew install trash`, and ask Claude to use `trash` instead of `rm` (put that line in your `~/.claude/CLAUDE.md`).

## Something else

Open Claude Code and paste the exact error. Start with: *"I'm new to the terminal. This happened when I ran X: <paste>. Explain what it means and how to fix it, step by step."*
