import unittest

from split_delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

    def test_extract_markdown_images_mixed(self):
        text = "A ![image](img.jpg) and a [link](url) together"
        expected = [("image", "img.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)
   
    def test_extract_markdown_images_edge_cases(self):
        text = "Empty ![](img.jpg) and ![alt text]() and ![]() and ![]()"
        expected = [
                ("", "img.jpg"),
                ("alt text", ""),
                ("", ""),
                ("", "")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links(self):
        text = "Multiple [link1](url1) and [link2](url2)"
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_edge_cases(self):
        text = "Empty [](url) and [text]() and ![]() and []()"
        expected = [
                ("", "url"),
                ("text", ""),
                ("", "")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_split_nodes_image(self):
        node = TextNode("This is a text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        nodes = [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                ]
        self.assertEqual(split_nodes_image([node]), nodes)

    def test_split_nodes_image_empty(self):
        node = TextNode("This is a text without an image", TextType.TEXT)
        nodes = [TextNode("This is a text without an image", TextType.TEXT)]
        self.assertEqual(split_nodes_image([node]), nodes)

    def test_split_nodes_double_images(self):
        node = TextNode(
                "This is the first pic's text ![rick roll](https://i.imgur.com/aKaOqIh.gif) and here comes the second ![brick stroller](https://i.imgur.com/bJbLwOj.gif)", TextType.TEXT,
                )
        nodes = [
                TextNode("This is the first pic's text ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and here comes the second ", TextType.TEXT),
                TextNode("brick stroller", TextType.IMAGE, "https://i.imgur.com/bJbLwOj.gif"),
                ]
        self.assertEqual(split_nodes_image([node]), nodes)
                    

    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        nodes = [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                ]
        self.assertEqual(split_nodes_link([node]), nodes)

    def test_split_nodes_link_empty(self):
        node = TextNode("This is a text without a link", TextType.TEXT)
        nodes = [TextNode("This is a text without a link", TextType.TEXT)]
        self.assertEqual(split_nodes_link([node]), nodes)

    def test_split_nodes_double_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        nodes = [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                    ),
        ]
        self.assertEqual(split_nodes_link([node]), nodes)


if __name__ == "__main__":
    unittest.main(verbose=2)

