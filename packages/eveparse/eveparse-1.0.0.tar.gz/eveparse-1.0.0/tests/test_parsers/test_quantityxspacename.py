from unittest import TestCase

from eveparse.errors import ParserError
from eveparse.parsers.quantityxspacename import QuantityXSpaceName


class QuantityXSpaceNameTestCase(TestCase):
    def test_example_passes(self):
        self.assertEqual(QuantityXSpaceName.parse("2x ragnarok"), ("ragnarok", 2))

    def test_multiple_x_space_passes(self):
        self.assertEqual(QuantityXSpaceName.parse("2x thorax blueprint"), ("thorax blueprint", 2))

    def test_no_x_space_fails(self):
        self.assertRaises(ParserError, QuantityXSpaceName.parse, "ragnarok")

    def test_string_quantity_fails(self):
        self.assertRaises(ParserError, QuantityXSpaceName.parse, "stringx ragnarok")
