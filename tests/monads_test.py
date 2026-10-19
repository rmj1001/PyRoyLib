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
        """Tests equality for variants"""
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
        """Test Option.map()"""
        opt = some(1)
        opt2 = nada()

        add_one = lambda x: x + 1

        self.assertEqual(opt.map(add_one), some(2))
        self.assertEqual(opt2.map(add_one), nada())

    def test_flatten(self):
        """Test Option.flatten()"""
        opt = some(1)
        opt2 = nada()
        opt3 = some(some(some(4)))
        opt4 = some(some(some(nada())))

        self.assertEqual(opt.flatten(), some(1))
        self.assertEqual(opt2.flatten(), nada())
        self.assertEqual(opt3.flatten(), some(4))
        self.assertEqual(opt4.flatten(), nada())

    def test_flatmap(self):
        """Test Option.flatmap()"""
        opt = some(1)
        opt2 = nada()
        opt3 = some(some(some(4)))
        opt4 = some(some(some(nada())))

        add_one = lambda x: x + 1

        self.assertEqual(opt.flatmap(add_one), some(2))
        self.assertEqual(opt2.flatmap(add_one), nada())
        self.assertEqual(opt3.flatmap(add_one), some(5))
        self.assertEqual(opt4.flatmap(add_one), nada())

    def test_ok_or(self):
        """Test Option.ok_or()"""
        opt = some(1)
        opt2 = nada()
        error = "Error"

        self.assertEqual(opt.ok_or(error), ok(1))
        self.assertEqual(opt2.ok_or(error), err(error))

    def test_ok_or_else(self):
        """Test Option.ok_or_else()"""
        opt = some(1)
        opt2 = nada()
        error_func = lambda: str("Error")

        self.assertEqual(opt.ok_or_else(error_func), ok(1))
        self.assertEqual(opt2.ok_or_else(error_func), err(error_func()))
        self.assertEqual(opt2.ok_or_else(print, "Hello world"), err(print, "Hello world"))

    def test_filter(self):
        """Test Option.filter()"""
        opt = some(1)
        opt2 = some(2)
        opt3 = nada()

        is_even = lambda x: x % 2 == 0

        self.assertEqual(opt.filter(is_even), nada())
        self.assertEqual(opt2.filter(is_even), some(2))
        self.assertEqual(opt3.filter(is_even), nada())

    def test_other_if_some(self):
        """Test Option.other_if_some()"""
        opt1 = some(1)
        opt1_other = some(2)
        opt2 = nada()
        opt2_other = some(3)

        self.assertEqual(opt1.other_if_some(opt1_other), opt1_other)
        self.assertEqual(opt2.other_if_some(opt2_other), opt2)

    def test_other_if_nada(self):
        """Test Option.other_if_nada()"""
        opt1 = some(1)
        opt1_other = some(2)
        opt2 = nada()
        opt2_other = some(3)

        self.assertEqual(opt1.other_if_nada(opt1_other), opt1)
        self.assertEqual(opt2.other_if_nada(opt2_other), opt2_other)

    def test_or_else(self):
        """Test Option.or_else()"""
        opt1 = some(1)
        opt2 = nada()
        func = lambda x: x*3

        self.assertEqual(opt1.or_else(func), some(1))
        self.assertEqual(opt2.or_else(func, 1), some(3))

    def test_take(self):
        """Test Option.take()"""
        opt = some(1)
        opt2 = nada()

        self.assertEqual(opt.take(), 1)
        self.assertEqual(opt, nada())
        self.assertEqual(opt2, nada())

    def test_replace(self):
        """Test Option.replace()"""
        opt = some(1)

        opt.replace(3)

        self.assertEqual(opt, some(3))

    def test_zip(self):
        """Test Option.zip()"""
        opt = some(1)
        opt2 = some(2)
        opt3 = nada()

        self.assertEqual(opt.zip(opt2), some((1, 2)))
        self.assertEqual(opt.zip(opt3), nada())
        self.assertEqual(opt3.zip(opt3), nada())

    def test_unzip(self):
        """Test Option.unzip()"""
        tup = some((1, 2))
        opt1 = some(1)
        opt2 = some(2)

        self.assertEqual(tup.unzip(), (opt1, opt2))


class TestResult(unittest.TestCase):
    def test_init(self):
        pass

    def test_str(self):
        pass

    def test_bool(self):
        pass

    def test_eq(self):
        pass

    def test_ok(self):
        pass

    def test_err(self):
        pass

    def test_is_ok(self):
        pass

    def test_is_ok_and(self):
        pass

    def test_is_err(self):
        pass

    def test_is_err_and(self):
        pass

    def test_map(self):
        pass

    def test_map_or(self):
        pass

    def test_map_or_else(self):
        pass

    def test_map_err(self):
        pass

    def test_expect(self):
        pass

    def test_unwrap(self):
        pass

    def test_expect_err(self):
        pass

    def test_unwrap_err(self):
        pass

    def test_into_ok(self):
        pass

    def test_into_err(self):
        pass

    def test_other_if_ok(self):
        pass

    def test_and_then(self):
        pass

    def test_other_if_err(self):
        pass

    def test_or_else(self):
        pass

    def test_unwrap_or(self):
        pass

    def test_unwrap_or_else(self):
        pass

if __name__ == '__main__':
    unittest.main()
