# Sakura Miner

Pre-made vocabulary decks teach words in isolation, often long before the learner meets them in anything they actually read or watch. Sentence mining takes the opposite approach: words are collected from material the learner already enjoys, so each card is tied to a familiar scene, lyric or line of dialogue, which makes it far easier to remember.

Mining by hand is slow, however, because every word has to be looked up and copied into Anki one at a time. Sakura Miner automates that work, so the learner can spend their time reviewing rather than building cards.

## Overview

Sakura Miner converts Japanese text, such as anime subtitles, song lyrics and articles, into Anki flashcards in the following stages:

1. Read a UTF-8 encoded text file.
2. Split the text into sentences and tokenize each sentence with fugashi.
3. Reduce each word to its dictionary form (for example, 食べた becomes 食べる).
4. Remove words listed in the user's known-words file.
5. Retrieve meanings and readings from JMdict, offline.
6. Assign a JLPT level to each word using the bundled vocabulary lists.
7. Export an Anki deck (`.apkg`) that includes the source sentence on every card.

The tool is designed primarily for learners at JLPT N3 and below, but it can be used with any Japanese text.

## Project Status

The project is under active development. Tokenization, dictionary lookup, deck export, known-word filtering and JLPT tagging are complete; sentence highlighting is planned.

- [x] Tokenization: produce a deduplicated list of words in dictionary form
- [x] Dictionary lookup: retrieve meanings and readings from JMdict
- [x] Export: write an Anki `.apkg` deck
- [x] Known words: exclude words the user already knows
- [x] JLPT tagging: add level tags and a `--level` filter
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

```
sakura-miner INPUT [-o OUTPUT.apkg] [--known PATH] [--level LEVEL] [--deck-name NAME] [--limit N]
```

| Option | Description | Default |
| --- | --- | --- |
| `INPUT` | Path to a UTF-8 text file | required |
| `-o`, `--output` | Path of the deck to write | `deck.apkg` |
| `--known` | File of words to skip (see [Known Words](#known-words)) | `data/known_words.txt` |
| `--level` | Keep only words at or below this JLPT level (`N5` to `N1`), plus words not on any list | no filter |
| `--deck-name` | Name of the deck in Anki | `Sakura Miner` |
| `--limit` | Maximum number of cards | no limit |

Example:

```bash
sakura-miner episode01.txt -o episode01.apkg --level N3 --deck-name "Episode 1"
```

```
words found: 10
skipped as known: 2
skipped above N3: 1
cards written: 7 -> episode01.apkg
```

The resulting file can be imported into Anki with **File > Import**.

### Known Words

Words that are already familiar can be listed in a known-words file so that they never appear in a deck. By default, Sakura Miner reads `data/known_words.txt` if it exists; another file can be given with `--known`. If the file does not exist, no words are skipped.

The file uses the following format:

- UTF-8 text, one word per line, written in dictionary form (食べる, not 食べた)
- lines beginning with `#` are comments, and text after `#` on a line is ignored
- blank lines are ignored
- to skip only one reading of a word, add the reading in hiragana after a tab, for example `上手<TAB>じょうず`

A template is provided in [`data/known_words.example.txt`](data/known_words.example.txt). To use it, copy it to `data/known_words.txt`, which is excluded from version control so that a personal word list is never committed.

```bash
cp data/known_words.example.txt data/known_words.txt
```

### JLPT Levels

Each word is tagged with a JLPT level from the vocabulary lists in `data/jlpt/`. The level is shown on the card and added as an Anki tag (`N5`, `N4` and so on), so cards can be searched or filtered by level in Anki's browser.

The JLPT has not published official vocabulary lists since 2010, so the bundled lists are the widely used unofficial lists compiled by Jonathan Waller (see [Acknowledgements](#acknowledgements)). They are a guide rather than a definitive standard, and some common words, particularly loanwords such as アニメ, do not appear on any list. Such words receive no level and are never removed by `--level`.

When a word appears on more than one list, the easiest level is used. This matters because the lists often record an easy word in kana at one level (おもしろい at N5) and its kanji spelling at a harder level (面白い at N1).

Additional or replacement lists can be placed in `data/jlpt/`. Every `.csv` file in that directory is loaded, and each must have the following columns:

```csv
word,reading,level
食べる,たべる,N5
賛成,さんせい,N3
```

`word` is the dictionary form, `reading` is in hiragana (or katakana for katakana words), and `level` is one of `N5` to `N1`.

### Cards

Each note has the fields `Word`, `Reading`, `Meaning`, `Sentence` and `Level`. The front of the card shows the word; the back shows the reading, up to three English meanings, the source sentence and the JLPT level, if known. The JLPT level is also added as an Anki tag.

The deck and note type use fixed IDs, and each note's ID is derived from the word and its reading. Importing a new deck built from the same or overlapping text therefore updates existing cards rather than creating duplicates.

### Library Use

The individual stages can also be used from Python:

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

- JLPT vocabulary lists are by Jonathan Waller, originally published at tanos.co.uk, and are used under the [Creative Commons Attribution (CC BY)](https://creativecommons.org/licenses/by/4.0/) licence. They were obtained from the parsed copies in [Bluskyo/JLPT_Vocabulary](https://github.com/Bluskyo/JLPT_Vocabulary). For this project, the lists were converted to the `word,reading,level` format, entries listing several spellings or readings were split into separate rows, one corrupted reading (賛成) was corrected, and a small number of malformed rows were removed.
- Dictionary data is taken from [JMdict and KANJIDIC2](https://www.edrdg.org/), compiled by the Electronic Dictionary Research and Development Group, and is used under the [CC BY-SA 4.0](https://www.edrdg.org/edrdg/licence.html) licence via [jamdict](https://github.com/neocl/jamdict).
- Tokenization is provided by [fugashi](https://github.com/polm/fugashi) with [unidic-lite](https://github.com/polm/unidic-lite).
- Kana conversion is provided by [jaconv](https://github.com/ikegami-yukino/jaconv).
- Anki decks are generated with [genanki](https://github.com/kerrickstaley/genanki).
- The command line interface is built with [click](https://click.palletsprojects.com/).

## Licence

This project is released under the MIT Licence; see [LICENSE](LICENSE). The dictionary data and JLPT vocabulary lists remain subject to their own licences, as noted above.
