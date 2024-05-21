#!/usr/bin/env python3

import argparse
import json
import os

import urllib.request

HOME = os.path.expanduser("~")
IMAGES_SAVE_DIR = os.path.join(HOME, ".local", "share", "nspawn-images")


class ImageIndex:
    def __init__(self):
        self.index = json.loads(
            urllib.request.urlopen(
                "https://raw.githubusercontent.com/Ernest1338/nspawn-registry/main/index.json"
                # "http://localhost:8080/index.json"
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

    def get_image_version(self, image_name: str):
        for filename in self.images:
            filename = filename.replace(".tar.gz", "")  # remove suffix
            local_image_name = filename.split("-")[0]
            if image_name == local_image_name:
                return filename.split("-")[1]
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

    pulled_images = PulledImages()
    if pulled_images.is_pulled(image_name):
        if os.path.exists(pull_path):
            print("[+] Up-to-date image already pulled")
            exit(0)
        else:
            print("[+] Image already exists. Updating instead...")
            os.remove(pulled_images.get_image_path(image_name))

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

    os.system(f"mkdir {new_image_path}")
    os.system(f"sudo tar --same-owner -xzf {image_path} -C {new_image_path}")


def command_rm(image_name: str):
    pulled_images = PulledImages()
    image_path = pulled_images.get_image_path(image_name)

    if image_path is None:
        print(f"[!] ERROR: Image not pulled: '{image_name}'")
        exit(1)

    print(f"[+] Removing image: '{image_name}' at '{image_path}'")
    os.remove(image_path)


def command_list(only_print_locally_pulled: bool):
    index = ImageIndex()
    pulled_images = PulledImages()
    out = ""

    for image in index.get_images():
        name = image["name"]
        version = image["version"]
        pulled = (
            f"\t[pulled v{pulled_images.get_image_version(name)}]"
            if pulled_images.is_pulled(name)
            else ""
        )
        if only_print_locally_pulled:
            if pulled != "":
                out += f"{name}\t(v{version}){pulled}\n"
        else:
            out += f"{name}\t(v{version}){pulled}\n"

    print(out.strip() if out != "" else "No images to list")


def main():
    parser = argparse.ArgumentParser(
        prog="nspawn-cli",
        description="systemd-nspawn registry CLI",
        epilog=f"Local registry path: {IMAGES_SAVE_DIR}",
    )

    subparsers = parser.add_subparsers(title="Subcommands", dest="subcommands")

    subcom_pull = subparsers.add_parser(
        "pull", help="pull given image (into local registry)"
    )
    subcom_pull.add_argument("image_name")

    subcom_new = subparsers.add_parser("new", help="instantiate new image at give path")
    subcom_new.add_argument("image_name")
    subcom_new.add_argument("path", nargs="?")

    subcom_rm = subparsers.add_parser(
        "rm", help="remove given image from local registry"
    )
    subcom_rm.add_argument("image_name")

    subcom_list = subparsers.add_parser(
        "list", help="list images present in the registry"
    )
    subcom_list.add_argument(
        "--local", help="only list locally pulled images", action="store_true"
    )

    args = parser.parse_args()

    if args.subcommands == "pull":
        command_pull(image_name=args.image_name)
    elif args.subcommands == "new":
        command_new(image_name=args.image_name, new_image_path=args.path)
    elif args.subcommands == "rm":
        command_rm(image_name=args.image_name)
    elif args.subcommands == "list":
        command_list(only_print_locally_pulled=args.local)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
