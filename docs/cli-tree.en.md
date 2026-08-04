# CLI Capability Map

This page is the compact capability map for the `ChatBrowser` CLI. Use it to review which commands are first-class entries and which are still boundaries or plans. The current release ships only the base identity entries and does not present unimplemented browser automation commands as available operations.

Importable Python functions are mapped in [Interface Tree](interface-tree.md). Current package boundaries are tracked in [Capability Map](capability-map.md).

## Top-Level Commands

```text
chatbrowser                  # ChatBrowser command-line entry
├── --help                     # Show CLI help and registered commands
└── --version                  # Print the current package version
```

## Base Entries

```text
chatbrowser --help           # Verify the command is installed and inspect the current command tree
chatbrowser --version        # Verify the installed version
```

`--help` and `--version` are the current verification entries. After adding business commands, follow the ChatTea CLI tree pattern: split command groups into their own sections and annotate every command line.

## Unimplemented Business Commands

```text
chatbrowser <browser-command> # Not implemented yet; add it only with real browser runtime capability
```

This is not a promise of future capability. Only document a command as implemented after the command, Python function, and tests exist.

## Status Contract

| Status | Meaning |
| --- | --- |
| Implemented | Command, function, and tests exist |
| Verified | Covered by CI, local smoke, or real-service practice |
| Planned / checkpoint | Keep only boundary notes; do not write operation tutorials before implementation |

## Implementation Contract

- Every implemented command must map back to a Python function, class, or service layer.
- If a command writes remote state, document credentials, permissions, dry-run/checkpoint behavior, or confirmation boundaries.
- When adding a command, update README, the interface tree, capability map, tests, and related flow pages together.
