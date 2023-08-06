from unittest import TestCase

from eveparse.errors import ParserError
from eveparse.parsers.contract import Contract


class NameOnlyTestCase(TestCase):
    def test_example_passes(self):
        self.assertEqual(Contract.parse("capital transverse bulkhead i	1	rig armor	module	rig slot"), ("capital transverse bulkhead i", 1))

    def test_not_4_tabs_fails(self):
        self.assertRaises(ParserError, Contract.parse, "capital transverse bulkhead i	1")

    def test_string_quantity_fails(self):
        self.assertRaises(ParserError, Contract.parse, "capital transverse bulkhead i	string	rig armor	module	rig slot")
