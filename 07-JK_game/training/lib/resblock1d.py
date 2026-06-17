import torch
import torch.nn as nn
import torch.nn.functional as F


class ResBlock1D(nn.Module):

    def __init__(self, inplanes, planes, seq_len, stride=1, downsample=None):
        super(ResBlock1D, self).__init__()
        self.conv1 = nn.Conv1d(inplanes, planes, kernel_size=3, stride=stride,
                               padding=1, bias=False)
        self.ln1 = nn.LayerNorm([planes, seq_len])
        self.conv2 = nn.Conv1d(planes, planes, kernel_size=3, stride=stride,
                               padding=1, bias=False)
        self.ln2 = nn.LayerNorm([planes, seq_len])

    def forward(self, x):
        residual = x
        x = F.relu(self.ln1(x))
        x = self.conv1(x)
        x = F.relu(self.ln2(x))
        x = self.conv2(x)
        x = x + residual
        return x
