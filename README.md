# SHADOWFRAG notices

Public JSON announcements for the SHADOWFRAG notice board.

Edit [notices.json](notices.json) to update the announcements. The three current
entries are clearly marked samples; replace them with real news when ready.

Direct JSON URL:
https://raw.githubusercontent.com/cyberfracture/shadowfrag-notices/main/notices.json

The feed is hosted by Cloudflare Pages under the project `shadowfrag-notices`.
Its intended public address is https://senpai.shadowfrag.com/notices.json.
The project is connected to this repository's `main` branch; GitHub Pages is not
used. The domain requires a DNS CNAME for `senpai` pointing to
`shadowfrag-notices.pages.dev` in the `shadowfrag.com` zone.

## Deployment

Cloudflare validates the feed, then publishes only `notices.json`. The configured
command is `python3 validate.py && mkdir -p public && cp notices.json public/`;
the output directory is `public`. No framework or Pages Functions are needed.
Cloudflare Pages supplies its built-in static-asset caching and ETag validation.
Do not add a separate cache-everything rule; it can delay new announcements.

The game checks in menus roughly every five minutes with a small random delay,
uses conditional requests, and retains its last valid feed when offline.

## Editing

Keep the newest notice first. Each notice has a unique `id`, `date` in
`YYYY-MM-DD` format, `title`, `summary`, plain-text `body`, and boolean `sample`.
Use `\n\n` for paragraph breaks. Set `sample` to `false` for real news.

Run `python3 validate.py` before publishing. The game accepts schema version 1,
at most 20 notices, and at most 64 KiB of JSON. Titles are limited to 96 UTF-8
bytes, summaries to 240, and bodies to 4,000. No HTML or executable content is
rendered. Invalid updates do not replace the game's last good feed.

This repository is public. Do not put credentials, private game source, or
private user information here.
