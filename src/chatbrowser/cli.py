"""CLI entrypoint for chatbrowser."""

from __future__ import annotations

import inspect
import json
from dataclasses import asdict, is_dataclass
from typing import Any

import click

from chatbrowser import __version__
from chatbrowser.backends import backend_list_payload
from chatbrowser.doctor import doctor_payload
from chatbrowser.registry import (
    RegistryError,
    connect_session,
    create_profile,
    disconnect_session,
    get_profile,
    get_session,
    list_profiles,
    list_sessions,
    parse_labels,
    profile_path,
    profile_status,
)

OUTPUT_CHOICES = click.Choice(["text", "json"])


def _purpose(command: click.Command) -> str:
    text = command.short_help or inspect.getdoc(command.callback) or ""
    return " ".join(text.strip().split()).rstrip(".")


def _metavar(parameter: click.Parameter) -> str:
    if isinstance(parameter.type, click.Choice):
        return "|".join(parameter.type.choices)
    return parameter.metavar or parameter.name.upper().replace("_", "-")


def _parameter_piece(parameter: click.Parameter) -> str | None:
    if getattr(parameter, "hidden", False) or parameter.name == "help":
        return None
    if isinstance(parameter, click.Argument):
        piece = _metavar(parameter)
        if not parameter.required:
            piece = f"[{piece}]"
        if parameter.nargs == -1:
            piece = f"{piece}..."
        return piece
    if not isinstance(parameter, click.Option):
        return None
    option_names = [name for name in (*parameter.opts, *parameter.secondary_opts) if name.startswith("--")]
    if not option_names:
        option_names = [name for name in (*parameter.opts, *parameter.secondary_opts) if name.startswith("-")]
    if not option_names:
        return None
    if parameter.is_flag or parameter.flag_value is not None:
        piece = "/".join(option_names)
    else:
        piece = f"{'/'.join(option_names)} {_metavar(parameter)}"
    if not parameter.required:
        piece = f"[{piece}]"
    return piece


def _command_signature(name: str, command: click.Command) -> str:
    pieces = [piece for piece in (_parameter_piece(parameter) for parameter in command.params) if piece]
    return " ".join([name, *pieces])


def _render_command_tree(command: click.Command, name: str, prefix: str, is_last: bool, lines: list[str]) -> None:
    connector = "└── " if is_last else "├── "
    line = f"{prefix}{connector}{_command_signature(name, command)}"
    purpose = _purpose(command)
    if purpose:
        line = f"{line}  # {purpose}"
    lines.append(line)
    if not isinstance(command, click.Group):
        return
    children = [(child_name, child) for child_name, child in command.commands.items() if not child.hidden]
    child_prefix = prefix + ("    " if is_last else "│   ")
    for index, (child_name, child) in enumerate(children):
        _render_command_tree(child, child_name, child_prefix, index == len(children) - 1, lines)


def _render_cli_tree(root: click.Group) -> str:
    children = [(name, command) for name, command in root.commands.items() if not command.hidden]
    lines = [f"chatbrowser  # {_purpose(root)}"]
    root_options = [
        ("--help", "Show help for the current command."),
        ("--version", "Show package version."),
        ("--tree", "Print the registered CLI tree."),
    ]
    for index, (option, purpose) in enumerate(root_options):
        is_last = not children and index == len(root_options) - 1
        lines.append(f"{'└──' if is_last else '├──'} {option}  # {purpose}")
    for index, (child_name, child) in enumerate(children):
        _render_command_tree(child, child_name, "", index == len(children) - 1, lines)
    return "\n".join(lines)


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def _emit(payload: Any, *, output: str = "text", text: str | None = None) -> None:
    """Render a payload in text or JSON form."""

    serializable = _jsonable(payload)
    if output == "json":
        click.echo(json.dumps(serializable, ensure_ascii=False, indent=2, sort_keys=True))
        return
    if text is not None:
        click.echo(text)
        return
    if isinstance(serializable, dict):
        for key, value in serializable.items():
            click.echo(f"{key}: {value}")
    else:
        click.echo(serializable)


def _handle_error(exc: RegistryError) -> None:
    raise click.ClickException(str(exc)) from exc


@click.group(
    name="chatbrowser",
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
    no_args_is_help=True,
)
@click.version_option(__version__, prog_name="chatbrowser")
@click.option("--tree", "show_tree", is_flag=True, is_eager=True, help="Print the registered CLI tree.")
@click.pass_context
def main(ctx: click.Context, show_tree: bool) -> None:
    """ChatBrowser browser runtime metadata CLI."""

    if show_tree:
        click.echo(_render_cli_tree(ctx.command))
        ctx.exit()


@main.command(name="doctor")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def doctor_command(output: str) -> None:
    """Check ChatBrowser without installing or changing browser state."""

    payload = doctor_payload()
    _emit(payload, output=output, text=f"chatbrowser {payload['version']} ok")


@main.group(name="backend")
def backend_group() -> None:
    """Discover browser backend executables."""


@backend_group.command(name="list")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def backend_list_command(output: str) -> None:
    """List known browser backends without installing them."""

    payload = backend_list_payload()
    if output == "text":
        lines = []
        for backend in payload["backends"]:  # type: ignore[index]
            status = "usable" if backend["usable"] else f"missing ({backend['reason']})"
            lines.append(f"{backend['name']}: {status}")
        _emit(payload, output=output, text="\n".join(lines))
    else:
        _emit(payload, output=output)


