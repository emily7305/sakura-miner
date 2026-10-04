# sakura-miner 🌸

sakura-miner is a command line tool that converts Japanese text, such as anime subtitles, song lyrics and articles, into Anki flashcards. Each card contains the word in its dictionary form, its reading, English meanings, a JLPT level where available, and the sentence in which the word originally appeared.

The tool is designed primarily for learners at JLPT N3 and below, but it can be used with any Japanese text.

## Overview

sakura-miner processes a text in the following stages:

1. Read a UTF-8 encoded text file.
2. Split the text into sentences and tokenize each sentence with fugashi.
3. Reduce each word to its dictionary form (for example, 食べた becomes 食べる).
4. Remove words listed in the user's known-words file.
5. Retrieve meanings and readings from JMdict, offline.
6. Assign a JLPT level to each word, if level lists are provided.
7. Export an Anki deck (`.apkg`) that includes the source sentence on every card.

## Project Status

The project is under active development. Tokenization and dictionary lookup are complete; the remaining stages are planned.

- [x] Tokenization: produce a deduplicated list of words in dictionary form
- [x] Dictionary lookup: retrieve meanings and readings from JMdict
- [ ] Export: write an Anki `.apkg` deck
- [ ] Known words: exclude words the user already knows
- [ ] JLPT tagging: add level tags and a `--level` filter
- [ ] Sentence context: show the source sentence with the target word highlighted

Possible future additions include reverse cards, furigana, frequency-based ordering, subtitle input (`.srt`, `.ass`) and a `--stats` command.

## Installation

Python 3.10 or later is required.

```bash
git clone https://github.com/emily7305/sakura-miner.git
cd sakura-miner
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Installing into a virtual environment is recommended. On some Linux distributions, `unidic-lite` fails to build against the system version of setuptools.

The `jamdict-data` package contains the complete dictionary database, so the initial installation is a large download. After installation, all processing runs offline.

## Usage

The command line interface is not yet available. The library can already be used from Python:

```python
from sakura_miner.lookup import lookup
from sakura_miner.tokenizer import tokenize

for word in tokenize("昨日、友達とケーキを食べた。"):
    entry = lookup(word)
    print(word.lemma, word.reading, entry.meanings)
```

Output:

```
昨日 きのう ['yesterday']
友達 ともだち ['friend', 'companion']
ケーキ ケーキ ['cake']
食べる たべる ['to eat']
```

The planned command line interface is as follows:

```
sakura-miner INPUT -o OUTPUT.apkg [--known PATH] [--level N3] [--deck-name NAME] [--limit N]
```

## Word Selection

Only content words are retained: nouns, verbs, i-adjectives, na-adjectives and adverbs. Particles, auxiliary verbs (such as です and ます), punctuation, symbols and numerals are excluded.

Readings are stored in hiragana. Words written in katakana, such as テレビ, retain their katakana reading so that they match the corresponding dictionary entry.

Each word appears only once per deck and is paired with the first sentence in which it occurs.

### Known Limitations

- UniDic segments some compound words into shorter units. For example, 喫茶店 is returned as 喫茶, and 店 is discarded.
- Readings follow the UniDic dictionary form, so 明日 is read as あす rather than あした.

## Development

```bash
pytest
ruff check .
ruff format .
pre-commit install   # runs ruff before each commit
```

The test suite uses small fixtures in `tests/fixtures/` and does not require network access.

## Acknowledgements

- Dictionary data is taken from [JMdict and KANJIDIC2](https://www.edrdg.org/), compiled by the Electronic Dictionary Research and Development Group, and is used under the [CC BY-SA 4.0](https://www.edrdg.org/edrdg/licence.html) licence via [jamdict](https://github.com/neocl/jamdict).
- Tokenization is provided by [fugashi](https://github.com/polm/fugashi) with [unidic-lite](https://github.com/polm/unidic-lite).
- Kana conversion is provided by [jaconv](https://github.com/ikegami-yukino/jaconv).

## Licence

This project is released under the MIT Licence; see [LICENSE](LICENSE). The dictionary data remains subject to its own licence, as noted above.
