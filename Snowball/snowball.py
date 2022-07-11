# Python Imports
import random
import pandas as pd
import numpy as np
from typing import List

# Project Imports
from node import Node
from Snowball.snowball_configuration import SnowballConfiguration


class SnowballAlgorithm:
    def __init__(self, config: SnowballConfiguration, preferences: List[str]):
        self._snowball_configuration = config
        self._preferences = preferences
        self._nodes = None
        self._register = pd.DataFrame(columns=["Iteration", "Preference", "Num_Votes"])
        self._heatmap_register = []

    def initialize_nodes(self) -> None:
        self._nodes = [Node(random.choice(self.preferences), i) for i in range(self.n * self.n)]

    def simulate(self) -> None:
        nodes_left = [node for node in self._nodes if not node.is_decided()]
        i = 0
        while len(list(nodes_left)) != 0:  # add max_iterations
            # Hardcoded 20 to see a slower gif, otherwise would update all nodes at once
            subsample_size = 20 if len(list(nodes_left)) >= 20 else len(list(nodes_left))
            random_subsample = random.sample(nodes_left, subsample_size)
            for node in random_subsample:
                node.update(self._nodes, self.k, self.alpha, self.beta)

            self._create_register_for_heatmap()

            nodes_left = [node for node in nodes_left if not node.is_decided()]
            i += 1

        print(f"Iteration {i}")

    def retrieve_register(self) -> pd.DataFrame:
        return self._register

    def retrieve_heatmap_register(self) -> List[List[np.array]]:
        return self._heatmap_register

    def _create_register_for_heatmap(self) -> None:
        sub_matrices = []
        for preference in self.preferences:
            node_consecutive_successes = [node.consecutive_successes if node.preference == preference
                                          else -1
                                          for node in self._nodes]
            node_consecutive_successes = np.array(node_consecutive_successes)
            matrix_form_data = np.reshape(node_consecutive_successes, (self.n, self.n))
            sub_matrices.append(matrix_form_data)
        self._heatmap_register.append(sub_matrices)

    @property
    def n(self) -> int:
        return self._snowball_configuration.n

    @property
    def k(self) -> int:
        return self._snowball_configuration.k

    @property
    def alpha(self) -> int:
        return self._snowball_configuration.alpha

    @property
    def beta(self) -> int:
        return self._snowball_configuration.beta

    @property
    def preferences(self) -> List[str]:
        return self._preferences
