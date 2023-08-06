from unittest import TestCase

from eveparse.errors import ParserError
from eveparse.parsers.shipfitname import ShipFitName


class QuantityXSpaceNameTestCase(TestCase):
    def test_example_passes(self):
        self.assertEqual(ShipFitName.parse("[ragnarok, bob's ragnarok]"), ("ragnarok", 1))

    def test_comma_in_name_passes(self):
        self.assertEqual(ShipFitName.parse("[ragnarok, one, two, ragnarok]"), ("ragnarok", 1))

    def test_no_open_bracket_fails(self):
        self.assertRaises(ParserError, ShipFitName.parse, "ragnarok, bob's ragnarok]")

    def test_no_close_bracket_fails(self):
        self.assertRaises(ParserError, ShipFitName.parse, "[ragnarok, bob's ragnarok")

    def test_no_comma_fails(self):
        self.assertRaises(ParserError, ShipFitName.parse, "[ragnarok bob's ragnarok")
