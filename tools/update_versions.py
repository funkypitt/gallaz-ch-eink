#!/usr/bin/env python3
"""Met à jour les numéros de version et les liens APK de index.html / fr.html.

Sources de vérité :
  - le dépôt F-Droid personnel (https://funkypitt.github.io/fdroid-repo/repo/index-v1.json) pour les
    applications Android, identifiées par le <code>paquet</code> de leur bloc ;
  - la dernière release GitHub pour les applications distribuées par release (Clavier Plume, versions Linux).
  - la boutique Google Play : une application dont la fiche publique existe reçoit un bouton
    « Google Play » en tête de ses liens (ajouté une fois, jamais retiré par ce script).
Ne touche qu'aux versions, aux noms de fichiers APK et à ce bouton ; le texte reste tel quel.
"""
import json, os, re, sys, urllib.request

FDROID_INDEX = "https://funkypitt.github.io/fdroid-repo/repo/index-v1.json"
PAGES = ["index.html", "fr.html"]
BLOCK = re.compile(r'<article class="app"[^>]*>.*?</article>', re.S)   # [^>]* : les articles portent une ancre id=… depuis le 2026-09-21
META = re.compile(r'<p class="meta">(.*?)</p>', re.S)
PKG = re.compile(r'<code>([\w.]+)</code>')
RELEASE_LINK = re.compile(r'github\.com/funkypitt/([\w-]+)/releases/latest')
APK_HREF = re.compile(r'(fdroid-repo/repo/)[^"]+\.apk')
DESKTOP_VERSION = re.compile(r'\b(Ordinateur|Desktop|Linux) v[\w.]+')


def fetch(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def latest_release(repo, cache={}):
    if repo not in cache:
        headers = {"Accept": "application/vnd.github+json"}
        if os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
        try:
            tag = json.loads(fetch(f"https://api.github.com/repos/funkypitt/{repo}/releases/latest", headers))["tag_name"]
            cache[repo] = tag.lstrip("v")
        except Exception as e:  # pas de release : on laisse la page telle quelle
            print(f"  (pas de release GitHub pour {repo} : {e})", file=sys.stderr)
            cache[repo] = None
    return cache[repo]


PLAY = "https://play.google.com/store/apps/details?id="
LINKS = re.compile(r'(<div class="links">\n)(\s*)')


def on_play(pkg, cache={}):
    """La fiche publique de la boutique existe-t-elle ? (200 : oui ; 404 ou panne : non, on réessaiera demain)"""
    if pkg not in cache:
        try:
            req = urllib.request.Request(PLAY + pkg + "&hl=en", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                cache[pkg] = r.status == 200
        except Exception:
            cache[pkg] = False
    return cache[pkg]


def display(version_name):
    return version_name.split("-")[0]          # « 0.2.24-magazine » s'affiche « 0.2.24 »


def update_block(block, fdroid):
    m = META.search(block)
    if not m:
        return block
    meta = m.group(1)
    new_meta, new_block = meta, block
    pkg = PKG.search(meta)
    if pkg and pkg.group(1) in fdroid:
        ver, apk = fdroid[pkg.group(1)]
        shown = display(ver)
        if "Android v" in new_meta:
            new_meta = re.sub(r"Android v[\w.]+", f"Android v{shown}", new_meta, count=1)
        else:
            new_meta = re.sub(r"\bv\d[\w.]*", f"v{shown}", new_meta, count=1)
        new_block = APK_HREF.sub(lambda mm: mm.group(1) + apk, new_block)
    if pkg and PLAY + pkg.group(1) not in new_block and on_play(pkg.group(1)):
        new_block = LINKS.sub(lambda mm: f'{mm.group(1)}{mm.group(2)}<a class="btn" href="{PLAY}{pkg.group(1)}">Google Play</a>\n{mm.group(2)}', new_block, count=1)
    for repo in RELEASE_LINK.findall(block):
        tag = latest_release(repo)
        if not tag:
            continue
        desktop = DESKTOP_VERSION.search(new_meta)          # « Ordinateur v1.2.0 » (fr), « Desktop v1.2.0 » (en), « Linux v… » d'avant
        if desktop:
            new_meta = new_meta.replace(desktop.group(0), f"{desktop.group(1)} v{tag}", 1)
        elif not (pkg and pkg.group(1) in fdroid):        # application distribuée par release seule (Clavier Plume)
            new_meta = re.sub(r"\bv\d[\w.]*", f"v{tag}", new_meta, count=1)
    if new_meta != meta:
        new_block = new_block.replace(f'<p class="meta">{meta}</p>', f'<p class="meta">{new_meta}</p>', 1)
    return new_block


def main():
    index = json.loads(fetch(FDROID_INDEX))
    fdroid = {pkg: (v[0]["versionName"], v[0]["apkName"]) for pkg, v in index["packages"].items() if v}
    changed = False
    for page in PAGES:
        text = open(page, encoding="utf-8").read()
        new = BLOCK.sub(lambda m: update_block(m.group(0), fdroid), text)
        if new != text:
            open(page, "w", encoding="utf-8").write(new)
            changed = True
            for a, b in zip(text.splitlines(), new.splitlines()):
                if a != b:
                    print(f"{page}: {a.strip()}\n{' ' * len(page)}→ {b.strip()}")
    print("modifié" if changed else "rien à changer")


if __name__ == "__main__":
    main()
