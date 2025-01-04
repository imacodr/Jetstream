import json
import os

from jsonmerge import merge

def read_file(path):
    if os.path.exists(path):
        with open(path, "r") as file:
            data = json.load(file)
        
        return data
    else:
         return None

def write_file(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent = 4)

def merge_file(path, new_data):
     current_data = read_file(path)
     
     merged_data = merge(current_data, new_data)
     
     write_file(path, merged_data)