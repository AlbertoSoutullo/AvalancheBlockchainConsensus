# The intuition above outlines the Snowball Algorithm, which is a building block of Avalanche consensus.

# Parameters
# n: number of participants
# k (sample size): between 1 and n (number of people to ask)
# α (quorum size): between 1 and k (α or more people give same response, this is adopted as preference)
# β (decision threshold): >= 1 (repeats this until β times quorum in a row)

# As the quorum size, α, increases, the safety threshold increases, and the liveness threshold decreases.
# This means the network can tolerate more byzantine (deliberately incorrect, malicious) nodes and remain safe,
# meaning all nodes will eventually agree whether something is accepted or rejected.
# The liveness threshold is the number of malicious participants that can be tolerated before the protocol is unable to
# make progress.


# Algorithm
# preference := pizza
# consecutiveSuccesses := 0
# while not decided:
#   ask k random people their preference
#   if >= α give the same response:
#     preference := response with >= α
#     if preference == old preference:
#       consecutiveSuccesses++
#     else:
#       consecutiveSuccesses = 1
#   else:
#     consecutiveSuccesses = 0
#   if consecutiveSuccesses > β:
#     decide(preference)
import random

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from dataclasses import dataclass
from collections import Counter

PREFERENCES = ["A", "B", "C"]


class Node:
    def __init__(self, vote, node_id):
        self._preference = vote
        self._id = node_id
        self._consecutive_successes = 0
        self._decided = False

    def __eq__(self, other):
        return self._id == other.id

    def update(self, all_nodes, k, alpha, beta):
        all_nodes_but_itself = [node for node in all_nodes if node != self]
        random_nodes = random.sample(all_nodes_but_itself, k)

        preference, nodes_agreed = self._check_for_nodes_preference(random_nodes, alpha)
        if nodes_agreed:
            self._update_preference_and_successes(preference)
        else:
            self._consecutive_successes = 0
        if self._consecutive_successes > beta:
            self._decided = True

    def _check_for_nodes_preference(self, random_nodes, alpha):
        random_votes = [node.preference for node in random_nodes]
        count_preferences = Counter(random_votes)
        ordered_preferences = count_preferences.most_common(1)

        if ordered_preferences[0][1] >= alpha:
            return ordered_preferences[0][0], True

        return None, False

    def _update_preference_and_successes(self, preference):
        if self._preference == preference:
            self._consecutive_successes += 1
        else:
            self._consecutive_successes = 1
            self._preference = preference

    def is_decided(self):
        return self._decided

    @property
    def id(self):
        return self._id

    @property
    def preference(self):
        return self._preference

    @property
    def consecutive_successes(self):
        return self._consecutive_successes


@dataclass
class SnowballConfiguration:
    n: int
    k: int
    alpha: int
    beta: int


class SnowballAlgorithm:
    def __init__(self, config):
        self._snowball_configuration = config
        self._nodes = None
        self._register = pd.DataFrame(columns=["Iteration", "Preference", "Num_Votes"])
        self._heatmap_register = []

    def initialize_nodes(self):
        self._nodes = [Node(random.choice(PREFERENCES), i) for i in range(self.n * self.n)]

    def simulate(self):
        nodes_left = [node for node in self._nodes if not node.is_decided()]
        i = 0
        while len(list(nodes_left)) != 0:  # add max_iter, refactor len
            for node in nodes_left:
                node.update(self._nodes, self.k, self.alpha, self.beta)

            # line plot
            votes = [node.preference for node in self._nodes]
            votes_count = Counter(votes)
            for key, value in votes_count.items():
                self._register.loc[len(self._register.index)] = [i, key, value]

            self._create_register_for_heatmap()

            nodes_left = [node for node in nodes_left if not node.is_decided()]
            i += 1

        print(f"Iteration {i}")

    def retrieve_register(self):
        return self._register

    def retrieve_heatmap_register(self):
        return self._heatmap_register

    def _create_register_for_heatmap(self):
        node_consecutive_successes = [node.consecutive_successes for node in self._nodes]
        node_consecutive_successes = np.array(node_consecutive_successes)
        matrix_form_data = np.reshape(node_consecutive_successes, (self.n, self.n))
        self._heatmap_register.append(matrix_form_data)

    def _create_register_for_heatmap(self):


    @property
    def n(self):
        return self._snowball_configuration.n

    @property
    def k(self):
        return self._snowball_configuration.k

    @property
    def alpha(self):
        return self._snowball_configuration.alpha

    @property
    def beta(self):
        return self._snowball_configuration.beta


if __name__ == '__main__':
    random.seed(0)

    n = 20
    k = 10
    alpha = 6
    beta = 20

    snowball_configuration = SnowballConfiguration(n, k, alpha, beta)
    snowball_alg = SnowballAlgorithm(snowball_configuration)

    snowball_alg.initialize_nodes()
    snowball_alg.simulate()

    data = snowball_alg.retrieve_register()
    hm_data = snowball_alg.retrieve_heatmap_register()

    # sns.lineplot(data=data, x="Iteration", y="Num_Votes", hue="Preference")

    for i in range(n):
        sns.heatmap(hm_data[i], vmin=0, vmax=beta)
        plt.show()

