import unittest
from datetime import datetime

from data_mapping import remove_html_tags, format_time


class MyTestCase(unittest.TestCase):

    def test_format_time(self):
        bad_datetime = format_time("2021-07-20-12;42;43")
        expected_time = datetime(2021, 7, 20, 12, 42, 43)
        self.assertEqual(bad_datetime, expected_time)

    def test_remove_html_tags(self):
        actual_string = remove_html_tags("<p>hello</p>")
        expected_string = "hello"
        self.assertEqual(actual_string, expected_string)


if __name__ == '__main__':
    unittest.main()
