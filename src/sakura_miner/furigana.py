import html
import re

import jaconv

from sakura_miner.tokenizer import get_tagger

KANJI = re.compile(r"[一-鿿々]")
KANJI_RUN = re.compile(r"([一-鿿々]+)")


def ruby(base: str, reading: str) -> str:
    return f"<ruby>{html.escape(base)}<rt>{html.escape(reading)}</rt></ruby>"


def token_ruby(surface: str, reading: str) -> str:
    """Put furigana over the kanji in surface, leaving okurigana bare.

    取り扱い with とりあつかい becomes 取[と]り扱[あつか]い.
    """
    parts = KANJI_RUN.split(surface)
    # odd indexes are kanji runs, even ones are the kana between them
    pattern = "".join(
        "(.+?)" if i % 2 else re.escape(jaconv.kata2hira(p))
        for i, p in enumerate(parts)
    )
    match = re.fullmatch(pattern, reading)
    if not match:
        return ruby(surface, reading)
    out = []
    groups = iter(match.groups())
    for i, part in enumerate(parts):
        out.append(ruby(part, next(groups)) if i % 2 else html.escape(part))
    return "".join(out)


def to_ruby(text: str) -> str:
    """Return text as HTML with furigana over every word that has kanji."""
    out = []
    for token in get_tagger()(text):
        surface = token.surface
        kana = getattr(token.feature, "kana", None)
        if kana and KANJI.search(surface):
            out.append(token_ruby(surface, jaconv.kata2hira(kana)))
        else:
            out.append(html.escape(surface))
    return "".join(out)
