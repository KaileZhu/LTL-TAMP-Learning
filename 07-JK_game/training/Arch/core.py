" Core. "

import torch
import torch.nn as nn
import torch.nn.functional as F


class Core(nn.Module):
    '''
    Inputs: prev_state, embedded_entity
    Outputs:
        next_state - The LSTM state for the next step
        lstm_output - The output of the LSTM
    '''

    def __init__(self, n_layers=1, hidden_dim=64, embedding_dim=64, batch_size=1, sequence_length=1, drop_prob=0):
        super(Core, self).__init__()
        self.n_layers = n_layers
        self.hidden_dim = hidden_dim
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_dim, num_layers=n_layers, dropout=drop_prob,
                            batch_first=True)
        self.batch_size = batch_size
        self.sequence_length = sequence_length

    def forward(self, embedded_entity,
                batch_size=None, sequence_length=None, hidden_state=None):
        batch_size = batch_size if batch_size is not None else self.batch_size
        sequence_length = sequence_length if sequence_length is not None else self.sequence_length

        input_tensor = embedded_entity

        embedding_size = input_tensor.shape[-1]

        input_tensor = input_tensor.reshape(batch_size, sequence_length, embedding_size)

        if hidden_state is None:
            hidden_state = self.init_hidden_state(batch_size=batch_size)

        lstm_output, hidden_state = self.forward_lstm(input_tensor, hidden_state)

        lstm_output = lstm_output.reshape(batch_size * sequence_length, self.hidden_dim)
        return lstm_output, hidden_state

    def forward_lstm(self, x, hidden):
        lstm_out, hidden = self.lstm(x, hidden)

        # DIFF: We apply layer norm to the gates.

        '''
        lstm_out = lstm_out.contiguous().view(-1, self.hidden_dim)

        out = self.dropout(lstm_out)
        out = self.fc(out)
        out = self.sigmoid(out)

        out = out.view(batch_size, -1)
        out = out[:,-1]
        '''

        return lstm_out, hidden

    def init_hidden_state(self, batch_size=1):
        '''
        weight = next(self.parameters()).data
        hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device),
                  weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device))
                  '''
        device = next(self.parameters()).device
        hidden = (torch.zeros(self.n_layers, batch_size, self.hidden_dim).to(device),
                  torch.zeros(self.n_layers, batch_size, self.hidden_dim).to(device))
        return hidden
