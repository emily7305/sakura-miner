from pathlib import Path

from sakura_miner.tokenizer import split_sentences, tokenize

FIXTURES = Path(__file__).parent / "fixtures"


def lemmas(words):
    return [w.lemma for w in words]


def test_conjugated_verb_becomes_dictionary_form():
    words = tokenize("ケーキを食べた。")
    assert "食べる" in lemmas(words)
    assert "食べ" not in lemmas(words)


def test_particles_and_punctuation_dropped():
    words = tokenize("私は猫が好きです。")
    for dropped in ["は", "が", "です", "。"]:
        assert dropped not in lemmas(words)
    assert "猫" in lemmas(words)


def test_reading_is_hiragana():
    words = tokenize("駅に行く。")
    eki = next(w for w in words if w.lemma == "駅")
    assert eki.reading == "えき"


def test_katakana_word_keeps_katakana_reading():
    words = tokenize("テレビを見る。")
    tv = next(w for w in words if w.lemma == "テレビ")
    assert tv.reading == "テレビ"


def test_duplicates_keep_first_sentence():
    words = tokenize("ケーキを食べた。また食べたい。")
    taberu = [w for w in words if w.lemma == "食べる"]
    assert len(taberu) == 1
    assert taberu[0].sentence == "ケーキを食べた。"


def test_numbers_skipped():
    words = tokenize("3人が来た。")
    assert "3" not in lemmas(words)


def test_empty_input():
    assert tokenize("") == []
    assert tokenize("   \n\n") == []


def test_no_japanese():
    assert tokenize("!!! ... ???") == []


def test_split_sentences():
    text = "おはよう。元気？\nうん！"
    assert split_sentences(text) == ["おはよう。", "元気？", "うん！"]


def test_sample_file():
    text = (FIXTURES / "sample.txt").read_text(encoding="utf-8")
    words = tokenize(text)
    assert "食べる" in lemmas(words)
    assert all(w.sentence for w in words)
