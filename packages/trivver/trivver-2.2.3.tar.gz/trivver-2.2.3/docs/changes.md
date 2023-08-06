<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# Changelog

All notable changes to the trivver project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

More information about in-development changes to `trivver` may be found
[in the GitLab repository][gitlab-changelog].

[gitlab-changelog]: https://gitlab.com/ppentchev/python-trivver/-/blob/master/docs/changes.md "This change log in the GitLab repository"

## [Unreleased]

## [2.2.3] - 2023-06-13

### Additions

- build infrastructure:
    - mark Python 3.10 and 3.11 as supported versions
    - add a couple more trove classifier tags
- test suite:
    - mark the Tox environments with tags for the `tox-stages` tool
    - add the `tools/test-docker.sh` tool to run Tox in a Docker
      container so that we can test with Python 3.7
    - add upper and lower constraints to all Tox dependencies
    - add a Nix expression for running Tox
- documentation:
    - move the changelog to the new mkdocs-based documentation

### Other changes

- switch to SPDX copyright and license tags
- switch to yearless copyright notices
- use `black` 23.x for source code formatting, no changes
- use Ruff's `isort` implementation
- trivver:
    - minor refactoring inspired by Ruff suggestions
    - hide some imports behind `typing.TYPE_CHECKING`
- test-cargo:
    - following Cargo's transition to sparse indexing by default,
      rework the way we get the crates.io index: expect the path to
      a cloned crates.io-index repository
    - minor refactoring inspired by Ruff suggestions
- build infrastructure:
    - switch to `hatchling` for the PEP 517 build
- test suite:
    - update the `tox.ini` file for Tox 4.x
    - drop the `flake8` + `hacking` test environment
    - switch from `ddt` to `pytest.mark.parametrize()`
    - use `utf8-locale` 1.x for the Cargo test, no changes
    - move the `mypy` configuration to the `pyproject.toml` file and
      drop the `python_version` setting, we have other ways to test with
      different versions of Python now
    - add the `ruff` and `ruff-all` test environments
    - drop the `pylint` and `flake8` test environments
- documentation:
    - convert the changelog to the "Keep a Changelog" format

## [2.2.2] - 2022-06-26

### Additions

- add an EditorConfig definitions file
- add a `test_cargo` tool that fetches the version information about
  some crates from Cargo's crates.io index and then uses the command-line
  `trivver` tool to sort the version strings

### Other changes

- drop Python 3.6 support
- drop the no-self-use ignore and make sure pylint is 2.14+ so that
  it does not produce that warning by default
- reformat the source code using 100 characters per line
- use type | None instead of Optional[type]
- use single-dispatch functions for the command-line tool's subcommands

## [2.2.1] - 2022-04-27

### Fixes

- stop `version_compare_split()` from modifying its arguments!
- work around Pylint not recognizing a Callable value as, well, callable

### Other changes

- use black version 22 for source code formatting
- drop the obsolete "basepython = python3" lines from the Tox configuration

## [2.2.0] - 2021-11-12

### Fixes

- if the version string contains a `:` character, it is treated as
  a separator between a single number representing an epoch and
  the rest of the version identifier. Version strings containing more
  than one `:` character or ones where the portion before the `:`
  character is not a valid number are considered invalid and
  the comparison functions will raise an `InvalidEpochError`

## [2.1.0] - 2021-10-24

### Additions

- expose the `version_compare_split()` function; it may be useful in
  other Python projects, too
- add Python 3.9 to the list of supported versions
- add a flake8 + hacking tox environment with some minor formatting
  fixes

### Other changes

- use unittest.mock instead of the standalone mock library

## [2.0.0] - 2021-09-17

### INCOMPATIBLE CHANGES

- teach the comparison algorithm about strings
  followed by numbers, e.g. RedHat's .el7 suffixes, and also about
  Debian's ~bpo suffixes that should compare less than anything, even
  the empty string, similarly to .beta-style suffixes

### Fixes

- catch up with mypy's unbundling of type definitions for third-party
  libraries

### Other changes

- use black version 21 with no changes to the source code
- follow pylint's suggestion to use an f-string

## [1.0.1] - 2021-03-30

### Additions

- add a MANIFEST.in file so that more files will be included in
  the source distribution even if built without `setuptools_scm`

### Other changes

- move some options to the tools invoked by tox.ini to the setup.cfg
  and pyproject.toml files

## [1.0.0] - 2021-03-22

### INCOMPATIBLE CHANGES

- drop Python 2.x compatibility:
  - use types and modules from the Python 3 standard library
  - use type annotations, not type hints
  - subclass NamedTuple, using Python 3.6 variable type annotations

### Additions

- add a PEP 517 buildsystem definition to the pyproject.toml file
- add the py.typed marker
- add a command-line utility exposing some of the functionality
- add a shell tool for testing the command-line utility
- add a manual page generated from an scdoc source file

### Other changes

- reformat the source code using black 20
- switch to a declarative setup.cfg file
- install the module into the `unit_tests` tox environment
- push the source down into a src/ subdirectory

## [0.1.0] - 2020-03-22

### Started

- first public release

[Unreleased]: https://gitlab.com/ppentchev/python-trivver/-/compare/release%2F2.2.3...master
[2.2.3]: https://gitlab.com/ppentchev/python-trivver/-/compare/release%2F2.2.2...release%2F2.2.3
[2.2.2]: https://gitlab.com/ppentchev/python-trivver/-/compare/release%2F2.2.1...release%2F2.2.2
[2.2.1]: https://gitlab.com/ppentchev/python-trivver/-/compare/release%2F2.2.0...release%2F2.2.1
[2.2.0]: https://gitlab.com/ppentchev/python-trivver/-/compare/release%2F2.1.0...release%2F2.2.0
[2.1.0]: https://gitlab.com/ppentchev/python-trivver/-/compare/release%2F2.0.0...release%2F2.1.0
[2.0.0]: https://gitlab.com/ppentchev/python-trivver/-/compare/release%2F1.0.1...release%2F2.0.0
[1.0.1]: https://gitlab.com/ppentchev/python-trivver/-/compare/release%2F1.0.0...release%2F1.0.1
[1.0.0]: https://gitlab.com/ppentchev/python-trivver/-/compare/release%2F0.1.0...release%2F1.0.0
[0.1.0]: https://gitlab.com/ppentchev/python-trivver/-/tags/release%2F0.1.0
