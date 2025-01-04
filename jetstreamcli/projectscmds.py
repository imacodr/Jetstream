import os
import click
import inquirer
from showinfm import show_in_file_manager

from pathlib import Path
from colorama import Fore
from jetstreamcli.robloxfuncs import generate_script, get_image_ids, upload_images
from jetstreamcli.files import read_file
from jetstreamcli.cmds import find

@click.command()
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


@click.command()
@click.pass_context
def download(ctx: click.Context):
    """Download Jetstream script (Must have finished build)"""

    projects = ctx.obj["projects_dir"]

    choices = []

    files = []

    index = 0

    project = 1

    for p in os.walk(projects):
      file = find("build.json", p[0])
      if file != None and index != 0:
         files.insert(index, file)
         
         jdic = read_file(file)
         
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

    if answers == None:
        return
   
    splitted_answer = answers["chosen_build"].split(".")

    answer_index = int(splitted_answer[0]) - 1
    
    data = read_file(files[answer_index])

    project_dir = files[answer_index].split("/build.json")[0]

    image_ids = read_file(project_dir + "/image_ids.json")

    generate_script(data["project_name"], image_ids, Path(project_dir))

@click.command()
@click.pass_context
def generate(ctx: click.Context):
    """Re-generate Decal IDs or Image IDs (Must have finished build)"""

    projects = ctx.obj["projects_dir"]

    choices = []

    files = []

    index = 0

    project = 1

    for p in os.walk(projects):
      file = find("build.json", p[0])
      if file != None and index != 0:
         files.insert(index, file)
         
         jdic = read_file(file)
         
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
      inquirer.List('chosen_build', message = "Select builds", choices=choices),
      inquirer.List('type', message = "What do you want to generate", choices=["decal_ids", "image_ids"])
    ]

    answers = inquirer.prompt(questions)

    if answers == None:
        return
    
    if not click.confirm("⚠️ Are you sure you want to continue? (This will generate a new build)"):
        click.echo("Cancelled.")
        return
   
    splitted_answer = answers["chosen_build"].split(".")

    answer_index = int(splitted_answer[0]) - 1

    data = read_file(files[answer_index])
    
    project_dir = files[answer_index].split("/build.json")[0]

    match answers["type"]:
        case "decal_ids":
            decal_ids = upload_images(data["project_name"], data["paths"], data["big_proj"], Path(project_dir))
            if decal_ids == None:
                return
            image_ids = get_image_ids(decal_ids, Path(project_dir), data["project_name"])
            if image_ids == None:
                return
            generate_script(data["project_name"], image_ids, Path(project_dir))

            click.echo("")
            click.echo(Fore.RED + "🚀 Sucessfully regenerated Decal IDs")
            click.echo("")
        case "image_ids":
            decal_ids = read_file(project_dir + "/decal_ids.json")
            if decal_ids == None:
                return
            image_ids = get_image_ids(decal_ids, Path(project_dir), data["project_name"])
            generate_script(data["project_name"], image_ids, Path(project_dir))

            click.echo("")
            click.echo(Fore.RED + "🚀 Successfully regenerated Image IDs and Script")
            click.echo("")
            

@click.command()
@click.pass_context
def open(ctx: click.Context):
    """Open a project in your file manager"""
    projects = ctx.obj["projects_dir"]

    choices = []

    files = []

    index = 0

    project = 1

    for p in os.walk(projects):
      file = find("build.json", p[0])
      if file != None and index != 0:
         files.insert(index, file)
         
         project_name_split = file.split("projects/")
         project_name = project_name_split[1].split("/build.json")

         choices.insert(project, str(project) + ". " + project_name[0])
         project = project + 1

      index = index + 1   


    if len(choices) <= 0:
        click.echo("")
        click.echo("ℹ️  You don't have any projects to open")
        click.echo("")
        return
    
    choices.append(str(len(choices) + 1) + ". 📁 Projects Folder")
    
    questions = [
      inquirer.List('project', message = "Select project", choices=choices),
    ]
    

    answers = inquirer.prompt(questions)

    if answers == None:
        return
   
    splitted_answer = answers["project"].split(".")

    if int(splitted_answer[0]) == len(choices):
        show_in_file_manager(str(projects))
        return

    answer_index = int(splitted_answer[0]) - 1

    project_dir = files[answer_index].split("/build.json")[0]
    show_in_file_manager(project_dir)