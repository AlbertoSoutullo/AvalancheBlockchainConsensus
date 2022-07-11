# Python Imports
import random
from collections import Counter
from typing import List, Optional, Tuple


class Node:
    def __init__(self, vote: str, node_id: int):
        self._preference = vote
        self._id = node_id
        self._consecutive_successes = 0
        self._decided = False

    def __eq__(self, other):
        return self._id == other.id

    def update(self, all_nodes, k, alpha, beta) -> None:
        all_nodes_but_itself = [node for node in all_nodes if node != self]
        random_nodes = random.sample(all_nodes_but_itself, k)

        preference, nodes_agreed = self._check_for_nodes_preference(random_nodes, alpha)
        if nodes_agreed:
            self._update_preference_and_successes(preference)
        else:
            self._consecutive_successes = 0
        if self._consecutive_successes > beta:
            self._decided = True

    def _check_for_nodes_preference(self, random_nodes: List, alpha: int) -> Tuple[Optional[str], bool]:
        random_votes = [node.preference for node in random_nodes]
        count_preferences = Counter(random_votes)
        ordered_preferences = count_preferences.most_common(1)

        if ordered_preferences[0][1] >= alpha:
            return ordered_preferences[0][0], True

        return None, False

    def _update_preference_and_successes(self, preference: str) -> None:
        if self._preference == preference:
            self._consecutive_successes += 1
        else:
            self._consecutive_successes = 1
            self._preference = preference

    def is_decided(self) -> bool:
        return self._decided

    @property
    def id(self) -> int:
        return self._id

    @property
    def preference(self) -> str:
        return self._preference

    @property
    def consecutive_successes(self) -> int:
        return self._consecutive_successes
