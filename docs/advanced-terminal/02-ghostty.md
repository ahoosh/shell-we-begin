# Step 2 · Ghostty, a terminal you'll actually enjoy

**Time: 5 minutes.**

The built-in Terminal works, but [Ghostty](https://ghostty.org) is faster, prettier, has proper tabs and splits, and handles the symbols Claude Code draws on screen far better. It's free and open source.

## 1. Install it

In Terminal.app (the one you used in Step 1):

```bash
brew install --cask ghostty
```

`--cask` is how Homebrew installs regular Mac apps (ones that end up in your Applications folder) rather than command-line tools.

## 2. Open it

Press **⌘ Space**, type `Ghostty`, press Enter. The first time, macOS may ask if you're sure you want to open an app downloaded from the internet. Click **Open**.

You get a window that looks a lot like Terminal.app. Type `pwd` to prove it's the same thing underneath.

> [!TIP]
> Drag Ghostty to your Dock. Right-click its Dock icon → **Options** → **Keep in Dock**. You can quit Terminal.app now and never open it again.

## 3. Give it a look you like

Ghostty is configured with a plain text file. Open it with **⌘ ,** (Command-comma), which opens the config file in TextEdit. If the file is empty, that's expected.

Paste this in:

```ini
theme = Catppuccin Mocha
font-size = 15
window-padding-x = 12
window-padding-y = 8
```

Save (**⌘S**), then go back to Ghostty and press **⌘ Shift ,** to reload the config. The colors change immediately.

Want a different theme? Ghostty ships with hundreds. Run this inside Ghostty to browse them with a live preview (arrow keys to move, **q** to quit):

```bash
ghostty +list-themes
```

Swap the theme name in your config and reload again.

> [!NOTE]
> The config file lives at `~/.config/ghostty/config`. You'll see this path again. `~` is your home folder, and `.config` is a hidden folder where many tools keep their settings.

## 4. The shortcuts worth knowing

| Shortcut | What it does |
|----------|--------------|
| **⌘T** | New tab |
| **⌘D** | Split the window side by side |
| **⌘ Shift D** | Split top/bottom |
| **⌘ [** / **⌘ ]** | Jump between splits |
| **⌘W** | Close tab or split |
| **⌘K** | Clear the screen |
| **⌘ +** / **⌘ -** | Bigger / smaller text |
| **⌘ ,** | Open config |
| **⌘ Shift ,** | Reload config |

You don't need splits yet. We'll use Herdr for that in Step 6, because Herdr's splits keep running when you close the window and Ghostty's don't.

→ [Step 3: Nerd Fonts](03-nerd-fonts.md)
