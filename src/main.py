import os
import shutil
from textnode import *
from htmlnode import *
from markdown import *


def print_files(rel_path):
    dir = os.path.join(os.curdir, rel_path)
    if os.path.exists(dir):
        if len(os.listdir(dir)) > 0:
            print(os.listdir(dir))
        else:
            print("no files in directory")
    else:
        print("path not found")


def copy_dir(path, new_path):
    if os.path.exists(path):
        files = [[os.path.join(path, file), file] for file in os.listdir(path)]
        for file in files:
            path = file[0]
            name = file[1]
            if os.path.isfile(path):
                shutil.copy(path, new_path)
            else:
                new_dir = os.path.join(new_path, name)
                os.mkdir(new_dir)
                copy_dir(path, new_dir)


def copy_static_dir():
    public_path = os.path.join(os.curdir, "public")
    static_path = os.path.join(os.curdir, "static")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)
    copy_dir(static_path, public_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as md_file:
        markdown = md_file.read()
    title = extract_title(markdown)

    with open(template_path) as template:
        template = template.read()

    html_nodes = markdown_to_html_node(markdown)
    html_str = html_nodes.to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_str)

    with open(dest_path, "w") as new_file:
        new_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_path = os.path.join(os.curdir, dir_path_content)
    dest_path = os.path.join(os.curdir, dest_dir_path)

    if os.path.exists(content_path):
        files = [
            [os.path.join(content_path, file), file]
            for file in os.listdir(content_path)
        ]
        for file in files:
            path = file[0]
            name = file[1]
            dest = os.path.join(dest_path, name.replace("md", "html"))
            if os.path.isfile(path):
                # convert to html
                generate_page(path, template_path, dest)
            else:
                # it's a directory
                new_dest_dir = os.path.join(dest_path, name)
                os.mkdir(new_dest_dir)
                generate_pages_recursive(path, template_path, new_dest_dir)


def main():
    copy_static_dir()
    from_path = "content"
    template = os.path.join(os.curdir, "template.html")
    dest_path = "public"
    generate_pages_recursive(from_path, template, dest_path)


main()
