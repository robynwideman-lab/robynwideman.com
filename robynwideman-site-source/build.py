#!/usr/bin/env python3
"""Static site generator for robynwideman.com.
Edit data/books.json, run `python3 build.py`, commit. Output goes to ./public.
"""
import json, os, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "data" / "books.json").read_text())
SITE = DATA["site"]
OUT = ROOT / "public"

CSS = r"""
:root{
  --bg:#f4efe3;--bg2:#fbf8f1;--ink:#1b2130;--muted:#5c6270;--line:#d9d2c2;
  --accent:#b8731d;--accent-ink:#1b2130;--accent2:#2f7a6d;--shadow:0 12px 30px rgba(27,33,48,.18);
  color-scheme:light;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#12161f;--bg2:#1a2030;--ink:#ece5d3;--muted:#9aa0b0;--line:#2a3142;
  --accent:#e0973b;--accent-ink:#12161f;--accent2:#5fb3a2;--shadow:0 16px 40px rgba(0,0,0,.45);
  color-scheme:dark;}}
:root[data-theme="dark"]{
  --bg:#12161f;--bg2:#1a2030;--ink:#ece5d3;--muted:#9aa0b0;--line:#2a3142;
  --accent:#e0973b;--accent-ink:#12161f;--accent2:#5fb3a2;--shadow:0 16px 40px rgba(0,0,0,.45);
  color-scheme:dark;}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Source Serif 4",Georgia,"Times New Roman",serif;font-size:18px;line-height:1.6;padding-inline:clamp(16px,4vw,40px)}
a{color:inherit}
img{max-width:100%;display:block}
h1,h2,h3{font-family:"Cormorant Garamond",Georgia,serif;font-weight:700;line-height:1.05;margin:0;text-wrap:balance;letter-spacing:-.01em}
h1{font-size:clamp(2.3rem,5.2vw,4rem)}
h2{font-size:clamp(1.9rem,4vw,3rem)}
h3{font-size:1.5rem}
p{margin:0;max-width:62ch}
.eyebrow{font-family:Cinzel,"Cormorant Garamond",serif;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.wrap{max-width:1180px;margin-inline:auto}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-block:22px;border-bottom:1px solid var(--line)}
.brand{font-family:Cinzel,serif;font-size:1.05rem;letter-spacing:.16em;text-transform:uppercase;text-decoration:none}
.nav ul{list-style:none;margin:0;padding:0;display:flex;gap:6px 22px;flex-wrap:wrap;font-size:.95rem}
.nav a{text-decoration:none;color:var(--muted)} .nav a:hover,.nav a[aria-current]{color:var(--ink)}
.btn{display:inline-flex;align-items:center;gap:.5em;padding:.8em 1.4em;border-radius:6px;text-decoration:none;font-weight:600;font-size:1rem;border:1px solid transparent;line-height:1.1}
.btn-primary{background:var(--accent);color:var(--accent-ink)}
.btn-ghost{border-color:var(--line);color:var(--ink)}
.btn:focus-visible,a:focus-visible{outline:2px solid var(--accent2);outline-offset:3px}
.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;padding-block:clamp(40px,7vw,90px)}
.hero p.lede{font-size:1.25rem;color:var(--muted);margin-top:18px}
.hero .cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.stack{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;transform:rotate(-2deg)}
.stack img{border-radius:4px;box-shadow:var(--shadow);aspect-ratio:2/3;object-fit:cover;width:100%}
.stack img:nth-child(2){transform:translateY(-18px)}
section{padding-block:clamp(36px,6vw,72px);border-top:1px solid var(--line)}
.shelf-head{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;margin-bottom:26px}
.shelf-head p{color:var(--muted);margin-top:8px}
.shelf{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:22px 16px}
.book{display:flex;flex-direction:column;gap:8px;text-decoration:none}
.book img{aspect-ratio:2/3;object-fit:cover;width:100%;border-radius:3px;box-shadow:var(--shadow);background:var(--bg2)}
.book .n{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.72rem;color:var(--muted);letter-spacing:.06em}
.book .t{font-weight:600;line-height:1.25;font-size:.98rem}
.book.first img{outline:2px solid var(--accent);outline-offset:3px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.free{display:grid;grid-template-columns:repeat(2,1fr);gap:28px}
.free article{display:grid;grid-template-columns:120px 1fr;gap:18px;align-items:center}
.free img{aspect-ratio:2/3;object-fit:cover;border-radius:3px;box-shadow:var(--shadow)}
.free .t{font-family:"Cormorant Garamond",serif;font-size:1.5rem;font-weight:700;line-height:1.1}
.free p{color:var(--muted);font-size:.95rem;margin-top:6px}
.sys{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.82rem;border:1px solid var(--accent2);color:var(--accent2);padding:12px 14px;border-radius:4px;max-width:34ch;line-height:1.5}
.sys b{color:var(--ink);font-weight:600}
footer{border-top:1px solid var(--line);padding-block:36px;color:var(--muted);font-size:.9rem;display:grid;gap:14px}
footer .row{display:flex;gap:8px 24px;flex-wrap:wrap}
footer a{color:var(--muted)}
.field{display:grid;gap:6px;margin-bottom:16px}
.field label{font-size:.9rem;color:var(--muted)}
input,textarea{font:inherit;padding:.7em .8em;border:1px solid var(--line);border-radius:6px;background:var(--bg2);color:var(--ink);width:100%}
textarea{min-height:160px}
/* landing pages */
.lp body{padding-inline:clamp(16px,4vw,40px)}
.lp-hero{display:grid;grid-template-columns:minmax(220px,340px) 1fr;gap:clamp(24px,5vw,64px);align-items:center;padding-block:clamp(28px,6vw,72px)}
.lp-hero img{aspect-ratio:2/3;object-fit:cover;border-radius:4px;box-shadow:var(--shadow);width:100%}
.lp-hero h1{font-size:clamp(2rem,5vw,3.8rem)}
.lp-hero .hook{font-size:1.25rem;margin-top:16px}
.lp-hero .cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px;align-items:center}
.lp-hero .rating{color:var(--muted);font-size:.92rem;margin-top:14px}
.bullets{list-style:none;padding:0;margin:0;display:grid;gap:12px;max-width:60ch}
.bullets li{padding-left:26px;position:relative}
.bullets li::before{content:"";position:absolute;left:0;top:.55em;width:12px;height:12px;background:var(--accent);clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%)}
.lp .shelf{grid-template-columns:repeat(auto-fill,minmax(120px,1fr))}
.sticky-cta{position:sticky;bottom:0;background:var(--bg2);border-top:1px solid var(--line);padding:12px clamp(16px,4vw,40px);display:flex;justify-content:space-between;align-items:center;gap:12px;margin-inline:calc(-1*clamp(16px,4vw,40px))}
.sticky-cta span{font-weight:600}
@media (max-width:760px){
  .hero,.two,.free,.lp-hero{grid-template-columns:1fr}
  .stack{transform:none}
  .lp-hero img{max-width:260px}
  .free article{grid-template-columns:96px 1fr}
  .sticky-cta span{display:none}
}
@media (prefers-reduced-motion:no-preference){.book img{transition:transform .2s}.book:hover img{transform:translateY(-4px)}}
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Cormorant+Garamond:wght@700&family=IBM+Plex+Mono:wght@400;600&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap">'

def e(s): return html.escape(s, quote=True)

def buy_url(book):
    if book.get("free_url"): return book["free_url"]
    if book.get("asin"): return f"https://www.amazon.com/dp/{book['asin']}"
    q = (book["title"] + " Robyn Wideman").replace(" ", "+")
    return f"https://www.amazon.com/s?k={q}"

def page(title, body, desc, path, current=None, landing=False, extra_head=""):
    nav = "" if landing else f"""
