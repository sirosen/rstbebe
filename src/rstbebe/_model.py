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
    line: str
    pos: Position
    message: str

    def __str__(self) -> str:
        offset1 = self.pos.start_col + 1
        offset2 = self.pos.col_range - 4
        return (
            f"{self.message} on line {self.pos.lineno}:\n"
            f"  {self.line}\n"
            f"  {offset1 * ' '}^{offset2 * ' '}^"
        )
