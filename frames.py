import os
import click
import json
from colorama import Fore, Back, Style
from termcolor import colored
from pathlib import Path
import ffmpeg

def transform_video(input, project, fps):
        try:
            extract_all_frames = False

            if fps == 0:
                extract_all_frames = True

            if not extract_all_frames:
                ffmpeg.input(input).output(str(project) + "/frame%d.png", vf='fps=' + str(fps)).run()
            else:
                ffmpeg.input(input).output(str(project) + "/frame%d.png").run()

            frame_files = os.listdir(project)
            frame_paths = []
            for i in range(0, len(frame_files)):
                 frame_paths.insert(i, Path(str(project) + "/frame" + str(i) + ".png"))

            return frame_paths
        except Exception as e:
             click.echo("")
             click.echo(Fore.RED + "❌ An error occured: " + str(e))
             click.echo("")
             with open(project / "build.json", "w") as file:
                  json.dump({"step": "transform_video", "completed": False}, file, indent = 4)          
             return None
    

