#!/usr/bin/env python3

import sys
import os
import tempfile
import tarfile
import shutil


# NOTE: maybe a better mirror?
MIRROR = "https://mirror.rackspace.com/archlinux"
VERSION = "latest"
PKG_GROUPS = "base"


def execute(cmd):
    print(f"[$] Executing: {cmd}")
    os.system(cmd)


def build_image():
    DESTINATION = sys.argv[1] if len(sys.argv) > 1 else f"arch-{VERSION}"

    # TODO: Find a way to require root (the apk.static exec requires it)
    if os.getuid() != 0:
        print("Run this script as root")
        exit(1)

    dir = tempfile.TemporaryDirectory(prefix="nspawn-registry-", dir="/tmp")

    # wget_or_curl "$MIRROR/iso/$ISO_DATE/archlinux-bootstrap-x86_64.tar.zst" $tarfile
    execute(
        f"wget '{MIRROR}/iso/{VERSION}/archlinux-bootstrap-x86_64.tar.zst' -O {dir.name}/arch.tar.zst"
    )

    execute(f"mkdir -p {DESTINATION}")

    execute(
        f"tar --zstd -xvf {dir.name}/arch.tar.zst -C {DESTINATION} --strip-components=1 --numeric-owner"
    )

    # configure mirror
    execute(
        f"printf 'Server = {MIRROR}/$repo/os/$arch\n' > {DESTINATION}/etc/pacman.d/mirrorlist"
    )

    # passwordless login
    execute(f"sed '/^root:/ s|\\*||' -i '{DESTINATION}/etc/shadow'")

    # systemd configures this
    execute(f"rm '{DESTINATION}/etc/resolv.conf'")

    # https://github.com/systemd/systemd/issues/852
    execute(
        f"[ -f '{DESTINATION}/etc/securetty' ] && printf 'pts/%d\n' $(seq 0 10) >>'{DESTINATION}/etc/securetty'"
    )

    # seems to be this bug https://github.com/systemd/systemd/issues/3611
    execute(f"systemd-machine-id-setup --root={DESTINATION}")

    # install the packages
    execute(
        f"""systemd-nspawn -q -D '{DESTINATION}' sh -c '
        pacman-key --init &&
        pacman-key --populate &&
        pacman -Syu --noconfirm --needed {PKG_GROUPS}'"""
    )

    # clean up pacman cache and unnecessary files
    execute(
        f"""systemd-nspawn -q -D '{DESTINATION}' sh -c '
        rm -rf /var/cache/pacman/pkg/* &&
        rm -rf /var/lib/pacman/sync/*'"""
    )

    # make all the files be owned by root
    execute(f'chown -R root:root {DESTINATION}')

    with tarfile.open(f"{DESTINATION}.tar.gz", "w:gz") as tar:
        print("[PACKING INTO FINAL TAR FILE] NOTE: This will take a while")
        tar.add(DESTINATION, arcname=".")

    shutil.rmtree(DESTINATION)

    print(f"\n[+] Successfully built arch {VERSION} at: {DESTINATION}.tar.gz")

    dir.cleanup()


if __name__ == "__main__":
    build_image()
