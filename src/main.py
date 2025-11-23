import os

from functions import copy_tree, generate_page

def main():
    root = os.path.expanduser("~/Projects/Training/boot.dev/static_site/")
    tmp = ["static", "public", "content/index.md", "template.html", "public/index.html"]
    source, destination, content, template, page = [os.path.join(root, f) for f in tmp]
    copy_tree(source, destination)
    generate_page(content, template, page)

main()
