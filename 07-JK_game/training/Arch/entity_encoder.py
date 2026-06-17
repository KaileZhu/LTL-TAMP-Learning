" Entity Encoder "

import math
import json
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from training.lib import utils as L
from training.lib.redblue_transformer import Transformer

name_list = ['蓝有人机', '蓝无人机1', '蓝无人机2', '蓝无人机3', '蓝无人机4', '红有人机', '红无人机1', '红无人机2', '红无人机3', '红无人机4']

class EntityEncoder(nn.Module):
    '''
    Inputs:entity_list
    outputs:embedded_entity
            entity_embeddings
    '''
    #Todo
    def __init__(self, dropout=0.1):
        super().__init__()
        self.platform_size = 4
        self.hidden_size = 64
        self.ori_512 = 128
        self.ori_64 = 32

        self.dropout = nn.Dropout(dropout)
        self.embedd_platform = nn.Linear(self.platform_size, self.hidden_size)
        self.transformer = Transformer(d_model=self.hidden_size, d_inner=self.ori_512,
                                       n_layers=3, n_head=2, d_k=self.ori_64,
                                       d_v=self.ori_64, dropout=0.1)
        self.conv1 = nn.Conv1d(self.hidden_size, self.hidden_size, kernel_size=1, stride=1,
                               padding=0, bias=False)

        self.fc = nn.Linear(self.hidden_size, self.hidden_size)

    def forward(self, x):
        entity_in = self.embedd_platform(x)

        entity_in = entity_in.unsqueeze(0)

        entity_out = self.transformer(entity_in)

        entity_embeddings = F.relu(self.conv1(F.relu(entity_out).transpose(1, 2))).transpose(1, 2)
        embedded_entity = F.relu(self.fc(torch.mean(entity_out, dim=1, keepdim=False)))

        return entity_embeddings, embedded_entity

    def preprocess(self, obs):
        redsituation = obs['redSituation']
        bluesituation = obs['blueSituation']
        red_platform_list = []
        red_name_list = []
        blue_platform_list = []
        blue_name_list = []

        for id, redentities in redsituation.items():
            for entity in redentities:
                field_encoding_list = []

                field_encoding_list.append(torch.tensor([entity['life'] / 100]).reshape(1, -1))
                field_encoding_list.append(torch.tensor([entity['speed'] / 500]).reshape(1, -1))
                field_encoding_list.append(torch.tensor([entity['longitude'] / 180]).reshape(1, -1))
                field_encoding_list.append(torch.tensor([entity['latitude'] / 90]).reshape(1, -1))

                entity_tensor = torch.cat(field_encoding_list, dim=1)
                red_platform_list.append(entity_tensor)
                red_name_list.append(entity['name'])
        red_platform_list = torch.cat(red_platform_list, dim=0)

        for id, blueentities in bluesituation.items():
            for entity in blueentities:
                field_encoding_list = []

                field_encoding_list.append(torch.tensor([entity['life'] / 100]).reshape(1, -1))
                field_encoding_list.append(torch.tensor([entity['speed'] / 500]).reshape(1, -1))
                field_encoding_list.append(torch.tensor([entity['longitude'] / 180]).reshape(1, -1))
                field_encoding_list.append(torch.tensor([entity['latitude'] / 90]).reshape(1, -1))

                entity_tensor = torch.cat(field_encoding_list, dim=1)
                blue_platform_list.append(entity_tensor)
                blue_name_list.append(entity['name'])
        blue_platform_list = torch.cat(blue_platform_list, dim=0)
        platform_list = torch.cat([red_platform_list, blue_platform_list], dim=0)

        return platform_list, red_name_list, blue_name_list








