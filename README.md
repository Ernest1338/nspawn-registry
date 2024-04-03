# `systemd-nspawn` image registry

Each file in the `images` directory is a script producing one image.
Each script independent of one another so it is possible to run just it to produce a image on it's own.

### `nspawn-cli`

This is the CLI for the registry allowing you to interact with the registry.
Main CLI functionalities:
- pull - Pull given image to local registry
- new - Create a new container instance given a locally pulled image
- rm - Remove image from local registry
- list - List images in the registry (with installed ones highlighted)

### `index.json`

This is the main image index. This file in beeing pulled by the `nspawn-cli` to get info about the
current state of the registry and it's images.

### LICENSE
MIT
