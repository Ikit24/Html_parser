import unittest

from split_delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TextSplitDelimiter(unittest.TestCase):
    def test_split_node_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
                nodes,
                [
                    TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )
    def test_split_node_delimiter_bold(self):
        node = TextNode("Hello **world** example", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
                nodes,
                [
                    TextNode("Hello ", TextType.TEXT),
                    TextNode("world", TextType.BOLD),
                    TextNode(" example", TextType.TEXT),
                ]
            )
    
    def test_split_node_delimiter_invalid(self):
        node = TextNode("Hello `world example", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_node_delimiter_preserve_non_text(self):
        node = TextNode("Already bold", TextType.BOLD)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
                nodes,
                [TextNode("Already bold", TextType.BOLD)]
        )

    def test_split_node_delimiter_empty(self):
        node = TextNode("Hello ``world", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
                nodes,
                [            
                    TextNode("Hello ", TextType.TEXT),
                    TextNode("", TextType.CODE),
                    TextNode("world", TextType.TEXT)]
            )

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), expected)

if __name__ == "__main__":
    unittest.main()

