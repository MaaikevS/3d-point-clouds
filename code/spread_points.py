# -*- coding: utf-8 -*-
"""
Created on Jul 20 15:39:23 2022

Script applies a Gaussian function with a mean of 0 and standard deviation of 2.5 to the point data in a 
json file. The purpose of this transformation is to depict data points within the tickness of the slice. 
This is a closer representation of the biological existence of cells.
The colour definitions of the newly generated files is the same as the original files.
Files are saved in the same folder as the original JSON files using the same file names, with the suffix _spread

Works for all meshview compatible JSON files that are located in any of the subfolder of the current 
working directory (please ensure that the files are ) If you the files are located in a specific folder 
or in a folder that is not part of the current working directory, fill in the path to the folder in folder_name

USAGE:
Navigate to the directory where the file is located, and then type python spread_points.py -f /path/to/file -sd 2.5
The default standard deviation (sd is set to 2.5, but you can change it by using -sd 1.0). If no path is given, 
it will find .txt files in any of the subfolder of the current working directory and convert those.

@author: mvanswieten
"""
import json
import numpy as np
import copy
import random
from pathlib import Path
import argparse
import os

def apply_spread(fnames, sd):
    
    random.seed(12345)
    
    for fname in fnames:
        with open(fname) as f:
            data = json.load(f)
    
        header = []
        for d in data:
            t = np.array(d['triplets'])
            
            # reshape the array into a matrix
            x = t.reshape(-1, 3)
    
            # Set the range for similarity (within +/- 1)
            similarity_range = 1.0
    
            # Get unique z values from the matrix
            unique_z_values = np.unique(x[:, 2])
    
            # Find three rows with similar z coordinates
            similar_rows = None
            row_numbers = None
            for z_value in unique_z_values:
                rows_with_z = x[np.abs(x[:, 2] - z_value) <= similarity_range]
                if len(rows_with_z) >= 3:
                    similar_rows = rows_with_z[:3]
                    row_numbers = np.unique(np.where(np.isin(x, similar_rows))[0])
                    break
            
            # Pick the first three elements if no similar rows were found
            row_numbers = row_numbers if len(row_numbers) == 3 else [0, 2, 1]
    
            i1, i2, i3 = row_numbers[0], row_numbers[2], row_numbers[1]
            
            # take the cross product to figure out the vector perpendicular to the cutting plane
            plane = np.cross(x[i1] - x[i2], x[i1] - x[i3])
            plane = plane / np.linalg.norm(plane)
    
            k = copy.deepcopy(d)
            k['triplets'] = []
            # spread the points perpendicular to the cutting plane
            for dd in x:
                vv = dd + plane * random.gauss(0, sd)
                k['triplets'].extend(vv)
            header.append(k)
    
        # Saving output file
        out_file = f"{fname.split('.')[0]}_spread.json"
        print(f"Saving file {out_file}")
        with open(out_file, "w") as of:
            json.dump(header, of)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSON files with customizable standard deviation (sd).")
    default_folder = os.path.abspath(os.path.join(os.getcwd(), "..", "data"))  # Set default folder to 'data' folder located one level up
    parser.add_argument("-f", "--folder", type=str, default=default_folder, help="Folder name where the JSON files are located. Defaults to the data folder.")
    parser.add_argument("-sd", "--standard-deviation", type=float, default=2.5, help="Standard deviation for spreading points.")
    args = parser.parse_args()

    fnames = [str(fname) for fname in sorted(Path(args.folder).rglob('*.json'))]
    apply_spread(fnames, sd=args.standard_deviation)