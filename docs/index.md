# ChatBrowser 文档

ChatBrowser 是 ChatArch 的浏览器运行态基础包：它提供 browser backend 探测、profile metadata registry、本机 loopback CDP endpoint 登记和 session endpoint 读取。它不安装系统依赖，不判断平台账号，也不发布草稿。

站点入口：<https://arch.gh.wzhecnu.cn/ChatBrowser/>

## 按场景选择文档

| 场景 | 文档 |
| --- | --- |
| 查看当前真实命令、JSON 输出和 session endpoint 用法 | [CLI 树](cli-tree.md) |
| 校对当前包有哪些一等能力和边界 | [能力地图](capability-map.md) |
| 从 Python 代码调用 profile/session/backend 能力 | [Python 接口树](interface-tree.md) |

## 角色边界

```text
ChatUp       = setup / install / configure
ChatBrowser  = browser backend / profile metadata / session endpoint / CDP registry
Wechatsync   = platform adapter / auth check / draft write
ChatPost     = post/task orchestration / multi-platform publishing workflow
```

## 核心入口

<div class="grid cards" markdown>

- **CLI 树**

    从命令行入口开始，记录已实现命令、命令状态和集成方式。

    [查看 CLI 树](cli-tree.md)

- **能力地图**

    用于 review 当前包的能力边界，避免把平台账号语义或安装职责写进 ChatBrowser。

    [查看能力地图](capability-map.md)

- **Python 接口树**

    保持命令行是薄入口，实质能力放在可 import 的 Python 接口中。

    [查看接口树](interface-tree.md)

</div>

## 本地预览

```bash
python -m pip install -e ".[docs]"
mkdocs serve
```

英文首页见站点语言入口：<https://arch.gh.wzhecnu.cn/ChatBrowser/en/>。
