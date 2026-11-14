import unittest

lazy from src.lib.monads.maybe import Maybe, Some, Nada, MaybeException, maybeify
lazy from src.lib.monads.result import Ok, Err


class TestMaybe(unittest.TestCase):
    """Class for testing lib.monads.Maybe"""

    def test_init(self):
        """Tests option creation with some and Nada variants"""
        opt = Nada()
        opt2 = Some(1)

        self.assertIsInstance(opt, Maybe)
        self.assertIsInstance(opt2, Maybe)

    def test_eq(self):
        """Tests equality for variants"""
        opt = Nada()
        opt2 = Some(1)

        # Test Nada variants
        self.assertEqual(opt, Nada())
        self.assertEqual(opt, Nada())

        # Test some variants
        self.assertEqual(opt2, Some(1))
        self.assertEqual(opt2, Some(1))

        # Other
        self.assertNotEqual(opt, opt2)
        self.assertNotEqual(opt2, Some(2))
        self.assertNotEqual(opt2, 1)

    def test_repr(self):
        """Tests str(Maybe)"""
        self.assertEqual(repr(Nada()), "Nada")
        self.assertEqual(repr(Some(1)), "Some(1)")

    def test_bool(self):
        """Tests bool(Maybe)"""
        self.assertEqual(bool(Some(True)), True)
        self.assertEqual(bool(Some(False)), True)
        self.assertEqual(bool(Nada()), False)

    def test_is_some(self):
        """Tests Maybe.is_some()"""
        opt = Some(True)
        self.assertEqual(opt.is_some(), True)
        self.assertEqual(opt.is_nada(), False)

    def test_is_nada(self):
        """Tests Maybe.is_nada()"""
        opt = Nada()
        self.assertEqual(opt.is_nada(), True)
        self.assertEqual(opt.is_some(), False)

    def test_is_some_and(self):
        """Tests Maybe.is_some_and()"""
        opt = Some(1)
        self.assertEqual(opt.is_some_and(lambda x: x == 1), True)
        self.assertEqual(opt.is_some_and(lambda x: x == 2), False)
        self.assertEqual(Nada().is_some_and(lambda x: x == 1), False)

    def test_is_nada_or(self):
        """Tests Maybe.is_nada_or()"""
        opt = Nada()
        opt2 = Some(1)

        self.assertEqual(opt.is_nada_or(lambda x: x == 1), True)
        self.assertEqual(opt.is_nada_or(lambda x: x == 1), True)
        self.assertEqual(opt2.is_nada_or(lambda x: x == 2), False)

    def test_expect(self):
        """Tests Maybe.expect()"""
        opt = Some(1)
        opt2 = Nada()
        message = "Test"

        # Should not raise exception
        self.assertEqual(opt.expect(message), 1)

        # Check to make sure custom message is contained in exception
        with self.assertRaises(MaybeException) as cm:
            opt2.expect(message)

        self.assertEqual(str(cm.exception), message)

    def test_unwrap(self):
        """Tests Maybe.unwrap()"""
        opt = Some(1)
        opt2 = Nada()

        # Should not raise exception
        self.assertEqual(opt.unwrap(), 1)

        with self.assertRaises(MaybeException):
            opt2.unwrap()

    def test_unwrap_or(self):
        """Tests Maybe.unwrap_or()"""
        opt = Some(1)
        opt2 = Nada()
        default = 3

        self.assertEqual(opt.unwrap_or(default), 1)
        self.assertEqual(opt2.unwrap_or(default), 3)

    def test_unwrap_or_else(self):
        """Tests Maybe.unwrap_or_else()"""
        opt = Some(1)
        opt2 = Nada()

        def twenty() -> int: return 10 * 2

        self.assertEqual(opt.unwrap_or_else(twenty), 1)
        self.assertEqual(opt2.unwrap_or_else(twenty), 20)

    def test_map(self):
        """Test Maybe.map()"""
        opt = Some(1)
        opt2 = Nada()

        add_one = lambda x: x + 1

        self.assertEqual(opt.map(add_one), Some(2))
        self.assertEqual(opt2.map(add_one), Nada())

    def test_flatten(self):
        """Test Maybe.flatten()"""
        opt = Some(1)
        opt2 = Nada()
        opt3 = Some(Some(Some(4)))

        self.assertEqual(opt.flatten(recursive=True), Some(1))
        self.assertEqual(opt2.flatten(recursive=True), Nada())
        self.assertEqual(opt3.flatten(recursive=True), Some(4))
        self.assertEqual(opt3.flatten(recursive=False), Some(Some(4)))

    def test_and_then(self):
        """Test Maybe.and_then()"""
        opt = Some(1)
        opt2 = Nada()
        opt3 = Some(Some(Some(4)))

        def add_one(x: int) -> Maybe[int]:
            return Some(x + 1)

        def fail_if_even(x: int) -> Maybe[int]:
            return Nada() if x % 2 == 0 else Some(x)

        # Success Chains
        self.assertEqual(opt.and_then(add_one), Some(2))
        self.assertEqual(opt2.and_then(add_one), Nada())
        self.assertEqual(opt3.flatten(recursive=True).and_then(add_one), Some(5))

        # Failure Chain: Some -> Nada
        self.assertEqual(Some(2).and_then(fail_if_even), Nada())

    def test_ok_or(self):
        """Test Maybe.ok_or()"""
        opt = Some(1)
        opt2 = Nada()
        error = "Error"

        self.assertEqual(opt.ok_or(error), Ok(1))
        self.assertEqual(opt2.ok_or(error), Err(error))

    def test_or_else(self):
        """Test Maybe.or_else()"""
        opt1 = Some(1)
        opt2 = Nada()

        def func() -> Maybe[int]: return Some(3)

        def fail_func() -> Maybe[int]: return Nada()

        self.assertEqual(opt1.or_else(func), Some(1))
        self.assertEqual(opt2.or_else(func), Some(3))

        # Recovery fails: Nada -> Nada
        self.assertEqual(opt2.or_else(fail_func), Nada())

    def test_filter(self):
        """Test Maybe.filter()"""
        opt = Some(1)
        opt2 = Some(2)
        opt3 = Nada()

        is_even = lambda x: x % 2 == 0

        self.assertEqual(opt.filter(is_even), Nada())
        self.assertEqual(opt2.filter(is_even), opt2)
        self.assertEqual(opt3.filter(is_even), Nada())

    def test_other_if_some(self):
        """Test Maybe.other_if_some()"""
        opt1 = Some(1)
        opt1_other = Some(2)
        opt2 = Nada()
        opt2_other = Some(3)

        self.assertEqual(opt1.other_if_some(opt1_other), opt1_other)
        self.assertEqual(opt2.other_if_some(opt2_other), opt2)

    def test_other_if_nada(self):
        """Test Maybe.other_if_nada()"""
        opt1 = Some(1)
        opt1_other = Some(2)
        opt2 = Nada()
        opt2_other = Some(3)

        self.assertEqual(opt1.other_if_nada(opt1_other), opt1)
        self.assertEqual(opt2.other_if_nada(opt2_other), opt2_other)

    def test_zip(self):
        """Test Maybe.zip()"""
        opt = Some(1)
        opt2 = Some(2)
        opt3 = Nada()

        self.assertEqual(opt.zip(opt2), Some((1, 2)))
        self.assertEqual(opt.zip(opt3), Nada())
        self.assertEqual(opt3.zip(opt3), Nada())
        self.assertEqual(opt3.zip(opt), Nada())

    def test_unzip(self):
        """Test Maybe.unzip()"""
        tup = Some((1, 2))
        opt1 = Some(1)
        opt2 = Some(2)

        self.assertEqual(tup.unzip(), (opt1, opt2))
        self.assertEqual(Nada().unzip(), (Nada(), Nada()))

    def test_match(self):
        """Test pattern matching"""
        opt1: Maybe[int] = Some(1)
        opt2: Maybe[int] = Nada()

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

    def test_some_init(self):
        """Test Some(None) raises a panic"""
        with self.assertRaises(MaybeException):
            opt1: Some = Some(None)

    def test_inspect(self):
        """Test Maybe.inspect()"""
        state: dict[str, bool] = {
            'some': False,
            'nada': False
        }

        def change_some(_): state['some'] = True
        def change_nada(_): state['nada'] = True

        opt1 = Some(1).inspect(change_some)
        opt2 = Nada().inspect(change_nada)

        self.assertTrue(state['some'])
        self.assertFalse(state['nada'])
        self.assertEqual(opt1, Some(1))
        self.assertEqual(opt2, Nada())

    def test_map_or(self):
        """Test Maybe.map_or()"""

        def add_one(x) -> int: return x + 1

        self.assertEqual(Some(1).map_or(5, add_one), 2)
        self.assertEqual(Nada().map_or(5, add_one), 5)

    def test_map_or_else(self):
        """Test Maybe.map_or_else()"""

        def add_one(x) -> int: return x + 1
        def default() -> int: return 20

        self.assertEqual(
            Some(1).map_or_else(default, add_one),
            2
        )

        self.assertEqual(
            Nada().map_or_else(default, add_one),
            20
        )

    def test_reduce(self):
        """Test Maybe.reduce()"""
        opt1 = Some(10)
        opt2 = Some(20)
        opt3 = Nada()
        def add(x: int, y: int) -> int: return x + y

        self.assertEqual(opt1.reduce(opt2, add), Some(30))
        self.assertEqual(opt1.reduce(opt3, add), Some(10))
        self.assertEqual(opt3.reduce(opt3, add), Nada())
        self.assertEqual(opt3.reduce(opt2, add), Some(20))

    def test_ok_or_else(self):
        """Test Maybe.ok_or_else()"""
        self.assertEqual(
            Some(10).ok_or_else(lambda: 'Custom Error'), Ok(10)
        )

        self.assertEqual(
            Nada().ok_or_else(lambda: 'Custom Error'), Err('Custom Error')
        )

    def test_xor(self):
        """Test Maybe.xor()"""

        self.assertEqual(
            Some(10).xor(Nada()), Some(10)
        )

        self.assertEqual(
            Nada().xor(Some(10)), Some(10)
        )

        self.assertEqual(
            Some(10).xor(Some(10)), Nada()
        )

        self.assertEqual(
            Nada().xor(Nada()), Nada()
        )

    def test_maybeify(self):
        """Test @maybeify decorator"""

        @maybeify
        def returner(mode: int):
            if mode == 0:
                return None
            elif mode == 1:
                raise Exception
            else:
                return 2

        self.assertEqual(
            returner(0), Nada()
        )

        self.assertEqual(
            returner(1), Nada()
        )

        self.assertEqual(
            returner(2), Some(2)
        )

if __name__ == '__main__':
    unittest.main()
