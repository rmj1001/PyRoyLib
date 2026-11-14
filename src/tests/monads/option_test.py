import unittest

from monads.exceptions.option_exception import OptionException
from monads.option import Option, Some, Nada
from monads.result import ok, err


class TestOption(unittest.TestCase):
    """Class for testing lib.monads.Option"""

    def test_init(self):
        """Tests option creation with some and Nada variants"""
        opt = Option(None)
        opt2 = Option(1)

        self.assertIsInstance(opt, Option)
        self.assertIsInstance(opt2, Option)

    def test_eq(self):
        """Tests equality for variants"""
        opt = Option(None)
        opt2 = Option(1)

        # Test Nada variants
        self.assertEqual(opt, Nada())
        self.assertEqual(opt, Nada())

        # Test some variants
        self.assertEqual(opt2, Some(1))
        self.assertEqual(opt2, Some(1))

    def test_str(self):
        """Tests str(Option)"""
        self.assertEqual(str(Nada()), "Nada")
        self.assertEqual(str(Some(1)), "Some(1)")

    def test_bool(self):
        """Tests bool(Option)"""
        self.assertEqual(bool(Option(True)), True)
        self.assertEqual(bool(Option(False)), True)
        self.assertEqual(bool(Option(None)), False)

    def test_is_some(self):
        """Tests Option.is_some()"""
        opt = Some(True)
        self.assertEqual(opt.is_some(), True)
        self.assertEqual(opt.is_nada(), False)

    def test_is_nada(self):
        """Tests Option.is_nada()"""
        opt = Nada()
        self.assertEqual(opt.is_nada(), True)
        self.assertEqual(opt.is_some(), False)

    def test_is_some_and(self):
        """Tests Option.is_some_and()"""
        opt = Some(1)
        self.assertEqual(opt.is_some_and(lambda x: x == 1), True)
        self.assertEqual(opt.is_some_and(lambda x: x == 2), False)

    def test_is_nada_or(self):
        """Tests Option.is_nada_or()"""
        opt = Nada()
        opt2 = Some(1)

        self.assertEqual(opt.is_nada_or(lambda x: x == 1), True)
        self.assertEqual(opt.is_nada_or(lambda x: x == 1), True)
        self.assertEqual(opt2.is_nada_or(lambda x: x == 2), False)

    def test_expect(self):
        """Tests Option.expect()"""
        opt = Some(1)
        opt2 = Nada()
        message = "Test"

        # Should not raise exception
        self.assertEqual(opt.expect(message), 1)

        # Check to make sure custom message is contained in exception
        with self.assertRaises(OptionException) as cm:
            opt2.expect(message)
            self.assertEqual(cm.msg, message)

    def test_unwrap(self):
        """Tests Option.unwrap()"""
        opt = Some(1)
        opt2 = Nada()

        # Should not raise exception
        self.assertEqual(opt.unwrap(), 1)

        with self.assertRaises(OptionException):
            opt2.unwrap()

    def test_unwrap_or(self):
        """Tests Option.unwrap_or()"""
        opt = Some(1)
        opt2 = Nada()
        default = 3

        self.assertEqual(opt.unwrap_or(default), 1)
        self.assertEqual(opt2.unwrap_or(default), 3)

    def test_unwrap_or_else(self):
        """Tests Option.unwrap_or_else()"""
        opt = Some(1)
        opt2 = Nada()

        def double(x: int) -> int:
            return x * 2

        self.assertEqual(opt.unwrap_or_else(double, 3), 1)
        self.assertEqual(opt2.unwrap_or_else(double, 3), 6)

    def test_map(self):
        """Test Option.map()"""
        opt = Some(1)
        opt2 = Nada()

        add_one = lambda x: x + 1

        self.assertEqual(opt.map(add_one), Some(2))
        self.assertEqual(opt2.map(add_one), Nada())

    def test_flatten(self):
        """Test Option.flatten()"""
        opt = Some(1)
        opt2 = Nada()
        opt3 = Some(Some(Some(4)))

        self.assertEqual(opt.flatten(), Some(1))
        self.assertEqual(opt2.flatten(), Nada())
        self.assertEqual(opt3.flatten(), Some(4))

    def test_flatmap(self):
        """Test Option.flatmap()"""
        opt = Some(1)
        opt2 = Nada()
        opt3 = Some(Some(Some(4)))

        add_one = lambda x: x + 1

        self.assertEqual(opt.flatmap(add_one), Some(2))
        self.assertEqual(opt2.flatmap(add_one), Nada())
        self.assertEqual(opt3.flatmap(add_one), Some(5))

    def test_ok_or(self):
        """Test Option.ok_or()"""
        opt = Some(1)
        opt2 = Nada()
        error = "Error"

        self.assertEqual(opt.ok_or(error), ok(1))
        self.assertEqual(opt2.ok_or(error), err(error))

    def test_ok_or_else(self):
        """Test Option.ok_or_else()"""
        opt = Some(1)
        opt2 = Nada()
        error_func = lambda: str("Error")

        self.assertEqual(opt.ok_or_else(error_func), ok(1))
        self.assertEqual(opt2.ok_or_else(error_func), err(error_func()))
        self.assertEqual(opt2.ok_or_else(print, "Hello world"), err(print, "Hello world"))

    def test_filter(self):
        """Test Option.filter()"""
        opt = Some(1)
        opt2 = Some(2)
        opt3 = Nada()

        is_even = lambda x: x % 2 == 0

        self.assertEqual(opt.filter(is_even), Nada())
        self.assertEqual(opt2.filter(is_even), Some(2))
        self.assertEqual(opt3.filter(is_even), Nada())

    def test_other_if_some(self):
        """Test Option.other_if_some()"""
        opt1 = Some(1)
        opt1_other = Some(2)
        opt2 = Nada()
        opt2_other = Some(3)

        self.assertEqual(opt1.other_if_some(opt1_other), opt1_other)
        self.assertEqual(opt2.other_if_some(opt2_other), opt2)

    def test_other_if_nada(self):
        """Test Option.other_if_nada()"""
        opt1 = Some(1)
        opt1_other = Some(2)
        opt2 = Nada()
        opt2_other = Some(3)

        self.assertEqual(opt1.other_if_nada(opt1_other), opt1)
        self.assertEqual(opt2.other_if_nada(opt2_other), opt2_other)

    def test_or_else(self):
        """Test Option.or_else()"""
        opt1 = Some(1)
        opt2 = Nada()
        func = lambda x: x * 3

        self.assertEqual(opt1.or_else(func), Some(1))
        self.assertEqual(opt2.or_else(func, 1), Some(3))

    def test_zip(self):
        """Test Option.zip()"""
        opt = Some(1)
        opt2 = Some(2)
        opt3 = Nada()

        self.assertEqual(opt.zip(opt2), Some((1, 2)))
        self.assertEqual(opt.zip(opt3), Nada())
        self.assertEqual(opt3.zip(opt3), Nada())

    def test_unzip(self):
        """Test Option.unzip()"""
        tup = Some((1, 2))
        opt1 = Some(1)
        opt2 = Some(2)

        self.assertEqual(tup.unzip(), (opt1, opt2))

    def test_match(self):
        """Test pattern matching"""
        opt1: Option[int] = Some(1)
        opt2: Option[int] = Nada()

        match opt1:
            case Some(val):
                self.assertEqual(val, 1)
            case Nada():
                raise Exception()

        match opt2:
            case Some(_):
                raise Exception()
            case Nada():
                pass
