# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
#
"""Test the command-line invocation routines."""

from __future__ import annotations

import sys
from unittest import mock

import pytest

from trivver import __main__ as tmain

from . import data


@pytest.mark.parametrize("case", data.VERSIONS)
def test_compare(case: data.VersionSet) -> None:
    """Test the 'trivver compare left right' subcommand."""
    res: list[str] = []
    with mock.patch("builtins.print", new=res.append):
        tmain.cmd_compare(tmain.ModeCompare(left=case.left, right=case.right))

    assert res == [data.EXPECTED_TO_STR[case.expected]]


@pytest.mark.parametrize("case", data.VERSIONS)
def test_main_compare(case: data.VersionSet) -> None:
    """Test the 'trivver compare left right' invocation."""
    res: list[str] = []
    with mock.patch.object(
        sys, "argv", new=["trivver", "compare", case.left, case.right]
    ), mock.patch("builtins.print", new=res.append):
        tmain.main()

    assert res == [data.EXPECTED_TO_STR[case.expected]]


@pytest.mark.parametrize("case", data.VERSIONS)
def test_verify(case: data.VersionSet) -> None:
    """Test the 'trivver verify left op right' subcommand."""
    rels = data.EXPECTED_TO_REL[case.expected]
    res: list[int] = []

    assert len(rels[False]) + len(rels[True]) == len(tmain.V_HANDLERS) + len(tmain.V_ALIASES)
    for rel in rels[False]:
        with mock.patch("sys.exit", new=res.append):
            tmain.cmd_verify(tmain.ModeVerify(left=case.left, right=case.right, rel=rel))

    for rel in rels[True]:
        with mock.patch("sys.exit", new=res.append):
            tmain.cmd_verify(tmain.ModeVerify(left=case.left, right=case.right, rel=rel))

    assert res == ([1] * len(rels[False])) + ([0] * len(rels[True]))


@pytest.mark.parametrize("case", data.VERSIONS)
def test_main_verify(case: data.VersionSet) -> None:
    """Test the 'trivver verify left op right' subcommand."""
    rels = data.EXPECTED_TO_REL[case.expected]
    res: list[int] = []

    assert len(rels[False]) + len(rels[True]) == len(tmain.V_HANDLERS) + len(tmain.V_ALIASES)
    for rel in rels[False]:
        with mock.patch.object(
            sys,
            "argv",
            new=["trivver", "verify", case.left, rel, case.right],
        ), mock.patch("sys.exit", new=res.append):
            tmain.main()

    for rel in rels[True]:
        with mock.patch.object(
            sys,
            "argv",
            new=["trivver", "verify", case.left, rel, case.right],
        ), mock.patch("sys.exit", new=res.append):
            tmain.main()

    assert res == ([1] * len(rels[False])) + ([0] * len(rels[True]))


def test_sort() -> None:
    """Test the 'trivver sort' functionality."""
    res: list[str] = []
    with mock.patch.object(
        sys.stdin,
        "readlines",
        return_value=[item + "\n" for item in data.UNSORTED],
    ), mock.patch("builtins.print", new=res.append):
        tmain.cmd_sort(tmain.ModeSort())

    assert res == ["\n".join(data.SORTED)]


def test_main_sort() -> None:
    """Test the 'trivver sort' functionality."""
    res: list[str] = []
    with mock.patch.object(sys, "argv", new=["trivver", "sort"]), mock.patch.object(
        sys.stdin,
        "readlines",
        return_value=[item + "\n" for item in data.UNSORTED],
    ), mock.patch("builtins.print", new=res.append):
        tmain.main()

    assert res == ["\n".join(data.SORTED)]
