from jsonmerge import merge
import json

def read_file(path):
    with open(path, "r") as file:
         data = json.load(file)
    
    return data

def write_file(path, data):
      with open(path, "w") as file:
          json.dump(data, file, indent = 4)

def merge_file(path, new_data):
     current_data = read_file(path)
     merged_data = merge(current_data, new_data)
     
     write_file(path, merged_data)