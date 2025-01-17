import os
import shutil
from converter import extract_title, to_html


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    fid = open(from_path)
    try:
        markdown = fid.read()
    except Exception as e:
        print(e)
    fid.close()
    fid = open(template_path)
    try:
        template = fid.read()
    except Exception as e:
        print(e)
    fid.close()
    try:
        content = to_html(markdown)
    except Exception as e:
        print(e)
    try:
        title = extract_title(markdown)
    except Exception as e:
        print(e)
    template = template.replace("""{{ Title }}""", title)
    template = template.replace("""{{ Content }}""", content)
    fid = open(dest_path, mode='w')
    try:
        fid.write(template)
    except Exception as e:
        print(e)
    fid.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)
    for item in items:
        from_path = os.path.join(dir_path_content, item)
        if os.path.isfile(from_path):
            dest_path = os.path.join(dest_dir_path, "index.html")
            generate_page(from_path, template_path, dest_path)
        else:
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            os.mkdir(new_dest_dir_path)
            generate_pages_recursive(from_path, template_path, new_dest_dir_path)
            

def my_copy(src, dst):
    items = os.listdir(src)
    for item in items:
        item_fullpath = os.path.join(src, item)
        if os.path.isfile(item_fullpath):
            shutil.copy(item_fullpath, dst)
        else:
            new_item_fullpath = os.path.join(dst, item)
            os.mkdir(new_item_fullpath) 
            my_copy(item_fullpath, new_item_fullpath)

def main():
    pub = "public"
    stat = "static"
    cwd = os.getcwd()
    dst = os.path.join(cwd, pub)
    src = os.path.join(cwd, stat)
    dirs = os.listdir(cwd)
    if stat not in dirs:
        raise Exception("static directory not found")
    if pub in dirs:
        shutil.rmtree(dst)
    os.mkdir(dst)
    my_copy(src, dst)
    dir_path_content = os.path.join(cwd, "content")
    template_path = os.path.join(cwd, "template.html")
    dest_dir_path = dst
    # generate_page(from_path, template_path, dest_path)
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)


main()
