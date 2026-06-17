" Location Head. "

import torch
import torch.nn as nn
import torch.nn.functional as F

from training.lib import utils as L

class LocationHead(nn.Module):
    '''
    Inputs: autogressive_embedding
    Outputs: Location
    '''

    def __init__(self, ori_128=64, ori_64=48, ori_32=32):
        super(LocationHead, self).__init__()
        super().__init__()
        self.fc_x1 = nn.Linear(ori_128, ori_64)
        self.fc_x2 = nn.Linear(ori_64, ori_32)
        self.fc_x3 = nn.Linear(ori_32, 10)

        self.fc_y1 = nn.Linear(ori_128, ori_64)
        self.fc_y2 = nn.Linear(ori_64, ori_32)
        self.fc_y3 = nn.Linear(ori_32, 10)

        self.softmax = nn.Softmax(dim=-1)

    def forward(self, autoregressive_embedding):

        location_x_logits = self.fc_x3(F.relu(self.fc_x2(F.relu(self.fc_x1(autoregressive_embedding)))))
        location_x_probs = self.softmax(location_x_logits)
        location_x_id = torch.multinomial(location_x_probs, 1)

        location_y_logits = self.fc_y3(F.relu(self.fc_y2(F.relu(self.fc_y1(autoregressive_embedding)))))
        location_y_probs = self.softmax(location_y_logits)
        location_y_id = torch.multinomial(location_y_probs, 1)

        return location_x_logits, location_x_probs, location_x_id, location_y_logits, location_y_probs, location_y_id