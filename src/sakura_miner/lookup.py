from jamdict import Jamdict

from sakura_miner.models import Entry, Word

MAX_GLOSSES = 3

_jam: Jamdict | None = None


def get_jamdict() -> Jamdict:
    # slow to start, so only build it once
    global _jam
    if _jam is None:
        _jam = Jamdict()
    return _jam


def _pick_entry(entries, reading: str):
    for entry in entries:
        if any(k.text == reading for k in entry.kana_forms):
            return entry
    return entries[0]


def meanings(lemma: str, reading: str) -> list[str]:
    """Return up to 3 English glosses for the best matching JMdict entry."""
    # jamdict treats % and _ as sql wildcards
    if not lemma.strip() or "%" in lemma or "_" in lemma:
        return []
    result = get_jamdict().lookup(lemma, strict_lookup=True)
    if not result.entries:
        return []
    entry = _pick_entry(result.entries, reading)
    if not entry.senses:
        return []
    return [g.text for g in entry.senses[0].gloss][:MAX_GLOSSES]


def lookup(word: Word) -> Entry:
    return Entry(word=word, meanings=meanings(word.lemma, word.reading))
