---
name: chatgpt-sources-outreach
description: Use when the user wants their product mentioned by ChatGPT for a prompt like "what is the best X tool" and asks to find the pages ChatGPT cites, find the contact emails behind those pages, log them in a Google Sheet, or email those site owners. Triggers on "chatgpt sources outreach", "email the sites chatgpt reads", "find emails for these urls", "get my saas on chatgpt lists".
---

# ChatGPT sources outreach

ChatGPT answers "best tool" prompts mostly from other people's pages: listicles, comparisons and reviews. This skill finds those pages, finds a real person at each one, logs everything in a Google Sheet and emails them something useful. The user picks whether Claude saves drafts, sends after approval, or sends on its own.

## Objective of the campaign

**Goal:** get your product named on the pages ChatGPT already reads for your prompt, so ChatGPT starts naming it too.

**How:** make it easy and worth it for the writer to look at your product when they next update their page. Every email gives them something they can use whether or not they add you. Nobody owes you a spot, and you never trade free stuff for a listing.

## Step 0: connect Gmail and Google Sheets first

Before anything else, check that the **Gmail** and **Google Sheets** connectors are available (look for their tools). If either is missing, stop and tell the user:

> Before we start, connect Gmail and Google Sheets to Claude.
> Claude.ai / desktop: Settings > Connectors > Gmail and Google Sheets > Connect, then sign in with the email you want to send from.
> Claude Code: add them as MCP connectors, then restart the session.
> Tell me when both are connected.

When they say done, confirm by listing their Gmail labels and creating nothing yet. Tell them which email address is connected, so they know who the emails will come from.

## Step 1: ask for the inputs (one message)

Ask for anything missing:

