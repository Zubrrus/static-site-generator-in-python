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
    from_path = os.path.join(cwd, "content/index.md")
    template_path = os.path.join(cwd, "template.html")
    dest_path = os.path.join(dst, "index.html")
    generate_page(from_path, template_path, dest_path)

main()
