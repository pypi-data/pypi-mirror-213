from unittest import TestCase

from eveparse.errors import ParserError
from eveparse.parsers.contractnodetails import ContractNoDetails


class NameOnlyTestCase(TestCase):
    def test_example_passes(self):
        self.assertEqual(ContractNoDetails.parse("cybernetic subprocessor - basic	1	cyber learning	implant"), ("cybernetic subprocessor - basic", 1))

    def test_not_3_tabs_fails(self):
        self.assertRaises(ParserError, ContractNoDetails.parse, "cybernetic subprocessor - basic	1")

    def test_string_quantity_fails(self):
        self.assertRaises(ParserError, ContractNoDetails.parse, "cybernetic subprocessor - basic	string	cyber learning	implant")

