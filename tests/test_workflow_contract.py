from pathlib import Path


def test_publish_workflow_uses_oidc_with_release_guards():
    workflow = Path(".github/workflows/publish.yml").read_text(encoding="utf-8")

    assert "id-token: write" in workflow
    assert "pypa/gh-action-pypi-publish@release/v1" in workflow
    assert "Check tag matches package version" in workflow
    assert "Check release commit is on default branch" in workflow
    assert "git fetch --no-tags origin main:refs/remotes/origin/main" in workflow
    assert "Check PyPI version" in workflow
    assert "environment: pypi" not in workflow


def test_preview_workflow_derives_public_url_from_site_url():
    workflow = Path(".github/workflows/preview.yaml").read_text(encoding="utf-8")

    assert "site_url" in workflow
    assert "CHATARCH_PREVIEW_URL" in workflow
    assert "${site_url}/dev/" in workflow
    assert "github.io/${repo}/dev" not in workflow
    assert "Preview available at:" in workflow