<header class="nav wrap">
  <a class="brand" href="/">Robyn Wideman</a>
  <nav><ul>
    <li><a href="/books/"{' aria-current="page"' if current=='books' else ''}>Books</a></li>
    <li><a href="/series/darkthorn-academy/"{' aria-current="page"' if current=='darkthorn-academy' else ''}>Darkthorn Academy</a></li>
    <li><a href="/series/new-realm-online/"{' aria-current="page"' if current=='new-realm-online' else ''}>New Realm Online</a></li>
    <li><a href="/series/stoneblood-saga/"{' aria-current="page"' if current=='stoneblood-saga' else ''}>Stoneblood Saga</a></li>
    <li><a href="/free/"{' aria-current="page"' if current=='newsletter' else ''}>Free stories</a></li>
    <li><a href="/about/"{' aria-current="page"' if current=='about' else ''}>About</a></li>
    <li><a href="/contact/"{' aria-current="page"' if current=='contact' else ''}>Contact</a></li>
  </ul></nav>
</header>"""
    sisters = " · ".join(f'<a href="{s["url"]}">{e(s["name"])}</a> ({e(s["note"])})' for s in SITE["sister_sites"])
    foot = f"""
<footer class="wrap">
  <div class="row"><span>© 2015–2026 Robyn Wideman · Magicblood Media</span></div>
  <div class="row"><span>More worlds: {sisters}</span></div>
  <div class="row"><a href="{SITE['amazon_author']}">Amazon author page</a><a href="{SITE['facebook']}">Facebook</a><a href="/free/">Free stories</a><a href="/contact/">Contact</a></div>
  <div class="row"><span>Robyn Wideman is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com.</span></div>
