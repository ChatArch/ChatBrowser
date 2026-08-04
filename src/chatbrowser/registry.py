"""Non-sensitive ChatBrowser profile/session registry."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from .paths import default_profile_root, registry_path, runtime_home


_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
_SENSITIVE_LABEL_KEY_RE = re.compile(
    r"(token|password|passwd|secret|cookie|session|account|credential|auth|api[_-]?key|login)",
    re.IGNORECASE,
)


@dataclass
class ProfileRecord:
    """A registered browser profile metadata record.

    The record deliberately stores only paths and non-sensitive metadata. It does
    not inspect or serialize browser cookies, tokens, LocalStorage, IndexedDB, or
    platform account details.
    """

    name: str
    path: str
    default_backend: str = "chrome-for-testing"
    labels: dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: _now())
    updated_at: str = field(default_factory=lambda: _now())


@dataclass
class SessionRecord:
    """A registered browser session endpoint."""

    id: str
    cdp_url: str
    profile: str | None = None
    owned: bool = False
    created_at: str = field(default_factory=lambda: _now())
    updated_at: str = field(default_factory=lambda: _now())


class RegistryError(ValueError):
    """Raised for invalid registry operations."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_name(name: str, *, field: str = "name") -> str:
    """Validate a registry key suitable for local metadata paths."""

    if not _NAME_RE.match(name):
        raise RegistryError(
            f"Invalid {field} {name!r}; use 1-64 letters, numbers, dot, underscore, or dash."
        )
    return name


def _empty_registry() -> dict[str, dict[str, dict[str, object]]]:
    return {"profiles": {}, "sessions": {}}


def load_registry(home: str | Path | None = None) -> dict[str, dict[str, dict[str, object]]]:
    """Load registry metadata, returning an empty registry if absent."""

    path = registry_path(home)
    if not path.exists():
        return _empty_registry()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RegistryError(f"Registry file {path} contains invalid JSON.") from exc
    if not isinstance(data, dict):
        raise RegistryError("Registry file must contain a JSON object.")
    data.setdefault("profiles", {})
    data.setdefault("sessions", {})
    if not isinstance(data["profiles"], dict) or not isinstance(data["sessions"], dict):
        raise RegistryError("Registry profiles and sessions must be JSON objects.")
    return data  # type: ignore[return-value]


def save_registry(data: dict[str, dict[str, dict[str, object]]], home: str | Path | None = None) -> None:
    """Atomically save registry metadata under ChatArch home."""

    root = runtime_home(home)
    root.mkdir(parents=True, exist_ok=True)
    path = registry_path(home)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def parse_labels(items: tuple[str, ...] | list[str]) -> dict[str, str]:
    labels: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise RegistryError(f"Invalid label {item!r}; expected key=value.")
        key, value = item.split("=", 1)
        validate_name(key, field="label key")
        if _SENSITIVE_LABEL_KEY_RE.search(key):
            raise RegistryError(
                f"Label key {key!r} is sensitive; labels must store only non-sensitive metadata."
            )
        labels[key] = value
    return labels


def create_profile(
    name: str,
    *,
    path: str | Path | None = None,
    backend: str = "chrome-for-testing",
    labels: dict[str, str] | None = None,
    home: str | Path | None = None,
) -> ProfileRecord:
    """Create or register a browser profile directory."""

    validate_name(name, field="profile")
    profile_path = Path(path) if path is not None else default_profile_root(home) / name
    profile_path.mkdir(parents=True, exist_ok=True)

    data = load_registry(home)
    now = _now()
    existing = data["profiles"].get(name)
    created_at = str(existing.get("created_at", now)) if existing else now
    record = ProfileRecord(
        name=name,
        path=str(profile_path),
        default_backend=backend,
        labels=labels or (existing.get("labels", {}) if existing else {}),
        created_at=created_at,
        updated_at=now,
    )
    data["profiles"][name] = asdict(record)
    save_registry(data, home)
    return record


