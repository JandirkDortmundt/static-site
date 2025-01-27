import unittest
from node_utils import markdown_to_blocks

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = list(filter(None, blocks))
    blocks = [block.strip() for block in blocks]
    return blocks

class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_single_block(self):
        markdown = "This is a single block of text."
        expected = ["This is a single block of text."]
        self.assertEqual(markdown_to_blocks(markdown), expected)
    
    def test_multiple_blocks(self):
        markdown = "First block\n\nSecond block\n\nThird block"
        expected = ["First block", "Second block", "Third block"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_trailing_newlines(self):
        markdown = "First block\n\nSecond block\n\n"
        expected = ["First block", "Second block"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_input(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_empty_lines(self):
        markdown = "\n\n"
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_extra_spaces(self):
        markdown = "  First block  \n\n  Second block  "
        expected = ["First block", "Second block"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_blank_lines_between_content(self):
        markdown = "First block\n\n\nSecond block"
        expected = ["First block", "Second block"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

if __name__ == "__main__":
    unittest.main()
