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

ChatBrowser 是 ChatArch 的浏览器运行态基础包。它不做平台账号语义，也不安装系统依赖；它只管理浏览器 backend 探测、profile 元数据、本机 loopback CDP endpoint 注册和 session endpoint 读取，供 ChatPost、Wechatsync 等上层发布工具复用。

文档入口：<https://arch.gh.wzhecnu.cn/ChatBrowser/>

## 边界

```text
ChatUp       = setup / install / configure
ChatBrowser  = browser backend / profile metadata / session endpoint / CDP registry
Wechatsync   = platform adapter / auth check / draft write
ChatPost     = post/task orchestration / multi-platform publishing workflow
```

ChatBrowser 不读取、打印或迁移平台账号数据；profile 目录里的浏览器状态由浏览器自己维护。

## 快速开始

```bash
pip install ChatBrowser
chatbrowser --help
chatbrowser doctor --output json
chatbrowser backend list --output json
```

注册一个已有浏览器 profile 目录：

```bash
chatbrowser profile create zhihu-test \
  --path /path/to/browser-profile \
  --backend chrome-for-testing \
  --output json

chatbrowser profile show zhihu-test --output json
chatbrowser profile path zhihu-test
```

接入一个已经运行的本机 loopback CDP endpoint（只接受 `http://127.0.0.1:<port>` / `http://localhost:<port>` / IPv6 localhost），不接管也不关闭该浏览器：

```bash
chatbrowser connect \
  --cdp-url http://127.0.0.1:9229 \
  --as-session-name zhihu-test-existing \
  --profile zhihu-test \
  --output json

chatbrowser session endpoint zhihu-test-existing
chatbrowser disconnect zhihu-test-existing
```

## 当前 CLI

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

## 开发检查

```bash
pip install -e ".[dev,docs]"
python -m pytest -q
python -m build
mkdocs build --strict
```

新增命令时保持 CLI 是薄封装：核心逻辑先放进可 import Python API，再让 Click 命令调用它。
