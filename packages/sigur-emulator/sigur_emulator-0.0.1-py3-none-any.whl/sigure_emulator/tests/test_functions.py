from sigure_emulator import functions
import unittest


class FunctionsTest(unittest.TestCase):

    def test_get_point_dict(self):
        response = functions.create_points_dict(4)
        self.assertTrue(len(response) == 4)


if __name__ == "__main__":
    unittest.main()