from textnode import TextNode, TextType
import re

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

