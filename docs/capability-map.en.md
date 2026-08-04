# Capability Map

Use this page to check which first-class capabilities `ChatBrowser` currently owns, which ones are verified, and what remains out of scope for this package.

## Capability Groups

<div class="grid cards" markdown>

- **Backend Discovery**

    Read-only discovery for Chrome for Testing, Chromium, Chrome, Edge, and related browser executables.

- **Profile Metadata**

    Register profile aliases, paths, default backends, and labels. A profile is a browser-state container, not a platform account.

- **Session Endpoint**

    Register an existing local loopback CDP endpoint for upper layers to consume. ChatBrowser does not take ownership of external browsers by default.

- **Config and Environment**

    Expose ChatEnv schema fields for `CHATBROWSER_DEFAULT_BACKEND` and `CHATBROWSER_REGISTRY_HOME`; metadata defaults to ChatArch home.

</div>

## Current Capabilities

| Capability | Status | Entry | Notes |
| --- | --- | --- | --- |
| Package identity | Implemented / verified | `chatbrowser --version` | PyPI project `ChatBrowser`, module `chatbrowser`, and CLI `chatbrowser` are aligned. |
| Read-only health check | Implemented / verified | `chatbrowser doctor --output json` | Reports version, metadata home, dependency versions, and `installs_dependencies=false`. |
| Backend discovery | Implemented / verified | `chatbrowser backend list` | Inspects PATH only; does not install browsers. |
| Profile registration | Implemented / verified | `chatbrowser profile create/show/list/path/status` | Stores only non-sensitive metadata and does not inspect profile internals. |
| External CDP registration | Implemented / verified | `chatbrowser connect` | Registers an existing local loopback CDP endpoint with `owned=false`. |
| Session endpoint lookup | Implemented / verified | `chatbrowser session endpoint` | Integration point for ChatPost and Wechatsync. |
| ChatEnv provider | Implemented / verified | `chatenv` entry point | Provides default backend and registry home schema. |

## Out of Scope

- Installing Chrome, Chromium, Chrome for Testing, Node.js, uv, or system dependencies; those belong to ChatUp or manual setup.
- Determining which Zhihu, WeChat, Juejin, or other platform account is logged in; that belongs to Wechatsync/ChatPost platform adapters.
- Reading or printing sensitive browser-profile internals.
- Creating drafts or orchestrating multi-platform publishing tasks; those belong to ChatPost.

## Safety Boundary

- Text/JSON outputs contain metadata, paths, backend names, CDP URLs, and session IDs by default.
- `disconnect` only removes a local registry record; it does not terminate processes or close external browsers.
- Do not write the same profile from multiple machines at the same time; profile migration should be handled by explicit future commands or upper-layer workflows.
