# SHADOWFRAG notices

Public JSON announcements for the SHADOWFRAG notice board.

Edit [notices.json](notices.json) to update the announcements. The three current
entries are clearly marked samples; replace them with real news when ready.

Direct JSON URL:
https://raw.githubusercontent.com/cyberfracture/shadowfrag-notices/main/notices.json

Hosting and the `senpai.shadowfrag.com` domain will be configured manually by
the owner. This repository contains the feed, not a GitHub Pages website.

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
