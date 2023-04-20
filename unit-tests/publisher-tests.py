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


if __name__ == '__main__':
    unittest.main()
