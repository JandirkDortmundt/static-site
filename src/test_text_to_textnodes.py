import unittest
from textnode import TextNode, TextType
from node_utils import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "This is plain text."
        expected = [
            TextNode("This is plain text.", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic_text(self):
        text = "This is *italic* text."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_code_block(self):
        text = "This is `code`."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image(self):
        text = "This is an ![image](https://example.com/image.png)."
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGES, "https://example.com/image.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link(self):
        text = "This is a [link](https://example.com)."
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINKS, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_combined_markdown(self):
        text = "This is **bold**, *italic*, `code`, an ![image](https://example.com/image.png), and a [link](https://example.com)."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", an ", TextType.TEXT),
            TextNode("image", TextType.IMAGES, "https://example.com/image.png"),
            TextNode(", and a ", TextType.TEXT),
            TextNode("link", TextType.LINKS, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)
# didn't bother to include this in the code. SO ONLY NON NESTED MARKDOWN TEXT IS VALID!!!
    # def test_nested_markdown(self):
    #     text = "[**bold link**](https://example.com)"
    #     expected = [
    #         TextNode("bold link", TextType.LINKS, "https://example.com"),
    #     ]
    #     self.assertEqual(text_to_textnodes(text), expected)
    #
    def test_unmatched_delimiters(self):
        text = "This is **bold with no ending"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_no_markdown(self):
        text = "Just some plain text with no markdown."
        expected = [
            TextNode("Just some plain text with no markdown.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_edge_case_empty_string(self):
        text = ""
        expected = []
        self.assertEqual(text_to_textnodes(text), expected)

    def test_images_and_links_combined(self):
        text = "![image1](https://example.com/image1.png) and [link1](https://example.com)."
        expected = [
            TextNode("image1", TextType.IMAGES, "https://example.com/image1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link1", TextType.LINKS, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

if __name__ == "__main__":
    unittest.main()
