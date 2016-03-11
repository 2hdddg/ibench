# -*- coding: utf-8 -*-
from __future__ import absolute_import

from unittest import TestCase

from ibench.definitions import Size
from ibench.subsample import planeYCbCr_to_planeYCbCr420

from .samples import get_random_ycbcr_plane


class TestYCbCrToYCbCr420(TestCase):

    def test_y_stays_the_same(self):
        size = Size(8, 8, 'pixel')
        yCbCrPlane = get_random_ycbcr_plane(size)
        yCbCr420Plane = planeYCbCr_to_planeYCbCr420(yCbCrPlane)

        self.assertEqual(yCbCrPlane.y, yCbCr420Plane.y)

    def test_y_is_copied(self):
        size = Size(8, 8, 'pixel')
        yCbCrPlane = get_random_ycbcr_plane(size)
        yCbCr420Plane = planeYCbCr_to_planeYCbCr420(yCbCrPlane)
        # Change something in source
        yCbCrPlane.y[0][0] = yCbCrPlane.y[0][0] + 1

        self.assertNotEqual(yCbCrPlane.y[0][0], yCbCr420Plane.y[0][0])

    def test_cb_cr_is_a_quarter_of_original(self):
        size = Size(8, 8, 'pixel')
        yCbCrPlane = get_random_ycbcr_plane(size)
        yCbCr420Plane = planeYCbCr_to_planeYCbCr420(yCbCrPlane)

        cbSize = (len(yCbCr420Plane.cb), len(yCbCr420Plane.cb[0]))
        crSize = (len(yCbCr420Plane.cr), len(yCbCr420Plane.cr[0]))

        self.assertTupleEqual(cbSize, (4, 4))
        self.assertTupleEqual(crSize, (4, 4))
