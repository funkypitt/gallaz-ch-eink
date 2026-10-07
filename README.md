# gallaz.ch/apps

The page of the apps written with Claude Code, for Android, the desktop and the browser. Two
languages, no build step: `index.html` (English, the default), `fr.html` (French), `en.html`
(a redirect kept for old links), `style.css`, `img/`, `manual/`.

The public address is `gallaz.ch/apps`, a 301 to this repository's GitHub Pages site
(https://funkypitt.github.io/gallaz-ch-eink/). `gallaz.ch/eink`, the address until October 2026,
redirects to the same place and keeps the old links alive (the app READMEs and the F-Droid
metadata still point at it). `redirect-gallaz.ch/` holds the two redirections (`eink/` and
`apps/`), dropped once by FTP on gallaz.ch; nothing else ever goes through FTP.

The look (since 2026-10-04): the apps are black-and-white screens full of words, so the page is
the pale paper around them — a hero with four real phone screenshots stepped down the right, a
sticky rail of sections on the left, each app a row of words with its screens beside them (under
them when a desktop window is shown), one accent colour for what can be clicked, light and dark
themes. One typeface, Atkinson Hyperlegible (Google Fonts), chosen because it was drawn for
low-vision readers. No JavaScript. `tools/restyle.py` is the one-off script that produced the
markup from the previous single-column version, kept for the record.

## What's listed, in this order

Everything public and of use beyond the author's circle, in both languages, each project linked
to its GitHub repository and to wherever else it is distributed (the F-Droid repository, GitHub
releases, the apt repository, PyPI).

1. **Getting the apps** (`#get`): Reader's Installer and Updater first (card `#readers-installer`,
   direct APK link, three steps), then the three other ways (`#fdroid`, `#obtainium`, `#apk`).
2. **The Reader's family** (`#readers`): one card per app, in the order of the installer's list.
   `tool/make_catalog.py` of the installer reads this section: each card's Obtainium link gives the
   app's id and name, and a download button starting with "Windows", "macOS" or "Linux" gives its
   desktop link.
3. **Also in the installer** (`#also`): ePub Magazine Reader, Le dictionnaire Littré, Clavier Plume,
   Funky's 2P Games.
4. **Meditation and breathing** (`#meditation`): Retreat Timer, Player, Walk, 4 Minutes Breathing.
5. **More Android apps** (`#android`): MP4 Remixer, MP4 to MP3, Timer for 9Barista, Tank Wars Mobile.
6. **On the desktop** (`#desktop`): Reader's Night Filter for the desktop and the browser, the apt
   repository, the first opening on Windows and macOS.
7. **Tools for the computer** (`#tools`): the traduction toolkit, Quai, epub2md.
8. **Browser extensions** (`#extensions`): PageTurn, Social Media Blocker.
9. **E-ink on the ThinkBook Plus** (`#thinkbook`): Tinta4PlusU, eInk Reader.
10. **More on GitHub** (`#more`): one line each for the smaller public projects.

E-ink is no longer the frame of the page; it is mentioned on the cards where it matters (Books,
Feeds, PageTurn, the ThinkBook tools). An app added to the installer's list gets its card in
section 2 or 3, in both languages; any other public project gets a card in the section of its
platform, or a line in section 10.

## Versions

`tools/update_versions.py` reads the F-Droid repository (`index-v1.json`) and the GitHub releases
and rewrites the version numbers and APK links of the `<article class="app">` blocks (the package
in `<code>` is the key; a `releases/latest` link gives the desktop or release-only version). The
`update-versions.yml` workflow runs it every day, by hand (`gh workflow run update-versions.yml`)
or on `repository_dispatch` (`app-updated`); it commits on `main`, which redeploys GitHub Pages.
