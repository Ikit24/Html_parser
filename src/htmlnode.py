from split_delimiter import *
from enum import Enum

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
                self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url
                )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)

    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})

    elif text_node.text_type == TextType.IMAGE:
        props = {"src": text_node.url}
        if text_node.text:
            props["alt"] = text_node.text
        return LeafNode(tag="img", value=None, props=props)

    else:
        raise ValueError("Wrong format")
    
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for key, value in self.props.items():
            result += " " +  key + "=\"" + value + "\""
        return result

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, value=None, tag=None, props=None):
        super().__init__(tag, value, None, props if props is not None else {})
        self.value = value

    def add_child(self, child):
        raise Exception("LeafNode cannot have children!")

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if self.tag is None:
            return self.value

        props_str = self.props_to_html()
        result = f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
        return result

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props if props is not None else {})
        self.children = children
        self.tag = tag

    def to_html(self):
        if self.tag is None:
            raise ValueError("All leaf nodes must have a tag.")
        if self.children is None:
            raise ValueError("Error, must have children.")
            
        props_str = self.props_to_html()
        if self.props:
            props_str = " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])
            
        tag_str = f"<{self.tag}{props_str}>"
        for child in self.children:
            tag_str += child.to_html()
        tag_str += f"</{self.tag}>"
        return tag_str
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    typed_blocks = block_to_block_type(blocks)

    html_nodes = []

    for block_type, block_content in typed_blocks:
        if block_type == "p":
            paragraph_node = HTMLNode(tag="p", children=text_to_children(block_content))
            html_nodes.append(paragraph_node)

        elif block_type.startswith("h"):
            level = block_type[1]
            heading_node = HTMLNode(tag=f"h{level}", children=text_to_children(block_content))
            html_nodes.append(heading_node)


        elif block_type == "code":
            code_node = HTMLNode(
                tag="pre",
                children=[HTMLNode(tag="code", children=[TextNode(block_content)])]
            )
            html_nodes.append(code_node)

        elif block_type == "blockquote":
            quote_node = HTMLNode(tag="blockquote", children=text_to_children(block_content))
            html_nodes.append(quote_node)

        elif block_type == "ul":
            list_items = block_content.split("\n")
            list_node = HTMLNode(
                tag="ul",
                children=[HTMLNode(tag="li", children=text_to_children(item)) for item in list_items if item.strip()]
            )
            html_nodes.append(list_node)

        elif block_type == "ol":
            list_items = block_content.split("\n")  # Split into individual list items
            list_node = HTMLNode(
                tag="ol",
                children=[HTMLNode(tag="li", children=text_to_children(item)) for item in list_items if item.strip()]
            )
            html_nodes.append(list_node)

    parent_node = HTMLNode(tag="div", children=html_nodes)
    return parent_node