</footer>"""
    doc = f"""<!DOCTYPE html>
<html lang="en"{' class="lp"' if landing else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE['domain']}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{SITE['domain']}{path}"><meta property="og:site_name" content="Robyn Wideman">
{FONTS}
{extra_head}
<style>{CSS}</style>
</head>
<body>
{nav}
<main class="wrap">
{body}
</main>
{foot}
</body>
</html>"""
    dest = OUT / path.lstrip("/")
    if path.endswith("/"): dest = dest / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc)

def shelf(series, limit=None, in_landing=False):
    books = series["books"][:limit] if limit else series["books"]
    items = []
    for i, b in enumerate(books):
        cls = "book first" if b["n"] == "1" else "book"
        label = "Free" if b.get("free_url") else f"Book {b['n']}"
        items.append(f'<a class="{cls}" href="{buy_url(b)}" rel="nofollow"><img src="{b["cover"]}" alt="{e(b["title"])} cover" loading="lazy" width="300" height="450"><span class="n">{label}</span><span class="t">{e(b["title"])}</span></a>')
    return f'<div class="shelf">{"".join(items)}</div>'

def series_section(s):
    return f"""
<section id="{s['slug']}">
  <div class="shelf-head">
    <div><div class="eyebrow">{e(s['eyebrow'])}</div><h2>{e(s['name'])}</h2><p>{e(s['hook'])}</p></div>
    <div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-primary" href="{buy_url(s['books'][0] if s['books'][0]['n']=='1' else s['books'][1])}" rel="nofollow">Start with book 1</a><a class="btn btn-ghost" href="/series/{s['slug']}/">Reading order</a></div>
  </div>
  {shelf(s)}
</section>"""

# ---------- Home ----------
S = {s["slug"]: s for s in DATA["series"]}
stack = "".join(f'<img src="{S[k]["books"][i]["cover"]}" alt="" width="300" height="450">' for k,i in [("darkthorn-academy",0),("new-realm-online",0),("stoneblood-saga",1)])
home = f"""
<div class="hero">
  <div>
    <div class="eyebrow">Epic fantasy · LitRPG · Progression</div>
    <h1>Worlds where the underdog levels up.</h1>
    <p class="lede">Academy dungeons, VR kingdoms and a hidden bloodline that changes a realm. Best-selling series from Robyn Wideman, complete and ready to binge.</p>
    <div class="cta"><a class="btn btn-primary" href="/free/">Get two free stories</a><a class="btn btn-ghost" href="/books/">Browse the series</a></div>
  </div>
  <div class="stack">{stack}</div>
</div>
{series_section(S['darkthorn-academy'])}
{series_section(S['new-realm-online'])}
{series_section(S['stoneblood-saga'])}
<section>
  <div class="two">
    <div>
      <div class="eyebrow">Free to read</div>
      <h2>Two stories, on the house.</h2>
      <p style="color:var(--muted);margin-top:12px">Join the newsletter for release news, deals and giveaways, and pick up both free stories on the way in.</p>
      <div class="cta" style="margin-top:22px"><a class="btn btn-primary" href="/free/">Join and download</a></div>
    </div>
    <div class="free">
      {''.join(f'<article><img src="{f["cover"]}" alt="{e(f["title"])} cover" width="200" height="300" loading="lazy"><div><div class="t">{e(f["title"])}</div><div class="eyebrow" style="font-size:.68rem;margin-top:4px">{e(f["series"])}</div><p>{e(f["hook"])}</p></div></article>' for f in SITE["free_reads"])}
    </div>
  </div>
</section>
"""
page("Robyn Wideman", home, SITE["tagline"], "/", current="home")

# ---------- Books ----------
books_body = f"""
<div style="padding-block:clamp(32px,5vw,64px)">
  <div class="eyebrow">Reading order</div>
  <h1>All the series, in order.</h1>
  <p class="lede" style="color:var(--muted);margin-top:14px">Every series is complete or in active release. Book 1 is outlined in gold; start there.</p>
