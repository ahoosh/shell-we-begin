# Step 3 · Use it from your phone

**Time: 5 minutes.**

Claude Code has a feature called **Remote Control**. The session keeps running on your Mac; your phone becomes a window into it. You can read what Claude did, approve things, send photos, and give new instructions from anywhere.

Requirements: Pro or Max plan, the Claude app on your phone signed in with the same account, and your Mac awake and online.

## 1. Install the Claude app on your phone

App Store (iPhone) or Google Play (Android): search **Claude by Anthropic**. Sign in with the same account. Allow notifications.

## 2. Turn Remote Control on for all sessions (recommended)

Remote Control is **off for every new session unless you say otherwise**, which is why a session you expect to see on your phone is often simply not connected. Set it once and forget it:

**Settings → Claude Code → Connect new sessions to Remote Control** → on.

(Behind the scenes this writes `remoteControlAtStartup: true` into your Claude settings. It also applies if you ever use the terminal version.)

For a session that was already open before you changed the setting, or if you'd rather connect one at a time: in the toolbar, before the session title, there is a small **laptop icon**. Click it and turn on the **Remote Control** switch, or type `/remote-control` in the prompt box. The icon lights up when connected.

## 3. Find it on your phone

Open the Claude app → tap **Code**. Connected sessions show a computer icon with a green dot. Tap one. Send a message from your phone and watch it appear on your Mac.

## 4. Keep your Mac awake

If the Mac sleeps, your phone loses the connection until it wakes. Fix it once:

**System Settings → Battery** (laptops) or **Energy** (desktops) → **Options…** → **Prevent automatic sleeping on power adapter when the display is off** → on.

Keep the Mac plugged in with the lid open. The screen can go dark; that's fine. Closing a laptop's lid sleeps it unless it's connected to an external display.

## 5. What you can do from the phone

- Approve "Can I run this?" prompts.
- Send a photo with a caption: *"add this exercise photo to C-0001 and reference it in the menu."*
- Start a task and go back to your day. The phone buzzes when Claude finishes or needs you.
- Check which sessions are working and which are waiting on you.

## Also: Dispatch

In the desktop app's **Cowork** tab there is **Dispatch**: a standing conversation you can message from your phone with a task ("draft the week-2 handout for C-0001 and tell me when it's ready"). It can open a Code session on its own, and the app pings your phone when it's done. Same account, same Mac, no setup beyond the above.

→ [Step 4: Working with Claude](04-working-with-claude.md)
