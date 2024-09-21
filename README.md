# 3D Point Clouds

Files in this repository were used for the manuscript "Spatially integrated cortico-subcortical tracing data for analyses of rodent brain topographical organization"

## How to use this repository
There are a few ways to use this repository:

**1. Download the zip file:** Click on the green "Code" and select "Download ZIP". You can now use the repository on your local device.

**2. Clone the repository:** To clone the repository click the green "Code" button. In the dropdown that appears you will have the option to clone over HTTPS, SSH, or by using the GitHub CLI.

**3. Fork the repository to your own GitHub account and clone it to your local PC/laptop:** Go to the top-right corner of the page and click "Fork". Go to your the forked repository on your own GitHub account and clone the repository as described above.

To be able to use the scripts, data should be downloaded from the [EBRAINS Knowledge Graph](https://search.kg.ebrains.eu/?category=Dataset), see the dataset options under "Data Availability" below. Place the downloaded files in the data folder of your (cloned) repository on your local device.

## Project Organization

------------

    ├── LICENSE
    ├── README.md          
    ├── data                <- place the EBRAINS dataset in this folder
    │   ├── dataset1
    │   ├── dataset2     
    │   ├── ...
    ├── code                 <- folder with python scripts and jupyter notebooks
    │   ├── img              <- image folder for images in jupyter notebooks
        |   ├── ...
        ├── calculate_distance.ipynb
        ├── change_color.ipynb
        ├── compare_extraction_method.ipynb
        ├── compare_genotype.ipynb
        ├── compare_regions
        ├── create_customcloud_transgenic
        ├── create_customcloud_WT
        ├── create_customcloud_rat
        ├── create_gradientmap_Nex-cKO
        ├── create_gradientmap_rat
        ├── create_gradientmap_transgenic
        ├── create_gradientmap_WT
        ├── helper.py
        ├── json2csv.py
        ├── json2txt.py
        ├── spead_points.py   
        ├── txt2json.py
        ├── xyz2json.py   
    ├── output              <- folder in which output files are stored
        ├── ...

--------

## Scripts

### Preprocessing
- ``change_color.ipynb:`` script for changing the color of points in Meshview compatible JSON files.
- ``json2csv.py:`` script for convert Meshview compatible JSON files to x,y,z coordinates in a csv file
- ``json2txt.py:`` script for convert Meshview compatible JSON files to x,y,z coordinates in a text file.
- ``spead_points.py:`` script for spreading point coordinates in Meshview compatible JSON files across a section thickness.
- ``txt2json.py:`` script for converting coordinates stored in text files to Meshview compatible JSON files.
- ``xyz2json.py:`` script for converting x,y,z point lists to Meshview compatible JSON files.

### Figures

The following scripts were used to produce the figures in the manuscript:

- **Figure 2:** script for quantifying the similarity between 2 point clouds based on Euclidean distance (``calculate_distance.ipynb``).
- **Figure 3:** script for the comparison of feature extraction methods (``compare_extraction_method.ipynb``).
- **Figure 4:** color coded visualization of injection sites in the wildtype mouse (``create_gradientmap_WT.ipynb``) and rat (``create_gradientmap_rat.ipynb``).
- **Figure 5:** script for comparing points representing projections to different subcortical regions in the same animal (``compare_regions.ipynb``).
- **Figure 6:** script for comparing mouse brain connectivity points in different mouse genotypes (``compare_genotype.ipynb``).

### Helper functions

- ``helper.py:`` script with processing and visualisation functions for the analysis of figure 2.
 
### Custom file creation
If you want to explore the datasets further, we made available three scripts that allow you to create custom Meshview compatible output files for up to 10 cases.

- ``create_customcloud_WT.ipynb:`` script for creating custom Meshview compatible JSON files for wildtype mice.
- ``create_customcloud_transgenic.ipynb:`` script for creating custom Meshview compatible JSON files for transgenic mice.
- ``create_customcloud_rat.ipynb:`` script for creating custom Meshview compatible JSON files for rat datasets. You can choose one or more of the four available rat datasets. This script allows you to combine and compare cases of different datasets.

## Data Availability

Datasets are available on [EBRAINS](https://search.kg.ebrains.eu/?category=Dataset)

- Wild-type mice: **DOI: [10.25493/GDYP-B1B](https://doi.org/10.25493/GDYP-B1B)**
- Transgenic mice: **DOI: [10.25493/HWJY-RDV](https://doi.org/10.25493/HWJY-RDV)**
- Nex-cKO: **DOI: [10.25493/11HT-S4B](https://doi.org/10.25493/11HT-S4B)**
- Rat cortex: **DOI: [10.25493/9TMN-64U](https://doi.org/10.25493/9TMN-64U)**
- Rat somatosensory cortex: **DOI: [10.25493/ZSZ9-3NN](https://doi.org/10.25493/ZSZ9-3NN)**
- Rat barrel cortex **DOI: [10.25493/W8MG-X2R](https://doi.org/10.25493/W8MG-X2R)**
- Rat sensorimotor cortex **DOI: [10.25493/TH1N-V8P](https://doi.org/10.25493/TH1N-V8P)**