</div>
{''.join(series_section(s) for s in DATA['series'])}
"""
page("Books · Robyn Wideman", books_body, "Complete reading order for Darkthorn Academy, New Realm Online and the Stoneblood Saga.", "/books/", current="books")

# ---------- Series pages ----------
for s in DATA["series"]:
    b1 = s["books"][0] if s["books"][0]["n"]=="1" else s["books"][1]
    body = f"""
<div class="hero">
  <div>
    <div class="eyebrow">{e(s['eyebrow'])}</div>
    <h1>{e(s['name'])}</h1>
    <p class="lede">{e(s['hook'])}</p>
    <p style="margin-top:16px">{e(s['pitch'])}</p>
    <p style="margin-top:12px;color:var(--muted);font-size:.95rem">{e(s['readers_like'])}. {e(s['rating'])}.</p>
    <div class="cta"><a class="btn btn-primary" href="{buy_url(b1)}" rel="nofollow">Read book 1 on Amazon</a><a class="btn btn-ghost" href="{s['amazon_series']}" rel="nofollow">Whole series</a></div>
  </div>
  <div class="stack">{''.join(f'<img src="{b["cover"]}" alt="" width="300" height="450">' for b in s["books"][:3])}</div>
</div>
<section>
  <div class="shelf-head"><div><div class="eyebrow">Reading order</div><h2>{len(s['books'])} books</h2></div></div>
  <div class="shelf">{''.join(f'<a class="book{" first" if b["n"]=="1" else ""}" href="{buy_url(b)}" rel="nofollow"><img src="{b["cover"]}" alt="{e(b["title"])} cover" loading="lazy" width="300" height="450"><span class="n">{"Free" if b.get("free_url") else "Book "+b["n"]}</span><span class="t">{e(b["title"])}</span><span style="font-size:.88rem;color:var(--muted)">{e(b["tag"])}</span></a>' for b in s["books"])}</div>
</section>
"""
    page(f"{s['name']} · Robyn Wideman", body, s["hook"], f"/series/{s['slug']}/", current=s["slug"])

# ---------- Landing pages (Facebook ads) ----------
for s in DATA["series"]:
    b1 = s["books"][0] if s["books"][0]["n"]=="1" else s["books"][1]
    free = next((b for b in s["books"] if b.get("free_url")), None)
    free_btn = f'<a class="btn btn-ghost" href="{free["free_url"]}">Try the free prequel first</a>' if free else '<a class="btn btn-ghost" href="/free/">Get a free story first</a>'
    body = f"""
<div class="lp-hero">
  <img src="{b1['cover']}" alt="{e(b1['title'])} cover" width="400" height="600">
  <div>
    <div class="eyebrow">{e(s['eyebrow'])}</div>
    <h1>{e(s['landing_headline'])}</h1>
    <p class="hook">{e(s['hook'])}</p>
    <div class="cta"><a class="btn btn-primary" href="{buy_url(b1)}" rel="nofollow">Read {e(b1['title'])} on Amazon</a>{free_btn}</div>
    <p class="rating">Free in Kindle Unlimited · {e(s['rating'])}</p>
  </div>
</div>
<section>
  <div class="two">
    <div><div class="eyebrow">Why readers stay</div><h2 style="margin-bottom:18px">What you're signing up for</h2><ul class="bullets">{''.join(f'<li>{e(x)}</li>' for x in s['landing_bullets'])}</ul></div>
    <div><div class="eyebrow">The story</div><p style="margin-top:12px">{e(s['pitch'])}</p><p style="margin-top:14px;color:var(--muted);font-size:.95rem">{e(s['readers_like'])}.</p></div>
  </div>
</section>
<section>
  <div class="shelf-head"><div><div class="eyebrow">The whole run</div><h2>{len(s['books'])} books, in order</h2></div><a class="btn btn-ghost" href="{s['amazon_series']}" rel="nofollow">Series page on Amazon</a></div>
  {shelf(s)}
