# Python Imports
from dataclasses import dataclass


@dataclass
class SnowballConfiguration:
    n: int
    k: int
    alpha: int
    beta: int
