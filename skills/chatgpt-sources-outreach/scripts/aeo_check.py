#!/usr/bin/env python3
"""AI-citation checks for one or more article URLs (Step 3b, tiers 2 and 3).

Usage: python3 aeo_check.py URL [URL ...] > findings.json

Every finding carries the evidence (what was seen on the page), so it can be
quoted in an email. Sources for the thresholds are in SKILL.md, Step 3b.
"""
import json
import re
import sys
import urllib.robotparser
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
AI_BOTS = ["OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "ClaudeBot", "Claude-SearchBot", "Google-Extended"]
THROAT = re.compile(r"\b(in this (article|post|guide)|in today'?s|we will (discuss|explore|cover)|let'?s dive|when it comes to)\b", re.I)
SUMMARY = re.compile(r"(summary|key takeaways?|tl;?dr|bottom line|verdict|conclusion|final thoughts|faq|frequently asked)", re.I)
YEAR = re.compile(r"\b(20[2-3]\d)\b")


def words(text):
    return len(text.split())


def robots_blocks(url):
    p = urlparse(url)
    rp = urllib.robotparser.RobotFileParser()
    try:
        r = requests.get(f"{p.scheme}://{p.netloc}/robots.txt", headers={"User-Agent": UA}, timeout=15)
        if r.status_code != 200:
            return []
        rp.parse(r.text.splitlines())
    except requests.RequestException:
        return []
    return [b for b in AI_BOTS if not rp.can_fetch(b, url)]


def jsonld(soup):
    items = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
        except (json.JSONDecodeError, TypeError):
            continue
        stack = data if isinstance(data, list) else [data]
        while stack:
            d = stack.pop()
            if isinstance(d, dict):
                items.append(d)
                stack.extend(d.get("@graph", []))
            elif isinstance(d, list):
                stack.extend(d)
    return items


def check(url):
    out = {"url": url, "findings": [], "facts": {}}
    add = lambda tier, issue, evidence: out["findings"].append({"tier": tier, "issue": issue, "evidence": evidence})
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=20)
    except requests.RequestException as e:
        out["error"] = str(e)
        return out
    out["facts"]["status"] = r.status_code
    soup = BeautifulSoup(r.text, "html.parser")
    for t in soup(["script", "style", "noscript", "svg"]):
        if t.name != "script" or t.get("type") != "application/ld+json":
            t.decompose()
    ld = jsonld(soup)
    body = soup.find("article") or soup.find("main") or soup.body or soup
    for t in body.find_all(["nav", "footer", "aside", "form"]):
        t.decompose()
    text = body.get_text(" ", strip=True)
    wc = words(text)
    out["facts"]["words"] = wc

    # Tier 2: technical blockers
    blocked = robots_blocks(url)
    if blocked:
        add(2, "robots.txt blocks AI crawlers", f"robots.txt disallows this page for: {', '.join(blocked)}")
    robots_meta = soup.find("meta", attrs={"name": re.compile("^robots$", re.I)})
    if robots_meta and "noindex" in (robots_meta.get("content") or "").lower():
        add(2, "page is noindex", f'<meta name="robots" content="{robots_meta.get("content")}">')
    if wc < 250:
        add(2, "article text missing from raw HTML (JS-rendered)", f"only {wc} words of article text in the HTML a crawler receives")
        return out
    types = sorted({str(t) for d in ld for t in (d.get("@type") if isinstance(d.get("@type"), list) else [d.get("@type")]) if t})
    out["facts"]["schema_types"] = types
    if not ld:
        add(2, "no structured data", "no JSON-LD on the page (no Article / ItemList schema)")
    modified = next((d.get("dateModified") for d in ld if d.get("dateModified")), None)
    out["facts"]["dateModified"] = modified
    if ld and not modified:
        add(2, "no dateModified in schema", f"schema types present: {', '.join(types)}; none has dateModified")
    if ld and not any(d.get("author") for d in ld):
        add(2, "no author in schema", "no author on any JSON-LD item (trust signal for E-E-A-T)")
    title = (soup.title.string or "").strip() if soup.title else ""
    out["facts"]["title"] = title
    ty = YEAR.search(title)
    if ty and modified and modified[:4] < ty.group(1):
        add(2, "title year ahead of last update", f'title says {ty.group(1)}, dateModified is {modified[:10]}')

    # Tier 3: Kevin Indig citation structure (ChatGPT, 18,012 citations)
    paras = [p.get_text(" ", strip=True) for p in body.find_all("p") if words(p.get_text(" ", strip=True)) >= 8]
    if paras:
        first = re.split(r"(?<=[.!?])\s", paras[0])[0]
        out["facts"]["first_sentence"] = first
        intro = " ".join(paras[:3])
        m = THROAT.search(intro)
        if m:
            add(3, "intro throat-clearing", f'intro says "{m.group(0)}": "{first[:160]}"')
    h2s = [h.get_text(" ", strip=True) for h in body.find_all("h2")]
    out["facts"]["h2_count"] = len(h2s)
    if len(h2s) >= 4:
        q = [h for h in h2s if h.endswith("?")]
        if len(q) / len(h2s) < 0.25:
            add(3, "few question headings", f"{len(q)} of {len(h2s)} H2s are questions, e.g. \"{h2s[0][:80]}\"")
    heads = [h.get_text(" ", strip=True) for h in body.find_all(["h2", "h3"])]
    if heads and not any(SUMMARY.search(h) for h in heads):
        add(3, "no summary / key takeaways section", f"none of the {len(heads)} H2/H3 headings is a summary, takeaways, verdict or FAQ")
    if wc > 3000:
        add(3, "very long page", f"{wc} words; Gemini used 13% of text on pages over 3,000 words vs 61% under 1,000 (DEJAN)")
    sections, cur = [], 0
    for el in body.find_all(["h2", "p", "li"]):
        if el.name == "h2":
            sections.append(cur)
            cur = 0
        else:
            cur += words(el.get_text(" ", strip=True))
    sections.append(cur)
    longest = max(sections) if sections else 0
    if longest > 600:
        add(3, "section too long for one chunk", f"longest H2 section is ~{longest} words; one retrieval chunk is ~600 words (OpenAI 800 tokens)")
    return out


if __name__ == "__main__":
    print(json.dumps([check(u) for u in sys.argv[1:]], indent=1, ensure_ascii=False))
