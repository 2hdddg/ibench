# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import unittest

from ibench.definitions import RGB, BlockRGB, Size
import ibench.colorspace as colorspace


_bw_striped_rgb_block = BlockRGB(
        Size(4, 4, 'pixel'),
        [
            [RGB(255, 255, 255), RGB(0, 0, 0), RGB(255, 255, 255), RGB(0, 0, 0)],
            [RGB(255, 255, 255), RGB(0, 0, 0), RGB(255, 255, 255), RGB(0, 0, 0)],
            [RGB(255, 255, 255), RGB(0, 0, 0), RGB(255, 255, 255), RGB(0, 0, 0)],
            [RGB(255, 255, 255), RGB(0, 0, 0), RGB(255, 255, 255), RGB(0, 0, 0)]
        ])


_precision = 0


class TestRGBToYCbCr(unittest.TestCase):

    def test_white(self):
        rgb = RGB(255, 255, 255)
        yCbCr = colorspace.rgb_to_yCbCr(rgb)

        self.assertAlmostEqual(yCbCr.y, 1, _precision, "Y should be 1 when color is white")
        self.assertAlmostEqual(yCbCr.cb, 0, _precision, "Cb should be 0 when color is white")
        self.assertAlmostEqual(yCbCr.cr, 0, _precision, "Cr should be 0 when color is white")

    def test_black(self):
        rgb = RGB(0, 0, 0)
        yCbCr = colorspace.rgb_to_yCbCr(rgb)

        self.assertAlmostEqual(yCbCr.y, 0, _precision, "Y should be 0 when color is black")
        self.assertAlmostEqual(yCbCr.cb, 0, _precision, "Cb should be 0 when color is black")
        self.assertAlmostEqual(yCbCr.cr, 0, _precision, "Cr should be 0 when color is black")

    def test_blue(self):
        rgb = RGB(0, 0, 255)

        yCbCr = colorspace.rgb_to_yCbCr(rgb)

        self.assertAlmostEqual(yCbCr.cb, 0.5, _precision, "Cb should be 0.5 when color is blue")
        self.assertAlmostEqual(yCbCr.cr, 0, _precision, "Cr should be 0 when color is blue")

    def test_red(self):
        rgb = RGB(255, 0, 0)

        yCbCr = colorspace.rgb_to_yCbCr(rgb)

        self.assertAlmostEqual(yCbCr.cr, 0.5, _precision, "Cr should be 0.5 when color is red")
        self.assertAlmostEqual(yCbCr.cb, 0, _precision, "Cb should be 0 when color is red")


class TestBlockRGBToPlaneYCbCr(unittest.TestCase):

    def test_y_plane(self):
        plane = colorspace.blockRgb_to_planeYCbCr(_bw_striped_rgb_block)

