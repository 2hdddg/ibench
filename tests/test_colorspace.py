# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import unittest

from ibench.definitions import RGB
import ibench.colorspace as colorspace

from .samples import random_rgb_block

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
    def _test_plane(self, rows, convert_fun):
        for i, row in enumerate(rows):
            for j, y in enumerate(row):
                rgb = random_rgb_block.rows[i][j]
                self.assertEqual(y, convert_fun(rgb))

    def test_y_plane(self):
        plane = colorspace.blockRgb_to_planeYCbCr(random_rgb_block)

        self.assertEqual(plane.size, random_rgb_block.size)

        self._test_plane(plane.y, lambda rgb: colorspace.rgb_to_yCbCr(rgb).y)

    def test_cb_plane(self):
        plane = colorspace.blockRgb_to_planeYCbCr(random_rgb_block)

        self.assertEqual(plane.size, random_rgb_block.size)

        self._test_plane(plane.cb, lambda rgb: colorspace.rgb_to_yCbCr(rgb).cb)

    def test_cr_plane(self):
        plane = colorspace.blockRgb_to_planeYCbCr(random_rgb_block)

        self.assertEqual(plane.size, random_rgb_block.size)

        self._test_plane(plane.cr, lambda rgb: colorspace.rgb_to_yCbCr(rgb).cr)


class TestYCbCrComponentsToRGB(unittest.TestCase):

    def test_y_empty(self):
        rgb = colorspace.y_to_rgb(0.0)

        self.assertEqual(rgb, RGB(0, 0, 0))

    def test_y_full(self):
        rgb = colorspace.y_to_rgb(1.0)

        self.assertEqual(rgb, RGB(255, 255, 255))

    def test_y_half(self):
        rgb = colorspace.y_to_rgb(0.5)

        self.assertEqual(rgb, RGB(127, 127, 127))

    def test_cb_empty(self):
        rgb = colorspace.cb_to_rgb(-0.5)

        self.assertEqual(rgb, RGB(0, 0, 0))

    def test_cb_full(self):
        rgb = colorspace.cb_to_rgb(0.5)

        self.assertEqual(rgb, RGB(0, 0, 255))

    def test_cb_half(self):
        rgb = colorspace.cb_to_rgb(0)

        self.assertEqual(rgb, RGB(0, 0, 127))

    def test_cr_empty(self):
        rgb = colorspace.cr_to_rgb(-0.5)

        self.assertEqual(rgb, RGB(0, 0, 0))

    def test_cr_full(self):
        rgb = colorspace.cr_to_rgb(0.5)

        self.assertEqual(rgb, RGB(255, 0, 0))

    def test_cr_half(self):
        rgb = colorspace.cr_to_rgb(0)

        self.assertEqual(rgb, RGB(127, 0, 0))
