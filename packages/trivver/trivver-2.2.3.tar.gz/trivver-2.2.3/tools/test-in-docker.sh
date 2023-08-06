#!/bin/sh
#
# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

set -e
set -x

usage()
{
	cat <<'EOUSAGE'
Usage:	test-in-docker -s srcdir
	-H	specify the value of the global.trusted-host pip config setting
	-I	specify the value of the global.index-url pip config setting
	-M	specify the Debian mirror to use instead of http://deb.debian.net/debian
	-s	specify the trivver source directory to copy
EOUSAGE
}

apt_update_if_needed()
{
	if [ -n "$apt_run" ]; then
		return
	fi

	apt-get update
	apt_run=1
}

apt_install()
{
	if [ "$#" -eq 0 ]; then
		echo 'test-in-docker internal error: apt_install invoked without arguments' 1>&2
		exit 1
	fi

	env DEBIAN_FRONTEND='noninteractive' apt-get -y -- install "$@"
}

install_python3()
{
	local py3=''
	py3="$(command -v python3 2>/dev/null || true)"
	if [ -n "$py3" ]; then
		return
	fi

	apt_update_if_needed
	apt_install python3
}

install_python3_venv()
{
	if dpkg-query -W -f '${db:Status-Abbrev}\n' -- python3-venv 2>/dev/null | grep -Eqe '^ii'; then
		return
	fi

	apt_update_if_needed
	apt_install python3-venv
}

unset mirror pip_index_url pip_trusted_host srcdir
while getopts 'H:I:M:s:' o; do
	case "$o" in
		H)
			pip_trusted_host="$OPTARG"
			;;

		I)
			pip_index_url="$OPTARG"
			;;

		M)
			mirror="$OPTARG"
			;;

		s)
			srcdir="$OPTARG"
			;;

		*)
			usage 1>&2
			exit 1
			;;
	esac
done

if [ -z "$srcdir" ]; then
	echo 'No trivver source directory specified' 1>&2
	exit 1
fi
if [ ! -f "$srcdir/src/trivver/__main__.py" ]; then
	echo "Not a trivver source directory: $srcdir" 1>&2
	exit 1
fi

if [ -n "$mirror" ]; then
	if [ -f /etc/apt/sources.list ]; then
		sed -r -i -e 's@\bhttp://deb.debian.org/debian @'"$mirror"' @' -- /etc/apt/sources.list
		cat /etc/apt/sources.list
	fi

	if [ -f /etc/apt/sources.list.d/debian.sources ]; then
		sed -r -i -e 's@\bhttp://deb.debian.org/debian$@'"$mirror"'@' -- /etc/apt/sources.list.d/debian.sources
		cat /etc/apt/sources.list.d/debian.sources
	fi
fi

tempd="$(mktemp -d -t trivver-test.XXXXXX)"
# We do intend to expand it when the "trap" builtin runs.
# shellcheck disable=SC2064
trap "rm -rf -- '$tempd'" HUP INT TERM QUIT EXIT

trivsrc="$tempd/trivver"
cp -Rpv -- "$srcdir/" "$trivsrc"
if [ ! -f "$trivsrc/src/trivver/__main__.py" ]; then
	echo "No $trivsrc/src/trivver/__main__.py file" 1>&2
	find -- "$trivsrc" -print 1>&2 || true
	echo "Could not copy the '$srcdir' trivver source directory to '$trivsrc'" 1>&2
	exit 1
fi

if [ -n "$pip_index_url$pip_trusted_host" ]; then
	mkdir -p "$HOME/.config/pip"
	cat >> "$HOME/.config/pip/pip.conf" <<EOCONF
[global]
${pip_index_url:+index-url = $pip_index_url}
${pip_trusted_host:+trusted-host = $pip_trusted_host}
EOCONF
	cat -- "$HOME/.config/pip/pip.conf"
fi

unset apt_run
install_python3
install_python3_venv

toxvenv="$tempd/venv-tox"
toxpy="$toxvenv/bin/python3"
python3 -m venv -- "$toxvenv"
"$toxpy" -m pip list --format freeze > "$tempd/venv-list-all.txt"
awk -F'==' '$2 != "0.0.0" { print $1 }' < "$tempd/venv-list-all.txt" > "$tempd/venv-list-real.txt"
xargs -r -- "$toxpy" -m pip install -U < "$tempd/venv-list-real.txt"

"$toxpy" -m pip install 'tox >= 4.1, < 5'

cd -- "$trivsrc"
env TEST_CARGO_INDEX_PATH= "$toxpy" -m tox run-parallel

echo 'Seems fine'