def list_profiles(home: str | Path | None = None) -> list[dict[str, object]]:
    """Return registered profiles sorted by name."""

    data = load_registry(home)
    profiles = []
    for name, record in sorted(data["profiles"].items()):
        item = dict(record)
        item["exists"] = Path(str(item["path"])).exists()
        profiles.append(item)
    return profiles


def get_profile(name: str, *, home: str | Path | None = None) -> dict[str, object]:
    validate_name(name, field="profile")
    data = load_registry(home)
    try:
        record = dict(data["profiles"][name])
    except KeyError as exc:
        raise RegistryError(f"Profile {name!r} is not registered.") from exc
    record["exists"] = Path(str(record["path"])).exists()
    return record


def profile_path(name: str, *, home: str | Path | None = None) -> Path:
    """Return a registered profile root path."""

    return Path(str(get_profile(name, home=home)["path"]))


def profile_status(name: str, *, home: str | Path | None = None) -> dict[str, object]:
    """Return non-sensitive profile status."""

    profile = get_profile(name, home=home)
    data = load_registry(home)
    running_sessions = [
        session_id
        for session_id, session in sorted(data["sessions"].items())
        if session.get("profile") == name
    ]
    return {
        "profile": name,
        "path": profile["path"],
        "exists": profile["exists"],
        "running": bool(running_sessions),
        "sessions": running_sessions,
    }


def validate_cdp_url(cdp_url: str) -> str:
    parsed = urlparse(cdp_url)
    if parsed.scheme != "http" or not parsed.netloc:
        raise RegistryError("CDP URL must be a localhost http URL, for example http://127.0.0.1:9229.")
    if parsed.username or parsed.password:
        raise RegistryError("CDP URL must not include credentials or userinfo.")
    if parsed.path not in {"", "/"} or parsed.params or parsed.query or parsed.fragment:
        raise RegistryError("CDP URL must not include a path, query string, or fragment.")
    host = parsed.hostname
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise RegistryError("CDP URL must point to localhost / 127.0.0.1 / ::1, not a remote host.")
    try:
        port = parsed.port
    except ValueError as exc:
        raise RegistryError("CDP URL must include a valid localhost port from 1 to 65535.") from exc
    if port is None:
        raise RegistryError("CDP URL must include a localhost port, for example http://127.0.0.1:9229.")
    host_for_url = f"[{host}]" if ":" in host else host
    return f"http://{host_for_url}:{port}"


def connect_session(
    *,
    cdp_url: str,
    session_id: str,
    profile: str | None = None,
    home: str | Path | None = None,
) -> SessionRecord:
    """Register an external CDP endpoint as a non-owned session."""

    validate_name(session_id, field="session")
    if profile is not None:
        validate_name(profile, field="profile")
    data = load_registry(home)
    if profile is not None and profile not in data["profiles"]:
        raise RegistryError(f"Profile {profile!r} is not registered.")
    now = _now()
    existing = data["sessions"].get(session_id)
    created_at = str(existing.get("created_at", now)) if existing else now
    record = SessionRecord(
        id=session_id,
        cdp_url=validate_cdp_url(cdp_url),
        profile=profile,
        owned=False,
        created_at=created_at,
        updated_at=now,
    )
    data["sessions"][session_id] = asdict(record)
    save_registry(data, home)
    return record


def list_sessions(home: str | Path | None = None) -> list[dict[str, object]]:
    data = load_registry(home)
    return [dict(record) for _, record in sorted(data["sessions"].items())]


def get_session(session_id: str, *, home: str | Path | None = None) -> dict[str, object]:
    validate_name(session_id, field="session")
    data = load_registry(home)
    try:
        return dict(data["sessions"][session_id])
    except KeyError as exc:
        raise RegistryError(f"Session {session_id!r} is not registered.") from exc


def disconnect_session(session_id: str, *, home: str | Path | None = None) -> dict[str, object]:
    """Remove a ChatBrowser client-side session record without closing browsers."""

    validate_name(session_id, field="session")
    data = load_registry(home)
    try:
        record = dict(data["sessions"].pop(session_id))
    except KeyError as exc:
        raise RegistryError(f"Session {session_id!r} is not registered.") from exc
    save_registry(data, home)
    return record
