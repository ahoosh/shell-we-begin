# Step 3 · Nerd Fonts, so icons aren't little boxes

**Time: 5 minutes.**

Terminal tools like Claude Code and Herdr draw icons, progress spinners, arrows, and status symbols. They do it with special characters that a normal font doesn't contain. Without the right font you see `▯` or `?` where there should be a ✓ or a folder icon.

A **Nerd Font** is a normal coding font with thousands of those symbols patched in.

## 1. Install JetBrains Mono Nerd Font

```bash
brew install --cask font-jetbrains-mono-nerd-font
```

That's one of the most readable fonts available and the one this guide was written with. (Alternatives, if you're curious later: `font-fira-code-nerd-font`, `font-hack-nerd-font`, `font-meslo-lg-nerd-font`.)

## 2. Tell Ghostty to use it

Press **⌘ ,** to open the Ghostty config and add this line:

```ini
font-family = JetBrainsMono Nerd Font
```

Your whole config now looks like:

```ini
theme = Catppuccin Mocha
font-family = JetBrainsMono Nerd Font
font-size = 15
window-padding-x = 12
window-padding-y = 8
```

Save, then **⌘ Shift ,** to reload. The letters change shape slightly.

## 3. Test it

Paste this and press Enter:

```bash
echo "        <- you should see five symbols, not boxes"
```

You should see something like a triangle, a house, a code icon, a leaf, a check mark and an hourglass. If you see boxes or question marks:

- Make sure the font line is spelled exactly `JetBrainsMono Nerd Font` (no space between JetBrains and Mono).
- Reload the config with **⌘ Shift ,**, or quit and reopen Ghostty.
- Run `ghostty +list-fonts | grep -i nerd` to confirm Ghostty can see the font. If nothing is printed, re-run the install command from step 1.

## Why this matters later

- **Claude Code** draws spinners, check marks and tree views while it works.
- **Herdr** shows a sidebar with status icons for every running agent.
- Many terminal tools (`eza`, `starship`, `lazygit`) assume a Nerd Font.

With this done, every screen you'll see for the rest of the guide renders the way its author intended.

→ [Step 4: Terminal basics](04-terminal-basics.md)
