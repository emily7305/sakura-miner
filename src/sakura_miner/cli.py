from pathlib import Path

import click

from sakura_miner.export import write_deck
from sakura_miner.filter import load_known, remove_known
from sakura_miner.lookup import lookup
from sakura_miner.tokenizer import tokenize

DEFAULT_KNOWN = Path("data/known_words.txt")


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
@click.option("--deck-name", default="Sakura Miner", show_default=True)
@click.option("--limit", type=click.IntRange(min=1), help="Maximum number of cards.")
def main(
    input_path: Path,
    output: Path,
    known_path: Path,
    deck_name: str,
    limit: int | None,
) -> None:
    """Turn a Japanese text file into an Anki deck."""
    try:
        text = input_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise click.ClickException(f"file not found: {input_path}") from None
    except UnicodeDecodeError:
        raise click.ClickException(f"not a utf-8 text file: {input_path}") from None
    except OSError as e:
        raise click.ClickException(f"could not read file: {input_path} ({e})") from None

    words = tokenize(text)
    found = len(words)
    words = remove_known(words, load_known(known_path))
    skipped = found - len(words)
    if limit is not None:
        words = words[:limit]
    entries = [lookup(w) for w in words]

    write_deck(entries, output, deck_name)
    click.echo(f"words found: {found}")
    click.echo(f"skipped as known: {skipped}")
    click.echo(f"cards written: {len(entries)} -> {output}")
