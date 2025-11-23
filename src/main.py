import os
import sys

from functions import copy_tree, generate_pages_recursive

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print(basepath)
    root = os.path.expanduser("~/Projects/Training/boot.dev/static_site/")
    def map_to_root(items):
        return [os.path.join(root, f) for f in items]
    # copy static content to public
    source, content, template, destination = map_to_root(["static", "content", "template.html", "docs"])
    copy_tree(source, destination)
    # generate pages from content/
    generate_pages_recursive(content, template, destination, basepath)

main()
