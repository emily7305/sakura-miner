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

## Before you start

### What you need

- **A Windows or Mac computer.** Sakura Miner runs on a computer, not on a phone. Once a deck is in Anki, it can be synced to your phone through AnkiWeb as usual.
- **Anki**, the free flashcard app, from [apps.ankiweb.net](https://apps.ankiweb.net/).
- **About 700 MB of free disk space**, mostly for the offline dictionary.
- **An internet connection for installation only.** After that, everything runs offline.
- **The ability to read hiragana and katakana.** Readings are shown in kana only, with no romaji.
- **Basic English**, as all meanings are given in English.

### Your input

- **The text must be actual text, not an image.** Sakura Miner cannot read scanned pages, screenshots, PDFs, or subtitles that are burned into a video. For anime and dramas, you need a separate subtitle file (`.srt` or `.ass`).
- **The file should be in Japanese.** Words written in the Latin alphabet, such as English, are skipped automatically. Text in other languages that use kanji, such as Chinese, is not detected and may produce incorrect cards.

### Good to know

- **Cards are made automatically and may contain mistakes.** Each card shows the most common meaning of a word, which may not be the meaning used in your sentence. It is worth checking new cards briefly before studying them.
- **Only individual words are collected**, not grammar patterns or set phrases. Particles such as は and を are skipped.
- **Names of people and places may appear as cards**, for example 田中 or 東京. You can delete these in Anki or add them to your known-words file.
- **JLPT levels are a guide only**, as explained in [Limitations](#limitations).
- **Decks are for personal study.** Subtitles, lyrics and articles are usually copyrighted, so decks containing their sentences should not be shared publicly.

## Installation

You only need to do this once. No coding experience is needed: you will copy and paste a few commands into a window called the *terminal*.

### Step 1: Install Python

Install Python 3.10 or later. On Windows, make sure to tick **Add python.exe to PATH** during installation.

### Step 2: Download Sakura Miner

1. At the top of this page, click the green **Code** button, then **Download ZIP**.
2. Find the ZIP file in your Downloads folder and unzip it (on Windows, right-click it and choose **Extract All**; on Mac, double-click it).
3. You now have a folder called `sakura-miner-main`. Move it somewhere easy to find, such as your Desktop.

### Step 3: Open a terminal in the folder

- **Windows:** open the `sakura-miner-main` folder, click the address bar at the top of the window, type `cmd` and press **Enter**. A black window opens.
- **Mac:** open the **Terminal** app (press **Cmd + Space** and search for "Terminal"). Type `cd ` (with a space after it), drag the `sakura-miner-main` folder into the Terminal window, and press **Enter**.

### Step 4: Install

Copy and paste these lines into the terminal, one at a time, pressing **Enter** after each.

**Windows:**

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

**Mac:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

The last line downloads a full Japanese dictionary, so it can take a few minutes. When the terminal accepts typing again, the installation is complete.

## Usage

### Making a deck

1. Put the file you want to study inside the `sakura-miner-main` folder. This can be a text file (`.txt`) or a subtitle file (`.srt` or `.ass`). To make a text file, paste the Japanese text into Notepad (Windows) or TextEdit (Mac) and save it as a `.txt` file (see [Saving text files](#saving-text-files) below).
2. Open a terminal in the folder (see Step 3 above) and turn Sakura Miner on with:
   - **Windows:** `.venv\Scripts\activate`
   - **Mac:** `source .venv/bin/activate`
3. Run Sakura Miner with the name of your file. For example, if your file is called `episode01.srt`:

   ```bash
   sakura-miner episode01.srt
   ```

4. A new file called `deck.apkg` appears in the folder. Double-click it, or open Anki and choose **File > Import**, and your new cards are ready.

Step 2 needs to be repeated each time you open a new terminal window. If you see an error such as `'sakura-miner' is not recognized` or `command not found`, it usually means this step was skipped.

Importing a newer deck later updates the existing cards instead of creating duplicates.

### Adding options

Options let you change what goes into the deck. They are typed on the same line as the command from step 3, after the file name, with a space between each one.

For example, to keep only words up to JLPT N3, type this instead of the plain command and press **Enter**:

```bash
sakura-miner episode01.srt --level N3
```

You can combine as many options as you like, in any order. This command also adds furigana and puts the most common words first:

```bash
sakura-miner episode01.srt --level N3 --furigana --sort frequency
```

### All options

Copy the text from the first column into your command. Where it shows an example value, such as `N3` or `30`, replace it with your own.

| Type this | What it does |
| --- | --- |
| `--level N3` | Only include words at this JLPT level or easier (`N5`, `N4`, `N3`, `N2` or `N1`) |
| `--furigana` | Show readings above the kanji in the example sentence |
| `--sort frequency` | Put the words used most often in the text first |
| `--limit 30` | Include at most this many words |
| `--reverse` | Also add cards that show the English meaning and ask for the Japanese word |
| `-o episode01.apkg` | Save the deck under this file name instead of `deck.apkg` |
| `--deck-name "Episode 1"` | Name of the deck inside Anki (use quotes if the name has spaces) |
| `--known my_words.txt` | Use a different known-words file (see below) |
| `--stats` | Show how difficult the text is instead of making a deck (see below) |

To see this list in the terminal, type `sakura-miner --help`.

### Skipping words you already know

1. Open the `data` folder inside `sakura-miner-main`.
2. Create a new text file called `known_words.txt` (see [Saving text files](#saving-text-files) below).
3. Write the words you already know, one per line, in their dictionary form (食べる, not 食べた). Lines starting with `#` are ignored, so you can use them for notes:

   ```text
   # week 1
   猫
   食べる
   とても
   ```

4. Save the file. From now on, these words will never appear in your decks.

You can add to this file whenever you learn new words.

### Saving text files

Sakura Miner needs plain text files saved in UTF-8, which is a standard way of storing Japanese characters.

- **Windows (Notepad):** choose **File > Save as**, make sure **Encoding** at the bottom is set to **UTF-8**, and type a file name ending in `.txt`.
- **Mac (TextEdit):** first choose **Format > Make Plain Text**. Then choose **File > Save**, set **Plain Text Encoding** to **Unicode (UTF-8)**, and type a file name ending in `.txt`.

### Checking the difficulty of a text

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
