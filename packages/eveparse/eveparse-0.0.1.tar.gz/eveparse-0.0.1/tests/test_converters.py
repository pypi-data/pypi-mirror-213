from unittest import TestCase

from eveparse.converters import normalize_string, to_int


class NormalizeStringTestCase(TestCase):
    def test_leading_removed(self):
        self.assertEqual(normalize_string(" Ragnarok"), "ragnarok")
        self.assertEqual(normalize_string("	Ragnarok"), "ragnarok")

    def test_trailing_removed(self):
        self.assertEqual(normalize_string("Ragnarok "), "ragnarok")
        self.assertEqual(normalize_string("Ragnarok	"), "ragnarok")


class ToIntTestCase(TestCase):
    def test_comma_passes(self):
        self.assertEqual(to_int("1,200,300"), 1200300)

    def test_period_passes(self):
        self.assertEqual(to_int("1.200.300"), 1200300)

    def test_space_passes(self):
        self.assertEqual(to_int("1 200 300"), 1200300)
