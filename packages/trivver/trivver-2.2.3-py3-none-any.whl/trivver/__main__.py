# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
#
"""Command-line version comparison tool."""

from __future__ import annotations

import argparse
import dataclasses
import functools
import sys
import typing

from . import trivver


if typing.TYPE_CHECKING:
    from collections.abc import Callable


V_HANDLERS: dict[str, Callable[[int], bool]] = {
    "<": lambda res: res < 0,
    "=": lambda res: res == 0,
    ">": lambda res: res > 0,
    "<=": lambda res: res <= 0,
    ">=": lambda res: res >= 0,
    "!=": lambda res: res != 0,
}
V_ALIASES = {
    "lt": "<",
    "eq": "=",
    "gt": ">",
    "le": "<=",
    "ge": ">=",
    "ne": "!=",
}
V_CHOICES = sorted(V_HANDLERS) + sorted(V_ALIASES)


@dataclasses.dataclass(frozen=True)
class Mode:
    """What they told us to do."""


@dataclasses.dataclass(frozen=True)
class ModeCompare(Mode):
    """Compare two version strings."""

    left: str
    right: str


@dataclasses.dataclass(frozen=True)
class ModeSort(Mode):
    """Sort a list of versions from the standard input stream to the standard output one."""


@dataclasses.dataclass(frozen=True)
class ModeVerify(Mode):
    """Check whether a version comparison relation holds true."""

    left: str
    rel: str
    right: str


def parse_args() -> Mode:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(prog="trivver")

    subp = parser.add_subparsers(help="trivver subcommands")

    cmd_p = subp.add_parser("compare", help="compare the specified versions")
    cmd_p.add_argument("left", type=str, help="the first version string")
    cmd_p.add_argument("right", type=str, help="the second version string")
    cmd_p.set_defaults(mode_func=lambda args: ModeCompare(left=args.left, right=args.right))

    cmd_p = subp.add_parser("verify", help="verify that a relation holds true")
    cmd_p.add_argument("left", type=str, help="the first version string")
    cmd_p.add_argument("rel", type=str, choices=V_CHOICES, help="the relation to verify")
    cmd_p.add_argument("right", type=str, help="the second version string")
    cmd_p.set_defaults(
        mode_func=lambda args: ModeVerify(left=args.left, rel=args.rel, right=args.right)
    )

    cmd_p = subp.add_parser("sort", help="sort a list of versions from stdin to stdout")
    cmd_p.set_defaults(mode_func=lambda _args: ModeSort())

    args = parser.parse_args()

    mode_func: Callable[[argparse.Namespace], Mode] | None = getattr(args, "mode_func", None)
    if mode_func is None:
        sys.exit("No command specified")

    return mode_func(args)


@functools.singledispatch
def run(mode: Mode) -> None:
    """Dispatch to the correct subcommand handler."""
    sys.exit(f"Internal error: unhandled operation mode {mode!r}")


@run.register
def cmd_compare(mode: ModeCompare) -> None:
    """Compare the two versions specified."""
    res = trivver.compare(mode.left, mode.right)
    if res < 0:
        print("<")
    elif res > 0:
        print(">")
    else:
        print("=")


@run.register
def cmd_verify(mode: ModeVerify) -> None:
    """Verify that a relation holds true for the specified versions."""
    rel = V_ALIASES.get(mode.rel, mode.rel)
    handler = V_HANDLERS.get(rel)
    if handler is None:
        sys.exit(f"Invalid relation '{mode.rel}' specified, must be one of {' '.join(V_CHOICES)}")

    res = trivver.compare(mode.left, mode.right)
    sys.exit(0 if handler(res) else 1)


@run.register
def cmd_sort(_mode: ModeSort) -> None:
    """Sort a list of versions supplied on the standard input stream."""
    lines = [line.strip() for line in sys.stdin.readlines()]
    print("\n".join(sorted(lines, key=trivver.key_compare)))


def main() -> None:
    """Parse the command-line arguments, perform the required actions."""
    run(parse_args())


if __name__ == "__main__":
    main()
