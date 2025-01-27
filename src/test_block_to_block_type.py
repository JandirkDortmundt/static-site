import unittest
from node_utils import block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a simple paragraph"
        self.assertEqual(block_to_block_type(block), 'paragraph')
    
    def test_heading(self):
        self.assertEqual(block_to_block_type('# Heading 1'), 'heading')
        self.assertEqual(block_to_block_type('### Heading 3'), 'heading')
        self.assertEqual(block_to_block_type('######  Heading 6'), 'heading')
    
    def test_code_block(self):
        block = "```\nsome code\nmore code\n```"
        self.assertEqual(block_to_block_type(block), 'code')
    
    def test_quote(self):
        block = "> First quote line\n> Second quote line"
        self.assertEqual(block_to_block_type(block), 'quote')
    
    def test_unordered_list(self):
        block1 = "* First item\n* Second item"
        block2 = "- First item\n- Second item"
        self.assertEqual(block_to_block_type(block1), 'unordered_list')
        self.assertEqual(block_to_block_type(block2), 'unordered_list')
    
    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), 'ordered_list')
    
    def test_invalid_ordered_list(self):
        block = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(block), 'paragraph')
    
    def test_mixed_block(self):
        block = "Some text that doesn't match any specific type"
        self.assertEqual(block_to_block_type(block), 'paragraph')

if __name__ == '__main__':
    unittest.main()
