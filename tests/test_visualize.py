# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import unittest

from ibench.visualize import it, rgb_block_to_image, rgb_blocks_to_image, ycbcr_plane_to_image
import PIL

from .samples import random_rgb_block, random_rgb_blocks, random_ycbcr_plane


class TestVisualizeSmoke(unittest.TestCase):
    def test_rgb_block_to_image_smoke(self):
        block = random_rgb_block
        image = rgb_block_to_image(block)

        self.assertIsInstance(image, PIL.Image.Image)

    def test_rgb_blocks_to_image_smoke(self):
        blocks = random_rgb_blocks
        image = rgb_blocks_to_image(blocks)

        self.assertIsInstance(image, PIL.Image.Image)

    def test_ycbcr_plane_to_image_smoke(self):
        plane = random_ycbcr_plane
        image = ycbcr_plane_to_image(plane)

        self.assertIsInstance(image, PIL.Image.Image)


class TestVisualizeIt(unittest.TestCase):
    def test_visualize_rgb_block(self):
        image = it(random_rgb_block)

        self.assertIsInstance(image, PIL.Image.Image)

    def test_visualize_rgb_blocks(self):
        image = it(random_rgb_blocks)

        self.assertIsInstance(image, PIL.Image.Image)

    def test_visualize_ycbr_plane(self):
        image = it(random_ycbcr_plane)

        self.assertIsInstance(image, PIL.Image.Image)

    def test_custom_visualizer(self):
        def get_custom(buf):
            return lambda b: "from custom"

        image = it(random_rgb_blocks, get_custom_visualizer=get_custom)

        self.assertEqual(image, "from custom")
