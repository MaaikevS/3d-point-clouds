# Import packages
import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

## Load the clouds of interest and extract the coordinates
def load_coordinates(exp_name, data_folder):
    """
    Load coordinates from a JSON file.
    
    This function searches for a JSON file in the specified folder (`data_folder`)
    that matches the experiment name (`exp_name`). It reads the JSON file and extracts
    the triplet coordinates (x, y, z), and returns them as a pandas DataFrame.

    Args:
        exp_name (str): The name of the experiment.
        data_folder (str or Path): The folder where the data is located.

    Returns:
        pd.DataFrame: A DataFrame containing x, y, and z coordinates.
    """
    fname = sorted(Path(data_folder).rglob(f"{exp_name}.json"))[0]
    with open(fname, "r") as f:
        points = json.load(f)
    
    if len(points) > 1:
        coordinate_list = points[2]["triplets"]
    else:
        coordinate_list = points[0]["triplets"]
    
    d = {
        "x_coordinate": coordinate_list[0::3],
        "y_coordinate": coordinate_list[1::3],
        "z_coordinate": coordinate_list[2::3]
    }
    return pd.DataFrame(d)

# Load groupdata and add metadata
def extract_groupdata(case_names, data_folder):
    """
    Process a list of experiments and return a DataFrame with coordinates and metadata.
    
    This function processes the experiment names in `case_names` by loading their
    coordinates, adding metadata like labels and case names, and concatenating the
    results into a single DataFrame.

    Args:
        case_names (list): List of experiment names or lists of names.
        data_folder (str or Path): Folder where the data is stored.

    Returns:
        pd.DataFrame: A DataFrame containing coordinates, labels, and case names.
    """

    if type(case_names[0]) == list:
        count = 1
        for case_num in range(len(case_names)):
            
            for exp_name in case_names[case_num]:
                cloud = load_coordinates(exp_name, data_folder)
                cloud["label"] = case_num + 1  # Label starts from 1
                cloud["case_name"] = exp_name

                if count == 1:
                    df_cloud = pd.DataFrame(cloud)
                else:
                    df_cloud = pd.concat([df_cloud, pd.DataFrame(cloud)], ignore_index=True)

                count +=1
    else:
        count = 1
        for exp_name in case_names:
            cloud = load_coordinates(exp_name, data_folder)
            cloud["label"] = count  # Label starts from 1
            cloud["case_name"] = exp_name

            if count == 1:
                df_cloud = pd.DataFrame(cloud)
            else:
                df_cloud = pd.concat([df_cloud, pd.DataFrame(cloud)], ignore_index=True)

            count +=1
    
    return df_cloud

def compare_clouds(case_overview, panel, data_folder):
    """
    Compare clouds of 3D coordinates and compute the minimum Euclidean distances between points.
    
    This function takes the `case_overview` DataFrame and iterates over comparisons of
    cases. It extracts the relevant cloud data for each case, calculates the Euclidean
    distance between points in two 3D clouds, and returns a DataFrame of the sorted
    distances for each comparison.

    Args:
        case_overview (pd.DataFrame): Overview of case comparisons.
        panel (str): Panel identifier, e.g., 'T'.
        data_folder (str or Path): Folder where the cloud data is stored.

    Returns:
        pd.DataFrame: DataFrame containing sorted distances and corresponding comparison information.
    """

    count = 0
    if panel == 'T':
        cases = ['ABC combined vs FGH combined', 'ABC combined vs KLM combined']
    for comp in case_overview.comparison.unique():

        subset = case_overview[(case_overview.panel == panel) & (case_overview.comparison == comp)].reset_index(drop=True)
        for comparison in range(len(subset)):
            case_names = [subset.case_1[comparison], subset.case_2[comparison]]
            if panel == 'T':
                case_description = cases[comp-1]
            else:
                case_description = f"{case_names[0]} vs {case_names[1]}"

            df = extract_groupdata(case_names, data_folder)

            cloud1 = df[df["label"] == 1].drop(columns=["label", "case_name"]).to_numpy()
            cloud2 = df[df["label"] == 2].drop(columns=["label", "case_name"]).to_numpy()

            result = []
            for i in range(len(cloud1)):
                result.append(np.min(calculate_euclidean(cloud1[i], cloud2)))
            dist = pd.DataFrame({'dist': sorted(result)})
            dist["comparison"] = comp
            dist["cases"] = case_description
            
            if count  == 0:
                dist_full = dist
            else:
                dist_full = pd.concat([dist_full, dist], ignore_index=True)

            count =+ 1


    return dist_full

