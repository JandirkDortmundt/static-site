
# tests/test_node_utils.py
import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from node_utils import text_node_to_html_node

class TestNodeUtils(unittest.TestCase):
    def test_normal_text(self):
        text_node = TextNode("Normal text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "Normal text")

    def test_bold_text(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_links(self):
        text_node = TextNode("Click me", TextType.LINKS, url="https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Click me</a>')

    def test_images(self):
        text_node = TextNode("", TextType.IMAGES, url="https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/image.png" alt=""></img>')

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node("Not a TextNode")

if __name__ == "__main__":
    unittest.main()
