import math
from typing import List

import numpy as np
import torch
import torch.nn as nn

from prediction.nn.constants import N_NOTES, TARGET_INDEX


class GRUDataTransformer:
    PERMUTATION = list(range(TARGET_INDEX)) + list(range(TARGET_INDEX + 1, N_NOTES)) + [TARGET_INDEX]
    CYCLE_LENGTH = 12
    MAGNITUDE_SCALE = 12

    def create_positions_tensor(self, positions_list: List[int]) -> torch.Tensor:
        positions = np.array(positions_list)[self.PERMUTATION]
        positions = (2 * math.pi / self.CYCLE_LENGTH) * np.expand_dims(positions, axis=1)
        positions_sin, positions_cos = np.sin(np.copy(positions)), np.cos(np.copy(positions))
        return torch.from_numpy(np.concatenate((positions_sin, positions_cos), axis=1)).float()

    def create_intervals_tensor(self, intervals_list: List[int]) -> torch.Tensor:
        # Pad on the left side (set first value to 0)
        intervals = np.pad(np.array(intervals_list), pad_width=[(1, 0)])
        intervals = intervals[self.PERMUTATION]
        intervals = np.expand_dims(intervals, axis=1)
        intervals_sign, intervals_mag = np.copy(intervals) > 0, np.abs(np.copy(intervals)) / self.MAGNITUDE_SCALE
        return torch.from_numpy(np.concatenate((intervals_sign, intervals_mag), axis=1)).float()

    def create_fingerings_one_hot_tensor(self, fingerings_list: List[int]) -> torch.Tensor:
        # Remove last value and pad first value to 0
        fingerings = np.pad(np.array(fingerings_list[:-1]), pad_width=[(1, 0)])[self.PERMUTATION]
        fingerings[list(range(TARGET_INDEX, N_NOTES - 1))] = 0
        return nn.functional.one_hot(torch.tensor(fingerings), num_classes=6)
