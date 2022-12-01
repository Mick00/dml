import unittest
import torch

from src.base.training.models.layers.conv import ConvLayer
from src.base.training.models.layers.interpolate import Interpolate


class ConvLayerTest(unittest.TestCase):

    def test_conv_layer_no_scaling(self):
        in_channels = 2
        x, y = (10, 10)
        x = torch.rand((5, in_channels, x, y))
        conv = ConvLayer(in_channels, 4)
        cx = conv(x)
        self.assert_dims(cx, 5, 4, 10, 10)

    def test_stride(self):
        in_channels = 2
        x, y = (10, 10)
        stride = 5
        x = torch.rand((5, in_channels, x, y))
        conv = ConvLayer(in_channels, 4, stride=stride)
        cx = conv(x)
        self.assert_dims(cx, 5, 4, 2, 2)

    def test_kernel_size(self):
        in_channels = 2
        x, y = (10, 10)
        kernel = 5
        x = torch.rand((5, in_channels, x, y))
        conv = ConvLayer(in_channels, 4, kernel_size=kernel)
        cx = conv(x)
        self.assert_dims(cx, 5, 4, 6, 6)

    def test_kernel_size_and_stride(self):
        in_channels = 2
        x, y = (10, 10)
        kernel = 5
        stride = 2
        x = torch.rand((5, in_channels, x, y))
        conv = ConvLayer(in_channels, 4, kernel_size=kernel, stride=stride)
        cx = conv(x)
        self.assert_dims(cx, 5, 4, 3, 3)

    def test_conv_layer_half_scaling(self):
        in_channels = 2
        x, y = (10, 10)
        x = torch.rand((5, in_channels, x, y))
        conv = ConvLayer(in_channels, 6, scale_factor=0.5)
        cx = conv(x)
        self.assert_dims(cx, 5, 6, 5, 5)

    def assert_dims(self, tensor, idx, ch, x, y):
        tidx, tch, tx, ty = tensor.size()
        self.assertEqual(idx, tidx)
        self.assertEqual(ch, tch)
        self.assertEqual(x, tx)
        self.assertEqual(y, ty)


if __name__ == '__main__':
    unittest.main()