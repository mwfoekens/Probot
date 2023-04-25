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
                            time_cluster_size=2,
                            random_cluster_size=1,
                            suites_location="unittest-suites")
        count = 0
        for i in range(len(res)):
            count += 1
        self.assertEqual(count, 7)

    def test_clear_empty_lists(self):
        """
        From the list passed as an argument, it should only have 3 clusters left
        :return:
        """
        clusters = splitter.remove_empty_clusters([["test 1"], [], ['test 2'], [], [], ['test 3'], [], []])
        self.assertEqual(len(clusters), 3)

    # def test_greedy_sort(self):
    #     nums = {"A": 12, "B": 1, "C": 21, "D": 7, "E": 65, "F": 2, "G": 9, "H": 54, "I": 4}
    #     name_c = splitter.generate_clusters(4)
    #     time_c = splitter.generate_clusters(4)
    #     splitter.greedy_sort(nums, name_c, time_c)
    #     print(name_c)
    #     print(time_c)


if __name__ == '__main__':
    unittest.main()