</section>
<div class="sticky-cta"><span>{e(s['name'])} · Book 1</span><a class="btn btn-primary" href="{buy_url(b1)}" rel="nofollow">Read on Amazon</a></div>
"""
    head = '<meta name="robots" content="noindex">'  # ad landing pages: don't compete with the series page in search
    page(f"{s['name']} — start here", body, s["landing_headline"], f"/go/{s['slug']}/", landing=True, extra_head=head)

# ---------- Free books funnel: /free/ → MailerLite → /free/thanks/ → welcome email → /free/download/<token>/ ----------
TOKEN = SITE["download_token"]
free_cards = ''.join(f'<article><img src="{f["cover"]}" alt="{e(f["title"])} cover" width="200" height="300"><div><div class="t">{e(f["title"])}</div><div class="eyebrow" style="font-size:.68rem;margin-top:4px">{e(f["series"])}</div><p>{e(f["hook"])}</p></div></article>' for f in SITE["free_reads"])
signup = f"""
<form class="ml-form" action="{SITE['newsletter_url']}" method="get" style="display:grid;gap:12px;max-width:420px;margin-top:24px">
  <!-- TODO Robyn: replace this whole <form> with the MailerLite "embedded form" HTML for form {SITE['newsletter_form_id']} (MailerLite → Forms → Embedded → copy HTML). Set the form's success redirect to {SITE['domain']}/free/thanks/ -->
  <div class="field" style="margin:0"><label for="ml-email">Email</label><input id="ml-email" type="email" name="email" placeholder="you@example.com" required></div>
  <button class="btn btn-primary" type="submit">Send me the free stories</button>
  <span style="font-size:.85rem;color:var(--muted)">Release news and deals a few times a month. Unsubscribe any time, keep the books.</span>
</form>"""
free_page = f"""
<div class="hero">
  <div>
    <div class="eyebrow">Free stories</div>
    <h1>Two free stories. One email address.</h1>
    <p class="lede">Join the newsletter and the download links land in your inbox in about a minute: a Stoneblood Saga prequel novella and a Darkthorn Academy short story, in EPUB and PDF, readable on Kindle, phone or tablet.</p>
    {signup}
    <div class="sys" style="margin-top:28px"><b>[System]</b> Quest accepted: <b>Join the Guild</b><br>Reward: 2 × story · release alerts · first look at new series</div>
  </div>
  <div class="free" style="grid-template-columns:1fr">{free_cards}</div>
</div>
"""
page("Free stories · Robyn Wideman", free_page, "Join Robyn Wideman's newsletter and get two free fantasy stories: Soron's Quest and Darkthorn Trials.", "/free/", current="newsletter")
# keep the old URL working
page("Free stories · Robyn Wideman", '<meta http-equiv="refresh" content="0;url=/free/">', "Redirecting", "/newsletter/")

thanks = f"""
<div class="hero"><div>
  <div class="eyebrow">One more step</div>
  <h1>Check your inbox.</h1>
  <p class="lede">A confirmation email is on its way. Click the link in it and the download page for both stories follows right after. Nothing there? Check spam or promotions, and add robyn@robynwideman.com to your contacts.</p>
  <div class="cta" style="margin-top:24px"><a class="btn btn-ghost" href="/books/">Browse the series while you wait</a></div>
</div></div>
"""
page("Almost there · Robyn Wideman", thanks, "Confirm your email to get the free stories.", "/free/thanks/", extra_head='<meta name="robots" content="noindex">')

dl_cards = ''.join(f"""
<article style="display:grid;grid-template-columns:140px 1fr;gap:22px;align-items:start">
  <img src="{f['cover']}" alt="{e(f['title'])} cover" width="200" height="300" style="border-radius:3px;box-shadow:var(--shadow)">
  <div>
    <div class="eyebrow">{e(f['series'])}</div>
    <h2 style="font-size:2rem">{e(f['title'])}</h2>
    <p style="color:var(--muted);margin-top:6px">{e(f['hook'])}</p>
    <div class="cta" style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px">
      <a class="btn btn-primary" href="/files/{f['file']}.epub" download>EPUB (Kindle, Kobo, Apple Books)</a>
      <a class="btn btn-ghost" href="/files/{f['file']}.pdf" download>PDF</a>
    </div>
  </div>
</article>""" for f in SITE["free_reads"])
download = f"""
<div style="padding-block:clamp(32px,5vw,64px)">
  <div class="eyebrow">Your free stories</div>
  <h1>Thanks for joining. Here they are.</h1>
  <p class="lede" style="color:var(--muted);margin-top:14px">Save this page; the links don't expire.</p>
