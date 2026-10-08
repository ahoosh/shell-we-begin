# Troubleshooting

## The Code tab says I need to upgrade

Claude Code needs a **Pro or Max** plan. Upgrade at claude.ai, then quit the app fully (⌘Q) and reopen.

## 403 or sign-in errors in the Code tab

Sign out and back in from the app menu. If that fails, quit completely (⌘Q, not just closing the window), reopen, sign in again.

## A dialog about "Command Line Developer Tools"

Click **Install**. It's Apple's free toolkit; the skill scripts need Python from it. Takes a few minutes. Then tell Claude "done, try again."

## Setup says Python is not available

Same cause as above. If no dialog appeared, paste into the session:

```
Run xcode-select --install and tell me what happens.
```

## Claude says `git` isn't available

Fine. The install prompt in [Step 2](02-install-a-skill.md) tells Claude to download the zip instead. Say "use the zip method."

## My phone can't see the session

1. Mac awake and online? ([Step 3, section 4](03-phone.md#4-keep-your-mac-awake))
2. Laptop icon lit up next to the session title? If not, click it → Remote Control on.
3. Same account on phone and Mac?
4. If the Mac was offline for more than ten minutes, the connection drops. Turn the switch off and on again.

## The handout has no PDF

LibreOffice isn't installed. Paste into a session:

```
Run ~/.claude/skills/pt-client-programming/scripts/setup.sh --with-pdf
```

Without it, PDFs come from Google Chrome if you have it (fine, but no page numbers).

## Claude asks permission for everything

Switch the permission mode to **Accept edits** for routine work.

## Something else

Paste the exact error into the session and say: *"I'm not technical. This happened: <paste>. Explain what it means and fix it step by step."*
