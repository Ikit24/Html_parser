from htmlnode import TextNode, TextType, HTMLNode
import re

from enum import Enum

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE) 
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)   
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result_nodes.append(old_node)
            continue
        
        text = old_node.text
        start = 0
        
        while start < len(text):
            delimiter_start = text.find(delimiter, start)
            
            if delimiter_start == -1:
                if start < len(text):
                    result_nodes.append(TextNode(text[start:], TextType.TEXT))
                break
            
            if delimiter_start > start:
                result_nodes.append(TextNode(text[start:delimiter_start], TextType.TEXT))
            
            delimiter_end = text.find(delimiter, delimiter_start + len(delimiter))
            if delimiter_end == -1:
                raise ValueError(f"Unmatched delimiter {delimiter}")
            
            content = text[delimiter_start + len(delimiter):delimiter_end]
            
            if delimiter == "**" and "_italic_" in content:
                parts = content.split("_italic_")
                if len(parts) == 2:
                    result_nodes.append(TextNode(parts[0], TextType.BOLD))
                    result_nodes.append(TextNode("italic", TextType.ITALIC))
                    if parts[1]:
                        result_nodes.append(TextNode(parts[1], TextType.BOLD))
                else:
                    result_nodes.append(TextNode(content, text_type))
            else:
                result_nodes.append(TextNode(content, text_type))
            
            start = delimiter_end + len(delimiter)
    
    return result_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    result_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        images = extract_markdown_images(remaining_text)
        
        if not images:
            result_nodes.append(old_node)
            continue

        for alt, url in images:
            parts = remaining_text.split(f"![{alt}]({url})", 1)
            
            if parts[0]:
                result_nodes.append(TextNode(parts[0], TextType.TEXT))

            result_nodes.append(TextNode(alt, TextType.IMAGE, url))

            remaining_text = parts[1]
            
        if remaining_text:
            result_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return result_nodes

def split_nodes_link(old_nodes):
    result_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result_nodes.append(old_node)
            continue

        remaining_text = old_node.text

        links = extract_markdown_links(remaining_text)

        if not links:
            result_nodes.append(old_node)
            continue

        for title, url in links:
            parts = remaining_text.split(f"[{title}]({url})", 1)

            if parts[0]:
                result_nodes.append(TextNode(parts[0], TextType.TEXT))

            result_nodes.append(TextNode(title, TextType.LINK, url))

            remaining_text = parts[1]

        if remaining_text:
            result_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return result_nodes

def markdown_to_blocks(markdown):
    blocks = [block for block in markdown.split("\n\n") if block.strip()]

    print(f"Validated Blocks: {blocks}")
    print(f"Markdown content being split: {markdown}")

    block_ls = []
    for block in blocks:
        print(f"Processing block: {block}, Type: {type(block)}")

        if not isinstance(block, str):
            raise TypeError(f"Expected block to be a string, got {type(block)}")
        
        typed_block = block_to_block_type(block)
        cleaned_block = block.strip()

        if cleaned_block:
            block_ls.append(cleaned_block)

    return block_ls

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_text):
    if not isinstance(markdown_text, str):
        raise TypeError(f"Expected markdown_text to be a string, got {type(markdown_text)}")
    if re.match(r"^#{1,6} ", markdown_text):
        return BlockType.HEADING
    if markdown_text.startswith("```") and markdown_text.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in markdown_text.splitlines()):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in markdown_text.splitlines()):
        return BlockType.UNORDERED_LIST
    lines = markdown_text.splitlines()
    for index, line in enumerate(lines, start=1):
        if not line.startswith(f"{index}. "):
            break
    else:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def parse_inline_markdown(text):
    pattern = r"(\*\*(.*?)\*\*|_(.*?)_|`(.*?)`)"

    matches = list(re.finditer(pattern, text))
    parts = []
    last_index = 0

    for match in matches:
        if match.start() > last_index:
            parts.append({"type": "text", "content": text[last_index:match.start()]})
        
        # Handle specific markdown types
        if match.group(1):  # Bold (**text**)
            parts.append({"type": "bold", "content": match.group(2)})
        elif match.group(3):  # Italic (_text_)
            parts.append({"type": "italic", "content": match.group(3)})
        elif match.group(4):  # Inline code (`text`)
            parts.append({"type": "code", "content": match.group(4)})

        # Update the last index to the end of the current match
        last_index = match.end()

    # Add any remaining text after the last match
    if last_index < len(text):
        parts.append({"type": "text", "content": text[last_index:]})

    return parts

def text_to_children(text):
    children = []

    parts = parse_inline_markdown(text)

    for part in parts:
        if part["type"] == "text":
            children.append(TextNode(part["content"]))
        elif part["type"] == "bold":
            children.append(HTMLNode(tag="b", children=[TextNode(part["content"])]))
        elif part["type"] == "italic":
            children.append(HTMLNode(tag="i", children=[TextNode(part["content"])]))

    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    print(f"Blocks passed to block_to_block_type: {blocks}")

    typed_blocks = [(block_to_block_type(block), block) for block in blocks]

    if not all(isinstance(block, str) for block in blocks):
        raise ValueError(f"Non-string block detected: {blocks}")
    print(f"Blocks: {blocks}")
    print(f"Typed Blocks: {typed_blocks}")

    html_nodes = []

    for block_type, block_content in typed_blocks:
        print(f"Current Block Type: {block_type}, Content: {block_content}")
        supported_types = {"p", "h1", "h2", "h3", "code", "blockquote", "ul", "ol"}
        if block_type not in supported_types:
            print(f"Unexpected block type: {block_type}")
            continue

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