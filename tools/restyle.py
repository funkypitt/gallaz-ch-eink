#!/usr/bin/env python3
"""One-off transformation of index.html / fr.html to the 2026-10 layout (kept for the record).
The parsers (tools/update_versions.py, the installer's make_catalog.py) still find what they need:
<article class="app" id=…>, <p class="meta"> with <code>pkg</code> and the version words, the
APK and release links, obtainium:// links inside #readers."""
import re, sys

T = {
 "index.html": dict(
   lang="en", wordmark="gallaz.ch",
   nav=[("#get","Get the apps"),("#readers","Reader's"),("#desktop","Desktop"),("#others","Other projects")],
   cta_primary=("#get","Get the installer"), cta_second=("#readers","See the apps"),
   rail_title="On this page", active="EN"),
 "fr.html": dict(
   lang="fr", wordmark="gallaz.ch",
   nav=[("#get","Obtenir les apps"),("#readers","Reader's"),("#desktop","Ordinateur"),("#others","Autres projets")],
   cta_primary=("#get","Obtenir l’installateur"), cta_second=("#readers","Voir les applications"),
   rail_title="Sur cette page", active="FR"),
}
PHONES = ["com.freedomfighter.readerslauncher-1", "com.freedomfighter.readersnotes-1",
          "com.freedomfighter.readerscalendar-1", "com.freedomfighter.readerstasks-1"]

def transform(page, t):
    s = open(page, encoding="utf-8").read()
    # fonts
    s = s.replace('<link rel="stylesheet" href="style.css">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;500;700&family=Atkinson+Hyperlegible+Mono&display=swap">\n'
        '<link rel="stylesheet" href="style.css">')
    # header
    nav = "".join(f'    <a href="{h}">{l}</a>\n' for h, l in t["nav"])
    langs = '    <a href="fr.html"%s>FR</a>\n    <a href="index.html"%s>EN</a>\n' % (
        ' class="active"' if t["active"] == "FR" else "", ' class="active"' if t["active"] == "EN" else "")
    s = re.sub(r'<header class="site">.*?</header>',
        '<header class="site">\n  <p class="title"><a href="%s">%s</a></p>\n  <nav>\n%s%s  </nav>\n</header>' % (
            page, t["wordmark"], nav, langs), s, count=1, flags=re.S)
    # hero: h1 + lede + the two toc lines → hero block; the first toc feeds the rail
    m = re.search(r'<h1>(.*?)</h1>\s*<p class="lede">(.*?)</p>\s*<p class="toc">(.*?)</p>\s*<p class="toc">(.*?)</p>', s, re.S)
    assert m, page
    h1, lede, toc, manual = m.groups()
    rail_links = re.findall(r'<a href="(#[^"]+)">([^<]+)</a>', toc)
    phones = "".join(f'<img src="img/{p}.png" alt="" width="260" height="462">' for p in PHONES)
    hero = ('<section class="hero">\n  <div>\n    <h1>%s</h1>\n    <p class="lede">%s</p>\n'
            '    <p class="cta"><a class="btn primary" href="%s">%s</a> <a class="btn" href="%s">%s</a></p>\n'
            '    <p class="manual">%s</p>\n  </div>\n  <p class="phones">%s</p>\n</section>\n\n'
            '<div class="layout">\n<nav class="rail" aria-label="%s">\n  <ol>\n%s  </ol>\n</nav>\n<div class="content">') % (
            h1, lede, t["cta_primary"][0], t["cta_primary"][1], t["cta_second"][0], t["cta_second"][1],
            manual, phones, t["rail_title"], "".join(f'    <li><a href="{h}">{l}</a></li>\n' for h, l in rail_links))
    s = s[:m.start()] + hero + s[m.end():]
    s = s.replace("\n<footer class=\"site\">", "\n</div>\n</div>\n\n<footer class=\"site\">", 1)
    # articles: words in .text, screens beside them; meta as spaced items
    def article(m):
        a = m.group(0)
        shots = re.search(r'\s*<p class="shots">.*?</p>', a, re.S)
        body = a
        if shots:
            body = a[:shots.start()] + a[shots.end():]
        head, inner, tail = re.match(r'(<article class="app"[^>]*>)(.*)(</article>)', body, re.S).groups()
        inner = re.sub(r'<p class="meta">(.*?)</p>', lambda mm: '<p class="meta">' + "".join(
            x if x.startswith("<code>") else f"<span>{x}</span>" for x in mm.group(1).split(" · ")) + '</p>', inner, count=1, flags=re.S)
        out = head + '\n    <div class="text">' + inner.rstrip() + '\n    </div>'
        if shots:
            out += "\n    " + shots.group(0).strip()
        return out + "\n  " + tail
    s = re.sub(r'<article class="app"[^>]*>.*?</article>', article, s, flags=re.S)
    # the three other ways side by side; the steps numbered
    s = re.sub(r'(<section class="way" id="fdroid">.*?</section>\s*<section class="way" id="obtainium">.*?</section>\s*<section class="way" id="apk">.*?</section>)',
               r'<div class="ways">\n\1\n  </div>', s, count=1, flags=re.S)
    s = s.replace('<section class="way" id="steps">\n    <h3>', '<section class="way" id="steps">\n    <h3>', 1)
    s = re.sub(r'(<section class="way" id="steps">\s*<h3>.*?</h3>\s*)<ol>', r'\1<ol class="steps">', s, count=1, flags=re.S)
    open(page, "w", encoding="utf-8").write(s)
    print(page, "ok")

for page, t in T.items():
    transform(page, t)
