from unittest import TestCase

from eveparse.errors import ParserError
from eveparse.parsers.nametabquantity import NameTabQuantity


class NameOnlyTestCase(TestCase):
    def test_example_passes(self):
        self.assertEqual(NameTabQuantity.parse("ragnarok	2"), ("ragnarok", 2))

    def test_no_tab_fails(self):
        self.assertRaises(ParserError, NameTabQuantity.parse, "ragnarok")

    def test_string_quantity_fails(self):
        self.assertRaises(ParserError, NameTabQuantity.parse, "ragnarok	string")
