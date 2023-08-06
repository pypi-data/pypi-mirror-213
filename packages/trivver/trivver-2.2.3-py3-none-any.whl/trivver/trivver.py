# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
#
"""Implement the version comparison function."""

from __future__ import annotations

import dataclasses
import functools
import os
import re
import typing


if typing.TYPE_CHECKING:
    from typing import Any


_RE_NUM_ALPHA = re.compile(r"(?P<num> [0-9]* ) (?P<alpha> .*) $", re.X)
_RE_NUM_END = re.compile(r"^(?P<prologue> .*? ) (?P<num> [0-9]* ) $", re.X)
_RE_EPOCH = re.compile(r"(?: (?P<epoch> [0-9]+ ) : )? (?P<rest> [^:]+ ) $", re.X)


class InvalidEpochError(ValueError):
    """The version string does not conform to the [epoch:]rest pattern."""


@dataclasses.dataclass
class InternalError(Exception):
    """Something went really, really wrong."""

    what: Any
    """The object(s) that had an unexpected value."""

    def __str__(self) -> str:
        """Provide a human-readable representation."""
        return f"trivver internal error: cannot handle {self.what!r}"


def _version_split_num_alpha(ver: str) -> tuple[str, str]:
    """Split a version component into a numeric and an alphanumeric part.

    "2a" is split into ('2', 'a').
    """
    match = _RE_NUM_ALPHA.match(ver)
    if match is None:
        raise InternalError(ver)
    data = match.groupdict()
    return data["num"], data["alpha"]


def _version_compare_split_empty(spl_a: list[str], spl_b: list[str]) -> int | None:
    """Check if any of the split version numbers is empty."""
    if not spl_a:
        if not spl_b:
            return 0
        if not _version_split_num_alpha(spl_b[0])[0]:
            return 1
        return -1
    if not spl_b:
        if not _version_split_num_alpha(spl_a[0])[0]:
            return -1
        return 1

    return None


def _version_compare_split_comp_int(comp_a: str, comp_b: str) -> int | None:
    """Compare a single component of split version numbers."""
    if comp_a:
        if comp_b:
            num_a, num_b = int(comp_a, 10), int(comp_b, 10)
            if num_a < num_b:
                return -1
            if num_a > num_b:
                return 1
        else:
            return 1
    elif comp_b:
        return -1

    return None


def _get_ver_prefix(comp_a: str, comp_b: str) -> tuple[int | None, str, str]:
    """Determine the common prefix, leaving trailing digits out."""
    prefix = os.path.commonprefix([comp_a, comp_b])
    if comp_a.startswith(prefix + "~"):
        return -1, "", ""
    if comp_b.startswith(prefix + "~"):
        return 1, "", ""

    if prefix:
        match_dig = _RE_NUM_END.match(prefix)
        if match_dig:
            prefix = match_dig.group("prologue")

    rest_a, rest_b = comp_a[len(prefix) :], comp_b[len(prefix) :]
    if not rest_a:
        return -1, "", ""
    if not rest_b:
        return 1, "", ""

    return None, rest_a, rest_b


def _version_compare_split_comp_str(comp_a: str, comp_b: str) -> int | None:
    """Compare strings, possibly recursing into version_compare_split()."""
    if comp_a == comp_b:
        return None

    res, comp_a, comp_b = _get_ver_prefix(comp_a, comp_b)
    if res is not None:
        return res

    # If they both start with numbers, go recurse.
    if comp_a[0] in "0123456789" and comp_b[0] in "0123456789":
        res = version_compare_split([comp_a], [comp_b])
        return None if res == 0 else res

    if comp_a < comp_b:
        return -1
    return 1


def version_compare_split(spl_a: list[str], spl_b: list[str]) -> int:
    """Compare two version numbers already split into component lists.

    Returns -1, 0, or 1 for the first version being less than, equal to,
    or greater than the second one.
    """
    res = _version_compare_split_empty(spl_a, spl_b)
    if res is not None:
        return res

    first_a, *spl_a = spl_a
    first_b, *spl_b = spl_b
    (num_a, rem_a) = _version_split_num_alpha(first_a)
    if (not num_a) and (not rem_a):
        raise InternalError(first_a)
    (num_b, rem_b) = _version_split_num_alpha(first_b)
    if (not num_b) and (not rem_b):
        raise InternalError(first_b)

    res = _version_compare_split_comp_int(num_a, num_b)
    if res is not None:
        return res

    res = _version_compare_split_comp_str(rem_a, rem_b)
    if res is not None:
        return res

    return version_compare_split(spl_a, spl_b)


def _version_compare_split_dash(spl_a: list[str], spl_b: list[str]) -> int:
    """Compare two lists of dash-separated dot-containing components.

    Returns -1, 0, or 1 for the first version being less than, equal to,
    or greater than the second one.
    """
    res = _version_compare_split_empty(spl_a, spl_b)
    if res is not None:
        return res

    (first_a, first_b) = (spl_a.pop(0), spl_b.pop(0))
    res = version_compare_split(first_a.split("."), first_b.split("."))
    if res != 0:
        return res

    return _version_compare_split_dash(spl_a, spl_b)


def parse_epoch(ver: str) -> tuple[str, str]:
    """Retrieve an epoch if there is one, otherwise return "0"."""
    data = _RE_EPOCH.match(ver)
    if data is None:
        raise InvalidEpochError(ver)

    return data.group("epoch") or "0", data.group("rest")


def compare(ver_a: str, ver_b: str) -> int:
    """Compare two version numbers as strings.

    Returns -1, 0, or 1 for the first version being less than, equal to,
    or greater than the second one.
    """
    (ep_a, rest_a), (ep_b, rest_b) = parse_epoch(ver_a), parse_epoch(ver_b)
    res = _version_compare_split_comp_int(ep_a, ep_b)
    if res is not None:
        return res

    return _version_compare_split_dash(rest_a.split("-"), rest_b.split("-"))


key_compare = functools.cmp_to_key(compare)

__all__ = ("compare", "key_compare")
