# Step 1 · Meet the terminal and install Homebrew

**Time: 15 minutes.** By the end you'll have typed your first commands and installed the tool that installs everything else.

## 1. Open the terminal that ships with your Mac

1. Press **⌘ Space** to open Spotlight.
2. Type `Terminal` and press **Enter**.

A plain window appears with a line of text and a blinking cursor. It looks something like:

```
yourname@Your-MacBook ~ %
```

That's the prompt. The `~` means you are in your **home folder** (the one with Desktop, Documents, Downloads inside it). The `%` means "type here."

> [!NOTE]
> We'll replace this app with a nicer one in Step 2. We need it now because it's the only terminal you have yet.

## 2. Type your first command

Type this and press Enter:

```bash
pwd
```

It prints something like `/Users/yourname`. `pwd` stands for *print working directory*: "where am I right now?"

Now:

```bash
ls
```

You'll see the folders in your home: `Desktop`, `Documents`, `Downloads`, and so on. `ls` means *list*.

That's it. You've used the terminal. Everything from here is more of the same.

## 3. Install Homebrew

[Homebrew](https://brew.sh) is an app store for the terminal. One command, `brew install something`, fetches and installs tools. We'll use it for Ghostty, fonts, Herdr, and more.

Paste this and press Enter:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

What happens next:

1. It explains what it will do and says **Press RETURN/ENTER to continue**. Press Enter.
2. It asks for your Mac password. **Nothing appears while you type.** That's normal. Type it and press Enter.
3. It may install Apple's "Command Line Tools" first. A dialog might pop up; click **Install**. This can take 5 to 10 minutes.
4. When it's done it prints **Installation successful!** and, below that, a section called **Next steps**.

## 4. Do the "Next steps" (important)

On Apple Silicon Macs (M1, M2, M3, M4), Homebrew lives in `/opt/homebrew`, and your terminal doesn't know to look there yet. The installer prints two commands to fix that. They look like this (yours will have your username in them):

```bash
echo >> /Users/yourname/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/yourname/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Copy **the ones from your own terminal**, paste them, press Enter.

Then verify:

```bash
brew --version
```

You should see `Homebrew 4.x.x`. If you see `command not found: brew`, close the Terminal window completely (**⌘Q**), open it again, and try `brew --version` once more.

## 5. Install a couple of basics while you're here

```bash
brew install git
```

Git is the tool that fetches this repo (and the skills in it) to your Mac. You won't have to learn it. Claude will use it on your behalf.

## What you just learned

| Command | Meaning |
|---------|---------|
| `pwd` | Where am I? |
| `ls` | What's here? |
| `brew install <name>` | Install a tool |
| `brew --version` | Is Homebrew working? |

→ [Step 2: Install Ghostty](02-ghostty.md)
