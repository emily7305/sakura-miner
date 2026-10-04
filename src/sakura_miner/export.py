import html
from pathlib import Path

import genanki

from sakura_miner.models import Entry

# fixed ids so re-importing updates existing cards instead of adding copies
MODEL_ID = 1607392319
DECK_ID = 2059400110

CARD_CSS = """
.card {
  font-family: "Hiragino Sans", "Noto Sans JP", "Yu Gothic", sans-serif;
  font-size: 20px;
  text-align: center;
  color: #4a3f4b;
  background-color: #fff7fa;
  padding: 24px;
}
.word { font-size: 48px; margin: 12px 0; }
.reading { font-size: 24px; color: #b5838d; }
.meaning { margin: 16px 0; color: #5e548e; }
.sentence {
  display: inline-block;
  margin-top: 8px;
  padding: 10px 16px;
  border-radius: 12px;
  background-color: #fde2e4;
  font-size: 22px;
}
.level {
  margin-top: 16px;
  font-size: 14px;
  color: #9a8c98;
}
hr#answer { border: none; border-top: 1px dashed #e5b3bb; }
"""

FRONT = '<div class="word">{{Word}}</div>'

BACK = """{{FrontSide}}
<hr id="answer">
<div class="reading">{{Reading}}</div>
<div class="meaning">{{Meaning}}</div>
<div class="sentence">{{Sentence}}</div>
{{#Level}}<div class="level">{{Level}}</div>{{/Level}}
"""

MODEL = genanki.Model(
    MODEL_ID,
    "Sakura Miner",
    fields=[
        {"name": "Word"},
        {"name": "Reading"},
        {"name": "Meaning"},
        {"name": "Sentence"},
        {"name": "Level"},
    ],
    templates=[{"name": "Recognition", "qfmt": FRONT, "afmt": BACK}],
    css=CARD_CSS,
)


def note_guid(entry: Entry) -> str:
    return genanki.guid_for(entry.word.lemma, entry.word.reading)


def make_note(entry: Entry) -> genanki.Note:
    word = entry.word
    fields = [
        html.escape(word.lemma),
        html.escape(word.reading),
        html.escape("; ".join(entry.meanings)),
        html.escape(word.sentence),
        entry.level or "",
    ]
    tags = [entry.level] if entry.level else []
    return genanki.Note(model=MODEL, fields=fields, tags=tags, guid=note_guid(entry))


def build_deck(entries: list[Entry], deck_name: str = "Sakura Miner") -> genanki.Deck:
    deck = genanki.Deck(DECK_ID, deck_name)
    for entry in entries:
        deck.add_note(make_note(entry))
    return deck


def write_deck(
    entries: list[Entry], path: Path, deck_name: str = "Sakura Miner"
) -> None:
    """Write entries to an Anki .apkg file at path."""
    genanki.Package(build_deck(entries, deck_name)).write_to_file(str(path))
