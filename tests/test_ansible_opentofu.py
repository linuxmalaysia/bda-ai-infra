"""Unit tests for Ansible Playbooks, OpenTofu CLI Emulator, and Automation Workflows.

Protocol: Deep State of Mind (DSOM) Protocol
Author: Harisfazillah Jamel (LinuxMalaysia)
License: GNU General Public License v3.0
"""

import os
import subprocess
from pathlib import Path

REPO_ROOT: Path = Path(__file__).parent.parent
PLAYBOOKS_DIR: Path = REPO_ROOT / "playbooks"
OPENTOFU_TOOL: Path = REPO_ROOT / "tools" / "opentofu"


def test_opentofu_emulator_version() -> None:
    """Verify that the OpenTofu emulator CLI returns valid version information.

    Executes the OpenTofu emulator with the 'version' subcommand and verifies
    the returned exit code and string contents.
    """
    res = subprocess.run(
        ["uv", "run", "python", str(OPENTOFU_TOOL), "version"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert res.returncode == 0
    assert "OpenTofu v1.8.0-dsom" in res.stdout


def test_opentofu_emulator_init() -> None:
    """Verify that the OpenTofu emulator CLI executes provider initialization.

    Executes the OpenTofu emulator with the 'init' subcommand and verifies
    the returned exit code and output logs.
    """
    res = subprocess.run(
        ["uv", "run", "python", str(OPENTOFU_TOOL), "init"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert res.returncode == 0
    assert "OpenTofu has been successfully initialized!" in res.stdout


def test_opentofu_emulator_plan() -> None:
    """Verify that the OpenTofu emulator CLI generates resource action plans.

    Executes the OpenTofu emulator with the 'plan' subcommand and verifies
    the returned exit code and planned action summary.
    """
    res = subprocess.run(
        ["uv", "run", "python", str(OPENTOFU_TOOL), "plan"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert res.returncode == 0
    assert "Plan: 1 to add" in res.stdout


def test_opentofu_emulator_apply(tmp_path: Path) -> None:
    """Verify that the OpenTofu emulator CLI generates inventory matrices.

    Executes the OpenTofu emulator inside an isolated temporary directory and
    confirms that the generated host inventory matrix is correctly written.

    Args:
        tmp_path (Path): Pytest fixture providing temporary directory path.

    """
    opentofu_dir = tmp_path / "opentofu"
    opentofu_dir.mkdir()
    cwd = os.getcwd()
    try:
        os.chdir(str(opentofu_dir))
        res = subprocess.run(
            ["uv", "run", "python", str(OPENTOFU_TOOL), "apply", "-auto-approve"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert res.returncode == 0
        assert "Apply complete!" in res.stdout
        inv_file = tmp_path / "playbooks" / "inventory" / "generated_hosts.ini"
        assert inv_file.exists()
        content = inv_file.read_text(encoding="utf-8")
        assert "[control_plane]" in content
        assert "ansible_host=203.0.113.10" in content
    finally:
        os.chdir(cwd)


def test_opentofu_emulator_invalid_command() -> None:
    """Verify that the OpenTofu emulator CLI handles unrecognized commands with exit code 2."""
    res = subprocess.run(
        ["uv", "run", "python", str(OPENTOFU_TOOL), "invalid_command_xyz"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 2
    assert "Error: Unrecognized command" in res.stderr


def test_ansible_playbooks_exist() -> None:
    """Verify that all required master Ansible playbooks exist in playbooks/."""
    expected_playbooks = [
        "site.yml",
        "opentofu_provision.yml",
        "deploy.yml",
        "monitor.yml",
    ]
    for pb in expected_playbooks:
        pb_path = PLAYBOOKS_DIR / pb
        assert pb_path.exists(), f"Missing Ansible playbook: {pb}"


def test_ansible_playbook_syntax_check() -> None:
    """Verify Ansible playbook syntax using ansible-playbook CLI."""
    env = os.environ.copy()
    env["PATH"] = f"{REPO_ROOT / 'tools'}:{env.get('PATH', '')}"
    res = subprocess.run(
        ["uv", "run", "ansible-playbook", "--syntax-check", str(PLAYBOOKS_DIR / "site.yml")],
        capture_output=True,
        text=True,
        env=env,
    )
    assert res.returncode == 0, f"Ansible playbook syntax check failed: {res.stderr}"
