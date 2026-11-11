import unittest

from src.lib.abstract.box import Box, BoxException


class TestBox(unittest.TestCase):
    def test_take(self):
        box: Box[int] = Box(1)

        self.assertEqual(box.take(), 1)

        with self.assertRaises(BoxException):
            box.take()

    def test_replace(self):
        box: Box[int] = Box(1)

        box.replace(2)
        self.assertEqual(box.take(), 2)

    def test_peek(self):
        box: Box[int] = Box(1)

        self.assertEqual(box.peek(), 1)
        self.assertEqual(box.peek(), 1)

    def test_str(self):
        self.assertEqual(str(Box(1)), 'Box(1)')

    def test_bool(self):
        self.assertTrue(Box(True))
        self.assertFalse(Box(None))
        self.assertFalse(Box(False))

    def test_and(self):
        # and
        self.assertTrue(Box(True) and Box(True))
        self.assertFalse(Box(False) and Box(True))

    def test_or(self):
        self.assertTrue(Box(True) or Box(True))
        self.assertTrue(Box(True) or Box(False))
        self.assertFalse(Box(False) or Box(False))

    def test_xor(self):
        pass

    def test_contains(self):
        # __contains__()
        self.assertTrue(1 in Box(1))
        self.assertTrue(1 in Box([1, 2, 3]))
        self.assertFalse(2 in Box(1))

    def test_comparisons(self):
        # >, >=, <, <=
        self.assertGreater(Box(3), Box(0))
        self.assertLess(Box(0), Box(3))
        self.assertGreaterEqual(Box(3), Box(3))
        self.assertLessEqual(Box(0), Box(0))

        # !=
        self.assertNotEqual(Box(3), Box(2))

    def test_len(self):
        # len()
        self.assertEqual(len(Box([1, 2, 3])), 3)

    def test_math(self):
        # +
        self.assertEqual(Box(1) + Box(1), Box(2))
        # -
        self.assertEqual(Box(10) - Box(5), Box(5))
        # *
        self.assertEqual(Box(2) * Box(5), Box(10))
        # /
        self.assertEqual(Box(3) / Box(2), Box(1.5))
        # //
        self.assertEqual(Box(3) // Box(2), Box(1))

    def test_mod(self):
        # modulus
        self.assertEqual(Box(2) % Box(1), Box(0))
        self.assertEqual(Box(10) % Box(3), Box(1))

    def test_iter(self):
        box: Box[int] = Box(1)
        box_list: Box[list[int]] = Box([1, 2, 3])

        list_1: list[int] = []
        list_2: list[int] = []

        with self.assertRaises(BoxException):
            for element in box:
                list_1.append(element)

        for element in box_list:
            list_2.append(element)

        self.assertEqual(list_1, [])
        self.assertEqual(list_2, [1, 2, 3])
