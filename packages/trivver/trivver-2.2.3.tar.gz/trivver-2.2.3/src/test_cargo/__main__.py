# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
#
"""Run some tests using the crates.io index."""

from __future__ import annotations

import argparse
import functools
import json
import os
import pathlib
import random
import re
import subprocess
import sys
from typing import NamedTuple

import utf8_locale


class GitTree(NamedTuple):
    """A single line in the `git ls-tree` output."""

    git_id: str
    git_type: str
    name: str


class CrateVersion(NamedTuple):
    """Cargo information about a single uploaded version of a crate."""

    name: str
    vers: str


class TestedCrate(NamedTuple):
    """A single crate to test."""

    name: str
    versions: list[str]


class Config(NamedTuple):
    """Runtime configuration for the test program."""

    cachedir: pathlib.Path
    program: pathlib.Path
    utf8_env: dict[str, str]


RE_CARGO_FETCH_HEAD = re.compile(r"^ (?P<cid> [0-9a-f]+ ) \s .*? (?P<url> \S+ ) $", re.X)

CARGO_FETCH_URL = "https://github.com/rust-lang/crates.io-index"
CARGO_CACHE_TIMEOUT = 4 * 3600

RE_GIT_TREE_LINE = re.compile(
    r""" ^
    (?P<mode> [0-7]+ ) \s+
    (?P<obj_type> [a-z]+ ) \s+
    (?P<obj_id> [0-9a-f]+ ) \s+
    (?P<name> \S .* )
    $ """,
    re.X,
)

CRATES = [
    TestedCrate(name="expect-exit", versions=["0.1.0", "0.2.0", "0.3.1", "0.4.3"]),
    TestedCrate(
        name="nom",
        versions=[
            "1.0.0-alpha2",
            "1.0.0-beta",
            "1.0.0",
            "7.0.0-alpha1",
            "7.0.0-alpha3",
            "7.0.0",
            "7.1.1",
        ],
    ),
    TestedCrate(
        name="cursed-trying-to-break-cargo",
        versions=[
            "0.0.0-Pre-Release2.7+wO30-w.8.0",
            "0.0.0",
            "1.0.0-0.HDTV-BluRay.1020p.YTSUB.L33TRip.mkv",
            "1.0.0-2.0.0-3.0.0+4.0.0-5.0.0",
            (
                "18446744073709551615.18446744073709551615.18446744073709551615"
                "---gREEAATT-.-V3R510N+--W0W.1.3-.nice"
            ),
            "18446744073709551615.18446744073709551615.18446744073709551615",
        ],
    ),
]


def find_cargo_cache(cargo_index: pathlib.Path, utf8_env: dict[str, str]) -> pathlib.Path:
    """Find the cargo cache directory."""
    remotes: dict[str, dict[str, str]] = {}
    for line in subprocess.check_output(
        ["git", "--no-pager", "config", "--get-regexp", r"^remote\.[^.]+\.(url|fetch)$"],
        cwd=cargo_index,
        encoding="UTF-8",
        env=utf8_env,
    ).splitlines():
        name, value = line.split(maxsplit=1)
        fields = name.split(".")
        if (
            len(fields) != 3  # noqa: PLR2004
            or fields[0] != "remote"
            or fields[2] not in ("fetch", "url")
        ):
            sys.exit(f"Unexpected 'git config get-regexp' output line at {cargo_index}: {line!r}")
        remote = fields[1]
        if remote not in remotes:
            remotes[remote] = {}
        remotes[remote][fields[2]] = value

    found = [item[0] for item in remotes.items() if item[1]["url"] == CARGO_FETCH_URL]
    if len(found) != 1:
        sys.exit(
            f"Expected exactly one {CARGO_FETCH_URL} Git remote repo at "
            f"{cargo_index}, got {found!r}"
        )
    remote = found[0]

    subprocess.check_call(["git", "fetch", remote], cwd=cargo_index)
    subprocess.check_call(["git", "merge", "--ff-only"], cwd=cargo_index)
    return cargo_index


def _parse_ver_line(line: str) -> GitTree:
    """Parse a `git ls-tree` output line."""
    mtree = RE_GIT_TREE_LINE.match(line)
    if not mtree:
        sys.exit(f"Unexpected `git ls-tree` output line: {line!r}")
    return GitTree(
        git_id=mtree.group("obj_id"), git_type=mtree.group("obj_type"), name=mtree.group("name")
    )


