#!/usr/bin/env python3

import sys
import os

if os.getuid() != 0:
    print("Run this script as root")
    exit(1)

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <destination>")

MIRROR = "http://dl-cdn.alpinelinux.org/alpine"
VERSION = "latest-stable"
APKTOOLS_VERSION = "2.14.0-r5"
DESTINATION = sys.argv[1]

# #!/bin/bash -e
# # Creates a systemd-nspawn container with Alpine
#
# MIRROR=http://dl-cdn.alpinelinux.org/alpine
# # VERSION=${VERSION:-v3.19}
# VERSION="latest-stable"
# APKTOOLS_VERSION=2.14.0-r5
#
#
# if [ $UID -ne 0 ]; then
# 	echo "run this script as root" >&2
# 	exit 1
# fi
#
# if [ -z "$1" ]; then
# 	echo "Usage: $0 <destination>" >&2
# 	exit 0
# fi
#
# dest="$1"
# apkdir=$(mktemp -d)
# guestarch=x86
# [ "$(uname -m)" == x86_64 ] && guestarch=x86_64
# trap 'rm -r $apkdir' EXIT
#
# wget -qO- $MIRROR/latest-stable/main/x86/apk-tools-static-$APKTOOLS_VERSION.apk \
# 	| tar -xz -C $apkdir || \
# 	{ echo "Couldn't download apk-tools, the version might have changed..."; exit 1; }
#
# $apkdir/sbin/apk.static \
# 	-X $MIRROR/$VERSION/main -U --arch $guestarch \
# 	--allow-untrusted --root "$dest" \
# 	--initdb add alpine-base
#
# mkdir -p "$dest"/{etc/apk,root}
# printf '%s/%s/main\n' $MIRROR $VERSION >"$dest"/etc/apk/repositories
# for i in $(seq 0 10); do # https://github.com/systemd/systemd/issues/852
# 	echo "pts/$i" >>"$dest/etc/securetty"
# done
# # make console work
# sed '/tty[0-9]:/ s/^/#/' -i "$dest"/etc/inittab
# printf 'console::respawn:/sbin/getty 38400 console\n' >>"$dest"/etc/inittab
# # minimal boot services
# for s in hostname bootmisc syslog; do
# 	ln -s /etc/init.d/$s "$dest"/etc/runlevels/boot/$s
# done
# for s in killprocs savecache; do
# 	ln -s /etc/init.d/$s "$dest"/etc/runlevels/shutdown/$s
# done
#
#
# echo ""
# echo "Alpine $VERSION container was created successfully."
