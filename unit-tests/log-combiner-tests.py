import unittest
import src.logcombiner.log_combiner as lc

longest_runtime_name, longest_runtime = lc.get_longest_running_cluster("unittest-log")


class LogCombinerTests(unittest.TestCase):
    def test_start_and_end_time(self):
        """
        Test if time gets subtracted properly
        :return:
        """
        start, end = lc.get_start_and_end_times(10.5)
        start = start.split(":")[-1]
        end = end.split(":")[-1]
        self.assertAlmostEqual(float(end) - float(start), 10.5, delta=.001)

    def test_longest_runtime(self):
        self.assertTrue(longest_runtime == 213.324924)

    def test_longest_runtime_name(self):
        self.assertTrue(longest_runtime_name == "1")


if __name__ == '__main__':
    unittest.main()
