import torch
import torch.nn as nn

from prediction.nn.models.gru import GRU


def load_model(model_name: str, **params) -> GRU:
    model: nn.Module = GRU(**params)
    model.load_state_dict(torch.load(model_name))
    return model
