import torch.nn as nn


class GRU(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, n_layers, drop_prob=0.1):
        super(GRU, self).__init__()
        self.hidden_size = hidden_size
        self.n_layers = n_layers

        self.gru = nn.GRU(input_size, hidden_size, n_layers, dropout=drop_prob)
        self.fc = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(drop_prob)
        self.softmax = nn.LogSoftmax(dim=0)

    def forward(self, input, hidden):
        output, hidden = self.gru(input, hidden)
        output = self.fc(self.relu(output[-1]))
        output = self.softmax(self.dropout(output))
        return output, hidden

    def init_hidden(self):
        weights = next(self.parameters()).data
        return weights.new(self.n_layers, self.hidden_size).zero_()
