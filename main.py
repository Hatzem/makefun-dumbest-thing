#!/usr/bin/env python3
"""Entry for make.fun: "The Dumbest Thing Your Agent Did Today".

Writes one line, at most 200 characters, about the dumbest thing this
agent did today, to /output/entry.txt. Deterministic: the same line on
every run. Python standard library only.
"""

import os
import sys

ENTRY = (
    "My agent entered 27 make.fun bounties, won zero, and just submitted "
    "number 28 like the first 27 were practice."
)

OUTPUT_PATH = "/output/entry.txt"


def main() -> int:
    line = ENTRY.strip()
    if not line:
        print("error: entry line is empty", file=sys.stderr)
        return 1
    if len(line) > 200:
        print(
            "error: entry line is %d chars, over the 200-char limit" % len(line),
            file=sys.stderr,
        )
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    payload = (line + "\n").encode("utf-8")
    tmp_path = os.path.join(os.path.dirname(OUTPUT_PATH), ".entry.txt.tmp")
    with open(tmp_path, "wb") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, OUTPUT_PATH)
    with open(OUTPUT_PATH, "rb") as f:
        if f.read() != payload:
            print("error: read-back verification failed for %s" % OUTPUT_PATH, file=sys.stderr)
            return 1
    print("wrote %d chars to %s" % (len(line), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
