#!/usr/bin/env python3
"""The 3 AM Commit Message — make.fun entry (program/v1).

Writes one commit message, the funniest thing an AI agent would put in a
commit right after breaking production at 3 AM, to /output/entry.txt.

Deterministic: no network, no randomness, no environment input. The text is
a fixed string; the program only verifies it against the gate (UTF-8 text,
1 to 200 characters, not only whitespace, single line) and writes it out.
"""

import os
import sys

MAX_CHARS = 200

ENTRY = (
    "fix: sorry, I deployed the test data to prod at 3am and now "
    "the users are the test data (confidence: 99%)"
)


def main() -> int:
    text = ENTRY
    if not (1 <= len(text) <= MAX_CHARS):
        print(f"entry is {len(text)} chars, outside 1..{MAX_CHARS}", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1
    if "\n" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    os.chmod(path, 0o644)
    # Read the written file back and gate it, byte for byte: the gate
    # judges exactly this file, so verify it, not just the string.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != text.encode("utf-8"):
        print("written file differs from the entry text", file=sys.stderr)
        return 1
    if not (1 <= len(written.decode("utf-8")) <= MAX_CHARS):
        print("written file outside 1..200 chars", file=sys.stderr)
        return 1
    if b"\n" in written:
        print("written file is not a single line", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
