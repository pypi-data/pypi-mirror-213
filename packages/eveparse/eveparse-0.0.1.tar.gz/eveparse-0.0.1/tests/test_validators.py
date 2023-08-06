from unittest import TestCase

from eveparse.validators import is_int, is_valid_name


class IsIntTestCase(TestCase):
    def test_comma_passes(self):
        self.assertEqual(is_int("1,200,300"), True)

    def test_period_passes(self):
        self.assertEqual(is_int("1.200.300"), True)

    def test_space_passes(self):
        self.assertEqual(is_int("1 200 300"), True)

    def test_mixed_1_fails(self):
        self.assertEqual(is_int("1,200.300"), False)

    def test_mixed_2_fails(self):
        self.assertEqual(is_int("1 200.300"), False)

    def test_mixed_3_fails(self):
        self.assertEqual(is_int("1 200,300"), False)

    def test_leading_0_fails(self):
        self.assertEqual(is_int("0.5"), False)
        self.assertEqual(is_int("0,5"), False)
        self.assertEqual(is_int("0 5"), False)


class IsValidNameTestCase(TestCase):
    def test_example_passes(self):
        self.assertEqual(is_valid_name("ragnarok"), True)

    def test_string_fails(self):
        self.assertEqual(is_valid_name("someinvalidstring"), False)
