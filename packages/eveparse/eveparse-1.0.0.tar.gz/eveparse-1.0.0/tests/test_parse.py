from unittest import TestCase

from eveparse import parse
from eveparse.errors import ParserError


class ParseTestCase(TestCase):
    def test_invalid_name_fails(self):
        self.assertRaises(ParserError, parse, "string")

    def test_nameonly(self):
        self.assertEqual(parse("Ragnarok"), (23773, "Ragnarok", 1))

    def test_contract(self):
        self.assertEqual(parse("Capital Transverse Bulkhead I	1	Rig Armor	Module	Rig Slot"), (33902, "Capital Transverse Bulkhead I", 1))

    def test_contractnodetails(self):
        self.assertEqual(parse("Cybernetic Subprocessor - Basic	1	Cyber Learning	Implant	"), (9943, "Cybernetic Subprocessor - Basic", 1))

    def test_namespacequantity(self):
        self.assertEqual(parse("Ragnarok 2"), (23773, "Ragnarok", 2))
        self.assertEqual(parse("Ragnarok* 2"), (23773, "Ragnarok", 2))

    def test_namespacexquantity(self):
        self.assertEqual(parse("Ragnarok x2"), (23773, "Ragnarok", 2))

    def test_nametabquantity(self):
        self.assertEqual(parse("Ragnarok	2"), (23773, "Ragnarok", 2))
        self.assertEqual(parse("Ragnarok*	2"), (23773, "Ragnarok", 2))

    def test_quantityspacename(self):
        self.assertEqual(parse("2 Ragnarok"), (23773, "Ragnarok", 2))

    def test_quantityspacexspacename(self):
        self.assertEqual(parse("4 x Ragnarok"), (23773, "Ragnarok", 4))

    def test_quantityxspacename(self):
        self.assertEqual(parse("3x Ragnarok"), (23773, "Ragnarok", 3))

    def test_shipfitname(self):
        self.assertEqual(parse("[Ragnarok, Bob's Ragnarok]"), (23773, "Ragnarok", 1))

    def test_viewcontents(self):
        self.assertEqual(parse("Burned Logic Circuit	Salvaged Materials	Cargo Hold	26"), (25600, "Burned Logic Circuit", 26))
