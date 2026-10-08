# Step 1 · Install the Claude app and open the Code tab

**Time: 10 minutes.**

## 1. Install

Download the Mac app: **[claude.ai/download](https://claude.ai/download)**. Open the `.dmg`, drag **Claude** into **Applications**, then open it from Applications (or press ⌘ Space, type `Claude`, Enter).

Sign in with the account that has your Pro or Max subscription.

## 2. Open the Code tab

At the top centre of the window are three tabs: **Chat**, **Cowork**, **Code**. Click **Code**.

- If it asks you to upgrade, your account isn't on a paid plan yet. Upgrade at [claude.ai](https://claude.ai) and come back.
- If it asks you to sign in online, finish that in the browser, then quit and reopen the app.

The app includes Claude Code. There is nothing else to install.

## 3. Make a home for your projects

In Finder, create a folder called `Projects` inside your home folder (the one with your name on it, next to Desktop and Documents). Everything Claude builds for you will live in there, where you can see it.

## 4. Start your first session

Back in the Code tab:

1. Make sure **Local** is selected (not Cloud or SSH). Local means "run on this Mac, with my files."
2. Click **Select folder** and choose the `Projects` folder you just made.
3. Next to the send button is a **permission mode** selector. Choose **Manual** for now: Claude will show you every change and wait for you to click **Accept**.
4. Type this and press Enter:

```
Create a file called hello.md in this folder with a short friendly note about what this folder is for, then show me the folder in Finder.
```

Claude proposes the file. Click **Accept**. A Finder window opens with your new file in it. That's the whole loop: say what you want, review, accept, look.

## 5. Four things to know

| Want to… | Do this |
|----------|---------|
| Stop Claude mid-task | Click the **stop** button. Or just type a correction and press Enter; it adjusts without stopping. |
| Give it a file | Type `@` and start typing the file's name, drag the file into the prompt box, or use the attachment button for images and PDFs. |
| Let it work without asking each time | Switch the permission mode to **Accept edits** (file changes auto-apply; you can review them in the diff view) or **Auto** (a safety check runs in the background and blocks risky actions). |
| Start a second task | Click **New session** in the sidebar. Each session has its own folder and its own conversation. |

> [!NOTE]
> The first time Claude runs certain commands, macOS may pop up a dialog asking to install **Command Line Developer Tools**. Click **Install**, wait a few minutes, then tell Claude "done, try again." It happens once.

→ [Step 2: Install this repo and a skill](02-install-a-skill.md)
