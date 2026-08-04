"""Read-only doctor helpers."""

from __future__ import annotations

from importlib import metadata

from chatbrowser import __version__
from chatbrowser.paths import runtime_home


def _version(package: str) -> str | None:
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return None


def doctor_payload() -> dict[str, object]:
    """Return a non-invasive runtime health payload."""

    dependencies = {
        "chatup": _version("chatup"),
        "chatstyle": _version("chatstyle"),
        "chatenv": _version("chatenv"),
    }
    return {
        "ok": True,
        "package": "ChatBrowser",
        "version": __version__,
        "runtime_home": str(runtime_home()),
        "installs_dependencies": False,
        "dependencies": dependencies,
    }
