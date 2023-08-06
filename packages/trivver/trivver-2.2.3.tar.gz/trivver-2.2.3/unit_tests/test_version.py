# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
#
"""Test the version comparison routines."""

from __future__ import annotations

import pytest

import trivver
import trivver.trivver as trivver_inner

from . import data


def sign(value: int) -> int:
    """Return the sign of an integer."""
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


@pytest.mark.parametrize(("left", "right", "expected"), data.VERSIONS)
def test_compare(left: str, right: str, expected: int) -> None:
    """Compare a single pair of versions."""
    assert sign(trivver.compare(left, right)) == sign(expected)
    assert sign(trivver.compare(right, left)) == sign(-expected)


def test_sort() -> None:
    """Sort a list of versions."""
    assert sorted(data.UNSORTED, key=trivver.key_compare) == data.SORTED


def test_immutable() -> None:
    """Make sure version_compare_split() does not modify its arguments."""
    first = ["0", "4", "1"]
    second = ["0", "4", "2"]
    assert sign(trivver_inner.version_compare_split(first, second)) == -1
    assert first == ["0", "4", "1"]
    assert second == ["0", "4", "2"]
