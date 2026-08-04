import json
import subprocess
import sys
from pathlib import Path

from click.testing import CliRunner

from chatbrowser.cli import main


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def invoke(*args, env=None):
    return CliRunner().invoke(main, list(args), env=env)


def parse_json_output(result):
    assert result.exit_code == 0, result.output
    return json.loads(result.output)


def test_pyproject_declares_chatup_dependency():
    text = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert "chatup>=" in text
    assert "<0.3.0" in text


def test_top_level_help_exposes_runtime_command_groups():
    result = invoke("--help")

    assert result.exit_code == 0
    for command in ["doctor", "backend", "profile", "session", "connect", "disconnect"]:
        assert command in result.output


def test_doctor_json_reports_runtime_contract_without_installing():
    data = parse_json_output(invoke("doctor", "--output", "json"))

    assert data["ok"] is True
    assert data["package"] == "ChatBrowser"
    assert data["installs_dependencies"] is False
    assert "chatup" in data["dependencies"]


def test_backend_list_show_and_resolve_json_report_known_backends(monkeypatch):
    monkeypatch.setenv("PATH", "")

    data = parse_json_output(invoke("backend", "list", "--output", "json"))

    names = {item["name"] for item in data["backends"]}
    assert {"chrome-for-testing", "chromium", "chrome"}.issubset(names)
    assert all("usable" in item for item in data["backends"])

    shown = parse_json_output(invoke("backend", "show", "chrome", "--output", "json"))
    assert shown["backend"]["name"] == "chrome"

    resolved = parse_json_output(invoke("backend", "resolve", "chrome", "--output", "json"))
    assert resolved["backend"]["name"] == "chrome"


def test_profile_create_show_path_status_use_task_local_home(tmp_path):
    home = tmp_path / "chatarch-home"
    profile_root = tmp_path / "zhihu-test-profile"
    env = {"CHATARCH_HOME": str(home)}

    created = parse_json_output(
        invoke(
            "profile",
            "create",
            "zhihu-test",
            "--path",
            str(profile_root),
            "--backend",
            "chrome-for-testing",
            "--output",
            "json",
            env=env,
        )
    )
    assert created["profile"]["name"] == "zhihu-test"
    assert created["profile"]["path"] == str(profile_root)
    assert created["profile"]["default_backend"] == "chrome-for-testing"
    assert profile_root.exists()

    listed = parse_json_output(invoke("profile", "list", "--output", "json", env=env))
    assert [profile["name"] for profile in listed["profiles"]] == ["zhihu-test"]

    shown = parse_json_output(invoke("profile", "show", "zhihu-test", "--output", "json", env=env))
    assert shown["profile"]["path"] == str(profile_root)
    assert shown["profile"]["exists"] is True
    assert "account" not in json.dumps(shown).lower()

    path_result = invoke("profile", "path", "zhihu-test", env=env)
    assert path_result.exit_code == 0
    assert path_result.output.strip() == str(profile_root)

    status = parse_json_output(invoke("profile", "status", "zhihu-test", "--output", "json", env=env))
    assert status["profile"] == "zhihu-test"
    assert status["running"] is False


def test_connect_registers_external_cdp_without_closing_it(tmp_path):
    home = tmp_path / "chatarch-home"
    env = {"CHATARCH_HOME": str(home)}

    connected = parse_json_output(
        invoke(
            "connect",
            "--cdp-url",
            "http://127.0.0.1:9229",
            "--as-session-name",
            "zhihu-test-existing",
            "--output",
            "json",
            env=env,
        )
    )
    assert connected["session"]["id"] == "zhihu-test-existing"
    assert connected["session"]["cdp_url"] == "http://127.0.0.1:9229"
    assert connected["session"]["owned"] is False

    endpoint = parse_json_output(invoke("session", "endpoint", "zhihu-test-existing", "--output", "json", env=env))
    assert endpoint["cdp_url"] == "http://127.0.0.1:9229"

    shown = parse_json_output(invoke("session", "show", "zhihu-test-existing", "--output", "json", env=env))
    assert shown["session"]["id"] == "zhihu-test-existing"
    assert shown["session"]["owned"] is False

    sessions = parse_json_output(invoke("session", "list", "--output", "json", env=env))
    assert sessions["sessions"][0]["id"] == "zhihu-test-existing"

    disconnected = parse_json_output(invoke("disconnect", "zhihu-test-existing", "--output", "json", env=env))
    assert disconnected["closed_browser"] is False
    assert disconnected["session"]["id"] == "zhihu-test-existing"

    sessions_after = parse_json_output(invoke("session", "list", "--output", "json", env=env))
    assert sessions_after["sessions"] == []


def test_invalid_profile_name_and_cdp_url_fail_with_nonzero_exit(tmp_path):
    env = {"CHATARCH_HOME": str(tmp_path / "chatarch-home")}

    bad_name = invoke("profile", "create", "../bad", "--output", "json", env=env)
    assert bad_name.exit_code != 0
    assert "invalid" in bad_name.output.lower()

    bad_url = invoke(
        "connect",
        "--cdp-url",
        "https://example.com:443",
        "--as-session-name",
        "bad-session",
        "--output",
        "json",
        env=env,
    )
    assert bad_url.exit_code != 0
    assert "localhost" in bad_url.output.lower()

    missing_profile = invoke(
        "connect",
        "--cdp-url",
        "http://127.0.0.1:9229",
        "--as-session-name",
        "missing-profile-session",
        "--profile",
        "missing-profile",
        "--output",
        "json",
        env=env,
    )
    assert missing_profile.exit_code != 0
    assert "not registered" in missing_profile.output.lower()



def test_profile_cookie_terms_are_not_exposed_in_help():
    result = invoke("profile", "--help")

    assert result.exit_code == 0
    lowered = result.output.lower()
    assert "cookie" not in lowered
    assert "token" not in lowered
    assert "account" not in lowered


def test_mkdocs_and_readme_are_utf8_text_files():
    for relative in ["README.md", "README.en.md", "mkdocs.yml"]:
        data = (PROJECT_ROOT / relative).read_bytes()
        assert b"\x00" not in data, f"{relative} contains NUL bytes"
        data.decode("utf-8")
