from torch import nn
from torch.nn import functional as F


class Interpolate(nn.Module):
    def __init__(self, scale_factor=1):
        super().__init__()
        self.scale_factor = scale_factor

    def forward(self, x):
        if self.scale_factor != 1:
            return F.interpolate(x, scale_factor=self.scale_factor)
        return x
