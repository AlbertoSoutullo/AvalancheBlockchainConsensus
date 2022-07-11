# Parameters
# n: number of participants
# k (sample size): between 1 and n (number of people to ask)
# α (quorum size): between 1 and k (α or more people give same response, this is adopted as preference)
# β (decision threshold): >= 1 (repeats this until β times quorum in a row)

# Python Imports
import json
import random

# Project Imports
from Snowball.snowball import SnowballAlgorithm
from Snowball.snowball_configuration import SnowballConfiguration
from plotting import create_custom_cmaps, make_gif, prepare_figures

if __name__ == '__main__':
    random.seed(1)

    with open('parameters.json') as parameters_file:
        parameters = json.load(parameters_file)

    cmaps = create_custom_cmaps(len(parameters['PREFERENCES']))

    snowball_configuration = SnowballConfiguration(parameters['n'], parameters['k'], parameters['alpha'],
                                                   parameters['beta'])
    snowball_alg = SnowballAlgorithm(snowball_configuration, parameters['PREFERENCES'])

    snowball_alg.initialize_nodes()
    snowball_alg.simulate()
    hm_data = snowball_alg.retrieve_heatmap_register()

    prepare_figures(hm_data, parameters['PREFERENCES'], cmaps, parameters['output_path'])

    make_gif(frame_folder='images')
