# sakura-miner 🌸

sakura-miner takes Japanese text you actually care about (anime subs, song lyrics, articles) and turns the words you don't know yet into Anki cards, complete with readings, meanings, JLPT level and the original sentence.

It's mostly built for N3 and below, but it works on any text.

## How it works

1. read a UTF-8 text file
2. split it into sentences and tokenize with fugashi
3. reduce every word to its dictionary form (食べた → 食べる)
4. drop the words you already know
5. look up meanings and readings offline in JMdict
6. tag each word with a JLPT level, if you have level lists
7. export an Anki deck (`.apkg`) with the original sentence on every card

## Status

Still early. Tokenizing and dictionary lookup work, the rest is on the way.

- [x] Tokenize: text in, deduplicated dictionary-form words out
- [x] Lookup: meanings and readings from JMdict
- [ ] Export: write an `.apkg` deck
- [ ] Known words: skip words you already know
- [ ] JLPT tagging: level tags and `--level` filter
- [ ] Sentence context: original sentence with the word highlighted

Maybe later: reverse cards, furigana, frequency sorting, `.srt` / `.ass` input, a `--stats` command.

## Install

Needs Python 3.10+.

```bash
git clone https://github.com/emily7305/sakura-miner.git
cd sakura-miner
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Use a venv. On some Linux distros `unidic-lite` won't build against the system setuptools.

`jamdict-data` ships the whole dictionary, so the first install is a fairly big download. After that everything runs offline.

## Usage

There's no command line yet, but you can already use it from Python:

```python
from sakura_miner.lookup import lookup
from sakura_miner.tokenizer import tokenize

for word in tokenize("昨日、友達とケーキを食べた。"):
    entry = lookup(word)
    print(word.lemma, word.reading, entry.meanings)
```

```
昨日 きのう ['yesterday']
友達 ともだち ['friend', 'companion']
ケーキ ケーキ ['cake']
食べる たべる ['to eat']
```

The planned CLI looks like this:

```
sakura-miner INPUT -o OUTPUT.apkg [--known PATH] [--level N3] [--deck-name NAME] [--limit N]
```

## What gets kept

Only content words: nouns, verbs, i-adjectives, na-adjectives and adverbs. Particles, auxiliaries (です, ます), punctuation, symbols and numbers are skipped.

Readings are stored in hiragana, except for katakana words like テレビ, which keep their katakana so they match the dictionary.

A word only shows up once per deck, together with the first sentence it appeared in.

### Known quirks

- unidic splits some compounds into shorter units, so 喫茶店 comes out as 喫茶 and the 店 is dropped
- the reading is unidic's dictionary reading, so 明日 is あす, not あした

## Development

```bash
pytest
ruff check .
ruff format .
pre-commit install   # runs ruff on every commit
```

Tests use small fixtures in `tests/fixtures/` and don't need network access.

## Credits

- Dictionary data comes from [JMdict and KANJIDIC2](https://www.edrdg.org/) by the Electronic Dictionary Research and Development Group, used under the [CC BY-SA 4.0](https://www.edrdg.org/edrdg/licence.html) licence, through [jamdict](https://github.com/neocl/jamdict)
- Tokenizing by [fugashi](https://github.com/polm/fugashi) with [unidic-lite](https://github.com/polm/unidic-lite)
- Kana conversion by [jaconv](https://github.com/ikegami-yukino/jaconv)

## Licence

MIT, see [LICENSE](LICENSE). The dictionary data keeps its own licence (see above).
