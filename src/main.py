import os
import shutil
from split_delimiter import markdown_to_html_node

def copy_static(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.mkdir(dest_dir)

    items = os.listdir(source_dir)

    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            print(f"Copying file : {source_path} to {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            copy_static(source_path, dest_path)

def extract_title(markdown):
    markdown = markdown.splitlines()
    for mark in markdown:
        if mark.startswith("# ") == True:
            extracted_markdown = mark.lstrip("#").strip()
            return extracted_markdown
    else:
        raise Exception("Error, no header!")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as file:
        markdown_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()
    
    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    
    title = extract_title(markdown_content)

    final_content = template_content.replace("{{Title}}", title)
    final_content = final_content.replace("{{Content}}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(final_content)

def main():
    source_dir = os.path.join(os.getcwd(), "static")
    dest_dir = os.path.join(os.getcwd(), "public")

    copy_static(source_dir, dest_dir)

    from_path = "content/index.md"
    template_path = "template.html"
    dest_path = "public/index.html"
    
    generate_page(from_path, template_path, dest_path)
    
if __name__ == "__main__":
    main()