@backend_group.command(name="show")
@click.argument("name")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def backend_show_command(name: str, output: str) -> None:
    """Show one backend descriptor."""

    payload = backend_list_payload()
    for backend in payload["backends"]:  # type: ignore[index]
        if backend["name"] == name:
            _emit({"backend": backend}, output=output)
            return
    raise click.ClickException(f"Backend {name!r} is unknown.")


@backend_group.command(name="resolve")
@click.argument("name")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def backend_resolve_command(name: str, output: str) -> None:
    """Resolve one backend executable path."""

    backend_show_command.callback(name=name, output=output)  # type: ignore[attr-defined]


@main.group(name="profile")
def profile_group() -> None:
    """Manage isolated browser profiles."""


@profile_group.command(name="list")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def profile_list_command(output: str) -> None:
    """List registered profiles."""

    try:
        payload = {"profiles": list_profiles()}
    except RegistryError as exc:
        _handle_error(exc)
    if output == "text":
        names = [profile["name"] for profile in payload["profiles"]]
        _emit(payload, output=output, text="\n".join(names) if names else "No profiles registered.")
    else:
        _emit(payload, output=output)


@profile_group.command(name="create")
@click.argument("name")
@click.option("--path", "profile_dir", type=click.Path(path_type=str, file_okay=False), default=None)
@click.option("--backend", "backend", default="chrome-for-testing", show_default=True)
@click.option("--label", "labels", multiple=True, help="Attach non-sensitive metadata as key=value.")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def profile_create_command(
    name: str,
    profile_dir: str | None,
    backend: str,
    labels: tuple[str, ...],
    output: str,
) -> None:
    """Create or register a profile directory."""

    try:
        record = create_profile(name, path=profile_dir, backend=backend, labels=parse_labels(labels))
    except RegistryError as exc:
        _handle_error(exc)
    _emit({"profile": record}, output=output, text=f"Profile {record.name}: {record.path}")


@profile_group.command(name="show")
@click.argument("name")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def profile_show_command(name: str, output: str) -> None:
    """Show non-sensitive profile metadata."""

    try:
        profile = get_profile(name)
    except RegistryError as exc:
        _handle_error(exc)
    _emit({"profile": profile}, output=output)


@profile_group.command(name="path")
@click.argument("name")
@click.option("--kind", "kind", default="root", show_default=True, type=click.Choice(["root", "downloads", "logs", "run"]))
def profile_path_command(name: str, kind: str) -> None:
    """Print a profile-related path."""

    try:
        root = profile_path(name)
    except RegistryError as exc:
        _handle_error(exc)
    paths = {
        "root": root,
        "downloads": root / "Downloads",
        "logs": root / "logs",
        "run": root / "run",
    }
    click.echo(str(paths[kind]))


@profile_group.command(name="status")
@click.argument("name")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def profile_status_command(name: str, output: str) -> None:
    """Show non-sensitive profile status."""

    try:
        payload = profile_status(name)
    except RegistryError as exc:
        _handle_error(exc)
    _emit(payload, output=output)


@main.group(name="session")
def session_group() -> None:
    """Read registered browser sessions."""


@session_group.command(name="list")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def session_list_command(output: str) -> None:
    """List registered sessions."""

    try:
        payload = {"sessions": list_sessions()}
    except RegistryError as exc:
        _handle_error(exc)
    if output == "text":
        ids = [session["id"] for session in payload["sessions"]]
        _emit(payload, output=output, text="\n".join(ids) if ids else "No sessions registered.")
    else:
        _emit(payload, output=output)


@session_group.command(name="show")
@click.argument("session_id")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def session_show_command(session_id: str, output: str) -> None:
    """Show one session record."""

    try:
        session = get_session(session_id)
    except RegistryError as exc:
        _handle_error(exc)
    _emit({"session": session}, output=output)


@session_group.command(name="endpoint")
@click.argument("session_id")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def session_endpoint_command(session_id: str, output: str) -> None:
    """Print the CDP endpoint for a registered session."""

    try:
        session = get_session(session_id)
    except RegistryError as exc:
        _handle_error(exc)
    payload = {"session": session_id, "cdp_url": session["cdp_url"], "owned": session.get("owned", False)}
    _emit(payload, output=output, text=str(session["cdp_url"]))


@main.command(name="connect")
@click.option("--cdp-url", "cdp_url", required=True, help="Existing localhost http CDP endpoint, for example http://127.0.0.1:9229.")
@click.option("--as-session-name", "session_id", required=True, help="Local session name to register.")
@click.option("--profile", "profile", default=None, help="Optional registered profile alias.")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def connect_command(cdp_url: str, session_id: str, profile: str | None, output: str) -> None:
    """Register an existing CDP endpoint without taking ownership."""

    try:
        record = connect_session(cdp_url=cdp_url, session_id=session_id, profile=profile)
    except RegistryError as exc:
        _handle_error(exc)
    _emit({"session": record}, output=output, text=f"Session {record.id}: {record.cdp_url}")


@main.command(name="disconnect")
@click.argument("session_id")
@click.option("--output", "output", default="text", show_default=True, type=OUTPUT_CHOICES)
def disconnect_command(session_id: str, output: str) -> None:
    """Remove a local session record without closing external browsers."""

    try:
        record = disconnect_session(session_id)
    except RegistryError as exc:
        _handle_error(exc)
    _emit({"session": record, "closed_browser": False}, output=output, text=f"Disconnected {session_id}")


if __name__ == "__main__":
    main()
