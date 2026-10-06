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
   - **A fix for their page**: a broken link, outdated price or dead tool you spotted on their list (only if you actually found one).
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
- **competitor**: page owned by a tool on the list. Skip, they won't add you.
- **platform**: G2, Capterra, Reddit, YouTube, Product Hunt etc. Not an email target; action = "create profile / post".
- **other**: skip unless the user says otherwise.

Open each list page, note if the product is already mentioned, and note one specific detail for the email (a tool they reviewed, how they tested, when they last updated it, anything broken or outdated).

## Step 4: find a real contact for each "list" page

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

| url | site | type | times cited | already mentions us | detail for email | contact name | email | found on | action | status | sent at | notes |

`action` = email / contact form / create profile / skip. `status` starts as "to write".

Share the sheet link with the user before writing any email.

## Step 6: write the emails

One email per row with action = email. Under 120 words, plain text, no images, no tracking. Lead with the value, not the ask. Use the real detail from Step 3.

```
Subject: {short, specific to their page, e.g. "your best AEO tools list"}

Hi {first name or "there"},

I read your "{article title}", {the specific detail, said honestly}.

I'm {your name}, I built {product}. {product one-liner}

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
