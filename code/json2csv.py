# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 16:39:23 2022

Script to convert x,y,z coordinates from a JSON file generated for the use of Meshview 
to a CSV file. Output file has three columns, x_coordinate, y_coordinate, and z_coordinate

The script will look for all JSON file in the subfolders of the current 
working directory. If you only want to extract files from a specific folder, 
please define a path to file. The output files are save in the same directory as
 the original files

USAGE:
Navigate to the directory where the file is located, and then type python json2csv.py -f /path/to/file
If no folder_name is given, it will find .txt files in any of the subfolder of 
the current working directory and convert those.

@author: mvanswieten
"""

import os
import json
import pandas as pd
from pathlib import Path
import argparse

def convert_json_to_csv(fnames):
    file_list = []
    for fname in fnames:
        with open(fname, 'r') as f:
            file_list.append(json.load(f))

    for i, fname in enumerate(fnames):
        exp_name = os.path.splitext(os.path.basename(fname))[0]
        print(f"Loading data for experiment: {exp_name}")
        json_file = file_list[i]

        for f in json_file:
            coordinate_list = f["triplets"]
            print("Extracting coordinates for: " + f["name"])

            d = {
                "x_coordinate": coordinate_list[0::3],
                "y_coordinate": coordinate_list[1::3],
                "z_coordinate": coordinate_list[2::3]
            }

            data = pd.DataFrame(d)

            new_fname = (f["name"].strip() if len(json_file) > 1 else exp_name) + ".csv"
            out_file = os.path.join(os.path.dirname(fname), new_fname)

            print(f"Saving coordinate file: {out_file}")
            data.to_csv(out_file, index=False, header=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text files to CSV.")
    default_folder = os.path.abspath(os.path.join(os.getcwd(), "..", "data"))  # Set default folder to 'data' folder located one level up
    parser.add_argument("-f", "--folder", default=default_folder, help="Folder path containing the JSON files. Defaults to the data folder.")
    args = parser.parse_args()

    folder_path = args.folder
    fnames = [str(fname) for fname in sorted(Path(folder_path).rglob('*.json'))]

    convert_json_to_csv(fnames)



