import itertools
from typing import List

from prediction.models.note_sequence import NoteSequence
from prediction.nn.constants import N_NOTES, TARGET_INDEX
from prediction.nn.models.gru import GRU
from prediction.workers.gru_model_predictor import GRUModelPredictor


class GRUDataHandler:
    def __init__(self, model: GRU) -> None:
        self._model_predictor: GRUModelPredictor = GRUModelPredictor(model)

    def _pad_data(self, data: List[int]) -> List[int]:
        return [0] * TARGET_INDEX + data + [0] * (N_NOTES - TARGET_INDEX - 1)

    def get_predictions(self, voice: NoteSequence) -> List[int | None]:
        positions: List[int] = [
            list(group_values) for _, group_values in itertools.groupby(voice.raw_rel_positions, lambda d: d is None)
        ]
        intervals: List[int] = [
            list(group_values) for _, group_values in itertools.groupby(voice.raw_intervals, lambda d: d is None)
        ]
        predictions: List[int] = list()
        for i in range(len(positions)):
            if positions[i][0] is not None and len(positions[i]) > 1:
                prediction = self._model_predictor.evaluate_continuous(
                    positions=positions[i],
                    intervals=intervals[i],
                    fingerings=[0] * len(positions[i]),
                )
                predictions.append(prediction)
            else:
                predictions.append([None] * len(positions[i]))
        return sum(predictions, list())
