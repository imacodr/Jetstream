---
sidebar_position: 2
---

# Installation

In this start guide we will guide you through the installation and usage of Jetstream, a utility tool for generating short videos on Roblox.

---

## Install Python

You will require Python version 3.10+ & PyPI (Included in Python) to install the CLI tool.

Install Python using this [link](https://www.python.org/downloads/).

---

## Install Jetstream

To install Jetstream run the following pip or pipx command.

=== "pip"

    ```sh
    pip install --user jetstreamcli
    ```
    (This will install it globally)

=== "pipx"

    ```sh
    pipx install jetstreamcli
    ```
    (This will only work if you have pipx installed with pip)

---

## Run the CLI

You should be able to read the CLI by executing the following command:

```sh
jetstream
```

This should return the following:

```
Usage: jetstream [OPTIONS] COMMAND [ARGS]...

  🚀 Jetstream - Roblox utility tool for converting videos/gifs into frames for
  importing into Roblox

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  builds    access your unfinished Jetstream builds
  create    create a Jetstream project
  projects  manage your Jetstream projects
  roblox    manage your Roblox configurations
```
