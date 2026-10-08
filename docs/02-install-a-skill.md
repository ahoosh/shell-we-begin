# Step 2 · Install this repo and a skill, by asking Claude

**Time: 10 minutes, mostly waiting.**

You don't install anything by hand. You tell Claude to do it.

## 1. Paste this into a session

In the Code tab, with your `Projects` folder selected (Step 1), paste this and press Enter:

```
Please set me up with the shell-we-begin skills:

1. Download https://github.com/ahoosh/shell-we-begin into a folder called shell-we-begin inside this folder. Use git clone if git is available; otherwise download https://github.com/ahoosh/shell-we-begin/archive/refs/heads/main.zip and unzip it, renaming the folder to shell-we-begin.
2. Run ./scripts/install-skill.sh pt-client-programming from inside that folder.
3. Run ~/.claude/skills/pt-client-programming/scripts/setup.sh --with-pdf and show me its output. If macOS pops up a dialog about Command Line Developer Tools, tell me to click Install and wait, then try again.
4. When it finishes, open ~/PT-Programs/practice.conf in TextEdit so I can fill in my details, and tell me which lines to edit.

Explain each step in one sentence before you do it. I'm not technical.
```

Swap `pt-client-programming` for whichever skill you want from the [list](../README.md#skills-in-this-repo). Claude will ask you to **Accept** a few commands if you're in Manual mode. Accept them.

The `--with-pdf` part downloads LibreOffice (about 400 MB), which is what turns handouts into PDFs that look exactly like the Word version. Leave it out if you don't need PDFs.

## 2. Fill in your details

TextEdit opens `practice.conf`. Replace the example name, practice, phone, email, website and scheduling link with yours. Save (⌘S). That text goes at the top and bottom of every handout.

## 3. Check it worked

Start a **new session** (sidebar → New session), pick your `Projects` folder again, and type `/`. You'll see `pt-client-programming` in the list of skills. You don't have to pick it from the list; Claude uses it automatically when you talk about a client program.

Try:

```
What can the pt-client-programming skill do, and what should I say to start my first client?
```

Then read the skill's own guide: [HOW-TO-USE](../skills/pt-client-programming/HOW-TO-USE.md).

## Updating later

Skills improve over time. To get the latest version, paste this into any session:

```
Update my shell-we-begin skills: go to ~/Projects/shell-we-begin, run git pull (or re-download the zip if git isn't available), then run ./scripts/install-skill.sh pt-client-programming again. My own data in ~/PT-Programs must not be touched.
```

→ [Step 3: Use it from your phone](03-phone.md)
