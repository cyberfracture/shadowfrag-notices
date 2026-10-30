# SHADOWFRAG notices

Public JSON announcements for the SHADOWFRAG notice board.

The same file now supplies the game's **Online** server directory. The `servers`
array is curated here; changing it updates clients without a game rebuild.

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
The repository's push webhook triggers the project's `main` deploy hook. Any
push rebuilds `main`; other branches are never published. Native Git push
triggers are disabled to avoid duplicate deployments. Hook credentials live in
GitHub/Cloudflare settings only, not this repository or the game.
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

## Server directory

Each `servers` entry has `id`, `name`, `description`, `address`, `port`,
`server_name`, `trust_pem`, and `protocol`. The first entry is Shadow 1, deployed on Debian 13 with its public
connection identity supplied here. A directory listing does not claim live availability, player count or ping.

- Use a stable unique ID, up to 64 letters/digits/underscores/hyphens.
- Names are at most 80 UTF-8 bytes; descriptions at most 240.
- Use a hostname, IPv4 or unbracketed IPv6 address, plus the separate UDP port.
- `server_name` must match the server certificate; `trust_pem` is one public PEM
  CA certificate (at most 4096 bytes). Never include a private key.
- `protocol` is the native wire version, currently 44. Incompatible entries are
  visible but cannot be joined with the wrong client version.
- Array order is the display order. Up to 32 unique servers fit within the shared
  64 KiB document limit. Address/port pairs must be unique.
- Keep `servers: []` to intentionally clear the directory. Omitting `servers`
  selects the client's bundled fallback, for compatibility with old notice feeds.

Use **Refresh List** in Online to pick up a publication, or wait for the normal
five-minute refresh. Clients keep the last good list offline and include Shadow 1
as a first-launch fallback. Joining caches only the selected public CA certificate;
TLS validation remains enabled. Administrator credentials are entered separately
in the game's owner login and are never part of this publication.

Run `python3 validate.py && python3 -m unittest` before publishing. The deployment
command is unchanged: both notices and server entries are in `notices.json`.

This repository is public. Do not put credentials, private game source, or
private user information here.
