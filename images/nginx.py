#!/usr/bin/env python3

import os
import sys

BASE_IMAGE = "alpine"


def execute(cmd):
    print(f"[$] Executing: {cmd}")
    os.system(cmd)


def build_image():
    DESTINATION = sys.argv[1] if len(sys.argv) > 1 else "nginx-image"

    # TODO: Find a way to require root (the apk.static exec requires it)
    if os.getuid() != 0:
        print("Run this script as root")
        exit(1)

    # TODO: maybe use the registry to get the base image instead of building it in a script?
    execute(f"./{BASE_IMAGE}.py {DESTINATION}")

    execute(f"systemd-nspawn -D {DESTINATION} apk add nginx")

    print(f"[+] Successfully built nginx image at: {DESTINATION}")


if __name__ == "__main__":
    build_image()
