" Action Type Head. "

import torch
import torch.nn as nn
import torch.nn.functional as F

from training.lib.resblock1d import ResBlock1D
from training.lib import utils as L

class ActionTypeHead(nn.Module):
    '''
    Inputs: lstm_output
    Outputs:
        action_type_logits
        action_type
        autoregressive_embedding
    '''

    def __init__(self, lstm_dim=64, ori_32=32, ori_128=64, n_resblocks=3, action_num=2):
        super(ActionTypeHead, self).__init__()

        self.action_num = action_num

        self.embed_fc = nn.Linear(lstm_dim, ori_32)
        self.resblock_stack = nn.ModuleList([
            ResBlock1D(inplanes=ori_32, planes=ori_32, seq_len=1)
            for _ in range(n_resblocks)])

        self.fc_1 = nn.Linear(ori_32, action_num)
        self.fc_2 = nn.Linear(1, ori_32)
        self.fc_3 = nn.Linear(ori_32, ori_128)
        self.fc_4 = nn.Linear(ori_128, ori_128)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, lstm_output):
        x = self.embed_fc(lstm_output)

        x = x.unsqueeze(-1)
        for resblock in self.resblock_stack:
            x = resblock(x)
        x = F.relu(x)
        x = x.squeeze(-1)

        action_type_logits = self.fc_1(x)
        action_type_probs = self.softmax(action_type_logits)
        # print(action_type_probs)

        action_type = torch.multinomial(action_type_probs, 1)
        action_type = action_type.reshape(-1, 1)

        z = F.relu(self.fc_3(F.relu(self.fc_2(action_type.to(torch.float32)))))
        t = F.relu(self.fc_4(lstm_output))
        autoregressive_embedding = z + t

        return action_type_logits, action_type_probs, action_type, autoregressive_embedding
