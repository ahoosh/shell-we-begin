# Cheat sheet

Print this. Or don't; it's one `open` away.

## Terminal

| Command | Meaning |
|---------|---------|
| `pwd` | Where am I? |
| `ls` · `ls -la` | What's here? (detailed, with hidden files) |
| `cd folder` · `cd ..` · `cd ~` | Go into / go up / go home |
| `mkdir name` | Make a folder |
| `touch file` | Make an empty file |
| `cat file` · `less file` | Show a file (all / scrollable, `q` to quit) |
| `open .` · `open file` | Open in Finder / in its app |
| `cp a b` · `mv a b` · `rm a` | Copy · move/rename · delete (permanent!) |
| `echo "text" > file` | Write text into a file (`>>` appends) |
| `man cmd` | Manual for a command |
| `which cmd` | Where is this command installed? |
| `brew install x` · `brew upgrade x` | Install / update a tool |

| Key | Meaning |
|-----|---------|
| **Tab** | Auto-complete |
| **↑** | Previous command |
| **Ctrl C** | Stop / cancel |
| **Ctrl D** | Exit |
| **Ctrl R** | Search history |
| **⌘K** | Clear screen (Ghostty) |
| **q** | Quit a pager |

## Ghostty

| Key | Action |
|-----|--------|
| **⌘T** / **⌘W** | New / close tab |
| **⌘D** / **⌘ Shift D** | Split right / down |
| **⌘ ,** / **⌘ Shift ,** | Open / reload config |
| **⌘ +** / **⌘ -** | Font bigger / smaller |

Config: `~/.config/ghostty/config`

## Claude Code

| Command | Action |
|---------|--------|
| `claude` | Start in this folder |
| `claude -c` | Continue the last conversation here |
| `claude -r` | Pick an older conversation |
| `/help` · `/clear` · `/exit` | Commands · fresh start · leave |
| `/model` | Switch model |
| `/init` | Create a CLAUDE.md for this folder |
| `/rc` · `/rc Name` | Remote Control on (phone access) |
| `/mobile` | QR code to install the phone app |
| `/config` | Settings, including push notifications |
| `/terminal-setup` | Fix Shift+Enter if it sends instead of newlining |

| Key | Action |
|-----|--------|
| **Esc** | Interrupt Claude |
| **Shift Enter** | New line |
| **Shift Tab** | Cycle permission mode |
| **Ctrl V** | Paste an image |
| `@` | Mention a file |

## Herdr (prefix = Ctrl B, release, then key)

| Key | Action |
|-----|--------|
| `q` | Detach (everything keeps running); `herdr` to come back |
| `v` / `-` | Split right / down |
| `h j k l` | Move focus |
| `z` | Zoom pane |
| `x` | Close pane |
| `c` · `n` · `p` | New tab · next · previous |
| `Shift N` · `w` | New workspace · switch workspace |
| `g` | Go-to picker |
| `?` | All shortcuts |

`herdr server stop` shuts everything down. `brew upgrade herdr` updates.

## Phone

1. `/mobile` → install the app, same account.
2. `/rc` in a session → scan the QR.
3. `/config` → push notifications on.
4. Mac plugged in, lid open, "prevent sleeping when display is off" on.

## Skills

```bash
cd ~/Projects/shell-we-begin && git pull
./scripts/install-skill.sh pt-client-programming
```
