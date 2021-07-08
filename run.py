from pathlib import Path
from subprocess import run, CompletedProcess
from typing import Sequence, List

from case import TestSession


def main(cases: Sequence[str] = ()):
    tox_ini = Path(__file__).parent / "tox.ini"

    _toxbase = tox_ini.read_text()
    completed: List[CompletedProcess] = []
    for case in TestSession.from_dir("cases").cases:
        if cases and case.name not in cases:
            continue
        try:
            text = _toxbase + "\n" + case.toxenv()
            tox_ini.write_text(text)
            completed.append(run(["tox", "-v", "-e", case.name]))
        finally:
            tox_ini.write_text(_toxbase)

    sys.exit(int(any(r.returncode for r in completed)))


if __name__ == "__main__":
    import os
    import sys

    tox_case = os.getenv("TEST_CASE")
    main([tox_case] if tox_case else sys.argv[1:])