</div>
<section style="display:grid;gap:40px">{dl_cards}</section>
<section>
  <div class="two">
    <div>
      <div class="eyebrow">Reading on a Kindle</div>
      <h2 style="font-size:1.8rem;margin-bottom:12px">Send the EPUB to your Kindle</h2>
      <p>Amazon accepts EPUB now. Easiest route: open <a href="https://www.amazon.com/sendtokindle">amazon.com/sendtokindle</a>, sign in, and drop the EPUB file on the page. It appears in your library on every Kindle device and app within a few minutes.</p>
      <p style="margin-top:10px">Or email the EPUB as an attachment to your Kindle address (find it under Amazon → Content &amp; Devices → Preferences → Personal Document Settings).</p>
    </div>
    <div>
      <div class="eyebrow">Phone, tablet, computer</div>
      <h2 style="font-size:1.8rem;margin-bottom:12px">Open the EPUB in any reader</h2>
      <p>Apple Books (iPhone, iPad, Mac): tap the EPUB and choose Books. Android: Google Play Books or Moon+ Reader. Kobo: connect by USB and copy the file, or use Kobo's Send-to-Kobo. Anything else: the PDF works everywhere.</p>
      <p style="margin-top:10px">Stuck? <a href="/contact/">Tell Robyn</a> which device you're on and you'll get a hand.</p>
    </div>
  </div>
</section>
"""
page("Your free stories · Robyn Wideman", download, "Download your free stories.", f"/free/download/{TOKEN}/", extra_head='<meta name="robots" content="noindex,nofollow">')
(OUT / "files").mkdir(exist_ok=True)
(OUT / "files" / "README.txt").write_text("Drop sorons-quest.epub, sorons-quest.pdf, darkthorn-trials.epub, darkthorn-trials.pdf here (assets/files in the repo).\n")

# ---------- About ----------
about = """
<div class="hero">
  <div>
    <div class="eyebrow">About the author</div>
    <h1>Robyn Wideman</h1>
    <p class="lede">Writer of fantasy fiction, from teen high fantasy to LitRPG and Gamelit, with a little urban fantasy and science fiction thrown in to keep things confusing.</p>
    <p style="margin-top:16px">Based in British Columbia, Canada. More than 140 published titles across three pen names, an audio partnership with Podium, and a bad habit of starting new series. When not writing, a sports junkie (Toronto Raptors) with a growing travel bug and snowbird ambitions.</p>
    <p style="margin-top:16px">Romantasy readers: the same author writes epic fantasy romance as <a href="https://www.robynwolfe.com">Robyn Wolfe</a>.</p>
  </div>
  <div><img src="https://www.robynwideman.com/uploads/5/0/3/1/50319333/covid-beard_orig.jpg" alt="Robyn Wideman" style="border-radius:6px;box-shadow:var(--shadow);max-width:380px"></div>
</div>
"""
page("About · Robyn Wideman", about, "About fantasy and LitRPG author Robyn Wideman.", "/about/", current="about")

# ---------- Contact ----------
contact = f"""
<div class="hero">
  <div>
    <div class="eyebrow">Contact</div>
    <h1>Say hello.</h1>
    <p class="lede">Reader questions, series requests, translation and audio enquiries all welcome. Robyn reads everything, and answers most of it.</p>
  </div>
  <form action="https://formspree.io/f/{SITE['formspree_id']}" method="POST">
    <div class="field"><label for="name">Name</label><input id="name" name="name" required></div>
    <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" required></div>
    <div class="field"><label for="message">Message</label><textarea id="message" name="message" required></textarea></div>
    <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
    <button class="btn btn-primary" type="submit">Send</button>
  </form>
</div>
"""
page("Contact · Robyn Wideman", contact, "Contact author Robyn Wideman.", "/contact/", current="contact")

# ---------- 404 + redirects ----------
page("Page not found · Robyn Wideman", '<div class="hero"><div><div class="eyebrow">404</div><h1>That page wandered off the map.</h1><p class="lede">Try the <a href="/books/">books</a> or head <a href="/">home</a>.</p></div></div>', "Page not found", "/404.html")
(OUT / "_redirects").write_text("""# Old Weebly URLs → new pages
/about.html            /about/                      301
/contact.html          /contact/                    301
/newsletter.html       /free/                       301
/darkthornacademy.html /series/darkthorn-academy/   301
/apocalypse.html       /books/                      301
/otherbooks.html       /books/                      301
""")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['domain']}/sitemap.xml\n")
urls = ["/", "/books/", "/free/", "/about/", "/contact/"] + [f"/series/{s['slug']}/" for s in DATA["series"]]
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{SITE['domain']}{u}</loc></url>" for u in urls) + "</urlset>\n")
shutil.copytree(ROOT/"assets", OUT/"assets", dirs_exist_ok=True)
print("built", sum(1 for _ in OUT.rglob("*.html")), "pages →", OUT)
