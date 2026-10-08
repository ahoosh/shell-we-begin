# Step 7 · Steer your sessions from your phone

**Time: 10 minutes.** The payoff step.

Claude Code has a feature called **Remote Control**. Your session keeps running on your Mac; your phone (or any browser) becomes a window into it. You can read what Claude did, answer its questions, approve actions, send it photos, and give it new instructions, from the couch or the clinic.

Requirements: a Pro or Max subscription, the Claude app on your phone, and your Mac awake and online.

## 1. Install the Claude app on your phone

Inside any Claude Code session, type:

```
/mobile
```

A QR code appears. Scan it with your phone's camera; it takes you to the right app store. Install the Claude app and **sign in with the same account** you used in Step 5. Allow notifications when it asks.

## 2. Turn on Remote Control for a session

In a running Claude Code session (ideally inside Herdr, so it survives you closing the window), type:

```
/rc
```

The first time, a dialog explains what Remote Control does. Choose **Enable Remote Control**. From now on you'll see a small **/rc active** indicator in the status line.

To see the QR code and link, type `/rc` again. It opens a status panel with the QR code.

Scan the QR code with your phone's camera. The Claude app opens on this session. Try sending a message from your phone and watch it appear on your Mac.

> [!TIP]
> Give the session a name so it's easy to find in the app: `/rc Client programs` instead of plain `/rc`.

## 3. Find your sessions in the app

Open the Claude app → tap **Code** in the navigation. Every Remote Control session shows a small computer icon with a **green dot** when it's online. Tap it to jump in. The same list exists at [claude.ai/code](https://claude.ai/code) in any browser.

## 4. Push notifications

Still inside Claude Code on your Mac:

```
/config
```

Find and turn on:

- **Push when actions required**: your phone buzzes when Claude needs a yes/no or an answer.
- **Push when Claude decides**: your phone buzzes when a long job finishes.

Claude is quiet while you're actively typing on the Mac, so you won't get buzzed for things you're already looking at.

## 5. Keep your Mac awake

Remote Control runs on your Mac. If the Mac goes to sleep, your phone loses the connection (it reconnects automatically when the Mac wakes, but nothing happens while it sleeps).

**Option A, the setting (recommended):** System Settings → **Battery** (laptops) or **Energy** (desktops) → **Options…** → turn on **Prevent automatic sleeping on power adapter when the display is off**. Keep the Mac plugged in with the lid open. The screen can go dark; that's fine.

**Option B, the command:** in a spare Herdr pane run

```bash
caffeinate -is
```

and leave it. The Mac won't sleep until you press Ctrl C in that pane.

Closing a MacBook's lid always sleeps it unless it's connected to an external display and power. Lid open, screen dark, plugged in: that's the setup.

## 6. Make it automatic

If you want **every** session to be reachable from your phone without typing `/rc`:

```
/config
```

→ **Enable Remote Control for all sessions** → on.

## 7. How it all fits together

```
┌─ Your Mac (plugged in, lid open) ─────────────────────┐
│  Ghostty ─▶ Herdr ─▶ claude  ◀── /rc active           │
│              └─ keeps running even if Ghostty closes  │
└───────────────────────────────────────────────────────┘
                 ▲
                 │ encrypted connection via Anthropic
                 ▼
┌─ Your phone ─────────────┐   ┌─ Any browser ──────────┐
│ Claude app → Code tab    │   │ claude.ai/code         │
│ read · reply · approve   │   │ same session           │
│ send photos · get pushes │   └────────────────────────┘
└──────────────────────────┘
```

Files never leave your Mac. Your phone sends text and photos to the session; Claude on your Mac does the work.

## What you can do from the phone

- Answer "Can I run this?" prompts.
- Send a photo (a whiteboard, a handwritten note, a screenshot) with a caption like *"add this exercise to the plan."*
- Start a new task and go back to your day. Your phone buzzes when it's done.
- Check the sidebar-equivalent: which sessions are working, which are waiting on you.

## Limits worth knowing

- If your Mac is offline for more than about ten minutes, the session drops. Restart it on the Mac with `claude -c` and `/rc`.
- Some slash commands behave differently from the phone; the basics (`/model`, `/clear`, plain conversation) all work.

→ [Step 8: Skills, teaching Claude your job](08-skills.md)
