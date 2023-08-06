from unittest import TestCase

from eveparse.parsers.nameonly import NameOnly


class NameOnlyTestCase(TestCase):
    def test_example_passes(self):
        self.assertEqual(NameOnly.parse("ragnarok"), ("ragnarok", 1))

    def test_spaced_name_passes(self):
        self.assertEqual(NameOnly.parse("siege module ii"), ("siege module ii", 1))
