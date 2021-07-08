from pathlib import Path
from subprocess import run
from typing import Sequence

from case import TestSession


def main(cases: Sequence[str] = ()):
    _toxbase = Path("tox.ini").read_text()
    completed = []
    for case in TestSession.from_dir("cases").cases:
        if cases and case.name not in cases:
            print(f"{case.name} not in {cases}.  Skipping.")
            continue
        try:
            text = _toxbase + "\n" + case.toxenv()
            print(text)
            Path("tox.ini").write_text(text)
            completed.append(run(["tox", "-v", "-e", case.name]))
        finally:
            Path("tox.ini").write_text(_toxbase)

    for c in completed:
        print(c)


if __name__ == "__main__":
    import os
    import sys

    tox_case = os.getenv("TEST_CASE")
    main([tox_case] if tox_case else sys.argv[1:])
