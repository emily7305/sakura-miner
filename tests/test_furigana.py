from sakura_miner.furigana import to_ruby, token_ruby


def test_okurigana_left_bare():
    assert token_ruby("食べ", "たべ") == "<ruby>食<rt>た</rt></ruby>べ"


def test_kana_between_kanji():
    out = token_ruby("取り扱い", "とりあつかい")
    assert out == "<ruby>取<rt>と</rt></ruby>り<ruby>扱<rt>あつか</rt></ruby>い"


def test_no_alignment_falls_back_to_whole_word():
    assert token_ruby("今日", "きょう") == "<ruby>今日<rt>きょう</rt></ruby>"


def test_sentence():
    out = to_ruby("ケーキを食べた。")
    assert out == "ケーキを<ruby>食<rt>た</rt></ruby>べた。"


def test_kana_only_text_unchanged():
    assert to_ruby("とても") == "とても"


def test_escapes_html():
    assert to_ruby("<猫>").startswith("&lt;")
