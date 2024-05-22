import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_bold, None)
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_image_false(self):
        node = TextNode(
            "This is an image node",
            text_type_image,
            "img.png",
        )
        node2 = TextNode(
            "This is a node",
            text_type_image,
            "img2.png",
        )
        self.assertNotEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_italic)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This text says one thing", text_type_text)
        node2 = TextNode("This text says another", text_type_text)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_code, "example.com")
        self.assertEqual(
            repr(node), 'TextNode("This is a text node", code, "example.com")'
        )

    def test_split_invalid(self):
        node = [TextNode("this is **invalid markdown", text_type_text)]
        self.assertRaises(Exception, split_nodes_delimiter, node, "**", text_type_bold)

    def test_split_bold(self):
        node = [TextNode("This is **text** that should be bold", text_type_text)]
        result = split_nodes_delimiter(node, "**", text_type_bold)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" that should be bold", text_type_text),
        ]
        self.assertEqual(result, expected)

    def test_split_multiple(self):
        node = [
            TextNode(
                "This is text with a `code block` word here and `another code block` here",
                text_type_text,
            )
        ]
        res = split_nodes_delimiter(node, "`", text_type_code)
        output = [
            TextNode("This is text with a ", "text", None),
            TextNode("code block", "code", None),
            TextNode(" word here and ", "text", None),
            TextNode("another code block", "code", None),
            TextNode(" here", "text", None),
        ]
        self.assertEqual(res, output)

    def test_extract_images(self):
        text = "This is text with an ![image](img.png) and ![another](img2.png)"
        result = extract_markdown_images(text)
        expected = [
            (
                "image",
                "img.png",
            ),
            (
                "another",
                "img2.png",
            ),
        ]
        self.assertEqual(result, expected)

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        result = extract_markdown_links(text)
        expected = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](img.png) and another ![second image](img2.png)",
            text_type_text,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "img.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image",
                text_type_image,
                "img2.png",
            ),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://example.com)",
            text_type_text,
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode(
                "link",
                text_type_link,
                "https://example.com",
            ),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](img.png) and a [link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "img.png",
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
