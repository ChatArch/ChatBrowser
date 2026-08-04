"""Path helpers for ChatBrowser runtime metadata."""

from __future__ import annotations

import os
from pathlib import Path

from chatenv import get_paths


PACKAGE_DIR_NAME = "chatbrowser"


def chatarch_home(home: str | Path | None = None) -> Path:
    """Return the effective ChatArch home.

    Explicit ``home`` wins, then ``CHATARCH_HOME``, then ChatEnv's default.
    """

    selected = home if home is not None else os.environ.get("CHATARCH_HOME")
    return Path(get_paths(selected).home_dir)


def runtime_home(home: str | Path | None = None) -> Path:
    """Return ChatBrowser's non-sensitive metadata directory.

    Explicit ``home`` means a ChatArch home override. When no explicit home is
    supplied, ``CHATBROWSER_REGISTRY_HOME`` can point directly at the
    ChatBrowser metadata root. Otherwise metadata lives under ChatArch home.
    """

    if home is None:
        registry_home = os.environ.get("CHATBROWSER_REGISTRY_HOME")
        if registry_home:
            return Path(registry_home)
    return chatarch_home(home) / PACKAGE_DIR_NAME


def registry_path(home: str | Path | None = None) -> Path:
    """Return the registry JSON path."""

    return runtime_home(home) / "registry.json"


def default_profile_root(home: str | Path | None = None) -> Path:
    """Return the default managed profile root."""

    return runtime_home(home) / "profiles"
