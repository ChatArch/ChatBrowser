# Changelog

## 0.1.4 - 2026-08-12

### Changed

- Enable the MkDocs Material emoji renderer (`pymdownx.emoji` with Material `twemoji`/`to_svg`) for the bilingual public docs site.
- Derive Preview Docs public URLs from `mkdocs.yml` `site_url` instead of duplicating the domain path.
- Harden the tag-driven Trusted Publishing workflow with package-version, default-branch, and PyPI exact-version guards.
- Add CI smoke checks for installed `chatbrowser --version` and `chatbrowser --tree`.

## 0.1.3 - 2026-08-09

### Added

- Add a top-level `chatbrowser --tree` readback path that renders the registered browser runtime CLI tree.

### Changed

- Align bilingual CLI tree docs with the runtime-registered tree and explicitly keep unimplemented launch/extension commands out of the visible tree.

## 0.1.2

### Fixed

- Reject CDP URLs containing userinfo, query strings, fragments, paths, malformed ports, or out-of-range ports before registry persistence.
- Convert malformed registry JSON into clean CLI errors instead of Python tracebacks.
- Reject sensitive profile label keys such as token, password, cookie, account, API key, auth, login, and session.
- Honor `CHATBROWSER_REGISTRY_HOME` as a direct ChatBrowser metadata root override.
- Clarify `connect --cdp-url` help as localhost HTTP only.

## 0.1.1

### Added

- Add the first real ChatBrowser runtime metadata CLI: `doctor`, `backend`, `profile`, `connect`, `disconnect`, and `session`.
- Add importable backend discovery, profile registry, session registry, path, and doctor APIs.
- Add a non-sensitive ChatEnv schema for default backend and optional registry home.
- Add tests covering CLI tree, JSON output, task-local ChatArch home, profile/session registry behavior, and UTF-8 docs/readme files.

### Changed

- Make ChatBrowser depend on `chatup>=0.2.1,<0.3.0` while keeping setup/install responsibilities in ChatUp.
- Replace scaffold documentation with the real browser runtime/profile/session boundary and CLI tree.

## 0.1.0

### Added

- Publish the initial `ChatBrowser` package identity with stable PyPI project name, Python import module, `chatbrowser` CLI entry point, and ChatEnv discovery entry point.
