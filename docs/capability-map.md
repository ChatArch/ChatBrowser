# 能力地图

这个页面用于校对 `ChatBrowser` 当前有哪些一等能力、哪些能力已经验证，以及哪些事情不属于当前包。

## 能力分组

<div class="grid cards" markdown>

- **命令行入口**

    `chatbrowser --help` 和 `chatbrowser --version` 是默认可验证入口。

- **Python 接口**

    实质能力应放到可 import 的 Python 函数、类或 service 层，而不是只写在 Click 回调里。

- **配置与环境**

    已接入 ChatEnv；后续浏览器运行时需要长期保存的配置应进入 `config.py`。

</div>

## 当前边界

| 能力 | 状态 | 说明 |
| --- | --- | --- |
| 命令行基础入口 | 已实现 | 模板生成 Click group、`--version` 和基础测试。 |
| Python package identity | 已实现 | `ChatBrowser` PyPI project、`chatbrowser` module 和 `chatbrowser` CLI 入口保持一致。 |
| ChatEnv 配置提供者 | 已实现 | 提供 `config.py` 和 `chatenv.configs` 入口点，供后续配置项扩展。 |
| 浏览器运行时业务命令 | 未实现 | 后续按真实运行时能力补充，当前不伪造未来命令。 |

## 不在当前范围

- 不把未实现能力写成用户可执行教程。
- 不在 README、docs、issue、PR 评论或 CI log 中输出 secret、token、cookie 或 Authorization header。
