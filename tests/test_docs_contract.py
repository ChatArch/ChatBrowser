from pathlib import Path


def test_mkdocs_material_i18n_public_domain_and_icon_renderer():
    mkdocs = Path("mkdocs.yml").read_text(encoding="utf-8")
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")

    assert "site_url: https://arch.gh.wzhecnu.cn/ChatBrowser/" in mkdocs
    assert "repo_url: https://github.com/ChatArch/ChatBrowser" in mkdocs
    assert "name: material" in mkdocs
    assert "- i18n:" in mkdocs
    assert "docs_structure: suffix" in mkdocs
    assert "mkdocs-static-i18n" in pyproject
    assert "pymdownx.emoji" in mkdocs
    assert "material.extensions.emoji.twemoji" in mkdocs
    assert "material.extensions.emoji.to_svg" in mkdocs


def test_cli_tree_docs_remain_bilingual():
    assert Path("docs/cli-tree.md").exists()
    assert Path("docs/cli-tree.en.md").exists()
    assert "chatbrowser --tree" in Path("docs/cli-tree.md").read_text(encoding="utf-8")
    assert "chatbrowser --tree" in Path("docs/cli-tree.en.md").read_text(encoding="utf-8")
