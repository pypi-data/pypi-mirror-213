trivver(1)
; 
; SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
; SPDX-License-Identifier: BSD-2-Clause

# NAME

trivver - compare version strings in all their varied glory

# SYNOPSIS

*trivver* *compare* _left_ _right_

*trivver* *verify* _left_ _rel_ _right_

*trivver* *sort* < _input_

# DESCRIPTION

The *trivver* utility exposes some of the functions in the *trivver*
Python library via a command-line interface.
Just as the underlying Python library, this utility does not strive for
completeness in the formats of version strings that it supports.
Some version strings sorted by its rules are:
- 0.1.0
- 0.2.alpha
- 0.2
- 0.2.1
- 0.2a
- 0.2a.1
- 0.2p3
- 1.0.beta
- 1.0.beta.2
- 1.0

In particular, note that "1.0a" is considered greater than "1.0";
alpha/beta/pre-release versions are indicated by another dot, as in
"1.0.a".

The *trivver* utility provides three commands:

- *compare*: compare two version strings ++
  The *compare* subcommand takes two version strings as arguments and
  outputs a single character followed by a newline.
  The character is "<", ">", or "=", if the left version string
  represents a version that is respectively less than, greater than, or
  the same as the one represented by the right version string.

- *verify*: check whether a relation holds ++
  The *verify* subcommand checks whether the two specified version strings
  are indeed in the specified relation.
  If so, the *trivver* utility will exit with a status code of 0.
  If not, the exit status will be 1.
  The relation may be one of "<", ">", "=", "<=", ">=", "!=",
  "lt", "gt", "eq", "le", "ge", or "ne".

- *sort*: read version strings and output them in sorted order ++
  The *sort* subcommand reads a list of version strings from the standard
  input stream, one per line, then prints them out on the standard output
  stream in sorted order.

# ENVIRONMENT

The operation of the *trivver* utility is not directly influenced by
any environment variables.

# FILES

The operation of the *trivver* utility is not directly influenced by
the contents of any files.

# EXAMPLES

Compare two version numbers; the result should be a single ">" line:

	trivver compare 1.0 0.5

Make sure the above relation holds:

	if trivver verify 0.5 lt 1.0; then echo yes; else echo no; fi

Sort a list of version strings:

	trivver sort < versions.txt

# DIAGNOSTICS

If run with the *compare* or *sort* subcommands, the *trivver* utility
will exit 0 on success and >0 if an error occurs.

If run with the *verify* subcommand, the *trivver* utility will exit with
0 or 1 depending on whether the specified relation holds.
Any other exit status indicates an error.

# HISTORY

The *trivver* Python library was written by Peter Pentchev in 2020.
The *trivver* command-line utility was written in 2021.

# AUTHORS

Peter Pentchev <roam@ringlet.net>
