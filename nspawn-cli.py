#!/usr/bin/env python3

import sys
import argparse
import json

import urllib.request

# urllib.request.urlopen
# urllib.request.urlretrieve


HELP_SCREEN = f"""\
Usage: {sys.argv[0]} [SUBCOMMAND] [OPTIONS]

Subcommands:
    run <IMAGE> [NAME] - Run a container image
        HELP FOR RUN
    pull <IMAGE> [PATH] - Pull base image
        OPTIONAL WHERE TO PULL
    list - List available base images
"""

if len(sys.argv) < 2:
    print("ERROR: Subcommand not provided. Check --help")
    exit(1)


def get_image_index():
    return json.loads(
        urllib.request.urlopen(
            "https://raw.githubusercontent.com/Ernest1338/nspawn-registry/main/index.json"
        )
        .read()
        .decode()
    )


def command_pull():
    pass


def command_new():
    pass


def command_list():
    images = get_image_index()
    for image in images:
        name = image["name"]
        version = image["version"]
        print(f"{name} (v{version})")


def main():
    parser = argparse.ArgumentParser(
        prog="nspawn-cli",
        description="systemd-nspawn registry CLI",
    )

    subparsers = parser.add_subparsers(title="Subcommands", dest="subcommands")

    subcom_pull = subparsers.add_parser("pull")
    subcom_new = subparsers.add_parser("new")
    subcom_list = subparsers.add_parser("list")

    args = parser.parse_args()

    if args.subcommands == "pull":
        command_pull()
    elif args.subcommands == "new":
        command_new()
    elif args.subcommands == "list":
        command_list()
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
