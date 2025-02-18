from textnode import TextNode, TextType

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

