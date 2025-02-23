from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result_nodes.append(old_node)
        else:
            delimiter_count = old_node.text.count(delimiter)
            if delimiter_count % 2 != 0:
                raise ValueError("Invalid markdown: delimiters must be matched pairs")
            parts = old_node.text.split(delimiter)
            for i in range(len(parts)):
                if i % 2 == 0:
                    result_nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    result_nodes.append(TextNode(parts[i], text_type))
    return result_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    result_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        
        if not images:
            result_nodes.append(old_node)
            continue

        for alt, url in images:
            parts = old_node.text.split(f"![{alt}]({url})", 1)
            
            if parts[0]:
                result_nodes.append(TextNode(parts[0], TextType.TEXT))

            result_nodes.append(TextNode(alt, TextType.IMAGE, url))

            if parts[1]:
                result_nodes.append(TextNode(parts[1], TextType.TEXT))
    
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
