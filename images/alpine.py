#!/usr/bin/env python3

import sys
import os
import tempfile
import tarfile
import shutil
import urllib.request
import re


MIRROR = "http://dl-cdn.alpinelinux.org/alpine"
VERSION = "v3.21"
GUESTARCH = "x86_64"
CHANNEL = "main"


def execute(cmd):
    print(f"[$] Executing: {cmd}")
    os.system(cmd)


def get_apk_tools_version():
    contents = (
        urllib.request.urlopen(f"{MIRROR}/{VERSION}/{CHANNEL}/{GUESTARCH}")
        .read()
        .decode()
    )
    pattern = r"(?<=apk-tools-static-)([0-9\.]*-r\d)"
    matches = re.findall(pattern, contents)
    return matches[0] if matches else exit(1)


def build_image():
    DESTINATION = sys.argv[1] if len(sys.argv) > 1 else f"alpine-{VERSION}"

    # TODO: Find a way to require root (the apk.static exec requires it)
    if os.getuid() != 0:
        print("Run this script as root")
        exit(1)

    dir = tempfile.TemporaryDirectory(prefix="nspawn-registry-", dir="/tmp")

    execute(
        f'wget -qO- {MIRROR}/{VERSION}/{CHANNEL}/{GUESTARCH}/apk-tools-static-{get_apk_tools_version()}.apk \
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

    for s in ["console", "null", "random", "urandom", "zero"]:
        execute(f"rm {DESTINATION}/dev/{s}")

    for s in ["hostname", "bootmisc", "syslog"]:
        execute(f'ln -s /etc/init.d/{s} "{DESTINATION}"/etc/runlevels/boot/{s}')

    for s in ["killprocs", "savecache"]:
        execute(f'ln -s /etc/init.d/{s} "{DESTINATION}"/etc/runlevels/shutdown/{s}')

    # make all the files be owned by root
    execute(f'chown -R root:root {DESTINATION}')

    with tarfile.open(f"{DESTINATION}.tar.gz", "w:gz") as tar:
        tar.add(DESTINATION, arcname=".")

    shutil.rmtree(DESTINATION)

    print(f"\n[+] Successfully built alpine {VERSION} at: {DESTINATION}.tar.gz")

    dir.cleanup()


if __name__ == "__main__":
    build_image()
