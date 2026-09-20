# gallaz.ch/eink

Static landing page for the three e-ink-focused Android apps shipped from
`funkypitt`'s personal F-Droid repo. No JS, no build step — three files
(`index.html`, `fr.html`, `en.html`, `style.css`).

`index.html` is English (the default); `fr.html` is French; `en.html` only redirects
to the home page, so links shared before the switch keep working. Both pages link to each
other via the header. Layout is serif, single-column, high-contrast, no
hero images — designed to look right on an e-ink browser if anyone
happens to be reading it on one.

## What's listed

**Reader's family** (section `#readers`, both languages): Reader's Launcher, Calendar (Android + Linux), Tasks (Android + Linux), Notes, Books, Feeds — sources under `github.com/funkypitt/readers-*`, APKs from the F-Droid repo, Linux packages from each desktop repo's latest release.

**Meditation** (section `#meditation`): Retreat Timer, Retreat Player, Retreat Walk — `github.com/funkypitt/retreat-*`.

**Other apps**

- **ePub Magazine reader** — `com.freedomfighter.magazinereader`,
  source: <https://github.com/funkypitt/funky-openlib>
- **Pluralis** — `com.pluralis.pluralis`,
  source: <https://github.com/funkypitt/pluralis>

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
