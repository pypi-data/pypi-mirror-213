#!/bin/sh
#
# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

set -e

if [ "$#" -ne 1 ]; then
	echo 'Usage: test_main.sh trivver-command' 1>&2
	exit 1
fi
trivver="$1"

echo "trivver invocation: $trivver"
echo "Python interpreter: $(command -v python3)"

tempd="$(mktemp -d -t testdata.XXXXXX)"
trap "rm -rf -- '$tempd'" EXIT HUP INT QUIT TERM

topdir="$(dirname -- "$(dirname -- "$(readlink -f "$0")")")"

echo 'Collecting the versions test data'
env PYTHONPATH="$topdir${PYTHONPATH+:${PYTHONPATH}}" python3 -B -c '
import json

from unit_tests import data

print(
    "\n".join(
        "{left} {right} {exp}".format(
            left=item.left,
            right=item.right,
            exp=data.EXPECTED_TO_STR[item.expected]
        )
        for item in data.VERSIONS
    )
)' > "$tempd/versions.txt"
wc -l -- "$tempd/versions.txt"

while read left right expected; do
	case "$expected" in
		'<')
			other='>'
			;;

		'>')
			other='<'
			;;

		'=')
			other='='
			;;

		*)
			echo "What do we do with '$expected'?'" 1>&2
			exit 1
			;;
	esac

	echo "Comparing $left to $right, expecting '$expected'"
	set +e
	res="$($trivver compare "$left" "$right")"
	exitcode="$?"
	set -e
	if [ "$exitcode" -ne 0 ] || [ "$res" != "$expected" ]; then
		echo "Got exit code $exitcode, result '$res'" 1>&2
		exit 1
	fi

	echo "Comparing $right to $left, expecting '$other'"
	set +e
	res="$($trivver compare "$right" "$left")"
	exitcode="$?"
	set -e
	if [ "$exitcode" -ne 0 ] || [ "$res" != "$other" ]; then
		echo "Got exit code $exitcode, result '$res'" 1>&2
		exit 1
	fi

	echo "Verifying $left $expected $right"
	set +e
	$trivver verify "$left" "$expected" "$right"
	exitcode="$?"
	set -e
	if [ "$exitcode" -ne 0 ]; then
		echo "Got exit code $exitcode" 1>&2
		exit 1
	fi

	echo "Verifying $right $other $left"
	set +e
	$trivver verify "$right" "$other" "$left"
	exitcode="$?"
	set -e
	if [ "$exitcode" -ne 0 ]; then
		echo "Got exit code $exitcode" 1>&2
		exit 1
	fi
done < "$tempd/versions.txt"

echo 'Versions test done'

echo 'Collecting the sorted/unsorted versions data'
env PYTHONPATH="$topdir${PYTHONPATH+:${PYTHONPATH}}" python3 -B -c 'from unit_tests import data; print("\n".join(data.UNSORTED))' > "$tempd/unsorted.txt"
wc -l -- "$tempd/unsorted.txt"

env PYTHONPATH="$topdir${PYTHONPATH+:${PYTHONPATH}}" python3 -B -c 'from unit_tests import data; print("\n".join(data.SORTED))' > "$tempd/expected.txt"
wc -l -- "$tempd/expected.txt"

echo 'Running the sorted/unsorted versions test'

set +e
$trivver sort < "$tempd/unsorted.txt" > "$tempd/sorted.txt"
exitcode="$?"
set -e

diff -u -- "$tempd/expected.txt" "$tempd/sorted.txt"

if [ "$exitcode" -ne 0 ]; then
	echo "Got exit code $exitcode" 1>&2
	exit 1
fi

echo 'Sorted/unsorted versions test done'
