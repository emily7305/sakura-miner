import re

import fugashi
import jaconv

from sakura_miner.models import Word

# 形状詞 covers na-adjectives like 静か
CONTENT_POS = {"名詞", "動詞", "形容詞", "形状詞", "副詞"}
INFLECTING_POS = {"動詞", "形容詞", "形状詞"}

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


def _full_surface(tokens, i: int) -> str:
    # pull in the endings so 食べ + た shows up as 食べた on the card
    surface = tokens[i].surface
    if tokens[i].feature.pos1 not in INFLECTING_POS:
        return surface
    for token in tokens[i + 1 :]:
        pos1 = token.feature.pos1
        if pos1 == "助動詞" or (pos1 == "助詞" and token.surface in ("て", "で")):
            surface += token.surface
        else:
            break
    return surface


def tokenize(text: str) -> list[Word]:
    """Return content words from text, deduplicated on (lemma, reading).

    The first sentence a word shows up in is kept.
    """
    tagger = get_tagger()
    seen: set[tuple[str, str]] = set()
    words: list[Word] = []
    for sentence in split_sentences(text):
        tokens = list(tagger(sentence))
        for i, token in enumerate(tokens):
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
                    surface=_full_surface(tokens, i),
                    lemma=lemma,
                    reading=reading,
                    pos=token.feature.pos1,
                    sentence=sentence,
                )
            )
    return words
