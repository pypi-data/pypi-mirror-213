#!/bin/sh
#
# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause

set -e
set -x

usage()
{
	cat <<'EOUSAGE'
Usage:	test-docker [-C] [-M mirror_url] -i image
	-C	copy the global.index-url and global.trusted-host pip config options
	-i	specify the Docker image name to use
	-M	specify the Debian mirror to use instead of http://deb.debian.net/debian
EOUSAGE
}

unset copy_pip image mirror
while getopts 'Ci:M:' o; do
	case "$o" in
		C)
			copy_pip=1
			;;

		i)
			image="$OPTARG"
			;;

		M)
			mirror="$OPTARG"
			;;
		*)
			usage 1>&2
			exit 1
			;;
	esac
done

if [ -z "$image" ]; then
	echo 'No Docker image name specified' 1>&2
	exit 1
fi

tools/cleanpy.sh

unset pip_index_url pip_trusted_host
if [ -n "$copy_pip" ]; then
	if python3 -m pip config list | grep -Eqe '^global\.index-url='; then
		pip_index_url="$(python3 -m pip config get global.index-url)"
	fi
	if python3 -m pip config list | grep -Eqe '^global\.trusted-host='; then
		pip_trusted_host="$(python3 -m pip config get global.trusted-host)"
	fi
fi

srcdir="$(pwd)"
docker run --rm -it -v "$srcdir:/opt/triv:ro" -- "$image" \
	/opt/triv/tools/test-in-docker.sh \
	${mirror:+-M "$mirror"} \
	${pip_index_url+-I "$pip_index_url"} \
	${pip_trusted_host:+-H "$pip_trusted_host"} \
	-s /opt/triv

tools/cleanpy.sh
