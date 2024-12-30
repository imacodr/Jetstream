import time
import datetime
import click
import requests
import xmltodict
import json

from rblxopencloud import User, AssetType
from colorama import Fore, Back, Style
from termcolor import colored

from config import load_config

def get_key():
    config = load_config()

    if config["robloxKey"] == None:
            return {"ok": False, "msg": Fore.YELLOW + "⚠️ You don't have a key! Add a key using " + colored("jetstream roblox set", "black", "on_yellow")}
    
    return {"ok": True, "key": config["robloxKey"]}

def get_uploader():
     config = load_config()

     if config["uploader"] == None:
           return {"ok": False, "msg": Fore.YELLOW + "⚠️ You don't have an uploader! Set your uploader using " + colored("jetstream roblox login", "black", "on_yellow")}
     
     return {"ok": True, "uploader": config["uploader"]}

def keyTest():
    try:
        keyc = get_key()

        if not keyc["ok"]:
             return keyc
        
        user = User(501780776, keyc["key"])

        info = user.fetch_info()

        return {"ok": True, "id": info.id, "username": info.username}
    except:
        return {"ok": False, "msg": Fore.RED + "❌ An error occured. Key may be invalid or no permissions have been given."}
    
def upload_images(projectName, paths, bigProject, project_dir, file_ticker = 1, rb_ids = []):
     try:
          click.echo("")
          click.echo(Fore.RED + "🚀 Jetstream Roblox Uploading (⏰ May take a while depending on video length)")
          click.echo("")
          keyc = get_key()
          uplc = get_uploader()

          if not keyc["ok"]:
               return keyc
          
          if not uplc["ok"]:
               return uplc
          
          user = User(uplc["uploader"], keyc["key"])

          rblx_ids = rb_ids

          for i in range(file_ticker, len(paths)):
               with open(paths[i], "rb") as file:
                         time.sleep(15 if bigProject else 6) # This is so it doesn't rate limit
                         operation = user.upload_asset(file, AssetType.Decal, projectName + "_" + "frame" + str(file_ticker), "Uploaded using 🚀 Jetstream")

               asset = operation.wait()

               rblx_ids.insert((file_ticker - 1), asset.id)
               click.echo(Fore.GREEN + "Frame " + str(file_ticker) + " uploaded.")
               click.echo(Fore.BLUE + "Link: " + "https://create.roblox.com/store/asset/" + asset.id)
               click.echo(Fore.RESET + "...")
               with open(project_dir / "build.json", "w") as file:
                    json.dump({"project_name": str(projectName), "big_proj": bigProject, "step": "upload_images", "rblx_ids": rblx_ids, "paths": str(paths), "last_file": file_ticker, "completed": False}, file, indent = 4)         
               file_ticker = file_ticker + 1  
               

          with open(project_dir / "decal_ids.json", "w") as file:
               json.dump(rblx_ids, file, indent = 4)

          with open(project_dir / "build.json", "w") as file:
                    json.dump({"project_name": str(projectName), "big_proj": bigProject, "step": "image_ids", "rblx_ids": rblx_ids, "paths": str(paths), "last_file": file_ticker, "completed": False}, file, indent = 4)
          
          click.echo(Fore.GREEN + "✅ Successfully uploaded all assets to Roblox.")
          return rblx_ids
     except Exception as e:
          click.echo("")
          click.echo(Fore.RED + "❌ An error occured: " + str(e))
          click.echo("")
          with open(project_dir / "build.json", "w") as file:
               json.dump({"project_name": str(projectName), "big_proj": bigProject, "step": "upload_images", "rblx_ids": rblx_ids, "paths": str(paths), "last_file": file_ticker, "completed": False}, file, indent = 4)         
          return None

def get_image_ids(id_list, project_dir, project_name):
     click.echo("")
     click.echo(Fore.RED + "🚀 Jetstream Decal ID -> Image ID Conversion (⏰ Somewhat fast)")
     click.echo("")
     
     base_url = "https://assetdelivery.roblox.com/v1/asset?id="

     new_list = []

     id_ticker = 0

     try:
          for id in id_list:
               response = requests.get(base_url + id)
               if response.status_code == 200:
                    dict_data = xmltodict.parse(response.content)

                    image_id_url = dict_data["roblox"]["Item"]["Properties"]["Content"]["url"]
                    image_id_split = image_id_url.split("=")
                    image_id = image_id_split[1]

                    new_list.insert(id_ticker, image_id)
                    click.echo(Fore.GREEN + "Converted Frame " + str(id_ticker + 1) + " to Image ID")
                    click.echo(Fore.RESET + "...")
                    id_ticker = id_ticker + 1
               else:
                    click.echo(Fore.RED + "❌ An error occcurred transforming sDecal IDs to Image IDs: " + Fore.RESET + str(e))

          with open(project_dir / "build.json", "w") as file:
               json.dump({"project_name": project_name, "step": "script", "img_ids": new_list, "completed": False}, file, indent = 4)

          with open(project_dir / "image_ids.json", "w") as file:
               json.dump(new_list, file, indent = 4)

          click.echo(Fore.GREEN + "✅ Successfully converted all Decals.")

          return new_list
     except requests.exceptions.RequestException as e:
          click.echo(Fore.RED + "❌ An error occcurred transforming Decal IDs to Image IDs: " + Fore.RESET + str(e))
          with open(project_dir / "build.json", "w") as file:
               json.dump({"project_name": project_name, "img_ids": new_list, "step": "image_ids", "completed": False}, file, indent = 4)
          return None


def generate_script(projectName, image_ids, project_dir):
     click.echo("")
     click.echo(Fore.RED + "🚀 Jetstream Script Generation (⏰ Very Fast)")
     click.echo("")
     into_str = f"--[[\n🚀 Jetstream Video\n\nProject: {projectName}\nGenerated on {str(datetime.datetime.now())}\n\nPlay this video using 🛩️ Flightplan\n]]--\n\n"
     script_str = "return {"

     image_ticker = 0

     length = len(image_ids)

     for img in image_ids:
          script_str = script_str + f"[{image_ticker}] = 'rbxassetid://{img}'"
          if not (image_ticker + 1) == length:
               script_str = script_str + ","
          image_ticker = image_ticker + 1

     script_str = script_str + "}"

     script_str = into_str + script_str

     with open(project_dir / "build.json", "w") as file:
          json.dump({"step": "done", "completed": False}, file, indent = 4)

     with open(project_dir / (projectName + ".luau"), "w") as file:
          file.write(script_str)
          click.echo("")
          click.echo(Fore.BLUE + "Flightplan Script created at " + file.name)
          click.echo(Fore.BLUE + "Or copy below: ")
          click.echo(Fore.RESET + "")

     click.echo(script_str)

     click.echo(Fore.GREEN + "✅ Successfully created script.")
     return script_str
     
          
        
             