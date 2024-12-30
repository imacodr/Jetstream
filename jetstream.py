import os
import click
import cmds
import inquirer
import json

from pathlib import Path
from config import load_config, save_config, PROJECTS_DIR
from colorama import Fore, Back, Style
from robloxFuncs import keyTest, generate_script

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
@click.pass_context
def view(ctx: click.Context):
    """View all Jetstream projects"""

    projects = ctx.obj["projects_dir"]
    
    click.echo("")
    click.echo(Fore.RED + "🚀 Jetstream Projects")
    click.echo(Fore.RESET + "")

    for dir in os.listdir(projects):
        if not str(dir).startswith("."):
            click.echo(Fore.WHITE + dir + Fore.BLUE + f" ({projects / dir})")

    click.echo("")


@projects.command()
@click.pass_context
def download(ctx: click.Context):
    """Download Jetstream script (Must have finished build)"""

    projects = ctx.obj["projects_dir"]

    choices = []

    files = []

    index = 0

    project = 1

    for p in os.walk(projects):
      file = cmds.find("build.json", p[0])
      if file != None and index != 0:
         files.insert(index, file)

         with open(file, "r") as f:
            jdic = json.load(f)

         project_name = file.split("projects/")
         if jdic["completed"]:
            choices.insert(project, str(project) + ". " + project_name[1])
         project = project + 1

      index = index + 1   

    if len(choices) <= 0:
        click.echo("")
        click.echo("ℹ️  You don't have any builds completed to download")
        click.echo("")
        return
    
    questions = [
      inquirer.List('chosen_build', message = "Select builds", choices=choices)
    ]

    answers = inquirer.prompt(questions)
   
    splitted_answer = answers["chosen_build"].split(".")

    answer_index = int(splitted_answer[0]) - 1

    with open(files[answer_index], "r") as file:
         data = json.load(file)

    project_dir = files[answer_index].split("/build.json")[0]

    with open(project_dir + "/image_ids.json", "r") as file:
        image_ids = json.load(file)

    generate_script(data["project_name"], image_ids, Path(project_dir))

