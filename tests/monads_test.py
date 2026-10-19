import unittest
from lib.monads import *

class TestOption(unittest.TestCase):
    """Class for testing lib.monads.Option"""
    def test_create_option(self):
        """Tests option creation with some and nada variants"""
        self.assertEqual(Option(None), nada())
        self.assertEqual(Option.nada(), nada())
        self.assertEqual(Option.nada(), None)
        self.assertEqual(Option(True), some(True))
        self.assertEqual(Option(False), Option.some(False))

    def test_option_stringify(self):
        """Tests string representation for Option"""
        self.assertEqual(str(Option.nada()), "nada")
        self.assertEqual(str(Option.some(1)), "some(1)")

    def test_option_boolean(self):
        """Tests boolean representation for Option"""
        self.assertEqual(bool(Option(True)), True)
        self.assertEqual(bool(Option(False)), True)
        self.assertEqual(bool(Option(None)), False)

    def test_option_is_some(self):
        """Tests if an option with Some variant passes its is_some() function"""
        opt = some(True)
        self.assertEqual(opt.is_some(), True)
        self.assertEqual(opt.is_nada(), False)

    def test_option_is_nada(self):
        """Tests if an option with nada variant passes its is_nada() function"""
        opt = nada()
        self.assertEqual(opt.is_nada(), True)
        self.assertEqual(opt.is_some(), False)


if __name__ == '__main__':
    unittest.main()
