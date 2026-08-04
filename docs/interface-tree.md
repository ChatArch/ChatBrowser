# Python 接口树

`ChatBrowser` 的 CLI 保持薄入口；实质能力放在可 import 的 Python 函数、类或 service 层里。

## 包入口

```python
from chatbrowser import __version__
```

## 当前模块

```text
chatbrowser
├── __init__.py      # 暴露包版本与 package identity
├── cli.py           # Click 薄封装，负责参数解析与输出格式
├── config.py        # ChatEnv 配置 schema
├── paths.py         # ChatArch home / registry path / profile root path
├── backends.py      # browser backend 只读探测
├── doctor.py        # 只读健康检查 payload
└── registry.py      # profile/session 非敏感 metadata registry
```

## 主要 API

### `chatbrowser.backends`

```python
from chatbrowser.backends import list_backends, backend_list_payload

backends = list_backends()
payload = backend_list_payload()
```

`list_backends()` 返回 backend descriptor 列表；只查 PATH，不安装任何依赖。

### `chatbrowser.registry`

```python
from chatbrowser.registry import (
    create_profile,
    list_profiles,
    get_profile,
    profile_path,
    profile_status,
    connect_session,
    list_sessions,
    get_session,
    disconnect_session,
)

profile = create_profile(
    "zhihu-test",
    path="/path/to/browser-profile",
    backend="chrome-for-testing",
)

session = connect_session(
    cdp_url="http://127.0.0.1:9229",
    session_id="zhihu-test-existing",
    profile="zhihu-test",
)
endpoint = get_session("zhihu-test-existing")["cdp_url"]
```

registry 只保存 profile/session metadata，不读取 profile 目录内部状态。

### `chatbrowser.doctor`

```python
from chatbrowser.doctor import doctor_payload

payload = doctor_payload()
```

`doctor_payload()` 用于 CLI、smoke test 或上层工具快速判断 ChatBrowser 是否可 import、依赖是否可见。

### `chatbrowser.paths`

```python
from chatbrowser.paths import chatarch_home, runtime_home, registry_path, default_profile_root
```

路径解析优先顺序：显式 home 参数、`CHATARCH_HOME`、ChatEnv 默认 home。

## 更新清单

- 每个实质 CLI 命令都要能映射到 importable API。
- 文档里的函数签名应和代码一致。
- 对外输出默认不要泄漏敏感浏览器状态或平台身份信息。
- 涉及安装/setup 的能力应优先放在 ChatUp，不要在 ChatBrowser 本地重做。
