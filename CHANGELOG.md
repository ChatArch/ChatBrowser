# Changelog

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
