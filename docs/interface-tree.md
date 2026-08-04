# Python 接口树

`ChatBrowser` 的 CLI 应保持薄入口；实质能力应放在可 import 的 Python 函数、类或 service 层里。

## 包入口

```python
from chatbrowser import __version__
```

## 当前模块

```text
chatbrowser
├── __init__.py     # 暴露包版本与 package identity
├── cli.py          # Click 入口，当前提供 --help 和 --version
└── config.py       # ChatEnv 配置 schema，供后续浏览器运行时配置扩展
```

当前版本还没有浏览器运行时 service 层。新增实质 CLI 命令前，应先落地可 import 的 Python 函数、类或 service 模块，再让 CLI 做薄封装。

## 更新清单

- 每个实质 CLI 命令都要能映射到 importable API。
- 文档里的函数签名应和代码一致。
- 对外输出默认不要泄漏 token、cookie、内部 URL 或人员信息。
