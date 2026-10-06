# chatgpt-sources-outreach

A Claude skill that gets your SaaS onto the pages ChatGPT reads before it answers "what is the best X tool".

ChatGPT builds those answers mostly from other people's pages: "best tools" lists, comparisons and reviews. So the move is simple: find those pages, find the person who writes them, and send them a short honest email.

**The objective:** get your product named on the pages ChatGPT already reads, by giving each writer something useful (a ready-to-paste entry, free access to test it, real data their readers care about, or a fix for their page). Value first, never a free account in exchange for a listing.

This skill does the boring parts for you:

1. Checks Gmail + Google Sheets are connected to Claude (and walks you through it if not)
2. Asks what value you're offering and how you want emails handled
3. Sorts the pages ChatGPT cites (lists vs competitors vs platforms)
4. Checks each page for a real fix to offer (broken links, outdated prices, dead or renamed tools, wrong facts), with proof
5. Finds a real contact email on each site (only emails it actually sees on the page, no guessing)
6. Logs everything in a Google Sheet
7. Writes a personal email for each site and delivers it your way:
   - **Drafts:** saved in Gmail, you send
   - **Send after approval:** you approve each batch in chat, Claude sends
   - **Send on its own:** Claude sends up to 20 a day without asking
8. Tracks replies, does one follow-up, and re-checks ChatGPT every 2 weeks

Built by Jeet ([@iojeet](https://instagram.com/iojeet)) for the "making chatgpt say my name" series.

## The steps

1. **Connect Gmail and Google Sheets** to Claude.
2. **Run your prompt in ChatGPT** with search on, e.g. "what is the best ai tool for aeo".
3. **Click Sources** under the answer and copy every URL. Do it 3 times in new chats, a minute apart.
4. **Give the URLs to Claude** with this skill installed. It asks for your product, the value you offer and how to send.
5. **Check the sheet** Claude makes: url, type, times cited, contact, email, where it found it.
6. **Pick drafts, approve-then-send, or auto-send.**
7. **Re-run the prompt** every 2 weeks and see if you show up.

## Install

You need Claude with the **Gmail** and **Google Sheets** connectors turned on.

**Claude Code:**

```bash
git clone https://github.com/mavekjeet/chatgpt-sources-outreach.git
cp -r chatgpt-sources-outreach/skills/chatgpt-sources-outreach ~/.claude/skills/
```

Then say: "use chatgpt-sources-outreach, here are my urls".

**Claude.ai:** zip the `skills/chatgpt-sources-outreach` folder and upload it under Settings > Capabilities > Skills.

## Rules it follows (so you don't get marked as spam)

- Max 20 emails a day, one person per site, one follow-up max.
- Only emails it actually found on the site, never guessed.
- Auto-send asks you once before the first email goes out.
- Every email has an easy opt-out line.
- The free account is for feedback, never in exchange for a link or a spot on the list. If someone reviews you after getting it free, they should disclose that.

## License

MIT
