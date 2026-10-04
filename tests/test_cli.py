import sqlite3
import zipfile
from pathlib import Path

from click.testing import CliRunner

from sakura_miner.cli import main

SAMPLE = Path(__file__).parent / "fixtures" / "sample.txt"


def run(tmp_path, *args, known=None):
    # never pick up a real data/known_words.txt from the working directory
    known = known or tmp_path / "no_known.txt"
    out = tmp_path / "out.apkg"
    argv = [*args, "-o", str(out), "--known", str(known)]
    return CliRunner().invoke(main, argv), out


def read_fields(apkg, tmp_path):
    with zipfile.ZipFile(apkg) as z:
        z.extract("collection.anki2", tmp_path)
    con = sqlite3.connect(tmp_path / "collection.anki2")
    try:
        return [row[0] for row in con.execute("select flds from notes")]
    finally:
        con.close()


def test_writes_deck(tmp_path):
    result, out = run(tmp_path, str(SAMPLE))
    assert result.exit_code == 0, result.output
    assert out.stat().st_size > 0
    assert "cards written" in result.output
    assert "skipped as known: 0" in result.output


def test_limit(tmp_path):
    result, _ = run(tmp_path, str(SAMPLE), "--limit", "2")
    assert result.exit_code == 0
    assert "cards written: 2" in result.output


def test_known_words_skipped(tmp_path):
    known = tmp_path / "known.txt"
    known.write_text("食べる\nケーキ\n", encoding="utf-8")
    result, _ = run(tmp_path, str(SAMPLE), known=known)
    assert result.exit_code == 0, result.output
    assert "skipped as known: 2" in result.output


def test_level_filter(tmp_path):
    text = tmp_path / "in.txt"
    # 食べる is N5, ケーキ is N4, 賛成 is N3
    text.write_text("ケーキを食べた。賛成です。", encoding="utf-8")
    result, _ = run(tmp_path, str(text), "--level", "n4")
    assert result.exit_code == 0, result.output
    assert "skipped above N4: 1" in result.output


def test_bad_level(tmp_path):
    result, _ = run(tmp_path, str(SAMPLE), "--level", "N6")
    assert result.exit_code != 0


def test_subtitle_input(tmp_path):
    srt = Path(__file__).parent / "fixtures" / "sample.srt"
    result, _ = run(tmp_path, str(srt))
    assert result.exit_code == 0, result.output
    assert "words found: 8" in result.output


def test_sort_by_frequency(tmp_path):
    text = tmp_path / "in.txt"
    text.write_text("犬を見た。猫がいる。猫が好き。", encoding="utf-8")
    result, out = run(tmp_path, str(text), "--sort", "frequency", "--limit", "1")
    assert result.exit_code == 0, result.output
    notes = read_fields(out, tmp_path)
    assert notes[0].startswith("猫")


def test_missing_file(tmp_path):
    result, _ = run(tmp_path, str(tmp_path / "nope.txt"))
    assert result.exit_code != 0
    assert "file not found" in result.output


def test_not_utf8(tmp_path):
    bad = tmp_path / "bad.txt"
    bad.write_bytes("日本語".encode("shift_jis"))
    result, _ = run(tmp_path, str(bad))
    assert result.exit_code != 0
    assert "utf-8" in result.output
