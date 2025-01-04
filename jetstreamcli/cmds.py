import os
import click
import json
import re

from pathlib import Path, PosixPath
from termcolor import colored
from colorama import Fore
import inquirer
from jetstreamcli.frames import transform_video
from jetstreamcli.robloxfuncs import upload_images, get_image_ids, generate_script
from jetstreamcli.files import read_file

regex = r"([a-zA-Z]+) (\d+)"

def createProject(projects_dir, name):
   project_dir = projects_dir / name

   if os.path.exists(project_dir):
      return {"ok": False, "msg": Fore.YELLOW + "⚠️ Project with this name already exists."}
   
   os.makedirs(project_dir)

   return {"ok": True, "path": project_dir}

def find(name, path):
   for root, dirs, files in os.walk(path):
      if name in files:
         return os.path.join(root, name)
      
def remove_special_chars(text):
    return re.sub(r'[^\w\s]@!', '', text)  

@click.command()
@click.option("-n", "--name", prompt="Name your project", help="Name for the project", type=str)
@click.option("-i", "--input", prompt="Provide path to video (You can drag it here!)", help="Video to create project", type=str)
@click.option("-f", "--fps", default=0, help="FPS for the video", type=int)
@click.option("-b", "--big", default=False, help="Big project (Will take longer but prevents ratelimit)", type=bool)
@click.pass_context
def create(ctx: click.Context, name: str, input: str, fps: int, big: bool) -> None: 
   """create a Jetstream project"""
   
   config = ctx.obj["config"]
   
   if config["robloxKey"] == None or config["uploader"] == None:
      click.echo(Fore.YELLOW + "⚠️ You must set an API key and uploader before creating projcets.")
      return
   
   project = createProject(ctx.obj["projects_dir"], remove_special_chars(name))

   if not project["ok"]:
      click.echo(project["msg"])
      return
   
   click.echo("")
   click.echo(Fore.RED + "🚀 Jetstream Video Transforming (⏰ Fast)")
   click.echo(Fore.RESET + "")
   paths = transform_video(input, project["path"], fps)

   if paths == None:
      return
   click.echo(Fore.GREEN + "✅ Successfully transformed video to frames.")

   rblx_ids = upload_images(name, paths, big, project["path"])

   if rblx_ids == None:
      return

   image_ids = get_image_ids(rblx_ids, project["path"], name)

   if image_ids == None:
      return

   generate_script(name, image_ids, project["path"])

   click.echo("")
   click.echo(Fore.RED + "🚀 Jetstream project created successfuly! Access information using " + colored("jetstream projects", "black", "on_red"))
   click.echo("")

@click.command()
@click.pass_context
def builds(ctx: click.Context):
   """access your unfinished Jetstream builds"""

   projects = ctx.obj["projects_dir"]

   choices = []

   files = []

   index = 0

   project = 1

   for p in os.walk(projects):
      file = find("build.json", p[0])
      if file != None and index != 0:
         files.insert(index, file)

         with open(file, "r") as f:
            jdic = json.load(f)

         project_name = file.split("projects/")
         if not jdic["completed"]:
            choices.insert(project, str(project) + "." + Fore.YELLOW + " ⚠️ Incomplete - " + project_name[1] + " | Current Step: " + jdic["step"])
         project = project + 1

      index = index + 1   

   if len(choices) <= 0:
       click.echo("")
       click.echo(Fore.YELLOW + "⚠ You don't have any active builds.")
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

   match data["step"]:
      case "upload_images":
         paths = eval(data["paths"])
         id_list = upload_images(data["project_name"], paths, data["big_proj"], Path(project_dir), data["last_file"] + 1, data["rblx_ids"])

         if id_list == None:
            return
         
         image_ids = get_image_ids(id_list, Path(project_dir), data["project_name"])

         if image_ids == None:
            return
         
         generate_script(data["project_name"], image_ids, Path(project_dir))  
      case "image_ids":
            image_ids = get_image_ids(data["rblx_ids"], Path(project_dir), data["project_name"])

            if image_ids == None:
               return
            
            generate_script(data["project_name"], image_ids, Path(project_dir))
      case "script":
            generate_script(data["project_name"], data["img_ids"], Path(project_dir))