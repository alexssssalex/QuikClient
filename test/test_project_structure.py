from src.config import VERSION, PROJECT_NAME
import re
from pathlib import Path


def get_value(file_name: str, reg_expr: str) -> str:
    with open(file_name) as f:
        for line in f:
            matches = re.findall(reg_expr, line)
            if matches:
                return matches[0]


def test_changelog_version():
    version_in_changelog = get_value("../CHANGELOG.md", r"\s*##\s*(\d+.\d+.\d+)\s+$")
    assert version_in_changelog == VERSION


def test_setupcfg_version():
    version_in_setupcfg = get_value("../setup.cfg", r"version\s*=\s*(\d+.\d+.\d+)\s*$")
    assert version_in_setupcfg == VERSION


def test_setupcfg_project_name():
    version_in_setupcfg = get_value("../setup.cfg", r"name\s*=\s*(\w*)\s*$")
    assert version_in_setupcfg == PROJECT_NAME


def test_doc_conf_project_name():
    version_in_setupcfg = get_value("../doc/source/conf.py", r"project\s*=\s*'(\w*)'\s*$")
    assert version_in_setupcfg == PROJECT_NAME


def test_doc_conf_version():
    version_in_setupcfg = get_value("../doc/source/conf.py", r"release\s*=\s*'(\d+.\d+.\d+)'\s*$")
    assert version_in_setupcfg == VERSION


def test_is_folder_doc_exist():
    assert Path("../doc").is_dir()


def test_is_folder_src_exist():
    assert Path("../src").is_dir()


def test_is_folder_test_exist():
    assert Path("../test").is_dir()


def test_is_file_changelog_exist():
    assert Path("../CHANGELOG.md").is_file()


def test_is_file_pyproject_exist():
    assert Path("../pyproject.toml").is_file()


def test_is_file_readme_exist():
    assert Path("../README.md").is_file()


def test_is_file_setup_exist():
    assert Path("../setup.cfg").is_file()


def test_is_file_config_exist():
    assert Path("../src/config.py").is_file()


def test_is_file_doc_config_exist():
    assert Path("../doc/source/conf.py").is_file()


def test_is_file_doc_index_exist():
    assert Path("../doc/source/index.rst").is_file()


def test_is_gitignore():
    assert Path("../.gitignore").is_file()
