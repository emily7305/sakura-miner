import sqlite3
import zipfile

from sakura_miner.export import build_deck, make_note, note_guid, write_deck
from sakura_miner.models import Entry, Word


def make_entry(lemma="食べる", reading="たべる", level=None):
    word = Word(
        surface="食べ",
        lemma=lemma,
        reading=reading,
        pos="動詞",
        sentence="ケーキを食べた。",
    )
    return Entry(word=word, meanings=["to eat"], level=level)


def read_notes(path, tmp_path):
    with zipfile.ZipFile(path) as z:
        z.extract("collection.anki2", tmp_path)
    con = sqlite3.connect(tmp_path / "collection.anki2")
    try:
        return con.execute("select guid, flds, tags from notes").fetchall()
    finally:
        con.close()


def test_guid_is_stable():
    assert note_guid(make_entry()) == note_guid(make_entry())


def test_guid_depends_on_reading():
    a = make_entry("上手", "じょうず")
    b = make_entry("上手", "うわて")
    assert note_guid(a) != note_guid(b)


def test_note_fields():
    note = make_note(make_entry())
    assert note.fields == ["食べる", "たべる", "to eat", "ケーキを食べた。", ""]
    assert note.tags == []


def test_level_becomes_tag():
    note = make_note(make_entry(level="N5"))
    assert note.tags == ["N5"]
    assert note.fields[4] == "N5"


def test_fields_are_escaped():
    entry = make_entry()
    entry.meanings = ["<b>x</b>"]
    assert make_note(entry).fields[2] == "&lt;b&gt;x&lt;/b&gt;"


def test_deck_name():
    deck = build_deck([make_entry()], "my deck")
    assert deck.name == "my deck"
    assert len(deck.notes) == 1


def test_write_deck(tmp_path):
    out = tmp_path / "deck.apkg"
    entries = [make_entry(), make_entry("猫", "ねこ", "N5")]
    write_deck(entries, out)
    assert out.exists()
    assert out.stat().st_size > 0

    notes = read_notes(out, tmp_path)
    assert len(notes) == 2
    assert {n[0] for n in notes} == {note_guid(e) for e in entries}
    assert any("N5" in n[2] for n in notes)
