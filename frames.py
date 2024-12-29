import os
from colorama import Fore, Back, Style
from termcolor import colored
from pathlib import Path
import ffmpeg

from config import load_config

def transformVideo(input, project):
        extract_all_frames = False
        fps = 1
        os.makedirs("/tmp/frames", exist_ok=True)


        if not extract_all_frames:
            ffmpeg.input(str(input)).output("frame%d.png", vf='fps=' + str(fps)).run()
        else:
            ffmpeg.input(input).output("frame%d.png").run()

        # frame_files = sorted(os.listdir("./tmp/frames"))
        # frame_paths = [Path(os.path.join("./tmp/frames", frame_file)) for frame_file in frame_files]

        # return frame_paths
    

