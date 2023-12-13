import itertools
from typing import List

from prediction.models.note_sequence import NoteSequence
from prediction.nn.models.gru import GRU
from prediction.workers.gru_model_predictor import GRUModelPredictor


class GRUDataHandler:
    def __init__(self, model: GRU) -> None:
        self._model_predictor: GRUModelPredictor = GRUModelPredictor(model)

    def get_predictions(self, voice: NoteSequence) -> List[int | None]:
        positions: List[int] = [
            list(group_values) for _, group_values in itertools.groupby(voice.raw_rel_positions, lambda d: d is None)
        ]
        intervals: List[int] = [
            list(group_values) for _, group_values in itertools.groupby(voice.raw_intervals, lambda d: d is None)
        ]
        predictions: List[int] = list()

        position_count = position_idx = interval_count = interval_idx = 0

        while position_idx < len(positions) and interval_idx < len(intervals):
            if interval_count <= position_count:
                position_count += len(positions[position_idx])
                interval_count += len(intervals[interval_idx])
            elif interval_count > position_count:
                position_count += len(positions[position_idx])
                position_idx += 1
                continue

            if positions[position_idx][0] is not None and len(positions[position_idx]) > 1:
                prediction = self._model_predictor.evaluate_continuous(
                    positions=positions[position_idx],
                    intervals=intervals[interval_idx],
                    fingerings=[0] * len(positions[position_idx]),
                )
                predictions.append(prediction)
            else:
                predictions.append([None] * len(positions[position_idx]))

            position_idx += 1
            interval_idx += 1

        return sum(predictions, list())
