# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from unittest import TestCase

from samples import RandomSource

from ibench.definitions import Size, Area
import ibench.slice as slice


class TestSliceSource(TestCase):

    def test_all_blocks_of_even_source(self):
        source = RandomSource(
            Size(10, 10, 'pizel'))
        block_size = Size(5, 5, 'pixel')

        blocks = slice.source(source, block_size)

        self.assertEqual(blocks.size, Size(2, 2, 'block'))
        # Samples
        self.assertEqual(blocks.rows[0][1].rows[0][0], source.pixels[0][5])
        self.assertEqual(blocks.rows[1][1].rows[0][0], source.pixels[5][5])

    def test_some_blocks_of_even_source(self):
        source = RandomSource(
            Size(10, 10, 'pizel'))
        block_size = Size(5, 5, 'pixel')
        area = Area(1, 0, 1, 2, 'pixel')

        blocks = slice.source(source, block_size, area)

        self.assertEqual(blocks.size, Size(1, 2, 'block'))
        # Samples
        self.assertEqual(blocks.rows[0][0].rows[0][0], source.pixels[0][5])
        self.assertEqual(blocks.rows[1][0].rows[0][0], source.pixels[5][5])
