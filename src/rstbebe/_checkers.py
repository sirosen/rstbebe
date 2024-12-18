import re
import typing as t

from ._model import ErrorLine, Position

BAD_BACKTICK_PAT = re.compile(r"(^|\s)`[^`]+`([.,?!\s]|$)", flags=re.MULTILINE)
CODE_BLOCK_START_PAT = re.compile(r"^\s*\.\.\s+code-block::")


class BacktickChecker:
    def __init__(self, filename: str, contents: list[str]) -> None:
        self.filename = filename
        self.contents = contents

    def iter_errors(self) -> t.Iterator[ErrorLine]:
        code_block_detector = _CodeBlockDetector()

        for lineno, line in enumerate(self.contents, 1):
            # consume/skip lines while in a code-block
            if code_block_detector.in_code_block and not code_block_detector.block_end(
                line
            ):
                continue

            # if we are on the first line of a code-block, start skipping!
            if code_block_detector.set_start(line):
                continue

            line = line.rstrip("\n")
            yield from self._iter_line_errors(line, lineno)

    def _iter_line_errors(self, line: str, lineno: int) -> t.Iterator[ErrorLine]:
        for m in BAD_BACKTICK_PAT.finditer(line):
            pos = Position(lineno=lineno, start_col=m.start(), end_col=m.end())
            yield ErrorLine(
                filename=self.filename,
                line=line,
                pos=pos,
                message="found what appear to be markdown backticks",
            )


class _CodeBlockDetector:
    def __init__(self) -> None:
        self.in_code_block = False
        self._indent = 0

    def set_start(self, line: str) -> bool:
        """
        Try to start a code-block.

        If the line begins a new code-block, return true. Otherwise, false.
        """
        if CODE_BLOCK_START_PAT.match(line):
            self.in_code_block = True
            self._indent = _get_indent(line)
            return True
        return False

    def block_end(self, line: str) -> bool:
        """
        Try to end a code-block.

        If the line ends the current code-block, return true. Otherwise, false.
        """
        # skip empty lines
        if not line.strip():
            return False
        if _get_indent(line) <= self._indent:
            self.in_code_block = False
            return True
        return False


def _get_indent(line: str) -> int:
    return len(line) - len(line.lstrip())
