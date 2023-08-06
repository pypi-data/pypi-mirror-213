<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# Compare package versions in all their varied glory.

\[[Home][ringlet] | [GitLab][gitlab] | [PyPI][pypi]\]

## Description

This module provides the `compare()` function which compares two
version strings and returns a negative value, zero, or a positive
value depending on whether the first string represents a version
number lower than, equal to, or higher than the second one, and
the `key_compare()` function which may be used as a key for e.g.
`sorted()`.

This module does not strive for completeness in the formats of
version strings that it supports. Some version strings sorted by
its rules are:

- 0.1.0
- 0.2.alpha
- 0.2
- 0.2.1
- 0.2a
- 0.2a.1
- 0.2a3
- 0.2a4
- 0.2p3
- 1.0~bpo3
- 1.0.beta
- 1.0.beta.2
- 1.0.beta2
- 1.0.beta3
- 1.0
- 1.0.4
- 1:0.3

See [the change log](changes.md) for the history of `trivver` development.

## Contact

This module is [developed in a Gitlab repository][gitlab].
The author is [Peter Pentchev][roam].

[ringlet]: https://devel.ringlet.net/devel/trivver/ "The trivver homepage at Ringlet"
[gitlab]: https://gitlab.com/ppentchev/python-trivver "The trivver repository at GitLab"
[pypi]: https://pypi.org/project/trivver/ "The trivver page at PyPI"
[roam]: mailto:roam@ringlet.net "Peter Pentchev"
