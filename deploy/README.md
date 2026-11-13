# MV33 server deployment

Public URL: https://mv33.par73e.cn/ . First deployment: 2026-11-13 (Asia/Shanghai).

## Runtime

Nginx serves the built `public/` directory. No Node/Python process, application database or new listening port is required. The domain has its own `/etc/nginx/conf.d/mv33.conf`; source template: `deploy/mv33.nginx.conf`. Existing application vhosts were preserved.

- Current symlink: `/opt/mv33/current`
- First published release: `/opt/mv33/releases/20261113-published`
- Initial upload retained: `/opt/mv33/releases/20261113-first-release` (includes harmless macOS archive metadata; the published copy excludes it)
- File inventory: `/opt/mv33/releases/20261113-first-release.files.json`
- 611 runtime files; SHA-256 inventory hash: `f19ca2b81fb645cfadc6b4a6e1945b1e5f8d22040b0a0112d68b05ec3e7b040f`
- TLS lineage: `/etc/letsencrypt/live/mv33.par73e.cn/`; initial expiry 2027-02-11.
- Renewal: enabled `certbot.timer`, HTTP webroot `/var/www/site-acme`, existing deploy hook `asrobot-nginx-reload` checks and reloads Nginx. The hook is generic despite its historic name. A renewal dry-run was not performed.
- HTML/JS/CSS revalidate (`no-cache`); WASM and GLB use a seven-day cache. Their MIME types are explicitly set. Unknown routes return 404, without an SPA fallback.

## Updating

Review the checkout and build only when necessary; ordinary deployment can reuse reviewed, built outputs. Package `public/` only, never the entire repository or local source models. On macOS disable AppleDouble metadata, for example `COPYFILE_DISABLE=1 tar --no-xattrs --no-mac-metadata -czf RELEASE.tar.gz -C public .`. Record a sorted file checksum manifest outside the public root.

Upload to a new dated version directory; verify every file checksum and permissions (directories 755, files 644). Change `current` with a prepared symlink and atomic rename only after checks. Static version switches do not require an Nginx reload. For vhost changes, save the prior config, run `nginx -t`, then reload; do not restart unrelated applications. Verify HTTPS, routes, font/WASM/GLB MIME types and the actual browser scene.

Rollback to a retained approved release by atomically repointing `current`. First public publication has no earlier distinct live release to restore; the initial upload is the same frontend bytes. Retain releases until cleanup is separately authorized.

## Evidence

First deployment verified all 611 uploaded runtime checksums, HTTPS certificate validation, HTTP→HTTPS 308, HTML routes, `application/wasm` and `model/gltf-binary`, and live homepage rendering with `window.landoGL` present and completed loader. Existing AURORA and AS Robot root redirects still returned 302; Nginx stayed active. These are smoke checks, not full regression tests of those applications. Frontend design limitations and local device testing remain in `docs/research/`.
