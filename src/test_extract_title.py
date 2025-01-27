import unittest
from node_utils import extract_title

# Function to test
def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# ") and len(line) > 2:
            return line[2:].strip()
    raise Exception("No H1 header found")

# Unit Test Class
class TestExtractTitle(unittest.TestCase):

    def test_single_h1_header(self):
        """Test with a simple H1 header."""
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_h1_with_whitespace(self):
        """Test with extra spaces around the header text."""
        self.assertEqual(extract_title("   #    Hello World   "), "Hello World")

    def test_multiline_markdown(self):
        """Test with a markdown file containing multiple lines."""
        markdown = """
        Some introduction text.
        
        # Title of the Document
        
        ## Subtitle
        """
        self.assertEqual(extract_title(markdown), "Title of the Document")

    def test_h1_not_first_line(self):
        """Test with an H1 header not at the start of the document."""
        markdown = """
        Some content first.
        
        # Header after content
        """
        self.assertEqual(extract_title(markdown), "Header after content")

    def test_no_h1_header(self):
        """Test when no H1 header is present."""
        markdown = """
        ## Subtitle
        ### Another subtitle
        """
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 header found")

    def test_h1_with_only_hash(self):
        """Test when a line starts with # but has no text."""
        markdown = """
        #
        #      
        ## Subtitle
        """
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No H1 header found")

    def test_h1_with_extra_hashes(self):
        """Test that only single # with space is recognized."""
        markdown = """
        ## Subtitle
        ### Another subtitle
        # Valid Header
        """
        self.assertEqual(extract_title(markdown), "Valid Header")

    def test_multiple_h1_headers(self):
        """Test when there are multiple H1 headers (should return the first)."""
        markdown = """
        # First Header
        Some content.
        # Second Header
        """
        self.assertEqual(extract_title(markdown), "First Header")

# Run tests
if __name__ == "__main__":
    unittest.main()
