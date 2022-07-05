import os
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import glob
from PIL import Image

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


def set_cmap_transparent_value(cmap_name):
    ncolors = 256
    color_array = plt.get_cmap(cmap_name)(range(ncolors))
    quick_gradient = np.linspace(0.0, 0.75, 10)
    slow_gradient = np.linspace(0.75, 1, 246)
    gradient = np.append(quick_gradient, slow_gradient)
    # color_array[:, -1] = np.linspace(0.0, 1.0, ncolors)
    color_array[:, -1] = gradient

    # create a colormap object
    map_object = LinearSegmentedColormap.from_list(name=cmap_name+'_alpha', colors=color_array)
    # register this new colormap with matplotlib
    plt.register_cmap(cmap=map_object)
    return cmap_name + '_alpha'


def create_custom_cmaps():
    # no reusar el mismo
    cmaps = []
    for i in range(3):
        choice = random.choice(plt.colormaps())
        cmap = set_cmap_transparent_value(choice)
        cmaps.append(cmap)

    return cmaps


def create_preference_info_matrix(data, preference):
    letters = [["" if number == -1 else preference for number in row] for row in data]

    return letters

# color_array = plt.get_cmap()(range(ncolors))


def make_gif(frame_folder):
    # frames = [Image.open(image) for image in sorted(glob.glob(f"{frame_folder}/*.png"))]
    frames = [image for image in glob.glob(f"{frame_folder}/*.png")]
    frames = sorted(frames, key=lambda i: int(os.path.splitext(os.path.basename(i))[0]))

    frames = [Image.open(image, formats=['PNG']) for image in frames]
    frame_one = frames[0]
    frame_one.save(frame_folder+"/result.gif", format="GIF", append_images=frames,
               save_all=True, duration=500, loop=0)


if __name__ == '__main__':
    random.seed(1)
    cmaps_to_use = create_custom_cmaps()


    f, ax = plt.subplots()
    for i in range(len(cmaps_to_use)):

        # show some example data
        h = sns.heatmap(datas[i], cmap=cmaps_to_use[i], annot=letters[i], ax=ax, vmin=0, vmax=5, fmt='', cbar=False)
        # plt.colorbar(mappable=h)

    plt.show()
