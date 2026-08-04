"""Browser backend discovery."""

from __future__ import annotations

import shutil
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BackendInfo:
    """A browser backend descriptor."""

    name: str
    executable: str | None
    usable: bool
    source: str
    reason: str | None = None


_BACKEND_CANDIDATES: dict[str, tuple[str, ...]] = {
    "chrome-for-testing": ("chrome", "chrome-for-testing", "google-chrome-for-testing"),
    "chromium": ("chromium", "chromium-browser"),
    "chrome": ("google-chrome", "google-chrome-stable", "chrome"),
    "edge": ("microsoft-edge", "microsoft-edge-stable"),
}


def list_backends() -> list[BackendInfo]:
    """Discover known browser backend executables without installing anything."""

    backends: list[BackendInfo] = []
    for name, candidates in _BACKEND_CANDIDATES.items():
        executable = next((path for binary in candidates if (path := shutil.which(binary))), None)
        backends.append(
            BackendInfo(
                name=name,
                executable=executable,
                usable=executable is not None,
                source="system" if executable else "unresolved",
                reason=None if executable else "executable not found on PATH",
            )
        )
    return backends


def backend_list_payload() -> dict[str, object]:
    """Return a JSON-serializable backend discovery payload."""

    return {"backends": [asdict(backend) for backend in list_backends()]}
