import unittest
from lib.monads import *


class TestOption(unittest.TestCase):
    """Class for testing lib.monads.Option"""

    def test_init(self):
        """Tests option creation with some and nada variants"""
        opt = Option(None)
        opt2 = Option(1)

        self.assertIsInstance(opt, Option)
        self.assertIsInstance(opt2, Option)

    def test_eq(self):
        opt = Option(None)
        opt2 = Option(1)

        # Test nada variants
        self.assertEqual(opt, opt.nada())
        self.assertEqual(opt, nada())
        self.assertEqual(opt, None)

        # Test some variants
        self.assertEqual(opt2, opt.some(1))
        self.assertEqual(opt2, some(1))

    def test_str(self):
        """Tests str(Option)"""
        self.assertEqual(str(Option.nada()), "nada")
        self.assertEqual(str(Option.some(1)), "some(1)")

    def test_bool(self):
        """Tests bool(Option)"""
        self.assertEqual(bool(Option(True)), True)
        self.assertEqual(bool(Option(False)), True)
        self.assertEqual(bool(Option(None)), False)

    def test_is_some(self):
        """Tests Option.is_some()"""
        opt = some(True)
        self.assertEqual(opt.is_some(), True)
        self.assertEqual(opt.is_nada(), False)

    def test_is_nada(self):
        """Tests Option.is_nada()"""
        opt = nada()
        self.assertEqual(opt.is_nada(), True)
        self.assertEqual(opt.is_some(), False)

    def test_is_some_and(self):
        """Tests Option.is_some_and()"""
        opt = some(1)
        self.assertEqual(opt.is_some_and(lambda x: x == 1), True)
        self.assertEqual(opt.is_some_and(lambda x: x == 2), False)

    def test_is_nada_or(self):
        """Tests Option.is_nada_or()"""
        opt = nada()
        opt2 = some(1)

        self.assertEqual(opt.is_nada_or(lambda x: x == 1), True)
        self.assertEqual(opt.is_nada_or(lambda x: x == 1), True)
        self.assertEqual(opt2.is_nada_or(lambda x: x == 2), False)

    def test_expect(self):
        """Tests Option.expect()"""
        opt = some(1)
        opt2 = nada()
        message = "Test"

        # Should not raise exception
        self.assertEqual(opt.expect(message), 1)

        # Check to make sure custom message is contained in exception
        with self.assertRaises(OptionException) as cm:
            opt2.expect(message)
            self.assertEqual(cm.msg, message)

    def test_unwrap(self):
        """Tests Option.unwrap()"""
        opt = some(1)
        opt2 = nada()

        # Should not raise exception
        self.assertEqual(opt.unwrap(), 1)

        with self.assertRaises(OptionException) as cm:
            opt2.unwrap()

    def test_unwrap_or(self):
        """Tests Option.unwrap_or()"""
        opt = some(1)
        opt2 = nada()
        default = 3

        self.assertEqual(opt.unwrap_or(default), 1)
        self.assertEqual(opt2.unwrap_or(default), 3)

    def test_unwrap_or_else(self):
        """Tests Option.unwrap_or_else()"""
        opt = some(1)
        opt2 = nada()

        def double(x: int) -> int:
            return x * 2

        self.assertEqual(opt.unwrap_or_else(double, 3), 1)
        self.assertEqual(opt2.unwrap_or_else(double, 3), 6)

    def test_map(self):
        pass


if __name__ == '__main__':
    unittest.main()
