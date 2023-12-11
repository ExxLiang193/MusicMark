from typing import List

import torch

from prediction.nn.constants import N_NOTES, TARGET_INDEX
from prediction.nn.models.gru import GRU
from prediction.workers.gru_data_transformer import GRUDataTransformer


class GRUModelPredictor:
    def __init__(self, model: GRU) -> None:
        self._model: GRU = model
        self._data_transformer: GRUDataTransformer = GRUDataTransformer()

    def _pad_data(self, data: List[int]) -> List[int]:
        return [0] * TARGET_INDEX + data + [0] * (N_NOTES - TARGET_INDEX - 1)

    def evaluate(
        self,
        positions: List[int],
        intervals: List[int],
        fingerings: List[int],
    ) -> int:
        self._model.eval()

        with torch.no_grad():
            # Setup
            positions_tensor = self._data_transformer.create_positions_tensor(positions_list=positions)
            intervals_tensor = self._data_transformer.create_intervals_tensor(intervals_list=intervals)
            fingerings_one_hot_tensor = self._data_transformer.create_fingerings_one_hot_tensor(fingerings)

            input_tensor = torch.cat((positions_tensor, intervals_tensor, fingerings_one_hot_tensor), dim=1)
            hidden = self._model.init_hidden()

            # Execute
            output, _ = self._model(input_tensor, hidden)

            # Extract
            _, top_i = output.topk(1)

        return top_i[0].item()

    def evaluate_continuous(
        self,
        positions: torch.Tensor,
        intervals: torch.Tensor,
        fingerings: torch.Tensor,
        window_size: int = N_NOTES,
    ) -> List[int]:
        self._model.eval()
        padded_positions: List[int] = self._pad_data(positions)

        for i in range(len(padded_positions) - window_size + 1):
            predicted_value: int = self.evaluate(
                padded_positions[i : i + window_size],
                self._pad_data(intervals)[i : i + window_size - 1],
                self._pad_data(fingerings)[i : i + window_size],
            )
            fingerings[i] = predicted_value

        return fingerings
