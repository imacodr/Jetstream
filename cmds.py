import os
import click
from colorama import Fore, Back, Style
from frames import transformVideo

def createProject(projects_dir, name):
   project_dir = projects_dir / name

   if os.path.exists(project_dir):
      return {"ok": False, "msg": Fore.YELLOW + "⚠️ Project with this name already exists."}

   os.makedirs(project_dir)

   return {"ok": True, "path": project_dir}



@click.command()
@click.option("-i", "--input", prompt="Provide path to video (You can drag it here!)", help="Video to create project", type=click.File('r'))
@click.option("-n", "--name", prompt="Name your project", help="Name for the project", type=str)
@click.pass_context
def create(ctx: click.Context, input, name) -> None: 
   """Create a Jetstream project"""
   config = ctx.obj["config"]

   project = createProject(ctx.obj["projects_dir"], name)

   if not project["ok"]:
      click.echo(project["msg"])
      return

   transformVideo(input, project["path"])
   

