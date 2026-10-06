# chatgpt-sources-outreach

A Claude skill that gets your SaaS onto the pages ChatGPT reads before it answers "what is the best X tool".

ChatGPT builds those answers mostly from other people's pages: "best tools" lists, comparisons and reviews. So the move is simple: find those pages, find the person who writes them, and send them a short honest email.

This skill does the boring parts for you:

1. Sorts the pages ChatGPT cites (lists vs competitors vs platforms)
2. Finds a real contact email on each site (only emails it actually sees on the page, no guessing)
3. Logs everything in a Google Sheet
4. Writes a personal Gmail **draft** for each site (you read and send them yourself)
5. Tracks replies and re-checks ChatGPT every 2 weeks

Built by Jeet ([@iojeet](https://instagram.com/iojeet)) for the "making chatgpt say my name" series.

## The steps

1. **Run your prompt in ChatGPT** with search on, e.g. "what is the best ai tool for aeo".
2. **Click Sources** under the answer and copy every URL. Do it 3 times in new chats, a minute apart.
3. **Give the URLs to Claude** with this skill installed, plus your product name, a one-line description and your offer (e.g. a free account for honest feedback).
4. **Check the sheet** Claude makes: url, type, times cited, contact, email, where it found it.
5. **Read the drafts** in Gmail, edit anything that doesn't sound like you, send.
6. **Re-run the prompt** every 2 weeks and see if you show up.

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

- Drafts only. Nothing is sent without you.
- Max 20 drafts a day, one person per site, one follow-up max.
- Every email has an easy opt-out line.
- The free account is for feedback, never in exchange for a link or a spot on the list. If someone reviews you after getting it free, they should disclose that.

## License

MIT
