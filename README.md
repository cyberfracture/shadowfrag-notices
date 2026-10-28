# SHADOWFRAG notices

Public, text-only announcements for the SHADOWFRAG main menu.

Feed: https://senpai.cyberfracture.com/notices.json

## Publish a notice

Edit `notices.json` on the `main` branch. Keep the newest entry first. Give each
notice a stable, unique `id`, a real `date` in `YYYY-MM-DD` format, a `title`, a
short `summary`, and a plain-text `body`. Use `\n\n` between paragraphs. Set
`sample` to `false` for real announcements. Delete the sample entries when ready.

Run `python3 validate.py` before committing. GitHub Pages publishes the root of
`main`; no application server, database, or Worker is required. Cloudflare caches
the exact `/notices.json` URL for five minutes. The game refreshes in menus about
every five minutes with a small random delay, uses conditional requests, and
keeps its last good copy when offline. Allow for both cache intervals after an
edit. A new installation fetches immediately.

## Format and limits

- `schema_version` must be the integer `1`.
- At most 20 notices; at most 65,536 UTF-8 bytes for the entire file.
- IDs: 1–64 ASCII letters, digits, hyphens, or underscores; no duplicates.
- Titles: 1–96 bytes; summaries: 1–240 bytes; bodies: 1–4,000 bytes.
- Dates must be valid calendar dates. `sample` must be a boolean.
- Plain UTF-8 text only. No HTML, Markdown rendering, images, executable content,
  or embedded links. Control characters are forbidden except newlines in bodies.
- An invalid update is rejected as a whole; it never replaces the last good feed.

This repository is public. Never put credentials, private game code, unreleased
private information, or user data here. The game needs no GitHub or Cloudflare
credentials to read it.

## Hosting

GitHub Pages serves this repository. `CNAME` names the custom domain. Cloudflare
must proxy its DNS record after GitHub's certificate is ready, with strict TLS
to the origin. An exact-host/path Cache Rule makes JSON cacheable and sets a
300-second edge TTL. Other cyberfracture.com pages and rules are unaffected.

The repository deliberately has no custom GitHub Actions workflows.
