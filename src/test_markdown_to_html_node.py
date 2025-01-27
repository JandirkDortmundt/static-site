import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode
from node_utils import markdown_to_html_node, text_node_to_html_node, text_to_textnodes
from textnode import TextNode, TextType

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        markdown = "This is a paragraph"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("p", [LeafNode("This is a paragraph")])
        ])
        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(len(result.children), len(expected.children))
        self.assertEqual(result.children[0].tag, expected.children[0].tag)
        self.assertEqual(result.children[0].children[0].value, expected.children[0].children[0].value)

    def test_heading(self):
        markdown = "## Heading 2"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("h2", [LeafNode("Heading 2")])
        ])
        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.children[0].tag, expected.children[0].tag)
        self.assertEqual(result.children[0].children[0].value, expected.children[0].children[0].value)

    def test_code_block(self):
        markdown = "```\nprint('hello')\n```"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("pre", [
                ParentNode("code", [LeafNode("print('hello')")])
            ])
        ])
        self.assertEqual(result.tag, expected.tag)
        self.assertEqual(result.children[0].tag, expected.children[0].tag)
        self.assertEqual(result.children[0].children[0].tag, expected.children[0].children[0].tag)
        self.assertEqual(result.children[0].children[0].children[0].value, expected.children[0].children[0].children[0].value)

if __name__ == '__main__':
    unittest.main()

# import unittest
# from htmlnode import HTMLNode, ParentNode, LeafNode
# from node_utils import markdown_to_html_node, text_node_to_html_node, text_to_textnodes
# from textnode import TextNode, TextType
#
# class TestMarkdownToHTMLNode(unittest.TestCase):
#     def test_paragraph(self):
#         markdown = "This is a paragraph"
#         result = markdown_to_html_node(markdown)
#         expected = ParentNode("div", [
#             ParentNode("p", [LeafNode("This is a paragraph")])
#         ])
#         self.assertEqual(result, expected)
#
#     def test_heading(self):
#         markdown = "## Heading 2"
#         result = markdown_to_html_node(markdown)
#         expected = ParentNode("div", [
#             ParentNode("h2", [LeafNode("Heading 2")])
#         ])
#         self.assertEqual(result, expected)
#
#     def test_quote(self):
#         markdown = "> This is a quote"
#         result = markdown_to_html_node(markdown)
#         expected = ParentNode("div", [
#             ParentNode("blockquote", [LeafNode("This is a quote")])
#         ])
#         self.assertEqual(result, expected)
#
#     def test_code_block(self):
#         markdown = "```\nprint('hello')\n```"
#         result = markdown_to_html_node(markdown)
#         expected = ParentNode("div", [
#             ParentNode("pre", [
#                 ParentNode("code", [LeafNode("print('hello')")])
#             ])
#         ])
#         self.assertEqual(result, expected)
#
#     def test_unordered_list(self):
#         markdown = "* First item\n* Second item"
#         result = markdown_to_html_node(markdown)
#         expected = ParentNode("div", [
#             ParentNode("ul", [
#                 ParentNode("li", [LeafNode("First item")]),
#                 ParentNode("li", [LeafNode("Second item")])
#             ])
#         ])
#         self.assertEqual(result, expected)
#
#     def test_ordered_list(self):
#         markdown = "1. First item\n2. Second item"
#         result = markdown_to_html_node(markdown)
#         expected = ParentNode("div", [
#             ParentNode("ol", [
#                 ParentNode("li", [LeafNode("First item")]),
#                 ParentNode("li", [LeafNode("Second item")])
#             ])
#         ])
#         self.assertEqual(result, expected)
#
#     def test_mixed_markdown(self):
#         markdown = "# Title\n\nThis is a paragraph\n\n* List item 1\n* List item 2"
#         result = markdown_to_html_node(markdown)
#         expected = ParentNode("div", [
#             ParentNode("h1", [LeafNode("Title")]),
#             ParentNode("p", [LeafNode("This is a paragraph")]),
#             ParentNode("ul", [
#                 ParentNode("li", [LeafNode("List item 1")]),
#                 ParentNode("li", [LeafNode("List item 2")])
#             ])
#         ])
#         self.assertEqual(result, expected)
#
# if __name__ == '__main__':
#     unittest.main()
