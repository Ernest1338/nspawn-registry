#!/usr/bin/env python3

import argparse
import json
import os
import tarfile
import shutil

import urllib.request

# TODO: handle image versions

HOME = os.path.expanduser("~")
IMAGES_SAVE_DIR = os.path.join(HOME, ".local", "share", "nspawn-images")


class ImageIndex:
    def __init__(self):
        self.index = json.loads(
            urllib.request.urlopen(
                # "https://raw.githubusercontent.com/Ernest1338/nspawn-registry/main/index.json"
                "http://localhost:8080/index.json"
            )
            .read()
            .decode()
        )

    def get_images(self):
        return self.index

    def get(self, image_name: str):
        for image in self.index:
            if image["name"] == image_name:
                return image
        return None


def get_pulled_images():
    images = []
    for subdir, dirs, files in os.walk(IMAGES_SAVE_DIR):
        for dir in dirs:
            images.append(dir)
    return images


def command_pull(image_name: str):
    if not os.path.exists(IMAGES_SAVE_DIR):
        os.makedirs(IMAGES_SAVE_DIR)

    index = ImageIndex()
    image = index.get(image_name)

    if image is None:
        print(f"[!] ERROR: Image not found: {image_name}")
        exit(1)

    pull_path = os.path.join(IMAGES_SAVE_DIR, image_name)

    if os.path.exists(pull_path):
        print("[!] Image already exists. Updating...")
        shutil.rmtree(pull_path)

    print(f"[+] Pulling image: '{image_name}' into '{IMAGES_SAVE_DIR}/{image_name}'")

    try:
        retrieved_image = urllib.request.urlretrieve(image["url"])[0]
        image_tar = tarfile.open(retrieved_image)
        image_tar.extractall(pull_path)
        os.remove(retrieved_image)
    except:
        print("[!] ERROR: Retrieving image")


def command_new():
    pass


def command_list():
    index = ImageIndex()
    pulled_images = get_pulled_images()
    for image in index.get_images():
        name = image["name"]
        version = image["version"]
        pulled = " [pulled]" if name in pulled_images else ""
        print(f"{name} (v{version}){pulled}")


def main():
    parser = argparse.ArgumentParser(
        prog="nspawn-cli",
        description="systemd-nspawn registry CLI",
    )

    subparsers = parser.add_subparsers(title="Subcommands", dest="subcommands")

    subcom_pull = subparsers.add_parser("pull")
    subcom_pull.add_argument("image_name")

    subcom_new = subparsers.add_parser("new")

    subcom_list = subparsers.add_parser("list")

    args = parser.parse_args()

    if args.subcommands == "pull":
        command_pull(args.image_name)
    elif args.subcommands == "new":
        command_new()
    elif args.subcommands == "list":
        command_list()
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
