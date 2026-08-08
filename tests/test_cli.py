from click.testing import CliRunner

from chatbrowser import __version__
from chatbrowser.cli import main


def test_version_option_reports_package_version():
    result = CliRunner().invoke(main, ["--version"])

    assert result.exit_code == 0
    assert f"chatbrowser, version {__version__}" in result.output


def test_tree_option_prints_registered_runtime_cli_tree():
    result = CliRunner().invoke(main, ["--tree"])

    assert result.exit_code == 0, result.output
    assert "chatbrowser  # ChatBrowser browser runtime metadata CLI" in result.output
    assert "├── --help  # Show help for the current command." in result.output
    assert "├── --version  # Show package version." in result.output
    assert "├── --tree  # Print the registered CLI tree." in result.output
    assert "├── backend  # Discover browser backend executables" in result.output
    assert "│   ├── list [--output text|json]  # List known browser backends without installing them" in result.output
    assert "├── profile  # Manage isolated browser profiles" in result.output
    assert "├── session  # Read registered browser sessions" in result.output
    assert "├── connect --cdp-url CDP-URL --as-session-name SESSION-ID" in result.output
    assert "└── disconnect SESSION-ID [--output text|json]" in result.output
    assert "extension" not in result.output