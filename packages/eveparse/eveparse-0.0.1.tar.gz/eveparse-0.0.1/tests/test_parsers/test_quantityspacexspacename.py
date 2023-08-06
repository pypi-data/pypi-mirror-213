from unittest import TestCase

from eveparse.errors import ParserError
from eveparse.parsers.quantityspacexspacename import QuantitySpaceXSpaceName


class QuantitySpaceXSpaceNameTestCase(TestCase):
    def test_example_passes(self):
        self.assertEqual(QuantitySpaceXSpaceName.parse("3 x ragnarok"), ("ragnarok", 3))

    def test_no_space_x_space_fails(self):
        self.assertRaises(ParserError, QuantitySpaceXSpaceName.parse, "ragnarok")

    def test_string_quantity_fails(self):
        self.assertRaises(ParserError, QuantitySpaceXSpaceName.parse, "string x ragnarok")