1. **The prompt** you want to show up for, e.g. "what is the best ai tool for aeo".
2. **Your product**: name, URL, and one sentence that says what it IS ("Acme is an X that does Y for Z"). Plain and definitive, no hype words.
3. **The value you give the writer.** Pick one or more (suggest the first two if they're unsure):
   - **A ready-to-paste entry**: one-line description, pricing, who it's for, 2 screenshots. Saves them research time when they update the list.
   - **Free access to test it properly**, e.g. a free 3-month account, for honest feedback. Never in exchange for a listing.
   - **Something their readers would care about**: a real data point, a short case study or an expert quote they can cite. Only if it's true and the user can back it up. Never invent numbers.
   - **A fix for their page**: Claude checks every list page for broken links, outdated prices, dead or renamed tools and wrong facts (Step 3b). Only used where it finds a real, proven problem. Recommended: it's the most useful thing you can give a writer and it costs you nothing.
4. **Your name + sign-off.**
5. **How to deliver the emails.** Ask exactly this:
   > How do you want the emails handled?
   > **A. Drafts:** I save every email as a Gmail draft. You read and send them yourself.
   > **B. Send after approval:** I show you each batch here, you say "send", I send them.
   > **C. Send on its own:** I send them without asking you, within the safety limits below.
6. **The source URLs**, if they already have them (CSV, sheet or pasted list). If not, do Step 2.

Save the answers to the sheet's "Setup" tab in Step 5 so a later session can pick up where this one stopped.

## Step 2: collect the pages ChatGPT reads

The user does this in their own ChatGPT (you cannot run their account):

1. Open ChatGPT with search on, paste the prompt, send.
2. Click **Sources** under the answer. Copy every URL.
3. Run it 3 times (new chat each time, a minute apart). Answers change run to run.
4. Paste all URLs back here.

Then you: dedupe the URLs, count how many runs each one appeared in, and sort by that count (most repeated first).

## Step 3: sort the list

Give every URL a type:

- **list**: third-party "best X tools" / comparison / review page. These are the targets.
- **competitor-list**: a rival tool's "best X tools" page that also lists other tools. Still a target: they already list rivals, so they can add you, and a real fix is welcome from anyone. Lower odds, so it goes after the plain lists.
- **competitor-self**: a rival's page about only itself or itself vs one tool ("Profound vs Otterly"). Skip, there is no list to join.
- **platform**: G2, Capterra, Reddit, YouTube, Product Hunt etc. Not an email target; action = "create profile / post".
- **other**: skip unless the user says otherwise.

Open each list page, note if the product is already mentioned, and note one specific detail for the email (a tool they reviewed, how they tested, when they last updated it, anything broken or outdated).

## Step 3b: find a fix for their page

Run this for every "list" and "competitor-list" page (even if the user didn't pick it as their value: a real fix is the best opener there is). The aim is at least one real, proven issue on every page. Work through three tiers and keep the strongest 1 or 2 finds.

### Tier 1: factual errors (strongest, the writer will want to fix these)


1. **Broken links.** Collect every outbound link in the article body (tool links, pricing links, sources). Request each one. Flag 404s, 410s, dead domains, and links that redirect to a homepage or a parked/for-sale page. In Claude Code use `curl -sL -m 15 -A "Mozilla/5.0" -o /dev/null -w "%{http_code} %{url_effective}" <url>`; elsewhere open the link.
   - Only links inside the article body. Ignore fonts, CDNs, scripts, analytics, social share buttons and the site's own nav.
   - 403, 429 or a timeout usually means the site blocks bots, not that the page is dead. Open it in a real browser before flagging; if it loads there, it's fine.
   - Only 404, 410, a dead domain, or a redirect to a homepage / parked page counts as broken.
2. **Outdated prices.** For each tool the page lists with a price, open that tool's own pricing page and compare. Flag only clear mismatches (different number, plan no longer exists, free plan removed or added).
3. **Dead, renamed or acquired tools.** Flag tools whose site is gone, that shut down, or that now go by another name (check the tool's own site or its official announcement).
4. **Wrong facts.** A feature, integration or limit the page states that the tool's own site or docs clearly contradict.
5. **Stale dates.** Title or intro says one year, but the content or screenshots are clearly older (e.g. "2026" in the title, prices from a plan retired in 2024).
6. **Broken page elements.** Images that don't load, empty tables, a comparison table cut off.
7. **The site's own price or plan.** On a competitor-list page, check their own product's price against their own pricing page too.
8. **Prices that only load in a browser.** If a pricing page shows no numbers to curl, open it in a real browser before giving up. If it still shows none, mark "unverifiable" and don't use it.

### Tier 2: technical blockers (proven, affect whether AI can use the page)

Run `python3 scripts/aeo_check.py <url> [<url> ...]` (in this skill's folder). It checks, for each page:

- **robots.txt blocks AI crawlers** (OAI-SearchBot, ChatGPT-User, GPTBot, PerplexityBot, ClaudeBot, Claude-SearchBot, Google-Extended). A blocked bot means that engine can't cite the page.
- **noindex**, and **article text missing from the raw HTML** (JS-rendered, so crawlers that don't run JS see an empty page).
- **No structured data, no dateModified, no author** in the JSON-LD. AI engines and Google use these for freshness and trust (E-E-A-T, AEO Bible "Trust signals").
- **Title year ahead of the last update** (title says 2026, dateModified is 2025).

### Tier 3: citation structure (suggestions, not errors)

Same script. These come from Kevin Indig's ChatGPT citation study (Growth Memo, "The science of how AI pays attention", 16 Feb 2026, 18,012 verified citations, data from Gauge) and Charles Floate's chunk/retrievability concepts (AEO Bible):

- **Intro throat-clearing** ("in this article", "in today's world"). 44.2% of ChatGPT citations come from the first 30% of the page, and cited intros open with a definitive "X is..." sentence.
- **Few question headings** (under 25% of H2s). Cited text is ~2x more likely to contain a question, and 78.4% of those come from headings.
- **No summary / key takeaways section.** Citations bump at 80 to 90% page depth when a summary sits before the footer.
- **Very long page** (over 3,000 words). Gemini used 13% of text on pages over 3,000 words vs 61% under 1,000 (DEJAN).
- **Section too long for one chunk** (an H2 section over ~600 words). OpenAI's file search cuts at 800 tokens (~600 words), so a long section gets split mid-idea.

Tier 3 is correlation from one vendor's data, so phrase it as a suggestion, never as "your page is wrong": "one thing that might help ChatGPT keep citing this page: ...". Name the source in one short clause. Use it only when tiers 1 and 2 found nothing.


Rules:

- **Proof or it doesn't count.** Every fix needs the exact thing on their page (quote or link) plus the evidence (status code, the tool's pricing page URL, the shutdown announcement). Save both in the sheet.
- Only check things you can verify right now. No opinions ("this tool is overrated"), no general SEO advice, no design feedback. The only advice allowed is tier 3, with its source.
- Never point at your own product as the fix, and never flag a competitor unfairly. If a competitor's price on the page is out of date, say so plainly, the same as for anyone else.
- Record the tier with every issue in the sheet (`fix found` starts with T1 / T2 / T3).
- If all three tiers turn up nothing, write "none found". Don't stretch a small thing into a fix. In practice almost every page has at least a tier 3 point.

## Step 4: find a real contact for each target page

Look, in this order:

1. The article itself: author name, author bio, author page.
2. Contact, About, "write for us" / "contribute" pages, footer, privacy policy, imprint.
3. `mailto:` links anywhere on those pages.

Rules:

- Only record emails you actually saw on a page, and record the URL where you saw it. Never guess a pattern (firstname@domain) and never use paid email-finder databases unless the user asks.
- Prefer the author or editor over generic inboxes. A generic inbox (hello@, contact@) is fine if it's the only one.
- No email but a contact form: record the form URL, action = "contact form" (the user fills it in by hand).
- Nothing at all: action = "skip".

## Step 5: log it in Google Sheets

Create one spreadsheet (or use the one the user gives) with two tabs.

**Setup** tab: the answers from Step 1 (prompt, product, one-liner, value, sign-off, delivery mode, connected email).

**Outreach** tab, one row per page:

| url | site | type | times cited | already mentions us | detail for email | fix found | fix evidence | contact name | email | found on | action | status | sent at | notes |

`action` = email / contact form / create profile / skip. `status` starts as "to write".

Share the sheet link with the user before writing any email.

## Step 6: write the emails

One email per row with action = email. Under 120 words, plain text, no images, no tracking. Lead with the value, not the ask. Use the real detail from Step 3.

```
Subject: {short, specific to their page, e.g. "your best AEO tools list"}

Hi {first name or "there"},

I read your "{article title}", {the specific detail, said honestly}.

I'm {your name}, I built {product}. {product one-liner}

{if a fix was found, put it first, e.g. "quick heads up: the {tool} link in your list goes to a 404 now, their pricing page moved to {new url}."}

{the value, in one or two lines. e.g. "If you update the list, here's a ready-to-paste entry (pricing, who it's for, 2 screenshots) so you don't have to dig." or "Happy to give you {free access} to test it properly, no strings. I'd value honest feedback even if it doesn't make the cut."}

{sign-off}

(If you'd rather not get emails like this, just say so and I won't follow up.)
```

Rules for every mode:

- One email per site, one person per site.
- Never ask for a link or a placement in exchange for free access. If they review or list the product after getting it free, ask them to disclose that.
- Never invent stats, customers or results.

## Step 7: deliver, based on the mode the user picked

Safety limits for all modes: max 20 emails a day, only to emails recorded in Step 4, never to anyone with status "opted out" or "not interested".

**A. Drafts**
- Create each email as a Gmail draft.
- Set `status` = "drafted".
- Tell the user how many drafts are waiting and that nothing has been sent.

**B. Send after approval**
- Show the user the next batch (up to 10) right here in chat: to, subject, body.
- Wait for an explicit "send" (they can also say "send all but 3" or edit any email).
- Send only the approved ones. Set `status` = "sent", fill `sent at`.
- Repeat until the day's limit or the list is done.

**C. Send on its own**
- Before the first send, confirm once: "I'll send up to 20 emails a day from {connected email} without asking you. OK?" Only start after a clear yes.
- Send the emails, oldest-cited rows first. Set `status` = "sent", fill `sent at`.
- Skip any row where the email or the detail looks shaky; mark it "needs review" instead of sending.
- After each batch, report: how many sent, to which sites, and the sheet link.

If the Gmail connector can't send (only draft), say so and fall back to mode A.

## Step 8: follow up and track

- When the user says "check replies" (or in mode C, at the start of each new session), search Gmail for replies to the sent threads and update `status` (replied / interested / not interested / opted out / no reply).
- One follow-up only, 5 to 7 days after the first email, as a short reply in the same thread, using the same delivery mode. Never follow up with someone who said no or asked not to be emailed.
- Re-run the prompt in ChatGPT every 2 weeks and add a column with the date and whether the product was named. Answers vary, so report "named in X of 3 runs", never a single run.
