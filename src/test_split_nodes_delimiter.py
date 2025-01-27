import unittest
from textnode import TextNode, TextType
from node_utils import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_basic_valid_input(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_invalid_syntax_unmatched_delimiter(self):
        node = TextNode("This is **invalid text", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid Markdown syntax: Unmatched ** in 'This is **invalid text'")

    def test_multiple_delimiters(self):
        node = TextNode("**Bold1** normal **Bold2**", TextType.TEXT)
        print(f"this is the starting node: {node}")
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        print(f"this is the result: {result}")
        expected = [
            TextNode("Bold1", TextType.BOLD),
            TextNode(" normal ", TextType.TEXT),
            TextNode("Bold2", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_empty_delimiter_content(self):
        node = TextNode("This is **empty** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("empty", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_mixed_input_types(self):
        nodes = [
            TextNode("Normal ", TextType.TEXT),
            TextNode("**Bold**", TextType.TEXT),
            TextNode(" and plain again", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Normal ", TextType.TEXT),
            TextNode("Bold", TextType.BOLD),
            TextNode(" and plain again", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiters(self):
        node = TextNode("This is plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [node]  # No splitting should occur
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
