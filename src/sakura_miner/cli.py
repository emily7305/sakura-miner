from collections import Counter
from pathlib import Path

import click

from sakura_miner.export import write_deck
from sakura_miner.filter import is_known, load_known, remove_known
from sakura_miner.jlpt import LEVELS, at_or_below, get_level
from sakura_miner.lookup import lookup
from sakura_miner.models import Word
from sakura_miner.subtitles import read_input
from sakura_miner.tokenizer import by_frequency, count_words, tokenize

DEFAULT_KNOWN = Path("data/known_words.txt")


def print_stats(words: list[Word], known: set[str]) -> None:
    total = Counter()
    new = Counter()
    for word in words:
        level = get_level(word.lemma, word.reading) or "none"
        total[level] += 1
        if not is_known(word, known):
            new[level] += 1

    click.echo(f"{'level':<6}{'words':>7}{'%':>6}{'new':>7}")
    for level in [*reversed(LEVELS), "none"]:
        share = 100 * total[level] / len(words) if words else 0
        click.echo(f"{level:<6}{total[level]:>7}{share:>6.0f}{new[level]:>7}")
    click.echo(f"{'total':<6}{len(words):>7}{'':>6}{sum(new.values()):>7}")


@click.command()
@click.argument("input_path", metavar="INPUT", type=click.Path(path_type=Path))
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default=Path("deck.apkg"),
    show_default=True,
    help="Where to write the deck.",
)
@click.option(
    "--known",
    "known_path",
    type=click.Path(path_type=Path),
    default=DEFAULT_KNOWN,
    show_default=True,
    help="File of words to skip.",
)
@click.option(
    "--level",
    type=click.Choice(LEVELS, case_sensitive=False),
    help="Only keep words at or below this JLPT level, plus unlisted words.",
)
@click.option(
    "--sort",
    type=click.Choice(["text", "frequency"]),
    default="text",
    show_default=True,
    help="Card order: as they appear in the text, or most frequent first.",
)
@click.option(
    "--stats",
    is_flag=True,
    help="Show the JLPT level breakdown of the text instead of writing a deck.",
)
@click.option("--deck-name", default="Sakura Miner", show_default=True)
@click.option("--limit", type=click.IntRange(min=1), help="Maximum number of cards.")
def main(
    input_path: Path,
    output: Path,
    known_path: Path,
    level: str | None,
    sort: str,
    stats: bool,
    deck_name: str,
    limit: int | None,
) -> None:
    """Turn a Japanese text or subtitle file into an Anki deck."""
    try:
        text = read_input(input_path)
    except FileNotFoundError:
        raise click.ClickException(f"file not found: {input_path}") from None
    except UnicodeDecodeError:
        raise click.ClickException(f"not a utf-8 text file: {input_path}") from None
    except OSError as e:
        raise click.ClickException(f"could not read file: {input_path} ({e})") from None

    words = tokenize(text)
    found = len(words)
    known = load_known(known_path)
    if stats:
        print_stats(words, known)
        return
    words = remove_known(words, known)
    skipped = found - len(words)

    levels = {w: get_level(w.lemma, w.reading) for w in words}
    if level is not None:
        before = len(words)
        words = [w for w in words if at_or_below(levels[w], level)]
        too_hard = before - len(words)

    if sort == "frequency":
        words = by_frequency(words, count_words(text))
    if limit is not None:
        words = words[:limit]
    entries = [lookup(w) for w in words]
    for entry in entries:
        entry.level = levels[entry.word]

    write_deck(entries, output, deck_name)
    click.echo(f"words found: {found}")
    click.echo(f"skipped as known: {skipped}")
    if level is not None:
        click.echo(f"skipped above {level}: {too_hard}")
    click.echo(f"cards written: {len(entries)} -> {output}")
