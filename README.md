# gallaz.ch/eink

Static landing page for the three e-ink-focused Android apps shipped from
`funkypitt`'s personal F-Droid repo. No JS, no build step — three files
(`index.html`, `en.html`, `style.css`).

`index.html` is French (default); `en.html` is English; both link to each
other via the header. Layout is serif, single-column, high-contrast, no
hero images — designed to look right on an e-ink browser if anyone
happens to be reading it on one.

## What's listed

- **ePub Magazine reader** — `ua.acclorite.book_story.debug`,
  source: <https://github.com/funkypitt/epub-eink-newsreader>
- **OpenLibe e-Ink Remix** — `dev.wath.openlibeextendedeinkremix`,
  source: <https://github.com/funkypitt/funky-openlib>
- **Pluralis** — `com.pluralis.pluralis`,
  source: <https://github.com/funkypitt/pluralis>

## Updating after a new release

Each app card hard-codes the current APK filename and version. When a new
APK lands in `code/fdroid-repo/repo/`, update three things in **both**
`index.html` and `en.html`:

1. The version in the `<p class="meta">` line.
2. The APK filename in the `Download APK` / `Télécharger l'APK` `href`.

The fingerprint and repo address never change.

## Deployment

The site is meant to live at `gallaz.ch/eink`. Drop these three files
under the `eink/` directory of whatever hosts `gallaz.ch` (Apache /
nginx static dir, GitHub Pages, etc.). No server-side logic required.
