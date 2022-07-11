# Python Imports
import os
import glob
import random
from typing import List

import numpy as np
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def set_cmap_transparent_value(cmap_name: str) -> str:
    # Create custom cmap with alpha values to zero at the beginning
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


def create_custom_cmaps(num_options: int) -> List[str]:
    # TODO: check not ot reuse same color map twice
    cmaps = []
    for i in range(num_options):
        choice = random.choice(plt.colormaps())
        cmap = set_cmap_transparent_value(choice)
        cmaps.append(cmap)

    return cmaps


def create_preference_info_matrix(data, preference) -> List[List[str]]:
    letters = [["" if number == -1 else preference for number in row] for row in data]

    return letters


def make_gif(frame_folder: str) -> None:
    frames = [image for image in glob.glob(f"{frame_folder}/*.png")]
    frames = sorted(frames, key=lambda i: int(os.path.splitext(os.path.basename(i))[0]))

    frames = [Image.open(image, formats=['PNG']) for image in frames]
    frame_one = frames[0]
    frame_one.save(frame_folder+"/result.gif", format="GIF", append_images=frames,
                   save_all=True, duration=200, loop=0)


def prepare_figures(heatmap_data: List[List[np.array]], PREFERENCES: List[str],
                    cmaps: List[str], path_to_save: str):

    for iteration in range(len(heatmap_data)):
        f, ax = plt.subplots()
        for preference in range(len(PREFERENCES)):

            heatmap_values = heatmap_data[iteration][preference]
            annotations = create_preference_info_matrix(heatmap_values, PREFERENCES[preference])
            sns.heatmap(heatmap_values, cmap=cmaps[preference], annot=annotations, ax=ax, vmin=0, vmax=20, fmt='', cbar=False)

            plt.savefig(path_to_save + f"{iteration}.png")

        # plt.show()
