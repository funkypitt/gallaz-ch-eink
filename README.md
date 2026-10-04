# gallaz.ch/eink

Static page for the apps, two languages, no build step: `index.html` (English, the default),
`fr.html` (French), `en.html` (a redirect kept for old links), `style.css`, `img/`, `manual/`.

The look (since 2026-10-04): the apps are black-and-white screens full of words, so the page is
the pale paper around them — a hero with four real phone screenshots stepped down the right, a
sticky rail of sections on the left, each app a row of words with its screens beside them (under
them when a desktop window is shown), one accent colour for what can be clicked, light and dark
themes. One typeface, Atkinson Hyperlegible (Google Fonts), chosen because it was drawn for
low-vision readers. No JavaScript. `tools/restyle.py` is the one-off script that produced the
markup from the previous single-column version, kept for the record.

## What's listed, in this order

1. **Getting the apps** (`#get`): Reader's Installer and Updater first (card `#readers-installer`,
   direct APK link, three steps), then the three other ways (`#fdroid`, `#obtainium`, `#apk`).
2. **The Reader's family** (`#readers`): one card per app, in the order of the installer's list.
   `tool/make_catalog.py` of the installer reads this section: each card's Obtainium link gives the
   app's id and name, and a download button starting with "Windows", "macOS" or "Linux" gives its
   desktop link.
3. **Also in the installer** (`#also`): ePub Magazine Reader, Le dictionnaire Littré, Clavier Plume,
   Funky's 2P Games.
4. **On the desktop** (`#desktop`): the apt repository, and the first opening on Windows and macOS.
5. **Other projects**, not in the installer's list: meditation (`#meditation`), Chrome extensions
   (`#extensions`), e-ink on the ThinkBook Plus (`#thinkbook`).

An app added to the installer's list gets its card in section 2 or 3, in both languages.

## Updating after a new release

Each app card hard-codes the current APK filename and version. When a new
APK lands in `code/fdroid-repo/repo/`, update three things in **both**
`index.html` and `fr.html`:

1. The version in the `<p class="meta">` line.
2. The APK filename in the `Download APK` / `Télécharger l'APK` `href`.

The fingerprint and repo address never change.

## Deployment

The site is meant to live at `gallaz.ch/eink`. Drop these three files
under the `eink/` directory of whatever hosts `gallaz.ch` (Apache /
nginx static dir, GitHub Pages, etc.). No server-side logic required.

## Versions automatiques

`tools/update_versions.py` relit le dépôt F-Droid (`index-v1.json`) et les releases GitHub, et réécrit les
numéros de version et les liens APK des blocs `<article class="app">` (le paquet dans `<code>` sert de clé).
Le workflow `update-versions.yml` le lance chaque jour, à la main (`gh workflow run update-versions.yml`),
ou sur `repository_dispatch` (`app-updated`) ; il committe sur `main`, ce qui redéploie GitHub Pages.
`redirect-gallaz.ch/` contient la redirection à déposer une dernière fois par FTP sur gallaz.ch/eink.
