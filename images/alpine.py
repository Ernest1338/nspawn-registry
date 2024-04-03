#!/usr/bin/env python3

import sys
import os
import tempfile
import tarfile
import shutil

# FIXME: Do not require root (the apk.static exec requires it)
# FIXME: Do not hard code apk-tools version
# FIXME: Extract system version + append to out file name

if os.getuid() != 0:
    print("Run this script as root")
    exit(1)

MIRROR = "http://dl-cdn.alpinelinux.org/alpine"
VERSION = "latest-stable"
APKTOOLS_VERSION = "2.14.3-r1"
GUESTARCH = "x86"
CHANNEL = "main"
DESTINATION = sys.argv[1] if len(sys.argv) > 1 else "alpine-linux-image"


def execute(cmd):
    print(f"[$] Executing: {cmd}")
    os.system(cmd)


dir = tempfile.TemporaryDirectory(prefix="nspawn-registry-", dir="/tmp")

os.system(
    f'wget -qO- {MIRROR}/{VERSION}/{CHANNEL}/{GUESTARCH}/apk-tools-static-{APKTOOLS_VERSION}.apk \
| tar -xz -C {dir.name} || \
{{ echo "Couldnt download apk-tools, the version might have changed..."; exit 1; }}'
)

execute(
    f'{dir.name}/sbin/apk.static \
-X {MIRROR}/{VERSION}/{CHANNEL} -U --arch {GUESTARCH} \
--allow-untrusted --root "{DESTINATION}" \
--initdb add alpine-base'
)

execute(f'mkdir -p "{DESTINATION}"/{{etc/apk,root}}')

execute(
    f'printf "%s/%s/{CHANNEL}\n" {MIRROR} {VERSION} >"{DESTINATION}"/etc/apk/repositories'
)

# https://github.com/systemd/systemd/issues/852
for i in range(0, 10):
    execute(f'echo "pts/{i}" >> "{DESTINATION}/etc/securetty"')

# make console work
execute(f'sed "/tty[0-9]:/ s/^/#/" -i "{DESTINATION}"/etc/inittab')

execute(
    f'printf "console::respawn:/sbin/getty 38400 console\n" >> "{DESTINATION}"/etc/inittab'
)

for s in ["hostname", "bootmisc", "syslog"]:
    execute(f'ln -s /etc/init.d/{s} "{DESTINATION}"/etc/runlevels/boot/{s}')


for s in ["killprocs", "savecache"]:
    execute(f'ln -s /etc/init.d/{s} "{DESTINATION}"/etc/runlevels/shutdown/{s}')

print(f"\n[+] Successfully built alpine {VERSION} at: {DESTINATION}")

with tarfile.open(f"{DESTINATION}.tar.gz", "w:gz") as tar:
    tar.add(DESTINATION, arcname=".")

shutil.rmtree(DESTINATION)

dir.cleanup()
