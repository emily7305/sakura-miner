from pathlib import Path

from click.testing import CliRunner

from sakura_miner.cli import main

SAMPLE = Path(__file__).parent / "fixtures" / "sample.txt"


def test_writes_deck(tmp_path):
    out = tmp_path / "out.apkg"
    result = CliRunner().invoke(main, [str(SAMPLE), "-o", str(out)])
    assert result.exit_code == 0, result.output
    assert out.stat().st_size > 0
    assert "cards written" in result.output


def test_limit(tmp_path):
    out = tmp_path / "out.apkg"
    result = CliRunner().invoke(main, [str(SAMPLE), "-o", str(out), "--limit", "2"])
    assert result.exit_code == 0
    assert "cards written: 2" in result.output


def test_missing_file(tmp_path):
    result = CliRunner().invoke(main, [str(tmp_path / "nope.txt")])
    assert result.exit_code != 0
    assert "file not found" in result.output


def test_not_utf8(tmp_path):
    bad = tmp_path / "bad.txt"
    bad.write_bytes("日本語".encode("shift_jis"))
    result = CliRunner().invoke(main, [str(bad), "-o", str(tmp_path / "x.apkg")])
    assert result.exit_code != 0
    assert "utf-8" in result.output
