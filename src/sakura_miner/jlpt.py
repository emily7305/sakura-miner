import csv
from pathlib import Path

LEVELS = ("N1", "N2", "N3", "N4", "N5")

DEFAULT_DIR = Path(__file__).resolve().parents[2] / "data" / "jlpt"

Table = dict[tuple[str, str], str]

_tables: dict[Path, Table] = {}


def easier(a: str | None, b: str) -> str:
    # N5 is the easiest, so a bigger number wins
    if a is None or int(b[1]) > int(a[1]):
        return b
    return a


def load_levels(directory: Path = DEFAULT_DIR) -> Table:
    """Read every CSV in directory into {(word, reading): level}.

    Each word is also stored under (word, "") so it can be found without a
    reading. A word listed at several levels keeps the easiest one.
    """
    if directory in _tables:
        return _tables[directory]
    table: Table = {}
    if directory.is_dir():
        for path in sorted(directory.glob("*.csv")):
            with path.open(encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    level = (row.get("level") or "").strip().upper()
                    word = (row.get("word") or "").strip()
                    if level not in LEVELS or not word:
                        continue
                    reading = (row.get("reading") or "").strip()
                    for key in ((word, reading), (word, "")):
                        table[key] = easier(table.get(key), level)
    _tables[directory] = table
    return table


def get_level(lemma: str, reading: str, directory: Path = DEFAULT_DIR) -> str | None:
    table = load_levels(directory)
    # the tanos lists often give easy words in kana only (おもしろい at N5)
    # while the kanji spelling sits in a harder list, so check both
    level = None
    for key in ((lemma, reading), (reading, reading)):
        if key in table:
            level = easier(level, table[key])
    return level or table.get((lemma, ""))


def at_or_below(level: str | None, limit: str) -> bool:
    """True if level is no harder than limit. Words with no level always pass."""
    if level is None:
        return True
    return int(level[1]) >= int(limit[1])
