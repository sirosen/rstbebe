import dataclasses


@dataclasses.dataclass
class Position:
    lineno: int
    start_col: int
    end_col: int

    @property
    def col_range(self) -> int:
        return self.end_col - self.start_col


@dataclasses.dataclass
class ErrorLine:
    filename: str
    line: str
    pos: Position
    message: str

    def indicators(self) -> str:
        offset1 = self.pos.start_col + 1
        offset2 = self.pos.col_range - 4
        return f"{offset1 * ' '}^{offset2 * '-'}^"


def collate_errors(errors: list[ErrorLine]) -> dict[str, dict[int, list[ErrorLine]]]:
    """
    Organize errors first by filename, secondarily by line number.
    """
    by_filename: dict[str, list[ErrorLine]] = {}
    for e in errors:
        by_filename.setdefault(e.filename, [])
        by_filename[e.filename].append(e)

    collated: dict[str, dict[int, list[ErrorLine]]] = {}
    for filename, file_errors in by_filename.items():
        by_lineno: dict[int, list[ErrorLine]] = {}
        for e in file_errors:
            by_lineno.setdefault(e.pos.lineno, [])
            by_lineno[e.pos.lineno].append(e)
        collated[filename] = by_lineno

    return collated
