from click.testing import CliRunner

from chatbrowser import __version__
from chatbrowser.cli import main


def test_version_option_reports_package_version():
    result = CliRunner().invoke(main, ["--version"])

    assert result.exit_code == 0
    assert f"chatbrowser, version {__version__}" in result.output


def test_tree_option_prints_shared_runtime_cli_tree_with_signatures():
    result = CliRunner().invoke(main, ["--tree"])

    assert result.exit_code == 0, result.output
    assert result.output.splitlines()[0] == "chatbrowser"
    assert "├── --tree  # Print the registered CLI tree and exit." in result.output
    assert "├── --tree-brief  # Print the registered CLI tree without parameter signatures and exit." in result.output
    assert "├── backend  # Discover browser backend executables" in result.output
    assert "│   ├── list [--output OUTPUT]  # List known browser backends without installing them" in result.output
    assert "├── profile  # Manage isolated browser profiles" in result.output
    assert "└── session  # Read registered browser sessions" in result.output
    assert "├── connect [--cdp-url CDP-URL] [--as-session-name SESSION-ID]" in result.output
    assert "├── disconnect <SESSION-ID> [--output OUTPUT]" in result.output
    assert "extension" not in result.output


def test_tree_brief_keeps_commands_and_descriptions_without_signatures():
    result = CliRunner().invoke(main, ["--tree-brief"])

    assert result.exit_code == 0, result.output
    assert result.output.splitlines()[0] == "chatbrowser"
    assert "│   ├── list  # List known browser backends without installing them." in result.output
    assert "├── connect  # Register an existing CDP endpoint without taking ownership." in result.output
    assert "└── session  # Read registered browser sessions." in result.output
    assert "[--output" not in result.output
    assert "<NAME>" not in result.output
    assert "CDP-URL" not in result.output
    assert "extension" not in result.output