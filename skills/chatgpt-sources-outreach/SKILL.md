---
name: chatgpt-sources-outreach
description: Use when the user wants their product mentioned by ChatGPT for a prompt like "what is the best X tool" and asks to find the pages ChatGPT cites, find the contact emails behind those pages, log them in a Google Sheet, or draft outreach emails to those site owners. Triggers on "chatgpt sources outreach", "email the sites chatgpt reads", "find emails for these urls", "get my saas on chatgpt lists".
---

# ChatGPT sources outreach

ChatGPT answers "best tool" prompts mostly from other people's pages: listicles, comparisons and reviews. This skill finds those pages, finds a real person to email at each one, logs everything in a Google Sheet and writes a personal draft email for each site. The user reviews and sends every email themselves.

Needs: Claude Code (or Claude with web access), the Gmail connector and the Google Sheets connector.

## Step 0: ask for the inputs (once, at the start)

Ask for anything missing, in one message:

1. **The prompt** you want to show up for, e.g. "what is the best ai tool for aeo".
2. **Your product**: name, URL, and one sentence that says what it IS ("Acme is an X that does Y for Z"). Plain and definitive, no hype words.
3. **Your offer** to the site owner, e.g. "a free 3-month account in exchange for honest feedback". Keep it about feedback, never "list me and get it free".
4. **Your name + sign-off** for the emails.
5. **The source URLs**, if they already have them (CSV, sheet or pasted list). If not, do Step 1.

## Step 1: collect the pages ChatGPT reads

The user does this part in their own ChatGPT (you cannot run their account):

1. Open ChatGPT with search on, paste the prompt, send.
2. Click **Sources** under the answer. Copy every URL.
3. Run it 3 times (new chat each time, a minute apart). Answers change run to run.
4. Paste all URLs back here.

Then you: dedupe the URLs, count how many runs each one appeared in, and sort by that count (most repeated first).

## Step 2: sort the list

Give every URL a type:

- **list**: third-party "best X tools" / comparison / review page. These are the targets.
- **competitor**: page owned by a tool on the list (e.g. a vendor comparing itself). Skip, they will not add you.
- **platform**: G2, Capterra, Reddit, YouTube, Product Hunt etc. Not an email target; note "create profile / post" as the action instead.
- **other**: anything else. Skip unless the user says otherwise.

Also note if your product is already mentioned on the page (open it and search for the name).

## Step 3: find a real contact for each "list" page

For each list page, open the site and look, in this order:

1. The article itself: author name, author bio, author page.
2. Contact page, About page, "write for us" / "contribute" page, footer, privacy policy, imprint.
3. `mailto:` links anywhere on those pages.

Rules:

- Only record emails you actually saw on a page, and record the URL where you saw it. Never guess a pattern (firstname@domain) and never use paid email-finder databases unless the user asks.
- Prefer the author or editor over generic inboxes. A generic inbox (hello@, contact@) is fine if it is the only one.
- No email but a contact form: record the form URL, action = "contact form" (the user fills it in by hand).
- Nothing at all: action = "skip".

## Step 4: log it in Google Sheets

Create one sheet (or use the one the user gives) with these columns, one row per page:

| url | site | type | times cited | already mentions us | contact name | email | found on | action | status | notes |

`action` = email / contact form / create profile / skip. `status` starts as "to draft".

Share the sheet link with the user before writing any email.

## Step 5: draft the emails (drafts only, never send)

For each row with action = email, create a **Gmail draft** (not a sent email) using the template below. Personalise the first line with something real from their article (a tool they reviewed, how they tested, the date they updated it). Under 120 words. Plain text, no images, no tracking.

```
Subject: {product} for your {article topic} list?

Hi {first name or "there"},

I read your "{article title}", {one specific, honest line about it}.

I'm {your name}, I built {product}. {product one-liner}

If you ever update the list, I'd love an honest look. Happy to give you {offer} so you can test it properly, no strings, and I'd value your feedback even if it doesn't make the cut.

{sign-off}

(If you'd rather not get emails like this, just say so and I won't follow up.)
```

Rules:

- One email per site, one person per site.
- Never ask for a link or a placement in exchange for the free account. The account is for feedback. If they review or list you after using it, remind them to disclose they got it free.
- Max 20 drafts a day so the user can actually read each one before sending.
- After creating the drafts, update `status` to "drafted" and tell the user how many drafts are waiting in Gmail.

## Step 6: follow up and track

- The user sends the drafts. When they say "check replies", search Gmail for replies to those threads and update `status` (replied / interested / not interested / no reply).
- One follow-up only, 5 to 7 days later, as a short reply in the same thread. Never follow up with someone who said no.
- Re-run the prompt in ChatGPT every 2 weeks and add a column with the date and whether your product was named. Answers vary, so report "named in X of 3 runs", never a single run.
