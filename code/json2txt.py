# -*- coding: utf-8 -*-
"""
Created on Jul 20 15:39:23 2022

Script to convert meshview compatible JSON files to TXT file using the same colour definitions.
Text files are saved in the same folder as the original JSON files using the same file names.

This script was written for a specific set of files, but works for all meshview compatible JSON files 
as long as the folder the JSON files are stored in is correctly defined. Default is the data folder, 
if you want to search in a different folder, please define it as in the example below.

USAGE:
Navigate to the directory where the file is located, and then type python json2txt.py -f /path/to/file
If no path is given, it will find .txt files in any of the subfolder of the data folder and convert those.

@author: mvanswieten
"""
import argparse
import glob
import os
import json
from pathlib import Path

def convert_json_to_txt(fnames):

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
            print("Extracting and saving coordinates for: " + f["name"])

            new_fname = (f["name"].strip() if len(json_file) > 1 else exp_name) + ".txt"
            out_file = os.path.join(os.path.dirname(fname), new_fname)

            xs = coordinate_list[0::3]
            ys = coordinate_list[1::3]
            zs = coordinate_list[2::3]
            with open(out_file, 'w') as fi:
                fi.write(f"RGB {f['r']} {f['g']} {f['b']}")
                fi.write('\n')
                for l in range(len(xs)):
                    fi.write(str(xs[l]))
                    fi.write('\t')
                    fi.write(str(ys[l]))
                    fi.write('\t')
                    fi.write(str(zs[l]))
                    fi.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text files to text.")
    default_folder = os.path.abspath(os.path.join(os.getcwd(), "..", "data"))  # Set default folder to 'data' folder located one level up
    parser.add_argument("-f", "--folder", default=default_folder, help="Folder path containing the JSON files. Defaults to the data folder.")
    args = parser.parse_args()

    folder_path = args.folder
    fnames = [str(fname) for fname in sorted(Path(folder_path).rglob('*.json'))]

    convert_json_to_txt(fnames)
