from dataclasses import dataclass


@dataclass(frozen=True)
class Word:
    surface: str
    lemma: str
    reading: str
    pos: str
    sentence: str


@dataclass
class Entry:
    word: Word
    meanings: list[str]
    level: str | None = None
