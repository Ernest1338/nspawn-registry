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
# # Creates a systemd-nspawn container with Ubuntu
#
# CODENAME=${CODENAME:-jammy}
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
# rootfs=$(mktemp)
# trap 'rm $rootfs' EXIT
#
# wget "http://cloud-images.ubuntu.com/${CODENAME}/current/${CODENAME}-server-cloudimg-amd64-root.tar.xz" -O $rootfs
#
# mkdir -p "$dest"
# tar -xaf $rootfs -C "$dest" --numeric-owner
#
# sed '/^root:/ s|\*||' -i "$dest/etc/shadow" # passwordless login
# rm "$dest/etc/resolv.conf" # systemd configures this
# # https://github.com/systemd/systemd/issues/852
# [ -f "$dest/etc/securetty" ] && \
# 	printf 'pts/%d\n' $(seq 0 10) >>"$dest/etc/securetty"
# >"$dest/etc/fstab"
# systemd-nspawn -q -D "$dest" /bin/systemctl disable \
# 	ssh systemd-{timesyncd,networkd-wait-online,resolved}
# # uninstall some packages
# systemd-nspawn -q -D "$dest" /usr/bin/apt-get -qq satisfy -y --purge 'Conflicts: lxcfs, lxd, snapd, cloud-init' || \
# 	systemd-nspawn -q -D "$dest" /usr/bin/apt-get -qq purge --autoremove snapd lxcfs lxd cloud-init
#
#
# echo ""
# echo "Ubuntu $CODENAME container was created successfully"
