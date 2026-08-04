# ChatBrowser 文档

ChatBrowser 是 ChatArch 的浏览器运行时与 artifact identity 包。当前首发版本固定 PyPI 包名、`chatbrowser` CLI 入口、Python import 面和 ChatEnv 配置发现入口；浏览器运行时的具体自动化命令会在后续版本中按真实能力补充。

站点入口：<https://arch.gh.wzhecnu.cn/ChatBrowser/>

## 按场景选择文档

| 场景 | 文档 |
| --- | --- |
| 第一次安装、运行命令行、确认包可用 | [CLI 树](cli-tree.md) |
| 校对当前包有哪些一等能力和边界 | [能力地图](capability-map.md) |
| 从 Python 代码调用包能力 | [Python 接口树](interface-tree.md) |

## 文档栏目组织

当前文档只记录已经存在的入口和边界：

- **CLI 树**：最直观的命令展示入口，当前包含 `--help` 与 `--version`。
- **能力地图**：当前一等能力、边界和不负责的范围。
- **接口树**：命令行背后的可 import Python 接口。

## 核心入口

<div class="grid cards" markdown>

- **CLI 树**

    从命令行入口开始，记录已实现命令、命令状态和交互约定。

    [查看 CLI 树](cli-tree.md)

- **能力地图**

    用于 review 当前包的能力边界，避免把浏览器自动化规划写成已实现功能。

    [查看能力地图](capability-map.md)

- **Python 接口树**

    保持命令行是薄入口，实质能力放在可 import 的 Python 接口中。

    [查看接口树](interface-tree.md)

</div>

## 文档状态约定

- **已实现**：代码、测试或 CLI 路径已经存在。
- **已验证**：已经通过本地 smoke、CI 或真实服务实践验证。
- **未实现**：只写边界和计划，不写成可执行教程；实现并验证后再升级为操作文档。

## 本地预览

```bash
python -m pip install -e ".[docs]"
mkdocs serve
```

英文首页见站点语言入口：<https://arch.gh.wzhecnu.cn/ChatBrowser/en/>。缺少英文翻译的专题页会按 i18n fallback 回退到中文页面。
