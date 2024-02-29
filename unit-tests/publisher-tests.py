import unittest
import src.splitter as splitter


class PublisherTests(unittest.TestCase):
    def test_generates_clusters(self):
        """
        With the supplied test cases, it should generate 7 clusters
        :return:
        """
        res = splitter.main(dependency_file="unittest-dependency.json",
                            output="unittest-log\\output.xml",
                            time_group_size=2,
                            random_group_size=1,
                            suites_location="unittest-suites")
        count = 0
        for i in range(len(res)):
            count += 1
        self.assertEqual(count, 7)

    def test_greedy_sort(self):
        nums = {"A": 12, "B": 1, "C": 21, "D": 7, "E": 25, "F": 2, "G": 9, "H": 24, "I": 4, "J": 5}
        name_c = splitter.generate_groups(4)
        time_c = splitter.generate_groups(4)
        splitter.greedy_sort(nums, name_c, time_c)
        sums = [sum(tc) for tc in time_c]
        # print(name_c)
        # print(time_c)
        # print(sums)
        self.assertAlmostEqual(sums[0], sums[1], delta=2)
        self.assertAlmostEqual(sums[0], sums[2], delta=2)
        self.assertAlmostEqual(sums[0], sums[3], delta=2)

        self.assertAlmostEqual(sums[1], sums[2], delta=2)
        self.assertAlmostEqual(sums[1], sums[3], delta=2)

        self.assertAlmostEqual(sums[2], sums[3], delta=2)


if __name__ == '__main__':
    unittest.main()
