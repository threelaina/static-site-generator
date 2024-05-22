import re
from htmlnode import *
from textnode import *

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    lines = markdown.strip().split("\n")
    blocks = []
    block = ""
    for line in lines:
        line = line.strip()
        if line != "":
            block += line + "\n"
        else:
            if block:
                blocks.append(block.strip())
                block = ""
    if block:
        blocks.append(block.strip())
    return blocks


def block_to_block_type(block):
    if re.findall(r"^#{1,6} .*", block):
        return block_type_heading
    if re.findall(r"```((.|\n)*?)```", block):
        return block_type_code
    if re.findall(r"^>(?:.|\n)*?$", block, re.MULTILINE):
        return block_type_quote
    if re.findall(r"^(?:\*|-) (?:.|\n)*?$", block, re.MULTILINE):
        return block_type_unordered_list
    digit_strings = re.findall(r"^(\d+?)\. (?:.|\n)*?$", block, re.MULTILINE)
    if digit_strings:
        digits = [int(x) for x in digit_strings]
        digits_ok = True
        if digits[0] != 1:
            digits_ok = False
        for i in range(1, len(digits)):
            if digits[i - 1] != digits[i] - 1:
                digits_ok = False
        if digits_ok:
            return block_type_ordered_list
    return block_type_paragraph


def paragraph_block_to_htmlnode(block):
    return ParentNode("p", text_to_html_nodes(block))


def heading_block_to_htmlnode(block):
    contents = re.findall(r"^(#{1,6}) (.*)", block)[0]
    heading_level = "h" + str(len(contents[0]))
    return ParentNode(heading_level, text_to_html_nodes(contents[1]))


def code_block_to_htmlnode(block):
    contents = re.findall(r"^```[.|\n]*((?:.|\n)*)```$", block)[0]
    inner_block = LeafNode("code", contents)
    return ParentNode("pre", [inner_block])


def quote_block_to_htmlnode(block):
    contents = re.findall(r"^> (.*)$", block, re.MULTILINE)
    quote_paragraphs = [
        ParentNode("p", text_to_html_nodes(paragraph)) for paragraph in contents
    ]
    return ParentNode("blockquote", quote_paragraphs)


def unordered_list_to_htmlnode(block):
    contents = re.findall(r"^(?:\*|-) ((?:.|\n)*?$)", block, re.MULTILINE)
    list_items = [ParentNode("li", text_to_html_nodes(item)) for item in contents]
    return ParentNode("ul", list_items)


def ordered_list_to_htmlnode(block):
    contents = re.findall(r"^(?:\d+?)\. ((?:.|\n)*?)$", block, re.MULTILINE)
    list_items = [ParentNode("li", text_to_html_nodes(item)) for item in contents]
    return ParentNode("ol", list_items)


def convert_block_by_type(block, block_type):
    if block_type == block_type_heading:
        return heading_block_to_htmlnode(block)
    if block_type == block_type_code:
        return code_block_to_htmlnode(block)
    if block_type == block_type_quote:
        return quote_block_to_htmlnode(block)
    if block_type == block_type_unordered_list:
        return unordered_list_to_htmlnode(block)
    if block_type == block_type_ordered_list:
        return ordered_list_to_htmlnode(block)
    return paragraph_block_to_htmlnode(block)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [
        convert_block_by_type(block, block_to_block_type(block)) for block in blocks
    ]
    return ParentNode("div", children)


def extract_title(markdown):
    title = re.findall(r"^#{1} (.*)", markdown)
    if title:
        return title[0]
    else:
        raise Exception("markdown file must have a single h1 header")
