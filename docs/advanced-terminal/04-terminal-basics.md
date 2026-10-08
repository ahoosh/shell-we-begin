# Step 4 · Terminal basics, the only ones you need

**Time: 20 minutes.** Do this with Ghostty open. Type every command; don't just read.

You're about to learn roughly twelve commands. That is enough to never feel lost, and more than enough to work with Claude Code, which will do the complicated stuff for you.

## Where am I? What's here?

```bash
pwd
```

*Print working directory.* Always tells you the folder you're standing in. When in doubt, `pwd`.

```bash
ls
```

*List.* Shows what's in the current folder.

```bash
ls -la
```

Same, but `-l` gives a long detailed listing (sizes, dates) and `-a` shows hidden files, the ones whose names start with a dot, like `.zshrc` or `.config`. Options (also called *flags*) are the letters after a dash. They modify a command.

## Moving around

```bash
cd Desktop
```

*Change directory.* You're now standing on your Desktop. Try `pwd` to confirm, then `ls` to see the files that are on it.

```bash
cd ..
```

Go **up** one level, back to home. Two dots mean "the parent folder."

```bash
cd ~
```

Go home from anywhere. The `~` (tilde) always means your home folder. Plain `cd` with nothing after it does the same.

```bash
cd ~/Documents
```

Jump straight to Documents from anywhere. A path with slashes is just folders inside folders.

> [!TIP]
> **Tab is your best friend.** Type `cd Doc` and press **Tab**. The terminal completes it to `cd Documents/`. If several names match, press Tab twice to see them all. You almost never need to type a full name.

> [!TIP]
> **Drag a folder from Finder into the terminal window.** Its full path gets pasted. Great for `cd ` + drag + Enter.

## Making things

Let's build a sandbox to play in:

```bash
cd ~
mkdir playground
cd playground
pwd
```

`mkdir` = *make directory*. You're now inside `~/playground`.

```bash
touch notes.txt
ls
```

`touch` creates an empty file (or updates the date on an existing one).

```bash
echo "hello from the terminal" > notes.txt
cat notes.txt
```

`echo` prints text. The `>` sends that text into a file instead of the screen (and **overwrites** what was there). `cat` prints the contents of a file.

```bash
echo "second line" >> notes.txt
cat notes.txt
```

`>>` **appends** instead of overwriting.

## Looking at things

```bash
open .
```

Opens the current folder in Finder. The dot means "here." You'll use this constantly: do something in the terminal, `open .` to look at it the normal way.

```bash
open notes.txt
```

Opens the file with its default app, as if you double-clicked it.

```bash
head -n 5 notes.txt
tail -n 5 notes.txt
```

First 5 lines / last 5 lines of a file. Useful for big files.

```bash
less notes.txt
```

Scroll through a file one screen at a time. Arrow keys to move, **q** to quit. (If a command ever shows you a screen that won't go away, **q** is usually the exit.)

## Copying, moving, renaming

```bash
cp notes.txt backup.txt
```

*Copy.* `cp source destination`.

```bash
mv backup.txt old-notes.txt
```

*Move.* Also how you **rename** something: moving it to a new name in the same place.

```bash
mkdir archive
mv old-notes.txt archive/
ls archive
```

Moving a file into a folder.

## Deleting

```bash
rm archive/old-notes.txt
```

*Remove.* **There is no Trash.** `rm` deletes immediately and permanently. Read the name twice before pressing Enter.

```bash
rm -r archive
```

`-r` (*recursive*) removes a folder and everything in it. Same warning, doubled.

> [!WARNING]
> Never run `rm -rf` on something you didn't create yourself, and never with `~` or `/` in the path, no matter who tells you to. If a tutorial says to, ask Claude what it does first.

A safer habit: install `trash` and use it instead of `rm`:

```bash
brew install trash
trash notes.txt
```

That moves things to the macOS Trash, where you can recover them.

## Spaces in names

The terminal splits commands on spaces, so `cd My Folder` means "cd into `My`, and also `Folder`." Wrap names with spaces in quotes:

```bash
cd "My Folder"
```

Or let **Tab** complete it: the terminal adds the backslash escapes (`My\ Folder`) for you.

## Stopping and cleaning up

| Key | What it does |
|-----|--------------|
| **Ctrl C** | Stop the running command. Also: "cancel this line I half-typed." |
| **Ctrl D** | "I'm done." Exits a program that's waiting for input, or closes the shell. |
| **⌘K** (Ghostty) or `clear` | Wipe the screen. Nothing is deleted; it's just tidy. |
| **q** | Quit a pager like `less` or `man`. |
| **↑ / ↓** | Scroll through commands you typed earlier. Press ↑ and Enter to re-run the last one. |
| **Ctrl A / Ctrl E** | Jump to the start / end of the line you're typing. |
| **Ctrl R** | Search your command history. Start typing, it finds the match. |

## Getting help

```bash
man ls
```

The manual page for any command. Dense, but it's all there. **q** to exit.

Or, once you have Claude Code (next step), just ask: *"what does `ls -la` do?"* It will explain better than the manual does.

## Running things you installed

When you `brew install` a tool, it becomes a command. Try:

```bash
which git
git --version
```

`which` tells you where a command lives. If `which` prints nothing, the command isn't installed or your terminal can't find it (see [troubleshooting](99-troubleshooting.md)).

## Clean up the sandbox

```bash
cd ~
rm -r playground
```

(You created it, it only has test files in it, and you just read the warning. This is the safe kind of `rm -r`.)

## The twelve commands

| Command | Meaning | Example |
|---------|---------|---------|
| `pwd` | Where am I? | `pwd` |
| `ls` | What's here? | `ls -la` |
| `cd` | Go to a folder | `cd ~/Documents` |
| `mkdir` | Make a folder | `mkdir projects` |
| `touch` | Make an empty file | `touch todo.md` |
| `cat` | Show a file | `cat todo.md` |
| `open` | Open in Finder / default app | `open .` |
| `cp` | Copy | `cp a.txt b.txt` |
| `mv` | Move or rename | `mv a.txt archive/` |
| `rm` | Delete (permanent) | `rm old.txt` |
| `echo` | Print text | `echo "hi" > file.txt` |
| `man` | Manual | `man cd` |

Plus the three keys: **Enter**, **Tab**, **Ctrl C**.

That's genuinely all the terminal you need. Everything else, you ask Claude.

→ [Step 5: Install Claude Code](05-claude-code.md)
