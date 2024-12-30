import os
import click
import cmds
from pathlib import Path
from config import load_config, save_config, PROJECTS_DIR
from colorama import Fore, Back, Style
from robloxFuncs import keyTest

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """🚀 Jetstream - Roblox utility tool for converting videos/gifs into frames for importing into Roblox"""\

    config = load_config()

    if not os.path.exists(PROJECTS_DIR):
        os.makedirs(PROJECTS_DIR)

    ctx.obj = {"projects_dir": PROJECTS_DIR, "config": config}

cli.add_command(cmds.create)
cli.add_command(cmds.builds)

@cli.group()
def roblox():
    """manage your Roblox configurations"""

@roblox.command()
@click.option("-k", "--key", prompt="Enter Key", help="Your Roblox Cloud Key", type = str)
def set(key):
    """Set the Roblox Cloud API Key"""
    
    config = load_config()
    config["robloxKey"] = key
    
    save_config(config)

    click.echo(Fore.GREEN + "✅ Successfully saved Roblox API Key.")

@roblox.command()
@click.option("-i", "--id", prompt="Provide the User ID of the uploader (If its a group key, must have permission to use key)", help="The User ID of the uploader", type = str)
def uploader(id):
    """Set the uploader for the Roblox assets"""
    
    config = load_config()
    config["uploader"] = id
    
    save_config(config)

    click.echo(Fore.GREEN + "✅ Successfully saved Roblox uploader.")
    
@roblox.command()
def test():
    """Test your current key"""
    result = keyTest()

    if not result["ok"]:
        click.echo(result["msg"])
    else:
        click.echo("")
        click.echo(Fore.RED + "🚀 Jetstream Key Test")
        click.echo("")
        click.echo(Fore.CYAN + "User found!")
        click.echo("")
        click.echo(Fore.RESET + "Id: " + str(result["id"]))
        click.echo("Username: " + str(result["username"]))
        click.echo("Link: " + Fore.BLUE + f"https://roblox.com/users/{result["id"]}")
        click.echo("")
        click.echo(Fore.GREEN + "✅ Key Works!")

@cli.group()
def projects():
    """manage your Jetstream projects"""

@projects.command()
def view():
    """View all Jetstream projects"""


