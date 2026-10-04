from pathlib import Path

from sakura_miner.subtitles import ass_to_text, read_input, srt_to_text

FIXTURES = Path(__file__).parent / "fixtures"

EXPECTED = "昨日、友達とケーキを食べた。\nとても美味しかった！\n明日も一緒に食べよう。"


def test_srt():
    assert read_input(FIXTURES / "sample.srt") == EXPECTED


def test_ass():
    assert read_input(FIXTURES / "sample.ass") == EXPECTED


def test_plain_text_untouched():
    text = (FIXTURES / "sample.txt").read_text(encoding="utf-8")
    assert read_input(FIXTURES / "sample.txt") == text


def test_srt_with_period_timestamps():
    srt = "1\n00:00:01.000 --> 00:00:02.000\n猫が好き\n"
    assert srt_to_text(srt) == "猫が好き"


def test_ass_text_with_commas():
    ass = (
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, "
        "Effect, Text\n"
        "Dialogue: 0,0:00:01.00,0:00:02.00,Default,,0,0,0,,はい、そうです\n"
    )
    assert ass_to_text(ass) == "はい、そうです"


def test_ass_hard_space():
    ass = "[Events]\nDialogue: 0,0,0,Default,,0,0,0,,猫\\h犬\n"
    assert ass_to_text(ass) == "猫 犬"


def test_bom(tmp_path):
    path = tmp_path / "bom.srt"
    path.write_text("1\n00:00:01,000 --> 00:00:02,000\n猫\n", encoding="utf-8-sig")
    assert read_input(path) == "猫"
