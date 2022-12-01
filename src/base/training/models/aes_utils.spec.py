import unittest
from unittest.mock import Mock

import torch

from src.base.training.models.aes_utils import get_conv_deconv_pair, get_enc_dec, preview_dims


class AESUtilsTest(unittest.TestCase):
    def test_conv_deconv_pair(self):
        x = torch.rand((10, 3, 8, 8))
        conv, deconv = get_conv_deconv_pair(3, 6, 0.5, 3, 1, 1)
        c_x = conv(x)
        d_x = deconv(c_x)
        i, ch, x, y = x.size()
        di, dch, dx, dy = d_x.size()
        self.assertEqual(i, di)
        self.assertEqual(ch, dch)
        self.assertEqual(x, dx)
        self.assertEqual(y, dy)

    def test_enc_dec(self):
        x = torch.rand((10, 3, 8, 8))
        enc, dec = get_enc_dec([
            {
                "in_channels": 3,
                "out_channels": 4,
                "scale_factor": 2,
                "kernel_size": 2,
                "stride": 1,
                "padding": 1
            },
            {
                "in_channels": 4,
                "out_channels": 6,
                "scale_factor": 1/2,
                "kernel_size": 2,
                "stride": 2,
                "padding": 1
            }
        ])
        enc_x = enc(x)
        dec_x = dec(enc_x)
        i, ch, x, y = x.size()
        di, dch, dx, dy = dec_x.size()
        self.assertEqual(i, di)
        self.assertEqual(ch, dch)
        self.assertEqual(x, dx)
        self.assertEqual(y, dy)

    def test_preview_dims(self):
        x = torch.rand((10, 3, 8, 8))
        layers = [
            {
                "in_channels": 3,
                "out_channels": 4,
                "scale_factor": 2,
                "kernel_size": 2,
                "stride": 1,
                "padding": 1
            },
            {
                "in_channels": 4,
                "out_channels": 6,
                "scale_factor": 1 / 2,
                "kernel_size": 2,
                "stride": 2,
                "padding": 1
            }
        ]
        enc, dec = get_enc_dec(layers)
        enc_x = enc(x)
        ch, x, y = preview_dims((8, 8), layers)
        e_i, e_ch, e_x, e_y = enc_x.size()
        self.assertEqual(ch, e_ch)
        self.assertEqual(x, e_x)
        self.assertEqual(y, e_y)

    def test_lenet_outputs(self):
        print(preview_dims((28, 28), [
            {
                "in_channels": 1,
                "out_channels": 6,
                "padding": 2,
                "kernel_size": 5,
                "scale_factor": 1 / 2
            },
            {
                "in_channels": 6,
                "out_channels": 16,
                "padding": 0,
                "kernel_size": 5,
                "scale_factor": 1 / 2
            }
        ]))



if __name__ == '__main__':
    unittest.main()