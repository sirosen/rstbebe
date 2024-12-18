import sys
import typing as t

import click

from ._checkers import BacktickChecker
from ._model import ErrorLine, collate_errors


@click.group
def main():
    """a linter for your rst mistakes"""


@main.command
@click.argument("files", required=True, nargs=-1, type=click.File("r"))
def bad_backticks(files: t.IO[bytes]):
    errors: list[ErrorLine] = []
    for file in files:
        errors.extend(BacktickChecker(file.name, file.readlines()).iter_errors())

    if errors:
        collated = collate_errors(errors)
        for filename, by_lineno in collated.items():
            print(f"encountered errors in {filename}:")
            for lineno, line_errors in by_lineno.items():
                prefix = f"  on line {lineno}: "
                prefixlen = len(prefix)
                line = line_errors[0].line
                print(f"{prefix}{line}")
                for e in line_errors:
                    indicators = e.indicators()
                    message = (" " * (len(e.line) - len(indicators) + 2)) + e.message
                    print(f"{' ' * prefixlen}{indicators}{message}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
