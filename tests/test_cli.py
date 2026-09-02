"""Tests du CLI.

- Tests unitaires : appel direct de `main()` (stdin/stdout pilotés),
  pour une couverture réelle du module.
- Smoke test : exécution du vrai `python -m bttf.cli` dans un
  sous-processus, pour vérifier le lancement réel.
"""

import io
import subprocess
import sys
from pathlib import Path

import pytest

from bttf.cli import main

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run_main(
    cart_text: str, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> tuple[int, str, str]:
    """Exécute main() avec stdin contrôlé et capture sorties."""
    monkeypatch.setattr(sys, "stdin", io.StringIO(cart_text))
    exit_code = main()
    captured = capsys.readouterr()
    return exit_code, captured.out, captured.err


def test_cli_prints_total_for_golden_example_1(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Given
    cart = "Back to the Future 1\nBack to the Future 2\nBack to the Future 3\n"

    # When
    exit_code, out, _ = _run_main(cart, monkeypatch, capsys)

    # Then
    assert exit_code == 0
    assert out.strip() == "36"


def test_cli_prints_total_with_other_movie(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Given
    cart = "Back to the Future 1\nBack to the Future 2\nBack to the Future 3\nLa chèvre\n"

    # When
    exit_code, out, _ = _run_main(cart, monkeypatch, capsys)

    # Then
    assert exit_code == 0
    assert out.strip() == "56"


def test_cli_empty_input_prints_zero(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code, out, _ = _run_main("", monkeypatch, capsys)
    assert exit_code == 0
    assert out.strip() == "0"


def test_cli_unknown_movie_exits_with_error_message(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code, out, err = _run_main("Back to the Future 4\n", monkeypatch, capsys)
    assert exit_code == 2
    assert "film inconnu" in err.lower()
    assert out == ""


def test_cli_runs_as_real_module() -> None:
    """Smoke test : `python -m bttf.cli` fonctionne de bout en bout."""
    result = subprocess.run(
        [sys.executable, "-m", "bttf.cli"],
        input="Back to the Future 1\nBack to the Future 2\n",
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={"PYTHONPATH": str(REPO_ROOT / "src"), "PATH": "/usr/bin:/bin"},
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "27"
