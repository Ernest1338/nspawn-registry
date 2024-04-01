#!/usr/bin/env python3

import argparse
import json
import os
import tarfile

import urllib.request

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


class PulledImages:
    def __init__(self):
        self.images = []
        for subdir, dirs, files in os.walk(IMAGES_SAVE_DIR):
            for file in files:
                self.images.append(file)

    def get_image_path(self, image_name: str):
        for filename in self.images:
            local_image_name = filename.split("-")[0]
            if image_name == local_image_name:
                return f"{IMAGES_SAVE_DIR}/{filename}"
        return None

    def is_pulled(self, image_name: str) -> bool:
        return self.get_image_path(image_name) is not None


def command_pull(image_name: str):
    if not os.path.exists(IMAGES_SAVE_DIR):
        os.makedirs(IMAGES_SAVE_DIR)

    index = ImageIndex()
    image = index.get(image_name)

    if image is None:
        print(f"[!] ERROR: Image not found: {image_name}")
        exit(1)

    image_version = image["version"]

    image_file = f"{image_name}-{image_version}.tar.gz"

    pull_path = os.path.join(IMAGES_SAVE_DIR, image_file)

    if os.path.exists(pull_path):
        print("[!] Image already exists. Updating...")
        os.remove(pull_path)

    print(f"[+] Pulling image: '{image_name}' into '{pull_path}'")

    try:
        urllib.request.urlretrieve(url=image["url"], filename=f"{pull_path}")
    except:
        print("[!] ERROR: Retrieving image")


def command_new(image_name: str, new_image_path: str):
    pulled_images = PulledImages()
    image_path = pulled_images.get_image_path(image_name)

    if image_path is None:
        print(f"[!] ERROR: Image not pulled: '{image_name}'")
        exit(1)

    if new_image_path is None:
        new_image_path = image_name

    if os.path.exists(new_image_path):
        print(f"[!] ERROR: Directory '{new_image_path}' already exists")
        exit(1)

    print(f"[+] Creating new instance of '{image_name}' at '{new_image_path}'")

    try:
        image_tar = tarfile.open(image_path)
        image_tar.extractall(new_image_path)
    except:
        print("[!] ERROR: Instancing a new image")
        exit(1)


def command_rm(image_name: str):
    pulled_images = PulledImages()
    image_path = pulled_images.get_image_path(image_name)

    if image_path is None:
        print(f"[!] ERROR: Image not pulled: '{image_name}'")
        exit(1)

    print(f"[+] Removing image: '{image_name}' at '{image_path}'")
    os.remove(image_path)


def command_list():
    index = ImageIndex()
    pulled_images = PulledImages()
    for image in index.get_images():
        name = image["name"]
        version = image["version"]
        pulled = " [pulled]" if pulled_images.is_pulled(name) else ""
        print(f"{name} (v{version}){pulled}")


def main():
    parser = argparse.ArgumentParser(
        prog="nspawn-cli",
        description="systemd-nspawn registry CLI",
    )

    subparsers = parser.add_subparsers(title="Subcommands", dest="subcommands")

    subcom_pull = subparsers.add_parser(
        "pull", help=f"Pull image into {IMAGES_SAVE_DIR}"
    )
    subcom_pull.add_argument("image_name")

    subcom_new = subparsers.add_parser("new", help="Instantiate new image at give path")
    subcom_new.add_argument("image_name")
    subcom_new.add_argument("path", nargs="?")

    subcom_rm = subparsers.add_parser(
        "rm", help="Remove given image from local registry"
    )
    subcom_rm.add_argument("image_name")

    subparsers.add_parser("list")

    args = parser.parse_args()

    if args.subcommands == "pull":
        command_pull(args.image_name)
    elif args.subcommands == "new":
        command_new(args.image_name, args.path)
    elif args.subcommands == "rm":
        command_rm(args.image_name)
    elif args.subcommands == "list":
        command_list()
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
