#!/usr/bin/env python3

import sys
import os

if os.getuid() != 0:
    print("Run this script as root")
    exit(1)

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <destination>")

MIRROR = ""
VERSION = ""
DESTINATION = sys.argv[1]

# #!/bin/bash -e
# # Creates a systemd-nspawn container with Arch Linux
#
# MIRROR=http://mirror.fra10.de.leaseweb.net/archlinux
# ISO_DATE=latest
# PKG_GROUPS="base"
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
# tarfile=$(mktemp)
# trap 'rm $tarfile' EXIT
#
# wget "$MIRROR/iso/$ISO_DATE/archlinux-bootstrap-x86_64.tar.gz" -O $tarfile
#
# mkdir -p "$dest"
# tar -xzf $tarfile -C "$dest" --strip-components=1 --numeric-owner
#
# printf 'Server = %s/$repo/os/$arch\n' $MIRROR >"$dest"/etc/pacman.d/mirrorlist
# sed '/^root:/ s|\*||' -i "$dest/etc/shadow" # passwordless login
# rm "$dest/etc/resolv.conf" # systemd configures this
# # https://github.com/systemd/systemd/issues/852
# [ -f "$dest/etc/securetty" ] && \
# 	printf 'pts/%d\n' $(seq 0 10) >>"$dest/etc/securetty"
# cat >"$dest"/setup.sh <<SCRIPT
# pacman-key --init && pacman-key --populate
# pacman -Sy --noconfirm --needed ${PKG_GROUPS}
# rm /setup.sh
# SCRIPT
# systemd-nspawn -q -D "$dest" sh /setup.sh
#
#
# echo ""
# echo "Arch Linux container was created successfully (bootstrapped from $ISO_DATE)"
