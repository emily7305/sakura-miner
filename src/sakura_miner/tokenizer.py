import re

import fugashi
import jaconv

from sakura_miner.models import Word

# 形状詞 covers na-adjectives like 静か
CONTENT_POS = {"名詞", "動詞", "形容詞", "形状詞", "副詞"}

SENTENCE_END = re.compile(r"(?<=[。！？!?])|\n")
KATAKANA_ONLY = re.compile(r"^[゠-ヿー]+$")

_tagger: fugashi.Tagger | None = None


def get_tagger() -> fugashi.Tagger:
    global _tagger
    if _tagger is None:
        _tagger = fugashi.Tagger()
    return _tagger


def split_sentences(text: str) -> list[str]:
    parts = SENTENCE_END.split(text)
    return [p.strip() for p in parts if p and p.strip()]


def _lemma(token) -> str:
    # orthBase keeps the spelling from the text (とても, not 迚も)
    base = getattr(token.feature, "orthBase", None)
    if base:
        return base
    lemma = getattr(token.feature, "lemma", None)
    if lemma:
        # loanwords come back as テレビ-television
        return lemma.split("-")[0]
    return token.surface


def _reading(token, lemma: str) -> str:
    kana = getattr(token.feature, "lForm", None) or token.surface
    if KATAKANA_ONLY.match(lemma):
        return kana
    return jaconv.kata2hira(kana)


def _is_content(token) -> bool:
    pos1 = getattr(token.feature, "pos1", None)
    pos2 = getattr(token.feature, "pos2", None)
    if pos1 not in CONTENT_POS:
        return False
    return pos2 != "数詞"


def tokenize(text: str) -> list[Word]:
    """Return content words from text, deduplicated on (lemma, reading).

    The first sentence a word shows up in is kept.
    """
    tagger = get_tagger()
    seen: set[tuple[str, str]] = set()
    words: list[Word] = []
    for sentence in split_sentences(text):
        for token in tagger(sentence):
            if not _is_content(token):
                continue
            lemma = _lemma(token)
            reading = _reading(token, lemma)
            key = (lemma, reading)
            if key in seen:
                continue
            seen.add(key)
            words.append(
                Word(
                    surface=token.surface,
                    lemma=lemma,
                    reading=reading,
                    pos=token.feature.pos1,
                    sentence=sentence,
                )
            )
    return words
