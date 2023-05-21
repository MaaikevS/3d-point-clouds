"""
Created on Mar 15 13:52:25 2022

File to convert coordinates from a tab separated txt file to a JSON file compatible with Meshview
If RBG colour is defined in the txt file, this colour is used for the JSON file, otherwise the colour is set to black

example txt file input:
RGB 0 1 0
23.5 356.2 231
79,2 124   211

USAGE:
Navigate to the directory where the file is located, and then type python txt2json.py -f /path/to/file
If no path is given, it will find .txt files in any of the subfolder of the data folder and convert those.

@author: mvanswieten
"""
import argparse
import glob
import json
import os
from pathlib import Path

def convert_txt_to_json(fname):
    triplets = []
    r, g, b = 0, 0, 0
    count = 0

    exp_name = os.path.split(fname)[-1].split(".txt")[0]
    print(f"Loading data for experiment: {str(exp_name)}")
    
    with open(fname, "r") as f:
        for line in f:
            if line.strip() != "":
                current_line = line.split(",")

                if count == 0 and "RGB" in line:
                    current_line = line.split()
                    r, g, b = map(float, current_line[1:4])
                    if any(value <= 1 for value in (r, g, b)):
                        r, g, b = [value * 255 if value <= 1 else value for value in (r, g, b)]
                else:
                    coordinates = current_line[0].split("\t")
                    triplets.extend(map(float, coordinates[:3]))

                count += 1

    exp_name = os.path.splitext(os.path.basename(fname))[0]
    exp = {
        "idx": 0,
        "count": len(triplets) // 3,
        "r": int(r),
        "g": int(g),
        "b": int(b),
        "name": "_".join(exp_name.split("_")[1:]),
        "triplets": triplets
    }

    json_output = os.path.join(os.path.dirname(fname), f"{exp_name}.json")
    print(f"Saving coordinate file: {json_output}")
    with open(json_output, 'w', encoding='utf-8') as json_file:
        json.dump([exp], json_file, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text files to JSON.")
    default_folder = os.path.abspath(os.path.join(os.getcwd(), "..", "data"))  # Set default folder to 'data' folder located one level up
    parser.add_argument("-f", "--folder", type=str, default=default_folder, help="Folder path containing the text files. Defaults to the data folder.")
    args = parser.parse_args()

    folder_path = args.folder
    fnames = [fname.__str__() for fname in sorted(Path(folder_path).rglob('*.txt'))]

    for fname in fnames:
        convert_txt_to_json(fname)
