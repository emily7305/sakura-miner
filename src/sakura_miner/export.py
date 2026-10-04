import html
from pathlib import Path

import genanki

from sakura_miner.furigana import to_ruby
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
  line-height: 2;
  border-radius: 12px;
  background-color: #fde2e4;
  font-size: 22px;
}
.sentence .target {
  color: #d1477a;
  font-weight: bold;
}
.sentence rt {
  font-size: 0.55em;
  color: #b5838d;
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

# only created when the Reverse field is filled in
REVERSE_FRONT = '{{#Reverse}}<div class="meaning">{{Meaning}}</div>{{/Reverse}}'

REVERSE_BACK = """{{FrontSide}}
<hr id="answer">
<div class="word">{{Word}}</div>
<div class="reading">{{Reading}}</div>
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
        {"name": "Reverse"},
    ],
    templates=[
        {"name": "Recognition", "qfmt": FRONT, "afmt": BACK},
        {"name": "Production", "qfmt": REVERSE_FRONT, "afmt": REVERSE_BACK},
    ],
    css=CARD_CSS,
)


def note_guid(entry: Entry) -> str:
    return genanki.guid_for(entry.word.lemma, entry.word.reading)


def highlight(sentence: str, target: str, furigana: bool = False) -> str:
    """Escape sentence for HTML and wrap the first match of target in a span.

    With furigana, readings are added over the kanji as <ruby> tags.
    """
    render = to_ruby if furigana else html.escape
    start = sentence.find(target) if target else -1
    if start == -1:
        return render(sentence)
    end = start + len(target)
    return (
        render(sentence[:start])
        + f'<span class="target">{render(target)}</span>'
        + render(sentence[end:])
    )


def make_note(
    entry: Entry, reverse: bool = False, furigana: bool = False
) -> genanki.Note:
    word = entry.word
    fields = [
        html.escape(word.lemma),
        html.escape(word.reading),
        html.escape("; ".join(entry.meanings)),
        highlight(word.sentence or word.surface, word.surface, furigana),
        entry.level or "",
        "y" if reverse else "",
    ]
    tags = [entry.level] if entry.level else []
    return genanki.Note(model=MODEL, fields=fields, tags=tags, guid=note_guid(entry))


def build_deck(
    entries: list[Entry],
    deck_name: str = "Sakura Miner",
    reverse: bool = False,
    furigana: bool = False,
) -> genanki.Deck:
    deck = genanki.Deck(DECK_ID, deck_name)
    for entry in entries:
        deck.add_note(make_note(entry, reverse, furigana))
    return deck


def write_deck(
    entries: list[Entry],
    path: Path,
    deck_name: str = "Sakura Miner",
    reverse: bool = False,
    furigana: bool = False,
) -> None:
    """Write entries to an Anki .apkg file at path.

    With reverse, each note also gets a meaning-to-word card. With furigana,
    the sentence gets readings over its kanji.
    """
    deck = build_deck(entries, deck_name, reverse, furigana)
    genanki.Package(deck).write_to_file(str(path))
