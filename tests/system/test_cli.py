import datetime
import subprocess
import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def run_cli(directory, stdin: str):
    return subprocess.run(
        [sys.executable, "main.py", str(directory)],
        input=stdin, capture_output=True, text=True, cwd=ROOT, timeout=30,
    )

def test_cli_rejects_invalid_directory(tmp_path):
    result = run_cli(tmp_path / "nope", "")
    assert result.returncode == 2
    assert "not a valid directory" in result.stderr

def test_cli_full_run(tmp_path, make_jpeg):
    make_jpeg("x.jpg", datetime.datetime(2024, 5, 1, 9, 0))
    result = run_cli(tmp_path, "2\n1\n1\n1\n")
    assert result.returncode == 0
    assert (tmp_path / "2024-05-01-00001.jpg").exists()

def test_cli_quit_changes_nothing(tmp_path, make_jpeg):
    make_jpeg("x.jpg", datetime.datetime(2024, 5, 1, 9, 0))
    assert run_cli(tmp_path, "3\n").returncode == 0
    assert (tmp_path / "x.jpg").exists()