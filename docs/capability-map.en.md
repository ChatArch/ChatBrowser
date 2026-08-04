# Capability Map

Use this page to check which first-class capabilities `ChatBrowser` currently owns, which ones are verified, and what remains out of scope for this package.

## Capability Groups

<div class="grid cards" markdown>

- **CLI Entry**

    `chatbrowser --help` and `chatbrowser --version` are the default verification entry points.

- **Python API**

    Substantive behavior should live in importable Python functions, classes, or service layers rather than only in Click callbacks.

- **Config and Environment**

    ChatEnv integration is enabled; future browser runtime settings that need stable storage should live in `config.py`.

</div>

## Current Boundary

| Capability | Status | Notes |
| --- | --- | --- |
| CLI base entry | Implemented | The template generates a Click group, `--version`, and a base test. |
| Python package identity | Implemented | The `ChatBrowser` PyPI project, `chatbrowser` module, and `chatbrowser` CLI entry point are aligned. |
| ChatEnv provider | Implemented | The package exposes `config.py` and a `chatenv.configs` entry point for future configuration fields. |
| Browser runtime business commands | Not implemented | Add these only when real runtime capabilities exist; do not fake future commands. |

## Out of Scope

- No unimplemented capability should be written as a user operation tutorial.
- No secret, token, cookie, or Authorization header should appear in README, docs, issues, PR comments, or CI logs.
