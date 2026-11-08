import unittest

from monads.result import Result, ok, err, ResultException, ResultVariant


class TestResult(unittest.TestCase):
    """Test suite for lib.monads.Result"""

    def test_init(self):
        """Test Result initialization with Ok and Err variants"""
        res1 = Result(1, ResultVariant.OK)
        res2 = Result("Error", ResultVariant.ERR)

        self.assertEqual(res1, ok(1))
        self.assertEqual(res2, err("Error"))

    def test_str(self):
        """Test str(Result)"""
        res1 = ok(1)
        res2 = err("Error")

        self.assertEqual(str(res1), "ok(1)")
        self.assertEqual(str(res2), "err(Error)")

    def test_bool(self):
        """Test bool(Result)"""
        res1 = ok(1)
        res2 = err("Error")

        self.assertEqual(bool(res1), True)
        self.assertEqual(bool(res2), False)

    def test_eq(self):
        """Test equality"""
        res1 = ok(1)
        res2 = err("Error")

        self.assertNotEqual(res1, res2)
        self.assertEqual(res1, ok(1))
        self.assertEqual(res2, err("Error"))

    def test_ok(self):
        """Test Result.ok()"""
        res = Result.ok(1)

        self.assertEqual(res, ok(1))

    def test_err(self):
        """Test Result.err()"""
        res = Result.err("Error")

        self.assertEqual(res, err("Error"))

    def test_is_ok(self):
        """Test Result.is_ok()"""
        res1 = ok(1)
        res2 = err("Error")

        self.assertEqual(res1.is_ok(), True)
        self.assertEqual(res2.is_ok(), False)

    def test_is_ok_and(self):
        """Test Result.is_ok_and()"""
        res1 = ok(1)
        res2 = err("Error")
        res3 = ok(2)
        pred = lambda x: x % 2 != 0

        self.assertEqual(res1.is_ok_and(pred), True)
        self.assertEqual(res2.is_ok_and(pred), False)
        self.assertEqual(res3.is_ok_and(pred), False)

    def test_is_err(self):
        """Test Result.is_err()"""
        res1 = ok(1)
        res2 = err("Error")

        self.assertEqual(res1.is_err(), False)
        self.assertEqual(res2.is_err(), True)

    def test_is_err_and(self):
        """Test Result.is_err_and()"""
        res1 = ok(1)
        res2 = err("Error")
        res3 = err("Help")
        pred = lambda x: x == "Error"

        self.assertEqual(res1.is_err_and(pred), False)
        self.assertEqual(res2.is_err_and(pred), True)
        self.assertEqual(res3.is_err_and(pred), False)

    def test_map(self):
        """Test Result.map()"""
        res1 = ok(1)
        res2 = err("Error")
        func = lambda x: x * 3

        self.assertEqual(res1.map(func), ok(3))
        self.assertEqual(res2.map(func), err("Error"))

    def test_map_or(self):
        """Test Result.map_or()"""
        res1 = ok(1)
        res2 = err("Error")
        func = lambda x: x * 3

        self.assertEqual(res1.map_or(func, 5), ok(3))
        self.assertEqual(res2.map_or(func, 5), ok(5))

    def test_map_or_else(self):
        """Test Result.map_or_else()"""
        res1 = ok(1)
        res2 = err("Error")
        func = lambda x: x * 3

        self.assertEqual(res1.map_or_else(func, func, 5), ok(3))
        self.assertEqual(res2.map_or_else(func, func, 5), ok(15))

    def test_map_err(self):
        """Test Result.map_err()"""
        res1 = ok(1)
        res2 = err("Error")
        func = lambda x: f"Result Error: {x}"

        self.assertEqual(res1.map_err(func), ok(1))
        self.assertEqual(res2.map_err(func), err("Result Error: Error"))

    def test_expect(self):
        """Test Result.expect()"""
        res1 = ok(1)
        res2 = err("Error")

        self.assertEqual(res1.expect("Default"), 1)

        with self.assertRaises(ResultException) as cm:
            res2.expect("Default")
            self.assertEqual(cm.msg, "Default")

    def test_unwrap(self):
        """Test Result.unwrap()"""
        res1 = ok(1)
        res2 = err("Error")

        self.assertEqual(res1.unwrap(), 1)

        with self.assertRaises(ResultException):
            res2.unwrap()

    def test_expect_err(self):
        """Test Result.expect_err()"""
        res1 = ok(1)
        res2 = err("Error")

        with self.assertRaises(ResultException) as cm:
            res1.expect_err("Is not an error")
            self.assertEqual(cm.msg, "Is not an error")

        self.assertEqual(res2.expect_err("Is not an error"), "Error")

    def test_unwrap_err(self):
        """Test Result.unwrap_err()"""
        res1 = ok(1)
        res2 = err("Error")

        with self.assertRaises(ResultException):
            res1.unwrap_err()

        self.assertEqual(res2.unwrap_err(), "Error")

    def test_into_ok(self):
        """Test Result.into_ok()"""
        res1 = ok(1)
        res2 = err(2)

        self.assertEqual(res1.into_ok(), ok(1))
        self.assertEqual(res2.into_ok(), ok(2))

    def test_into_err(self):
        """Test Result.into_err()"""
        res1 = ok(1)
        res2 = err(2)

        self.assertEqual(res1.into_err(), err(1))
        self.assertEqual(res2.into_err(), err(2))

    def test_other_if_ok(self):
        """Test Result.other_if_ok()"""
        res1 = ok(1)
        res2 = ok(2)
        res3 = err("Error")

        self.assertEqual(res1.other_if_ok(res2), res2)
        self.assertEqual(res3.other_if_ok(res2), res3)

    def test_and_then(self):
        """Test Result.and_then()"""
        res1 = ok(1)
        res2 = err("Error")
        func = lambda x: x * 3

        self.assertEqual(res1.and_then(func, 3), ok(9))
        self.assertEqual(res2.and_then(func, 3), err("Error"))

    def test_other_if_err(self):
        """Test Result.other_if_err()"""
        res1 = ok(1)
        res2 = ok(2)
        res3 = err("Error")

        self.assertEqual(res1.other_if_err(res2), res1)
        self.assertEqual(res3.other_if_err(res2), res2)

    def test_or_else(self):
        """Test Result.or_else()"""
        res1 = ok(1)
        res2 = err("Error")
        func = lambda x: x * 3

        self.assertEqual(res1.or_else(func, 3), ok(1))
        self.assertEqual(res2.or_else(func, 3), err(9))

    def test_unwrap_or(self):
        """Test Result.unwrap_or()"""
        res1 = ok(1)
        res2 = err("Error")
        default = 5

        self.assertEqual(res1.unwrap_or(default), 1)
        self.assertEqual(res2.unwrap_or(default), 5)

    def test_unwrap_or_else(self):
        """Test Result.unwrap_or_else()"""
        res1 = ok(1)
        res2 = err("Error")
        func = lambda x: x * 3

        self.assertEqual(res1.unwrap_or_else(func, 3), 1)
        self.assertEqual(res2.unwrap_or_else(func, 3), 9)


if __name__ == '__main__':
    unittest.main()
