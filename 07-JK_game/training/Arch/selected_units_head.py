" Selected Units Head "

import torch
import torch.nn as nn
import torch.nn.functional as F

from training.lib import utils as L


class SelectedUnitsHead(nn.Module):
    '''
    Inputs: autoregressive_emdedding, action_type, entity_embeddings
    Outputs:
        entity_logits
        entity
    '''

    def __init__(self, embedding_size=64, original_256=256, original_32=32,
                 autoregressive_embedding_size=64):
        super().__init__()


        self.conv_1 = nn.Conv1d(in_channels=embedding_size,
                                out_channels=original_32, kernel_size=1, stride=1,
                                padding=0, bias=False)

        self.small_lstm = nn.LSTM(input_size=original_32, hidden_size=original_32, num_layers=1,
                                  dropout=0.0, batch_first=True)
        self.fc_1 = nn.Linear(autoregressive_embedding_size, original_256)
        self.fc_2 = nn.Linear(original_256, original_32)

        self.softmax = nn.Softmax(dim=-1)


    def forward(self, autoregressive_embedding, entity_embeddings, num):
        '''
        Inputs:
            autoregressive_embedding: [batch_size x autoregressive_embedding_size]
            action_type: [batch_size x 1]
            entity_embeddings: [batch_size x entity_size x embedding_size]
        Output:
            entity_logits
            entity
        '''
        entity_embeddings = entity_embeddings[:, :num, :]
        key = self.conv_1(entity_embeddings.transpose(-1, -2)).transpose(-1, -2)
        x = self.fc_1(autoregressive_embedding)
        z = F.relu(self.fc_2(x))
        z = z.unsqueeze(1)

        query, hidden = self.small_lstm(z)

        y = torch.bmm(key, query.transpose(-1, -2))
        y = y.squeeze(-1)

        entity_logits = y
        entity_probs = self.softmax(entity_logits)

        entity_id = torch.multinomial(entity_probs, 1)

        return entity_logits, entity_probs, entity_id
