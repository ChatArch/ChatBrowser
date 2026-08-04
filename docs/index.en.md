# ChatBrowser Docs

ChatBrowser is the ChatArch browser runtime foundation package. It provides browser backend discovery, profile metadata registry, local loopback CDP endpoint registration, and session endpoint lookup. It does not install system dependencies, determine platform accounts, or create publishing drafts.

Site entry: <https://arch.gh.wzhecnu.cn/ChatBrowser/en/>

## Choose Documentation by Scenario

| Scenario | Document |
| --- | --- |
| Inspect the real command tree, JSON output, and session endpoint flow | [CLI Tree](cli-tree.md) |
| Check first-class capabilities and current boundaries | [Capability Map](capability-map.md) |
| Call profile/session/backend behavior directly from Python | [Python Interface Tree](interface-tree.md) |

## Role Boundaries

```text
ChatUp       = setup / install / configure
ChatBrowser  = browser backend / profile metadata / session endpoint / CDP registry
Wechatsync   = platform adapter / auth check / draft write
ChatPost     = post/task orchestration / multi-platform publishing workflow
```

## Primary Entry Points

<div class="grid cards" markdown>

- **CLI Tree**

    Start from the CLI entry point and record implemented commands, command status, and integration flows.

    [Open CLI Tree](cli-tree.md)

- **Capability Map**

    Review current package boundaries and keep platform-account semantics and setup responsibilities out of ChatBrowser.

    [Open Capability Map](capability-map.md)

- **Python Interface Tree**

    Keep the CLI thin and put substantive behavior in importable Python APIs.

    [Open Interface Tree](interface-tree.md)

</div>

## Local Preview

```bash
python -m pip install -e ".[docs]"
mkdocs serve
```

The Chinese home page is available at <https://arch.gh.wzhecnu.cn/ChatBrowser/>.
