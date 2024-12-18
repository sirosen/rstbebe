import re
import typing as t

from ._model import ErrorLine, Position

BAD_BACKTICK_PAT = re.compile(r"(^|\s)`[^`]+`(\s|$)", flags=re.MULTILINE)


class BacktickChecker:
    def __init__(self, filename: str, contents: list[str]) -> None:
        self.filename = filename
        self.contents = contents

    def iter_errors(self) -> t.Iterator[ErrorLine]:
        for lineno, line in enumerate(self.contents, 1):
            line = line.rstrip("\n")
            yield from self._iter_line_errors(line, lineno)

    def _iter_line_errors(self, line: str, lineno: int) -> t.Iterator[ErrorLine]:
        for m in BAD_BACKTICK_PAT.finditer(line):
            pos = Position(lineno=lineno, start_col=m.start(), end_col=m.end())
            yield ErrorLine(
                line=line, pos=pos, message="found what appear to be markdown backticks"
            )
