from torch import nn

from src.protocol.training.models.layers.interpolate import Interpolate


class ConvLayer(nn.Module):
    def __init__(self,
                 in_channels,
                 out_channels,
                 scale_factor=1,
                 kernel_size=1,
                 stride=1,
                 padding=0
                 ):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(
                in_channels=in_channels,
                out_channels=out_channels,
                kernel_size=kernel_size,
                stride=stride,
                padding=padding,
            ),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
            Interpolate(scale_factor)
        )

    def forward(self, x):
        return self.conv(x)
