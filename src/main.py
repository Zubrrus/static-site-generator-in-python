import os
import shutil
from converter import *


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


main()
