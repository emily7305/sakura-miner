from sakura_miner.lookup import lookup, meanings
from sakura_miner.models import Word


def make_word(lemma, reading):
    return Word(surface=lemma, lemma=lemma, reading=reading, pos="名詞", sentence="")


def test_common_word_has_glosses():
    assert "to eat" in meanings("食べる", "たべる")


def test_at_most_three_glosses():
    assert len(meanings("行く", "いく")) <= 3


def test_reading_picks_matching_entry():
    assert "skillful" in meanings("上手", "じょうず")
    assert "skillful" not in meanings("上手", "うわて")


def test_unknown_reading_falls_back_to_first_entry():
    assert meanings("駅", "xxx") == meanings("駅", "えき")


def test_unknown_word_returns_empty():
    assert meanings("ほげほげぴよ", "ほげほげぴよ") == []


def test_empty_lemma():
    assert meanings("", "") == []


def test_wildcard_characters_not_matched():
    assert meanings("_", "") == []
    assert meanings("食べ%", "") == []


def test_lookup_returns_entry():
    word = make_word("猫", "ねこ")
    entry = lookup(word)
    assert entry.word == word
    assert entry.meanings[0].startswith("cat")
    assert entry.level is None
