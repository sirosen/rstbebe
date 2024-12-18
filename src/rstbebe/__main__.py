import sys
import textwrap
import typing as t

import click

from ._checkers import BacktickChecker
from ._model import ErrorLine


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
        print("encountered errors:")
        for e in errors:
            print(textwrap.indent(str(e), "  "))
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
