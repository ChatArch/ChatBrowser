<div align="center">
    <a href="https://pypi.python.org/pypi/ChatBrowser">
        <img src="https://img.shields.io/pypi/v/ChatBrowser.svg" alt="PyPI version" />
    </a>
    <a href="https://github.com/ChatArch/ChatBrowser/actions/workflows/ci.yml">
        <img src="https://github.com/ChatArch/ChatBrowser/actions/workflows/ci.yml/badge.svg" alt="Tests" />
    </a>
    <a href="https://arch.gh.wzhecnu.cn/ChatBrowser/">
        <img src="https://img.shields.io/badge/docs-mkdocs-blue.svg" alt="Documentation" />
    </a>
</div>

<div align="center">

[English](README.en.md) | [简体中文](README.md)
</div>

# ChatBrowser

ChatBrowser is the ChatArch browser runtime foundation package. It does not own platform-account semantics and does not install system dependencies. It owns browser backend discovery, profile metadata, local loopback CDP endpoint registration, and session endpoint lookup for higher-level tools such as ChatPost and Wechatsync.

Documentation entry: <https://arch.gh.wzhecnu.cn/ChatBrowser/en/>

## Boundaries

```text
ChatUp       = setup / install / configure
ChatBrowser  = browser backend / profile metadata / session endpoint / CDP registry
Wechatsync   = platform adapter / auth check / draft write
ChatPost     = post/task orchestration / multi-platform publishing workflow
```

ChatBrowser does not read, print, or migrate platform account data; browser state inside profile directories remains owned by the browser.

## Quick Start

```bash
pip install ChatBrowser
chatbrowser --help
chatbrowser doctor --output json
chatbrowser backend list --output json
```

Register an existing browser profile directory:

```bash
chatbrowser profile create zhihu-test \
  --path /path/to/browser-profile \
  --backend chrome-for-testing \
  --output json

chatbrowser profile show zhihu-test --output json
chatbrowser profile path zhihu-test
```

Attach an already-running local loopback CDP endpoint (`http://127.0.0.1:<port>`, `http://localhost:<port>`, or IPv6 localhost) without taking ownership of the browser:

```bash
chatbrowser connect \
  --cdp-url http://127.0.0.1:9229 \
  --as-session-name zhihu-test-existing \
  --profile zhihu-test \
  --output json

chatbrowser session endpoint zhihu-test-existing
chatbrowser disconnect zhihu-test-existing
```

## Current CLI

```text
chatbrowser
├── doctor
├── backend
│   ├── list
│   ├── show <name>
│   └── resolve <name>
├── profile
│   ├── list
│   ├── create <name>
│   ├── show <name>
│   ├── path <name>
│   └── status <name>
├── connect
├── disconnect <session-id>
└── session
    ├── list
    ├── show <session-id>
    └── endpoint <session-id>
```

## Development Checks

```bash
pip install -e ".[dev,docs]"
python -m pytest -q
python -m build
mkdocs build --strict
```

Keep the CLI thin when adding commands: implement importable Python APIs first, then call them from Click commands.
