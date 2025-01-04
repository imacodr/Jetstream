import os
import click

from jetstreamcli.config import load_config, PROJECTS_DIR
from jetstreamcli.cmds import create, builds
from jetstreamcli.robloxcmds import set,uploader,test
from jetstreamcli.projectscmds import view, open, generate, download

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """🚀 Jetstream - Roblox utility tool for converting videos/gifs into frames for importing into Roblox"""

    config = load_config()

    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)

    ctx.obj = {"projects_dir": PROJECTS_DIR, "config": config}

cli.add_command(create)
cli.add_command(builds)

@cli.group()
def roblox():
    """manage your Roblox configurations"""
    
roblox.add_command(set)
roblox.add_command(uploader)
roblox.add_command(test)

@cli.group()
def projects():
    """manage your Jetstream projects"""

projects.add_command(view)
projects.add_command(open)
projects.add_command(generate)
projects.add_command(download)
