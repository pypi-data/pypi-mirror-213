from unittest import TestCase

from eveparse.errors import ParserError
from eveparse.parsers.viewcontents import ViewContents


class NameOnlyTestCase(TestCase):
    def test_example_passes(self):
        self.assertEqual(ViewContents.parse("burned logic circuit	salvaged materials	cargo hold	26"), ("burned logic circuit", 26))

    def test_not_3_tabs_fails(self):
        self.assertRaises(ParserError, ViewContents.parse, "burned logic circuit	cargo hold	26")

    def test_string_quantity_fails(self):
        self.assertRaises(ParserError, ViewContents.parse, "burned logic circuit	salvaged materials	26	cargo hold")
