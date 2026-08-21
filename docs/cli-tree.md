# CLI 树

`chatbrowser` 当前是浏览器运行态元数据 CLI：探测 browser backend、登记 profile、登记本机 loopback CDP endpoint，并把 session endpoint 提供给上层工具。它不做平台账号语义，也不安装依赖。

Python 接口映射见 [接口树](interface-tree.md)。能力边界见 [能力地图](capability-map.md)。

## 顶层

```text
chatbrowser                  # ChatBrowser 命令行入口
├── --help                   # 显示 CLI 帮助和已注册命令
├── --version                # 输出当前包版本
├── --tree                   # 输出真实已注册 CLI 树（默认包含参数签名）
├── --tree-brief             # 输出命令节点和描述（省略参数签名）
├── doctor                   # 只读检查 ChatBrowser 与依赖状态
├── backend                  # 探测本机 browser backend
├── profile                  # 管理隔离 browser profile 元数据
├── session                  # 读取已登记 browser session
├── connect                  # 登记已有本机 loopback CDP endpoint，不接管浏览器
└── disconnect               # 删除本地 session 记录，不关闭外部浏览器
```

顶层选项使用 ChatStyle 共享 Click tree runtime。运行 `chatbrowser --tree` 可回读包含参数签名的真实注册树；运行 `chatbrowser --tree-brief` 可保留命令节点和描述并省略参数签名。两种输出的根节点都是 `chatbrowser`。文档中的命令树不得写入未实现的启动或 extension 子命令。

## doctor

```bash
chatbrowser doctor --output text|json
```

`doctor` 是只读命令；它报告包版本、ChatBrowser metadata home、`chatstyle` / `chatenv` 依赖版本、可选的 ChatUp 检测结果，以及 `installs_dependencies=false`，明确 ChatBrowser 不承担安装职责。ChatUp 不再是硬依赖，因为其当前发布版本要求 ChatStyle `<0.2.0`。

## backend

```text
chatbrowser backend list --output text|json
chatbrowser backend show <name> --output text|json
chatbrowser backend resolve <name> --output text|json
```

当前识别的 backend 名称：

- `chrome-for-testing`
- `chromium`
- `chrome`
- `edge`

这些命令只做 `PATH` 探测，不安装浏览器。缺少 backend 时应交给 ChatUp 或人工 setup 解决。

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

profile 是浏览器状态容器的别名和路径登记，不等于某个平台账号。ChatBrowser 只保存非敏感元数据：名称、路径、默认 backend、非敏感 labels 和时间戳；敏感 label key 会被拒绝。

## connect / disconnect

```text
chatbrowser connect \
  --cdp-url http://127.0.0.1:9229 \
  --as-session-name <session-id> \
  [--profile <profile-name>] \
  [--output text|json]

chatbrowser disconnect <session-id> --output text|json
```

`connect` 只登记已有本机 loopback CDP endpoint（`http://127.0.0.1:<port>` / `http://localhost:<port>` / IPv6 localhost；不允许 userinfo、path、query 或 fragment），`owned=false`；`disconnect` 只删除 ChatBrowser 本地 session 记录，不关闭外部浏览器。

## session

```text
chatbrowser session list --output text|json
chatbrowser session show <session-id> --output text|json
chatbrowser session endpoint <session-id> --output text|json
```

`session endpoint` 是 ChatPost / Wechatsync 这类上层工具最常消费的入口。

## 状态约定

| 状态 | 含义 |
| --- | --- |
| 已实现 | 命令、Python 函数和测试已经存在 |
| 已验证 | 通过本地测试、CLI smoke、CI 或真实服务实践 |
| 规划 | 只保留边界说明；实现前不要写操作教程 |
