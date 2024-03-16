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
