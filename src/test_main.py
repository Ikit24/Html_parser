import unittest

from main import extract_title

class Test_Main(unittest.TestCase):
    def test_with_proper_input(self):
        example = "# Hello"
        expected = "Hello"
        self.assertEqual(extract_title(example), expected)

    def test_with_multiline_markdown(self):
        example = """
## Secondary Header
This is a paragraph.
# Main Title
Another paragraph.
"""
        expected = "Main Title"
        self.assertEqual(extract_title(example), expected)

    def test_without_header(self):
        example = "Headerless"
        with self.assertRaises(Exception) as context:
            extract_title(example)
        self.assertEqual(str(context.exception), "Error, no header!")