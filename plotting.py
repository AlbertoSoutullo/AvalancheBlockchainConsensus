import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

data = [
    [5, 0, 0, 0],
    [0, 5, 0, 0],
    [0, 0, 5, 0],
    [0, 0, 0, 5],
]

data2 = [
    [0, 0, 0, 4],
    [0, 0, 4, 0],
    [0, 4, 0, 0],
    [4, 0, 0, 0],
]

data3 = [
    [0, 3, 3, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 3, 3, 0],
]

data_letter_A = [
    ["A", "", "", ""],
    ["", "A", "", ""],
    ["", "", "A", ""],
    ["", "", "", "A"]
]

data_letter_B = [
    ["", "", "", "B"],
    ["", "", "B", ""],
    ["", "B", "", ""],
    ["B", "", "", ""]
]

data_letter_C = [
    ["", "C", "C", ""],
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "C", "C", ""]
]

letters = [data_letter_A,data_letter_B,data_letter_C]

datas = [data, data2, data3]

def set_cmap_transparent_value(cmap_name, cmaps):
    ncolors = 256
    color_array = plt.get_cmap(cmap_name)(range(ncolors))
    color_array[:, -1] = np.linspace(0.0, 1.0, ncolors)

    # create a colormap object
    map_object = LinearSegmentedColormap.from_list(name=cmap_name+'_alpha', colors=color_array)
    # register this new colormap with matplotlib
    plt.register_cmap(cmap=map_object)
    cmaps.append(cmap_name+'_alpha')


# color_array = plt.get_cmap()(range(ncolors))

if __name__ == '__main__':
    random.seed(1)
    cmaps_to_use = []
    # no reusar el mismo
    for i in range(3):
        choice = random.choice(plt.colormaps())
        set_cmap_transparent_value(choice, cmaps_to_use)

    f, ax = plt.subplots()
    for i in range(len(cmaps_to_use)):

        # show some example data
        h = sns.heatmap(datas[i], cmap=cmaps_to_use[i], annot=letters[i], ax=ax, vmin=0, vmax=5, fmt='', cbar=False)
        # plt.colorbar(mappable=h)

    plt.show()
