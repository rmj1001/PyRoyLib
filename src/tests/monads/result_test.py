import unittest

lazy from src.lib.monads.option import Some, Nada
lazy from src.lib.monads.result import Result, Ok, Err, ResultException, ResultVariant


class TestResult(unittest.TestCase):
    """Test suite for lib.monads.Result"""

    def test_init(self):
        """Test Result initialization with Ok and Err variants"""
        res1 = Result(1, ResultVariant.OK)
        res2 = Result("Error", ResultVariant.ERR)

        self.assertEqual(res1, Ok(1))
        self.assertEqual(res2, Err("Error"))

    def test_str(self):
        """Test str(Result)"""
        res1 = Ok(1)
        res2 = Err("Error")

        self.assertEqual(str(res1), "Ok(1)")
        self.assertEqual(str(res2), "Err(Error)")

    def test_bool(self):
        """Test bool(Result)"""
        res1 = Ok(1)
        res2 = Err("Error")

        self.assertEqual(bool(res1), True)
        self.assertEqual(bool(res2), False)

    def test_eq(self):
        """Test equality"""
        res1 = Ok(1)
        res2 = Err("Error")

        self.assertNotEqual(res1, res2)
        self.assertEqual(res1, Result(1, ResultVariant.OK))
        self.assertEqual(res2, Result("Error", ResultVariant.ERR))

    def test_ok(self):
        """Test Result.ok()"""
        res = Ok(1)

        self.assertEqual(res.value, 1)
        self.assertEqual(res.state, ResultVariant.OK)

    def test_err(self):
        """Test Result.err()"""
        res = Err("Error")

        self.assertEqual(res.value, 'Error')
        self.assertEqual(res.state, ResultVariant.ERR)

    def test_is_ok(self):
        """Test Result.is_ok()"""
        res1 = Ok(1)
        res2 = Err("Error")

        self.assertEqual(res1.is_ok(), True)
        self.assertEqual(res2.is_ok(), False)

    def test_is_ok_and(self):
        """Test Result.is_ok_and()"""
        res1 = Ok(1)
        res2 = Err("Error")
        res3 = Ok(2)
        pred = lambda x: x % 2 != 0

        self.assertEqual(res1.is_ok_and(pred), True)
        self.assertEqual(res2.is_ok_and(pred), False)
        self.assertEqual(res3.is_ok_and(pred), False)

    def test_is_err(self):
        """Test Result.is_err()"""
        res1 = Ok(1)
        res2 = Err("Error")

        self.assertEqual(res1.is_err(), False)
        self.assertEqual(res2.is_err(), True)

    def test_is_err_and(self):
        """Test Result.is_err_and()"""
        res1 = Ok(1)
        res2 = Err("Error")
        res3 = Err("Help")
        pred = lambda x: x == "Error"

        self.assertEqual(res1.is_err_and(pred), False)
        self.assertEqual(res2.is_err_and(pred), True)
        self.assertEqual(res3.is_err_and(pred), False)

    def test_flatten(self):
        ok1 = Ok(Ok(Ok(1)))
        ok2 = Ok(1)
        ok3 = Ok(Err(1))
        err = Err(Ok(1))

        self.assertEqual(ok1.flatten(True), Ok(1))
        self.assertEqual(ok2.flatten(True), Ok(1))
        self.assertEqual(ok3.flatten(True), Err(1))
        self.assertEqual(err.flatten(True), Ok(1))

        ok4 = Ok(Ok(Err(5)))

        self.assertEqual(ok4.flatten(False), Ok(Err(5)))

    def test_map(self):
        """Test Result.map()"""
        res1 = Ok(1)
        res2 = Err("Error")
        func = lambda x: x * 3

        self.assertEqual(res1.map(func), Ok(3))
        self.assertEqual(res2.map(func), Err("Error"))

    def test_map_or(self):
        """Test Result.map_or()"""
        res1 = Ok(1)
        res2 = Err("Error")
        success = lambda x: x * 3

        self.assertEqual(res1.map_or(success, 5), 3)
        self.assertEqual(res2.map_or(success, 5), 5)

    def test_map_or_else(self):
        """Test Result.map_or_else()"""
        res1 = Ok(1)
        res2 = Err("Error")
        success = lambda x: x * 3
        failure = lambda x: x + 'Test'

        self.assertEqual(res1.map_or_else(success, failure), 3)
        self.assertEqual(res2.map_or_else(success, failure), 'ErrorTest')

    def test_map_err(self):
        """Test Result.map_err()"""
        res1 = Ok(1)
        res2 = Err("Error")
        func = lambda x: f"Result Error: {x}"

        self.assertEqual(res1.map_err(func), Ok(1))
        self.assertEqual(res2.map_err(func), Err("Result Error: Error"))

    def test_expect(self):
        """Test Result.expect()"""
        res1 = Ok(1)
        res2 = Err("Error")

        self.assertEqual(res1.expect("Default"), 1)

        with self.assertRaises(ResultException) as cm:
            res2.expect("Default")
            self.assertEqual(cm.msg, "Default")

    def test_unwrap(self):
        """Test Result.unwrap()"""
        res1 = Ok(1)
        res2 = Err("Error")

        self.assertEqual(res1.unwrap(), 1)

        with self.assertRaises(ResultException):
            res2.unwrap()

    def test_expect_err(self):
        """Test Result.expect_err()"""
        res1 = Ok(1)
        res2 = Err("Error")

        with self.assertRaises(ResultException) as cm:
            res1.expect_err("Is not an error")
            self.assertEqual(cm.msg, "Is not an error")

        self.assertEqual(res2.expect_err("Is not an error"), "Error")

    def test_unwrap_err(self):
        """Test Result.unwrap_err()"""
        res1 = Ok(1)
        res2 = Err("Error")

        with self.assertRaises(ResultException):
            res1.unwrap_err()

        self.assertEqual(res2.unwrap_err(), "Error")

    def test_into_ok(self):
        """Test Result.into_ok()"""
        res1 = Ok(1)
        res2 = Err(2)

        self.assertEqual(res1.into_ok(), Ok(1))
        self.assertEqual(res2.into_ok(), Ok(2))

    def test_into_err(self):
        """Test Result.into_err()"""
        res1 = Ok(1)
        res2 = Err(2)

        self.assertEqual(res1.into_err(), Err(1))
        self.assertEqual(res2.into_err(), Err(2))

    def test_other_if_ok(self):
        """Test Result.other_if_ok()"""
        res1 = Ok(1)
        res2 = Ok(2)
        res3 = Err("Error")

        self.assertEqual(res1.other_if_ok(res2), res2)
        self.assertEqual(res3.other_if_ok(res2), res3)

    def test_and_then(self):
        """Test Result.and_then()"""
        res1 = Ok(1)
        res2 = Err("Error")
        func = lambda x: Ok(x * 3)

        self.assertEqual(res1.and_then(func), Ok(3))
        self.assertEqual(res2.and_then(func), Err("Error"))

    def test_or_else(self):
        """Test Result.or_else()"""
        res1 = Ok(1)
        res2 = Err("Error")
        func = lambda x: Ok(x * 3)

        self.assertEqual(res1.or_else(func), Ok(1))
        self.assertEqual(res2.or_else(func), Ok('ErrorErrorError'))

    def test_other_if_err(self):
        """Test Result.other_if_err()"""
        res1 = Ok(1)
        res2 = Ok(2)
        res3 = Err("Error")

        self.assertEqual(res1.other_if_err(res2), res1)
        self.assertEqual(res3.other_if_err(res2), res2)

    def test_unwrap_or(self):
        """Test Result.unwrap_or()"""
        res1 = Ok(1)
        res2 = Err("Error")
        default = 5

        self.assertEqual(res1.unwrap_or(default), 1)
        self.assertEqual(res2.unwrap_or(default), 5)

    def test_unwrap_or_else(self):
        """Test Result.unwrap_or_else()"""
        res1 = Ok(1)
        res2 = Err("Error")
        func = lambda x: x * 3

        self.assertEqual(res1.unwrap_or_else(func), 1)
        self.assertEqual(res2.unwrap_or_else(func), 'ErrorErrorError')

    def test_pattern_matching(self):
        """Test pattern matching with Results"""
        r1 = Ok(1)
        r2 = Err("Error")

        match r1:
            case Ok(val):
                self.assertEqual(val, 1)
            case Err(_):
                raise Exception()

        match r2:
            case Ok(_):
                raise Exception()
            case Err(val):
                self.assertEqual(val, "Error")

    def test_into_option(self):
        """Test Result.into_option()"""
        r1 = Ok(1)
        r2 = Err("Error")

        self.assertEqual(r1.ok(), Some(1))
        self.assertEqual(r2.ok(), Nada())
        self.assertEqual(r1.err(), Nada())
        self.assertEqual(r2.err(), Some('Error'))

    def test_inspect(self):
        """Test Result.inspect() and Result.inspect_err()"""
        r1 = Ok(1)
        r2 = Err("Error")

        def printer(value: int):
            print(f'test_inspect: {value}')

        # The value is never updated with inspect() calls
        self.assertEqual(r1.inspect(printer), Ok(1))
        self.assertEqual(r2.inspect(printer), Err("Error"))  # does nothing

        # inspect_err() only calls function on error variants
        self.assertEqual(r2.inspect_err(printer), Err("Error"))


if __name__ == '__main__':
    unittest.main()
