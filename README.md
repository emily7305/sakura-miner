# Sakura Miner

Pre-made vocabulary decks teach words in isolation, often long before you meet them in anything you actually read or watch. Sentence mining takes the opposite approach: you collect words from material you already enjoy, so each card is tied to a familiar scene, lyric or line of dialogue, which makes it far easier to remember.

Mining by hand is slow, because every word has to be looked up and copied into Anki one at a time. Sakura Miner does that work for you, so you can spend your time reviewing rather than building cards.

## Features

- Works with plain text files and `.srt` / `.ass` subtitle files
- Converts every word to its dictionary form, so 食べた becomes 食べる
- Adds the reading, up to three English meanings and the JLPT level (N5 to N1) to each card
- Shows the original sentence on every card, with the word highlighted
- Skips words you already know
- Optional furigana, reverse cards and frequency ordering
- Runs entirely offline once installed

## Installation

Python 3.10 or later is required.

```bash
git clone https://github.com/emily7305/sakura-miner.git
cd sakura-miner
python -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate
pip install -e .
```

The first installation downloads a full Japanese dictionary, so it may take a few minutes.

## Usage

Run Sakura Miner on a text or subtitle file:

```bash
sakura-miner episode01.srt
```

This creates `deck.apkg`, which can be opened in Anki with **File > Import**. Importing a newer deck later updates existing cards instead of creating duplicates.

A more typical example, which keeps words up to N3, puts the most frequent words first, adds furigana and saves the deck under a custom name:

```bash
sakura-miner episode01.srt -o episode01.apkg --level N3 --sort frequency --furigana
```

### Options

| Option | Description |
| --- | --- |
| `-o FILE` | Where to save the deck (default: `deck.apkg`) |
| `--level N3` | Only include words at this JLPT level or easier |
| `--sort frequency` | Put the words used most often in the text first |
| `--limit 30` | Include at most this many words |
| `--furigana` | Show readings above the kanji in the example sentence |
| `--reverse` | Also add cards that show the English meaning and ask for the Japanese word |
| `--known FILE` | Use a different known-words file (see below) |
| `--deck-name NAME` | Name of the deck in Anki (default: `Sakura Miner`) |
| `--stats` | Show how difficult the text is instead of making a deck (see below) |

Run `sakura-miner --help` to see all options.

### Skipping Words You Already Know

Create a file called `data/known_words.txt` and list the words you already know, one per line, in dictionary form (食べる, not 食べた). These words will never appear in a deck. Lines starting with `#` are ignored, so you can add notes.

```text
# week 1
猫
食べる
とても
```

An example file is included at [`data/known_words.example.txt`](data/known_words.example.txt). Your own `known_words.txt` is ignored by Git, so it stays private.

### Checking the Difficulty of a Text

Use `--stats` to see how many words from each JLPT level a text contains before you mine it:

```bash
sakura-miner article.txt --stats
```

```
level   words     %    new
N5          6    60      6
N4          2    20      2
N3          0     0      0
N2          0     0      0
N1          1    10      1
none        1    10      1
total      10           10
```

`new` counts only the words that are not in your known-words file, and `none` covers words that are not on any JLPT list.

## Limitations

- The JLPT has not published official vocabulary lists since 2010, so levels come from widely used unofficial lists. Some common words, especially loanwords such as アニメ, have no level. These words are always kept when `--level` is used.
- Some compound words are split into shorter parts. For example, 喫茶店 becomes 喫茶.
- Occasionally a reading is correct but not the most common one, for example 明日 as あす rather than あした.

## Acknowledgements

- JLPT vocabulary lists by Jonathan Waller (originally published at tanos.co.uk), used under the [CC BY](https://creativecommons.org/licenses/by/4.0/) licence and obtained from [Bluskyo/JLPT_Vocabulary](https://github.com/Bluskyo/JLPT_Vocabulary). The lists have been reformatted and lightly corrected; see [`data/jlpt/SOURCE.md`](data/jlpt/SOURCE.md) for details.
- Dictionary data from [JMdict](https://www.edrdg.org/) by the Electronic Dictionary Research and Development Group, used under the [CC BY-SA 4.0](https://www.edrdg.org/edrdg/licence.html) licence via [jamdict](https://github.com/neocl/jamdict).
- Built with [fugashi](https://github.com/polm/fugashi), [unidic-lite](https://github.com/polm/unidic-lite), [jaconv](https://github.com/ikegami-yukino/jaconv), [genanki](https://github.com/kerrickstaley/genanki) and [click](https://click.palletsprojects.com/).

## Licence

Sakura Miner is released under the MIT Licence; see [LICENSE](LICENSE). The dictionary data and JLPT vocabulary lists remain subject to their own licences, as noted above.
