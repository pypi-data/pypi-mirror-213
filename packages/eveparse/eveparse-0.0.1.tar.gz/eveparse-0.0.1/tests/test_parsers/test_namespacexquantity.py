from unittest import TestCase

from eveparse.errors import ParserError
from eveparse.parsers.namespacexquantity import NameSpaceXQuantity


class NameOnlyTestCase(TestCase):
    def test_example_passes(self):
        self.assertEqual(NameSpaceXQuantity.parse("ragnarok x2"), ("ragnarok", 2))

    def test_no_space_fails(self):
        self.assertRaises(ParserError, NameSpaceXQuantity.parse, "ragnarok")

    def test_string_quantity_fails(self):
        self.assertRaises(ParserError, NameSpaceXQuantity.parse, "ragnarok xstring")
