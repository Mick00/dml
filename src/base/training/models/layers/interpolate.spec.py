import unittest
import torch

from src.base.training.models.layers.interpolate import Interpolate


class InterpolateLayerTest(unittest.TestCase):

    def test_no_interpolation(self):
        interpolate = Interpolate(1)
        x = torch.Tensor([[1, 2], [3, 4]])
        ix = interpolate(x)
        self.assertTrue(torch.equal(x, ix))

    def test_half_interpolation(self):
        interpolate = Interpolate(1/2)
        x = torch.rand((10, 2, 10, 10))
        ix = interpolate(x)
        idx, ch, x, y = ix.size()
        self.assertEqual(idx, 10)
        self.assertEqual(ch, 2)
        self.assertEqual(x, 5)
        self.assertTrue(y, 5)

    def test_double_interpolation(self):
        interpolate = Interpolate(2)
        x = torch.rand((10, 2, 4, 4))
        ix = interpolate(x)
        idx, ch, x, y = ix.size()
        self.assertEqual(idx, 10)
        self.assertEqual(ch, 2)
        self.assertEqual(x, 8)
        self.assertTrue(y, 8)

    def test_odd_numbers(self):
        interpolate = Interpolate(1/2)
        x = torch.rand((10, 2, 9, 9))
        ix = interpolate(x)
        idx, ch, x, y = ix.size()
        self.assertEqual(idx, 10)
        self.assertEqual(ch, 2)
        self.assertEqual(x, 4)
        self.assertTrue(y, 4)

    def test_odd_scale_number(self):
        interpolate = Interpolate(10/14)
        x = torch.rand((10, 2, 14, 14))
        ix = interpolate(x)
        idx, ch, x, y = ix.size()
        self.assertEqual(idx, 10)
        self.assertEqual(ch, 2)
        self.assertEqual(x, 10)
        self.assertTrue(y, 10)


if __name__ == '__main__':
    unittest.main()