# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from unittest import TestCase

import PIL

from .samples import composition_of_two_parts

from ibench.definitions import Size
from ibench.layout import fixed_grid, compose_image


def _dummy_renderer(row, col):
    return "dummy renderer"


class TestFixedGrid(TestCase):
    def test_size_no_padding(self):
        grid = Size(3, 3, 'block')
        padding = Size(0, 0, 'pixel')
        cell = Size(1, 1, 'pixel')

        composition = fixed_grid(grid, padding, cell, _dummy_renderer)

        size = composition.size

        # 3 x 3 cells where each cell is 1x1 pixels and no padding
        self.assertEqual((size.cx, size.cy), (3, 3))
        self.assertEqual(composition.size.unit, 'pixel')

    def test_padding_offset(self):
        # Offset in first part
        grid = Size(1, 1, 'block')
        padding = Size(2, 3, 'pixel')
        cell = Size(1, 1, 'pixel')

        composition = fixed_grid(grid, padding, cell, _dummy_renderer)

        part = composition.parts[0]
        self.assertEqual((part.offset.x, part.offset.y), (2, 3))

    def test_padding(self):
        # Offset between parts
        grid = Size(2, 2, 'block')
        padding = Size(2, 3, 'pixel')
        cell = Size(1, 1, 'pixel')

        composition = fixed_grid(grid, padding, cell, _dummy_renderer)

        topleft_part = composition.parts[0]
        bottomright_part = composition.parts[3]
        x_between = bottomright_part.offset.x - topleft_part.size.cx - topleft_part.offset.x
        y_between = bottomright_part.offset.y - topleft_part.size.cy - topleft_part.offset.y
        self.assertEqual((x_between, y_between), (2, 3))


class TestCompositionSmoke(TestCase):
    def test_compose_image_smoke(self):
        image = compose_image(composition_of_two_parts)

        self.assertIsInstance(image, PIL.Image.Image)