# Calculate Euclidean distance
def calculate_euclidean(cloudA, cloudB):
    """
    Calculate the Euclidean distance between points in two 3D clouds.
    
    This function computes the pairwise Euclidean distance between points
    in two 3D arrays of coordinates.

    Args:
        cloudA (np.ndarray): First array of 3D points.
        cloudB (np.ndarray): Second array of 3D points.

    Returns:
        np.ndarray: Array of Euclidean distances between points in cloud A and cloud B.
    """
    diff = cloudA.reshape(-1, 1, 3) - cloudB
    return np.linalg.norm(diff, ord=2, axis=-1)

# Extract the peak of the density curve - this corresponds with the "mode" of the distribution
def calculate_stats(data):
    """
    Calculate peak, mean, and median values for distance distributions.
    
    This function calculates the mode (peak of the KDE), mean, and median
    values for the Euclidean distance distributions in `data` and returns
    them as a summary DataFrame.

    Args:
        data (pd.DataFrame): DataFrame containing distance data.

    Returns:
        pd.DataFrame: Summary DataFrame with peak, mean, and median for each comparison.
    """    
    peak_values = []
    mean_values = []
    median_values = []
    cases = []

    for comparison in data.comparison.unique():
        d = data[data.comparison == comparison].reset_index(drop=True)
        case_name = data['cases'][data.comparison == comparison].reset_index(drop=True)[0]
        my_kde = sns.displot(data=d, x='dist', hue='comparison', kind='kde')
        plt.close()

        axes = my_kde.axes.flatten()

        for i, ax in enumerate(axes):
            for line in ax.lines:
                max_x = line.get_xdata()[np.argmax(line.get_ydata())]
                peak_values.append(max_x)

        mean_values.append(data["dist"][data.comparison == i+1].mean())
        median_values.append(data["dist"][data.comparison == i+1].median())
        cases.append(case_name)
        
    summary = {'comparison': cases,
                'peak': peak_values,
                'mean': mean_values,
                'median' : median_values}

    sum_df = pd.DataFrame.from_dict(summary)

    blankIndex=[''] * len(sum_df)
    sum_df.index=blankIndex
    print(sum_df)

    return sum_df

# Plot all the KDE in the same plot
def plot_groupdata(data, label, title="", filename=None):
    """
    Plot Kernel Density Estimate (KDE) for distance data with labels.
    
    This function generates a KDE plot for the Euclidean distance distributions
    in `data` grouped by `label`. The plot can optionally be saved to a file.

    Args:
        data (pd.DataFrame): Data containing the distances.
        label (str): Column name for grouping the data.
        title (str, optional): Title of the plot. Default is "".
        filename (str, optional): Filename to save the plot. If no file name is given, 
                                  the plot will not be saved

    Returns:
        None
    """
    # sns.set_style('whitegrid')

    fig = plt.figure(figsize=(5, 5))

    ax = fig.add_subplot(111)
    sns.kdeplot(data= data, x = "dist", hue=label, fill=True, 
                common_norm=False, palette=['grey', 'red'],
                alpha=.5, linewidth=0.1, cut=0, ax=ax)
    ax.set_title(title, fontsize = 10)
    ax.set_xlabel('Minimum Euclidean distance')
    ax.set_ylabel('Density')
    ax.set_xlim([0, 15])
    ax.set_ylim([0,1.3])

    label_format = '{:,.0f}'
    ax.xaxis.set_major_locator(mticker.MaxNLocator(3))
    ticks_loc = ax.get_xticks().tolist()
    ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    ax.set_xticklabels([label_format.format(x) for x in ticks_loc])


    if filename:
        plt.savefig(filename)

    plt.tight_layout()
    plt.show()

    return

