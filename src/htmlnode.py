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