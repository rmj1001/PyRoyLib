import unittest
from src.lib.monads.functor import Functor, FunctorException

class TestFunctors(unittest.TestCase):
    def test_init(self):
        ft = Functor(None)

        self.assertEqual(ft.value, None)

    def test_eq(self):
        ft1 = Functor(None)
        ft2 = Functor(None)
        ft3 = Functor(3)

        self.assertEqual(ft1, ft2)
        self.assertNotEqual(ft1, ft3)

    def test_map(self):
        ft = Functor(1)
        ft2 = Functor(None)

        ft.map(lambda x: x + 1)
        ft2.map(lambda x: x + 1)

        self.assertEqual(ft.value, 2)
        self.assertEqual(ft2.value, None)

    def test_flatten(self):
        ft = Functor(1)
        ft2 = Functor(Functor(Functor(3)))

        ft.flatten()
        ft2.flatten()

        self.assertEqual(ft.value, 1)
        self.assertEqual(ft2.value, 3)

    def test_flatmap(self):
        ft = Functor(1)
        ft2 = Functor(Functor(Functor(3)))

        ft.flatmap(lambda x: x + 1)
        ft2.flatmap(lambda x: x + 1)

        self.assertEqual(ft.value, 2)
        self.assertEqual(ft2.value, 4)


if __name__ == '__main__':
    unittest.main()
