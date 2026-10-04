from sakura_miner.jlpt import at_or_below, get_level, load_levels


def write_lists(tmp_path):
    (tmp_path / "n5.csv").write_text(
        "word,reading,level\n猫,ねこ,N5\n上手,じょうず,N5\n",
        encoding="utf-8",
    )
    (tmp_path / "n3.csv").write_text(
        "word,reading,level\n上手,うわて,N3\n猫,ねこ,N3\n賛成,さんせい,N3\n,,N3\n",
        encoding="utf-8",
    )
    return tmp_path


def test_missing_directory(tmp_path):
    assert get_level("猫", "ねこ", tmp_path / "nope") is None


def test_exact_match(tmp_path):
    d = write_lists(tmp_path)
    assert get_level("賛成", "さんせい", d) == "N3"


def test_reading_picks_level(tmp_path):
    d = write_lists(tmp_path)
    assert get_level("上手", "じょうず", d) == "N5"
    assert get_level("上手", "うわて", d) == "N3"


def test_easiest_level_wins(tmp_path):
    d = write_lists(tmp_path)
    assert get_level("猫", "ねこ", d) == "N5"


def test_kana_listing_counts(tmp_path):
    (tmp_path / "n5.csv").write_text(
        "word,reading,level\nおもしろい,おもしろい,N5\n", encoding="utf-8"
    )
    (tmp_path / "n1.csv").write_text(
        "word,reading,level\n面白い,おもしろい,N1\n", encoding="utf-8"
    )
    assert get_level("面白い", "おもしろい", tmp_path) == "N5"


def test_falls_back_to_word_only(tmp_path):
    d = write_lists(tmp_path)
    assert get_level("賛成", "さんせ", d) == "N3"


def test_unknown_word(tmp_path):
    d = write_lists(tmp_path)
    assert get_level("犬", "いぬ", d) is None


def test_blank_rows_ignored(tmp_path):
    d = write_lists(tmp_path)
    assert ("", "") not in load_levels(d)


def test_at_or_below():
    assert at_or_below("N5", "N3")
    assert at_or_below("N3", "N3")
    assert not at_or_below("N2", "N3")
    assert at_or_below(None, "N3")


def test_bundled_lists():
    assert get_level("食べる", "たべる") == "N5"
    assert get_level("面白い", "おもしろい") == "N5"
    assert get_level("賛成", "さんせい") == "N3"