def _parse_ver_tree(cfg: Config, treeish: str) -> dict[str, GitTree]:
    """Parse the `git ls-tree` output for the specified tree-like name."""
    lines = subprocess.check_output(
        ["git", "ls-tree", treeish], cwd=cfg.cachedir, encoding="UTF-8", env=cfg.utf8_env
    ).splitlines()
    print(f"Got {len(lines)} lines of `git ls-tree` output")
    return {tree.name: tree for tree in (_parse_ver_line(line) for line in lines)}


def _get_next_ver_tree(cfg: Config, treeish: str, part: str, exp_type: str) -> str:
    """Get the next part of the tree chain."""
    tree = _parse_ver_tree(cfg, treeish).get(part)
    if tree is None:
        sys.exit(f"Could not find '{part}' in the {treeish} Git tree.")
    elif tree.git_type != exp_type:
        sys.exit(f"Not a {exp_type}: {tree!r}")
    return tree.git_id


def get_crate_versions(cfg: Config, crate: str) -> list[str]:
    """Fetch some data about a crate."""

    def get_tree_id() -> str:
        """Parse the trees until we find the crate."""
        if len(crate) in (1, 2):
            parts = [str(len(crate))]
        elif len(crate) == 3:  # noqa: PLR2004
            parts = [str(len(crate)), crate[:1]]
        else:
            parts = [crate[:2], crate[2:4]]

        return functools.reduce(
            lambda current, part: _get_next_ver_tree(
                cfg, current, part, "blob" if part == crate else "tree"
            ),
            [*parts, crate],
            "FETCH_HEAD",
        )

    def parse_vers_line(line: str) -> str:
        """Parse a single crates.io crate version line."""
        raw = json.loads(line)
        if (
            not isinstance(raw, dict)
            or "name" not in raw
            or raw["name"] != crate
            or "vers" not in raw
            or not isinstance(raw["vers"], str)
        ):
            sys.exit(f"Unexpected Cargo version line for {crate}: {line}")
        return raw["vers"]

    print(f"Fetching crates.io data for {crate}")
    tree_id = get_tree_id()
    jlines = subprocess.check_output(
        ["git", "show", tree_id], cwd=cfg.cachedir, encoding="UTF-8", env=cfg.utf8_env
    ).splitlines()
    return [parse_vers_line(line) for line in jlines]


def parse_args(cargo_index: pathlib.Path) -> Config:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(prog="test_cargo")
    parser.add_argument(
        "-p",
        "--program",
        type=pathlib.Path,
        required=True,
        help="the path to the trivver implementation to test",
    )

    args = parser.parse_args()

    utf8_env = utf8_locale.UTF8Detect().detect().env
    return Config(
        cachedir=find_cargo_cache(cargo_index, utf8_env),
        program=args.program,
        utf8_env=utf8_env,
    )


def main() -> None:
    """Parse command-line options, do stuff."""
    cargo_index = os.environ.get("TEST_CARGO_INDEX_PATH")
    if not cargo_index:
        print("Skipping the test, set TEST_CARGO_INDEX_PATH to the path to a Git checkout")
        return

    cfg = parse_args(pathlib.Path(cargo_index))

    for crate in CRATES:
        print(f"Testing {crate.name}")
        versions = get_crate_versions(cfg, crate.name)
        print(f"Got {len(versions)} versions for {crate.name}")
        missing = [vers for vers in crate.versions if vers not in versions]
        if missing:
            sys.exit(f"Cargo metadata for {crate.name} missing versions {missing!r}")

        shuffled = list(versions)
        random.shuffle(shuffled)
        res = subprocess.run(
            [cfg.program, "sort"],
            capture_output=True,
            check=True,
            encoding="UTF-8",
            env=cfg.utf8_env,
            input="".join(vers + "\n" for vers in versions),
        )
        result = res.stdout.splitlines()
        if set(result) != set(versions):
            sys.exit(
                f"`trivver sort` failed: expected {sorted(versions)!r}, got {sorted(result)!r}"
            )

        indices = [result.index(vers) for vers in crate.versions]
        if indices != sorted(indices):
            sys.exit(f"`trivver sort` did not sort the versions correctly: {indices!r}")

        print(f"Tested {crate.name} just fine!")


if __name__ == "__main__":
    main()
