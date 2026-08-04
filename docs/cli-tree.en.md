# CLI Tree

`chatbrowser` is the browser runtime metadata CLI. It discovers browser backends, registers profiles, registers local loopback CDP endpoints, and exposes session endpoints to higher-level tools. It does not own platform-account semantics and does not install dependencies.

Importable APIs are mapped in [Interface Tree](interface-tree.md). Package boundaries are tracked in [Capability Map](capability-map.md).

## Top Level

```text
chatbrowser                  # ChatBrowser command-line entry
├── --help                   # Show CLI help and registered commands
├── --version                # Print the package version
├── doctor                   # Read-only package and dependency check
├── backend                  # Discover local browser backends
├── profile                  # Manage isolated browser profile metadata
├── connect                  # Register an existing local loopback CDP endpoint without taking ownership
├── disconnect               # Remove a local session record without closing external browsers
└── session                  # Read registered browser sessions
```

## doctor

```bash
chatbrowser doctor --output text|json
```

`doctor` is read-only. It reports the package version, ChatBrowser metadata home, `chatup` / `chatstyle` / `chatenv` dependency versions, and `installs_dependencies=false` to make the setup boundary explicit.

## backend

```text
chatbrowser backend list --output text|json
chatbrowser backend show <name> --output text|json
chatbrowser backend resolve <name> --output text|json
```

Known backend names:

- `chrome-for-testing`
- `chromium`
- `chrome`
- `edge`

These commands only inspect `PATH`; they do not install browsers. Missing backends should be handled by ChatUp or manual setup.

## profile

```text
chatbrowser profile list --output text|json
chatbrowser profile create <name> \
  [--path <profile-dir>] \
  [--backend chrome-for-testing] \
  [--label key=value] \
  [--output text|json]
chatbrowser profile show <name> --output text|json
chatbrowser profile path <name> [--kind root|downloads|logs|run]
chatbrowser profile status <name> --output text|json
```

A profile is an alias and path registration for a browser-state container. It is not a platform account. ChatBrowser stores only non-sensitive metadata: name, path, default backend, non-sensitive labels, and timestamps; sensitive label keys are rejected.

## connect / disconnect

```text
chatbrowser connect \
  --cdp-url http://127.0.0.1:9229 \
  --as-session-name <session-id> \
  [--profile <profile-name>] \
  [--output text|json]

chatbrowser disconnect <session-id> --output text|json
```

`connect` only registers an existing local loopback CDP endpoint (`http://127.0.0.1:<port>`, `http://localhost:<port>`, or IPv6 localhost; userinfo, paths, query strings, and fragments are rejected) with `owned=false`; `disconnect` removes ChatBrowser's local session record and does not close external browsers.

## session

```text
chatbrowser session list --output text|json
chatbrowser session show <session-id> --output text|json
chatbrowser session endpoint <session-id> --output text|json
```

`session endpoint` is the main integration point for upper layers such as ChatPost and Wechatsync.

## Status Contract

| Status | Meaning |
| --- | --- |
| Implemented | Command, Python function, and tests exist |
| Verified | Covered by local tests, CLI smoke, CI, or real-service practice |
| Planned | Keep only boundary notes; do not write operation tutorials before implementation |
