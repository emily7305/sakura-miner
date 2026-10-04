from pathlib import Path

from sakura_miner.models import Word


def load_known(path: Path) -> set[str]:
    """Read a known-words file into a set of lemmas and lemma<TAB>reading pairs.

    A missing file just means nothing is known yet.
    """
    if not path.exists():
        return set()
    known = set()
    # utf-8-sig so files saved by Notepad with a BOM still match
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if "\t" in line:
            lemma, reading = (part.strip() for part in line.split("\t", 1))
            known.add(f"{lemma}\t{reading}")
        else:
            known.add(line)
    return known


def is_known(word: Word, known: set[str]) -> bool:
    return word.lemma in known or f"{word.lemma}\t{word.reading}" in known


def remove_known(words: list[Word], known: set[str]) -> list[Word]:
    return [w for w in words if not is_known(w, known)]
