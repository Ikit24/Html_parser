import os
import markdown
from markdown_blocks import markdown_to_html_node
from inline_markdown import *


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def textnodes_to_html(textnodes):
    html_content = ""
    for node in textnodes:
        if node.text_type == TextType.TEXT:
            html_content += node.text
        elif node.text_type == TextType.BOLD:
            html_content += f"<b>{node.text}</b>"
        elif node.text_type == TextType.ITALIC:
            html_content += f"<i>{node.text}</i>"
        elif node.text_type == TextType.CODE:
            html_content += f"<code>{node.text}</code>"
        elif node.text_type == TextType.IMAGE:
            html_content += f'<img src="{node.attributes}" alt="{node.text}">'
        elif node.text_type == TextType.LINK:
            html_content += f'<a href="{node.attributes}">{node.text}</a>'
    return html_content

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for filename in files:
            if filename.endswith(".md"):
                # Get the source markdown file path
                source_path = os.path.join(root, filename)
                
                # Calculate the destination HTML file path
                # Preserve directory structure relative to content_dir
                rel_path = os.path.relpath(root, dir_path_content)
                if rel_path == ".":  # If file is directly in content directory
                    dest_path = os.path.join(dest_dir_path, filename.replace(".md", ".html"))
                else:
                    # Preserves subdirectory structure
                    dest_path = os.path.join(dest_dir_path, rel_path, filename.replace(".md", ".html"))
                
                # Generate the page using your existing function
                generate_page(source_path, template_path, dest_path)