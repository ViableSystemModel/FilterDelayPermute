import unittest
import timeit

import fdp_original
import fdp_optimized
from numpy import array_equal

class TestCorrectOutput (unittest.TestCase):

    GIVEN_SECRET = b'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    @classmethod
    def setUpClass (cls):
        state, echoes = fdp_original.encode(cls.GIVEN_SECRET)
        cls.expected_state = state
        cls.expected_echoes = echoes

    def perform_test (self, encode):
        state, echoes = encode(self.GIVEN_SECRET)
        self.assertEqual(state, self.expected_state)
        self.assertTrue(array_equal(echoes, self.expected_echoes))

    def test_optimized (self):
        self.perform_test(fdp_optimized.encode)


class TimeAlgorithms (unittest.TestCase):

    def time (self, name):
        REPETITIONS = 100
        setup = f'from {name} import encode; import secrets'
        statement = 'encode(secrets.token_bytes(40))'
        seconds = timeit.timeit(statement, setup=setup, number=REPETITIONS)
        seconds /= REPETITIONS
        millisecs = seconds * 1000
        print(f'{name} time: {REPETITIONS} loops, average {millisecs:.2f} msec')

    def test_time_original (self):
        self.time('fdp_original')

    def test_time_optimized (self):
        self.time('fdp_optimized')

if __name__ == '__main__':
    print("Running FilterDelayPermute tests (should take less than 10 seconds)")
    print("Currently, this file:")
    print('\t', "* tests the correctness of fdp_optimized.encode")
    print('\t', "* times both the original encoding and the optimized one")
    print()
    unittest.main()
