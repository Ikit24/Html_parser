import os
import shutil

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

def main():
    source_dir = os.path.join(os.getcwd(), "static")
    dest_dir = os.path.join(os.getcwd(), "public")

    copy_static(source_dir, dest_dir)
    
if __name__ == "__main__":
    main()
