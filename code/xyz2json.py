"""
Created on Jul 20 13:52:25 2022

Script to convert coordinates from a .xyz file to a JSON file compatible with Meshview. Please 
ensure that the xyz files have already been converted to the WHS coordinate space prior to using 
this script.

This script was written for a specific set of files, but works for all .xyz files as long 
as the folder the .xyz files are stored in is correctly defined. It will look for any .xyz files 
in the data folder and its subfolders if no folder is defined.

The colour used for the JSON file is dependent on the type of injection tracer. BDA/PHA/WGA is 
black, Fe/FE is green, Fr is red, FG is yellow, and FB is blue. If the files do not follow the 
naming convention of the files the script was written for, then the colour of the points is set 
to black by default.

USAGE:
Navigate to the directory where the file is located, and then type python xyz2json.py -f /path/to/file
If no path is given, it will find .txt files in any of the subfolder of the data folder and convert those.

@author: mvanswieten
"""

import argparse
import json
import glob
import os
from pathlib import Path


def convert_xyz_to_json(fname):
    with open(fname, "r") as xyz_file:
        lines = xyz_file.readlines()

    output_folder = os.path.dirname(fname)
    filename = os.path.basename(fname)
    name = os.path.splitext(filename)[0]

    print(f"Loading data for experiment: {str(name)}")

    r, g, b = 0, 0, 0
    triplets = []
    for line in lines:
        if line.startswith("#") or line.strip() == "":
            continue

        current_line = line.split(",")
        coordinates = current_line[0].split()
        triplets.extend(map(float, coordinates[:3]))

    if "Fr" in name:
        r, g, b = 1, 0, 0
    elif "FB" in name:
        r, g, b = 0, 0, 1
    elif "Fe" in name:
        r, g, b = 0, 0.5, 0
    elif "FG" in name:
        r, g, b = 1, 1, 0

    json_data = [{
        "idx": 0,
        "count": len(triplets) // 3,
        "r": int(r * 255),
        "g": int(g * 255),
        "b": int(b * 255),
        "name": name,
        "triplets": triplets
    }]

    json_output = os.path.join(output_folder, f"{name}.json")
    print(f"Saving coordinate file: {json_output}")
    with open(json_output, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text files to JSON.")
    default_folder = os.path.abspath(os.path.join(os.getcwd(), "..", "data"))  # Set default folder to 'data' folder located one level up
    parser.add_argument("-f", "--folder", type=str, default=default_folder, help="Folder path containing the XYS files. Defaults to the data folder.")
    args = parser.parse_args()

    folder_path = args.folder
    fnames = [fname.__str__() for fname in sorted(Path(folder_path).rglob('*.xyz'))]

    for fname in fnames:
        convert_xyz_to_json(fname)
