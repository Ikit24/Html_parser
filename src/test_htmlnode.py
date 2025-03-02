import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_None(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLNode(
                props={"href": "https://google.com", "target": "_blank"}
        )
        expected = ' href="https://google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_add_child(self):
        node = LeafNode("some value", "p")
        with self.assertRaises(Exception):
            node.add_child()

class TestLeafNode(unittest.TestCase):
    def test_leafnode_to_html_value_isNone(self):
        node = LeafNode(None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leafnode_to_html_tag_isNone(self):
        node = LeafNode("generic value", None)
        expected = "generic value"
        self.assertEqual(node.to_html(), expected)

    def test_leafnode_to_html_with_attrs(self):
        node = LeafNode("Click me!", "a", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

class TestParentNode(unittest.TestCase):
    def test_to_html_tag_is_None(self):
        node = ParentNode(None, "child")
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "All leaf nodes must have a tag.")

    def test_to_html_children_is_None(self):
        node = ParentNode("a", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Error, must have children.")
        
    def test_nested_parent_nodes(self):
        child_node = ParentNode("div", [LeafNode("hello", "span")])
        parent_node = ParentNode("p", [child_node])
        expected = "<p><div><span>hello</span></div></p>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_multiple_children(self):
        node = ParentNode("div", [
            LeafNode("first", "p"),
            LeafNode("second", "p"),
            LeafNode("third", "p")
        ])
        expected = "<div><p>first</p><p>second</p><p>third</p></div>"
        self.assertEqual(node.to_html(), expected)

    def test_empty_children_list(self):
        node = ParentNode("div", [])
        expected = "<div></div>"
        self.assertEqual(node.to_html(), expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)
