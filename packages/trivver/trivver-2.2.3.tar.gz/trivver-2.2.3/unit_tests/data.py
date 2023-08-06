# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
#
"""Definitions and data for the trivver unit tests."""

from __future__ import annotations

from typing import NamedTuple


class VersionSet(NamedTuple):
    """A basic test case for comparing versions."""

    left: str
    right: str
    expected: int


VERSIONS = [
    VersionSet(left="1.0", right="2.0", expected=-1),
    VersionSet(left="1.0", right="1.0.1", expected=-1),
    VersionSet(left="1.0", right="1.0a", expected=-1),
    VersionSet(left="1.0", right="1.0", expected=0),
    VersionSet(left="1.0a", right="1.0a", expected=0),
    VersionSet(left="0.1.0.b", right="0.1.0", expected=-1),
    VersionSet(
        left="3.10.0-1062.1.1.el7.x86_64",
        right="3.10.0-983.13.1.el7.x86_64",
        expected=1,
    ),
    VersionSet(
        left="3.10.0-1062.1.1.el7.x86_64",
        right="3.10.0-1062.1.1.el6.x86_64",
        expected=1,
    ),
    VersionSet(left="2.1", right="2", expected=1),
    VersionSet(left="2.1", right="2.1.a", expected=1),
    VersionSet(left="2.1", right="2.1", expected=0),
    VersionSet(left="2.1", right="2.1a", expected=-1),
    VersionSet(left="2.1", right="2.1.0", expected=-1),
    VersionSet(left="2.1", right="2.1.1", expected=-1),
    VersionSet(left="2.1", right="3", expected=-1),
    VersionSet(left="2.1", right="10", expected=-1),
    VersionSet(left="2.1", right="10.1", expected=-1),
    VersionSet(left="2.1", right="1:1.0", expected=-1),
    VersionSet(left="3.0.beta2", right="1", expected=1),
    VersionSet(left="3.0.beta2", right="3.0", expected=-1),
    VersionSet(left="3.0.beta2", right="3.0.beta1", expected=1),
    VersionSet(left="3.0.beta2", right="3.0.beta2", expected=0),
    VersionSet(left="3.0.beta2", right="3.0.beta3", expected=-1),
    VersionSet(left="3.0.beta2", right="3.0.0", expected=-1),
    VersionSet(left="str12foo7", right="str1foo7", expected=1),
    VersionSet(left="str12foo7", right="str12foo1", expected=1),
    VersionSet(left="str12foo7", right="str12foo6", expected=1),
    VersionSet(left="str12foo7", right="str12foo7", expected=0),
    VersionSet(left="str12foo7", right="str12foo8", expected=-1),
    VersionSet(left="str12foo7", right="str12foo10", expected=-1),
    VersionSet(left="str12foo7", right="str12foo73", expected=-1),
    VersionSet(left="str12foo7", right="str13foo1", expected=-1),
    VersionSet(left="4.15.0-3", right="4.15.0-3~bpo10", expected=1),
    VersionSet(left="4.15.0-3bpo10", right="4.15.0-3~bpo10", expected=1),
    VersionSet(left="1:1.0", right="2.1", expected=1),
    VersionSet(left="42:2.1", right="10.1", expected=1),
]

EXPECTED_TO_STR = {
    -1: "<",
    0: "=",
    1: ">",
}

EXPECTED_TO_REL = {
    -1: {
        False: ["=", ">", ">=", "eq", "gt", "ge"],
        True: ["<", "<=", "!=", "lt", "le", "ne"],
    },
    0: {
        False: ["<", ">", "!=", "lt", "gt", "ne"],
        True: ["=", "<=", ">=", "eq", "le", "ge"],
    },
    1: {
        False: ["<", "=", "<=", "lt", "eq", "le"],
        True: [">", ">=", "!=", "gt", "ge", "ne"],
    },
}

UNSORTED = [
    "3.10.0-1062.1.1.el7.x86_64",
    "1.0a",
    "0.1.0.b",
    "3.10.0-983.13.1.el11.x86_64",
    "1.0",
    "3.10.0-983.13.1.el7.x86_64",
    "4:0.4",
    "4.15.0-3",
    "0.1.0",
    "1.0.1",
    "2.0",
    "3:1.0",
    "3.10.0-1062.1.1.el6.x86_64",
    "4.15.0-3~bpo10",
    "3.10.0-983.13.1.el1.x86_64",
]
SORTED = [
    "0.1.0.b",
    "0.1.0",
    "1.0",
    "1.0.1",
    "1.0a",
    "2.0",
    "3.10.0-983.13.1.el1.x86_64",
    "3.10.0-983.13.1.el7.x86_64",
    "3.10.0-983.13.1.el11.x86_64",
    "3.10.0-1062.1.1.el6.x86_64",
    "3.10.0-1062.1.1.el7.x86_64",
    "4.15.0-3~bpo10",
    "4.15.0-3",
    "3:1.0",
    "4:0.4",
]
