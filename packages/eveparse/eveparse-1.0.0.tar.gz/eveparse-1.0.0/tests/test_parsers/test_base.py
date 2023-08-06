from unittest import TestCase

from eveparse.errors import ParserError
from eveparse.parsers.base import TabbedParser, UnTabbedParser


class TabbedParserTestCase(TestCase):
    def test_tabbed_passes(self):
        self.assertEqual(TabbedParser.parse("ragnarok	1"), None)

    def test_untabbed_fails(self):
        self.assertRaises(ParserError, TabbedParser.parse, "ragnarok")


class UnTabbedParserTestCase(TestCase):
    def test_untabbed_passes(self):
        self.assertEqual(UnTabbedParser.parse("ragnarok"), None)

    def test_tabbed_fails(self):
        self.assertRaises(ParserError, UnTabbedParser.parse, "ragnarok	1")
