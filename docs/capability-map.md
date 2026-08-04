# 能力地图

这个页面用于校对 `ChatBrowser` 当前有哪些一等能力、哪些能力已经验证，以及哪些事情不属于当前包。

## 能力分组

<div class="grid cards" markdown>

- **Backend 探测**

    只读识别本机是否存在 Chrome for Testing、Chromium、Chrome、Edge 等 browser executable。

- **Profile 元数据**

    登记 profile alias、路径、默认 backend 和 labels；profile 是浏览器状态容器，不等于平台账号。

- **Session endpoint**

    登记已有本机 loopback CDP endpoint，供上层工具读取 endpoint；默认不接管、不关闭外部浏览器。

- **配置与环境**

    通过 ChatEnv 提供 `CHATBROWSER_DEFAULT_BACKEND` 与 `CHATBROWSER_REGISTRY_HOME` schema；默认 metadata 存在 ChatArch home 下。

</div>

## 当前能力

| 能力 | 状态 | 入口 | 说明 |
| --- | --- | --- | --- |
| 包身份 | 已实现 / 已验证 | `chatbrowser --version` | PyPI project `ChatBrowser`、module `chatbrowser`、CLI `chatbrowser` 对齐。 |
| 只读健康检查 | 已实现 / 已验证 | `chatbrowser doctor --output json` | 报告版本、metadata home、依赖版本和 `installs_dependencies=false`。 |
| Backend 探测 | 已实现 / 已验证 | `chatbrowser backend list` | 只查 PATH，不安装 browser。 |
| Profile 登记 | 已实现 / 已验证 | `chatbrowser profile create/show/list/path/status` | 只保存非敏感元数据，不读取 profile 内部状态。 |
| 外部 CDP 接入 | 已实现 / 已验证 | `chatbrowser connect` | 登记已有本机 loopback CDP endpoint，`owned=false`。 |
| Session endpoint 读取 | 已实现 / 已验证 | `chatbrowser session endpoint` | 面向 ChatPost / Wechatsync 的集成点。 |
| ChatEnv 配置提供者 | 已实现 / 已验证 | `chatenv` entry point | 提供默认 backend 和 registry home schema。 |

## 不属于 ChatBrowser

- 不安装 Chrome、Chromium、Chrome for Testing、Node.js、uv 或系统依赖；这些属于 ChatUp 或人工 setup。
- 不判断知乎、公众号、掘金等平台账号是谁；这些属于 Wechatsync/ChatPost 的平台 adapter。
- 不读取或输出 browser profile 内部的敏感状态。
- 不发布草稿、不调度多平台任务；这些属于 ChatPost。

## 安全边界

- 对外 JSON/text 默认只包含 metadata、路径、backend 名称、CDP URL 和 session id。
- `disconnect` 只删除本地 registry 记录，不杀进程、不关闭外部浏览器。
- 同一 profile 不应在多台机器上同时写入；迁移 profile 目录应由显式后续命令或上层 workflow 处理。
