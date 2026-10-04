from sakura_miner.filter import load_known, remove_known
from sakura_miner.models import Word


def make_word(lemma, reading):
    return Word(surface=lemma, lemma=lemma, reading=reading, pos="名詞", sentence="")


def write(tmp_path, text):
    path = tmp_path / "known.txt"
    path.write_text(text, encoding="utf-8")
    return path


def test_missing_file_is_empty(tmp_path):
    assert load_known(tmp_path / "nope.txt") == set()


def test_comments_and_blank_lines(tmp_path):
    path = write(tmp_path, "# my words\n\n猫\n  犬  \n食べる # week 1\n#駅\n")
    assert load_known(path) == {"猫", "犬", "食べる"}


def test_tab_pairs(tmp_path):
    path = write(tmp_path, "上手\tじょうず\n")
    assert load_known(path) == {"上手\tじょうず"}


def test_bom_is_ignored(tmp_path):
    path = tmp_path / "known.txt"
    path.write_text("猫\n", encoding="utf-8-sig")
    assert load_known(path) == {"猫"}


def test_remove_by_lemma():
    words = [make_word("猫", "ねこ"), make_word("駅", "えき")]
    assert remove_known(words, {"猫"}) == [make_word("駅", "えき")]


def test_tab_pair_only_matches_that_reading():
    words = [make_word("上手", "じょうず"), make_word("上手", "うわて")]
    left = remove_known(words, {"上手\tじょうず"})
    assert left == [make_word("上手", "うわて")]


def test_nothing_known():
    words = [make_word("猫", "ねこ")]
    assert remove_known(words, set()) == words
