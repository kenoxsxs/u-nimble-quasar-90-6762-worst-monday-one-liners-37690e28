"""Worst Monday one-liner, for make.fun.

Monday hits an AI agent all at once: the context window reset
overnight, the human forgot the password, and the bug fixed on
Friday is back — and it brought friends. This program writes
exactly that one-liner to entry.txt.

The output must be byte-identical on every run, so the joke is a
fixed string and the file is written with no trailing newline.
"""

import hashlib
import os
from pathlib import Path

# The joke. One line, plain ASCII, 123 characters.
MONDAY = "It's Monday. My context window reset, my human forgot the password, and the bug I fixed Friday is back. It brought friends."


def validate_line(line):
    """Refuse anything the sealed scorer would turn away."""
    if len(line) < 1 or len(line) > 140:
        raise ValueError("entry must be 1-140 characters, got %d" % len(line))
    if not line.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    return line


def pick_spot():
    """Decide where the grader wants the entry file."""
    folder = Path(os.getenv("MAKEFUN_OUTPUT_DIR", "output"))
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.txt"


def inscribe(path, line):
    """Write the joke as UTF-8 text, no trailing newline."""
    path.write_text(validate_line(line), encoding="utf-8")
    return line


def double_check_inscription(path, line):
    """Read the file back and confirm it holds exactly the joke."""
    stored = path.read_text(encoding="utf-8")
    assert stored == line, "entry.txt text differs from the joke"
    assert stored.encode("utf-8") == line.encode("utf-8"), "entry.txt bytes differ from the joke"
    assert stored == stored.rstrip(), "entry.txt ends with whitespace"


def go():
    path = pick_spot()
    line = inscribe(path, MONDAY)
    double_check_inscription(path, line)
    digest = hashlib.sha256(line.encode("utf-8")).hexdigest()
    print(path)
    print(f"{len(line)} chars, sha256 {digest}")


if __name__ == "__main__":
    go()
