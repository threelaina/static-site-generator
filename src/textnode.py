from htmlnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"[^!]?\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if len(n.text) == 0:
            pass
        elif n.text_type is not text_type_text:
            new_nodes.append(n)
        elif len(extract_markdown_images(n.text)) == 0:
            new_nodes.append(n)
        else:
            tup = extract_markdown_images(n.text)[0]
            split_text = n.text.split(f"![{tup[0]}]({tup[1]})", 1)
            if len(split_text[0]) > 0:
                new_nodes.append(TextNode(split_text[0], text_type_text))
            new_nodes.append(TextNode(tup[0], text_type_image, tup[1]))
            new_nodes.extend(
                split_nodes_image([TextNode(split_text[1], text_type_text)])
            )
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if len(n.text) == 0:
            pass
        elif n.text_type is not text_type_text:
            new_nodes.append(n)
        elif len(extract_markdown_links(n.text)) == 0:
            new_nodes.append(n)
        else:
            tup = extract_markdown_links(n.text)[0]
            split_text = n.text.split(f"[{tup[0]}]({tup[1]})", 1)
            if len(split_text[0]) > 0:
                new_nodes.append(TextNode(split_text[0], text_type_text))
            new_nodes.append(TextNode(tup[0], text_type_link, tup[1]))
            new_nodes.extend(
                split_nodes_image([TextNode(split_text[1], text_type_text)])
            )
    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if n.text_type is not text_type_text:
            new_nodes.append(n)
        elif delimiter not in n.text:
            new_nodes.append(n)
        elif n.text.count(delimiter) % 2 != 0:
            raise Exception("invalid Markdown syntax")
        else:
            split_nodes = n.text.split(delimiter, maxsplit=2)
            if split_nodes:
                new_nodes.append(TextNode(split_nodes[0], text_type_text))
                new_nodes.append(TextNode(split_nodes[1], text_type))
                new_nodes.extend(
                    split_nodes_delimiter(
                        [TextNode(split_nodes[2], text_type_text)], delimiter, text_type
                    )
                )
    return new_nodes


def text_to_textnodes(text):
    delimiters = {text_type_bold: "**", text_type_italic: "*", text_type_code: "`"}
    node_list = [TextNode(text, text_type_text)]

    for text_type, delim in delimiters.items():
        node_list = split_nodes_delimiter(node_list, delim, text_type)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list


class TextNode:
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        if self.url is not None:
            return f'TextNode("{self.text}", {self.text_type}, "{self.url}")'
        return f'TextNode("{self.text}", {self.text_type}, {self.url})'


def text_node_to_html_node(text_node):
    if text_node.text_type not in [
        text_type_text,
        text_type_bold,
        text_type_italic,
        text_type_code,
        text_type_link,
        text_type_image,
    ]:
        raise Exception("invalid text type")
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def text_to_html_nodes(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
