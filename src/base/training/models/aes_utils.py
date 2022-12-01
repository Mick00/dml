from torch import nn

from src.base.training.models.layers.conv import ConvLayer
from src.base.training.models.layers.deconv import DeconvLayer


def flattened_len(dims):
    if isinstance(dims, int):
        return dims
    channels, x, y = dims
    return channels * x * y


def preview_dims(dims, layers):
    x, y = dims
    channels = 0
    for layer in layers:
        channels = layer.get("out_channels")
        x = ((x - (layer.get("kernel_size", 1)) + (layer.get("padding", 0) * 2)) / layer.get("stride", 1)) + 1
        x = x * layer.get("scale_factor", 1)
        y = ((y - (layer.get("kernel_size", 1)) + (layer.get("padding", 0) * 2)) / layer.get("stride", 1)) + 1
        y = y * layer.get("scale_factor", 1)
    if x % 1 != 0 or y % 1 != 0:
        print(f"Warning dimensions are not ints: ({channels}, {x}, {y})")
    return int(channels), int(x), int(y)


def get_enc_dec(layers) -> tuple[nn.Sequential, nn.Sequential]:
    encoders = []
    decoders = []
    for layer in layers:
        encoder, decoder = get_conv_deconv_pair(layer["in_channels"],
                                                layer["out_channels"],
                                                layer.get("scale_factor", 1),
                                                layer.get("kernel_size", 1),
                                                layer.get("stride", 1),
                                                layer.get("padding", 0)
                                                )
        encoders += [encoder]
        decoders = [decoder] + decoders
    return nn.Sequential(*encoders), nn.Sequential(*decoders)


def get_conv_deconv_pair(in_channels, out_channels, scale_factor=1, kernel_size=1, stride=1, padding=0):
    return \
        ConvLayer(in_channels, out_channels, scale_factor, kernel_size, stride, padding), \
        DeconvLayer(out_channels, in_channels, 1 / scale_factor, kernel_size, stride, padding)
