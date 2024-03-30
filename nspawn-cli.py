#!/usr/bin/env python3

import sys

# DEPENDENCIES: requests

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


def image_list():
    # TODO: grab from the "index.json" from main branch
    return [
        ("alpine", 1.0),
        ("arch", 1.0),
        ("debian", 1.0),
        ("ubuntu", 1.0),
        ("nginx", 1.0),
    ]


def command_pull():
    pass


def command_new():
    pass


def command_list():
    pass


def main():
    match sys.argv[1]:
        case "pull":
            command_pull()
        case "new":
            command_new()
        case "list":
            command_list()
        case _:
            print("Incorrect subcommand. Check --help")


if __name__ == "__main__":
    main()
