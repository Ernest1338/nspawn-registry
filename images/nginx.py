#!/usr/bin/env python3

import os
import sys

BASE_IMAGE = "alpine"
DESTINATION = sys.argv[1] if len(sys.argv) > 1 else "nginx-image"


def execute(cmd):
    print(f"[$] Executing: {cmd}")
    os.system(cmd)


# TODO: maybe use the registry to get the base image instead of building it in a script?
execute(f"./{BASE_IMAGE}.py {DESTINATION}")

execute(f"systemd-nspawn -D {DESTINATION} apk add nginx")

print(f"[+] Successfully built nginx image at: {DESTINATION}")
