---
sidebar_position: 2
---

# Installation

In this start guide we will guide you through the installation and usage of Jetstream, a utility tool for generating short videos on Roblox.

---

## Install Python

You will require Python version 3.12+ & PyPI (Included in Python) to install the CLI tool.

Install Python using this [link](https://www.python.org/downloads/){: target="_blank"}.

---

## Install ffmpeg

For our frame splicing to do its work you will need to install a tool called ffmpeg.

You can find info on how to install it on its [website](https://www.ffmpeg.org/download.html){: target="_blank"}

Or if you have a package manager it is recommended to use it:

=== "choco (Windows)"

    ```sh
    choco install ffmpeg
    ```

=== "homebrew (MacOS)"

    ```sh
    brew install ffmpeg
    ```

=== "apt (Ubuntu)"

    ```sh
    sudo apt install ffmpeg
    ```

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
