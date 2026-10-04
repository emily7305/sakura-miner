import re
from pathlib import Path

SRT_TIMING = re.compile(r"^\d{1,2}:\d{2}:\d{2}[,.]\d{1,3}\s*-->")
HTML_TAG = re.compile(r"<[^>]+>")
ASS_OVERRIDE = re.compile(r"\{[^}]*\}")


def srt_to_text(srt: str) -> str:
    """Return the dialogue from an .srt file, one subtitle line per line."""
    lines = []
    for line in srt.splitlines():
        line = line.strip()
        if not line or line.isdigit() or SRT_TIMING.match(line):
            continue
        # some srt files carry ass-style tags like {\an8}
        line = ASS_OVERRIDE.sub("", HTML_TAG.sub("", line)).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def ass_to_text(ass: str) -> str:
    """Return the dialogue from an .ass/.ssa file, one subtitle line per line."""
    lines = []
    text_index = 9
    in_events = False
    for line in ass.splitlines():
        line = line.strip()
        if line.startswith("["):
            in_events = line.lower() == "[events]"
            continue
        if not in_events:
            continue
        if line.startswith("Format:"):
            fields = [f.strip().lower() for f in line[7:].split(",")]
            if "text" in fields:
                text_index = fields.index("text")
            continue
        if not line.startswith("Dialogue:"):
            continue
        # the text field is last and may contain commas itself
        text = line[9:].split(",", text_index)[-1]
        text = ASS_OVERRIDE.sub("", text)
        text = text.replace("\\h", " ")
        for part in re.split(r"\\[Nn]", text):
            part = part.strip()
            if part:
                lines.append(part)
    return "\n".join(lines)


def read_input(path: Path) -> str:
    """Read a text or subtitle file and return plain text."""
    # utf-8-sig because a lot of subtitle files start with a BOM
    raw = path.read_text(encoding="utf-8-sig")
    suffix = path.suffix.lower()
    if suffix == ".srt":
        return srt_to_text(raw)
    if suffix in (".ass", ".ssa"):
        return ass_to_text(raw)
    return raw
