import unittest
from node_utils import extract_markdown_links, extract_markdown_images

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        # Test simple case
        text1 = "![duck](https://example.com/duck.jpg)"
        self.assertEqual(extract_markdown_images(text1), [("duck", "https://example.com/duck.jpg")])

        # Test multiple images
        text2 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text2), [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ])

        # Test no images
        text3 = "This is text with no images"
        self.assertEqual(extract_markdown_images(text3), [])

        # Test images with special characters
        text4 = "![weird name!@#](https://example.com/weird-image.png)"
        self.assertEqual(extract_markdown_images(text4), [("weird name!@#", "https://example.com/weird-image.png")])

    def test_extract_markdown_links(self):
        # Test simple case
        text1 = "[boot dev](https://www.boot.dev)"
        self.assertEqual(extract_markdown_links(text1), [("boot dev", "https://www.boot.dev")])

        # Test multiple links
        text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text2), [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ])

        # Test no links
        text3 = "This is text with no links"
        self.assertEqual(extract_markdown_links(text3), [])

        # Test links with special characters
        text4 = "[weird link!@#](https://example.com/weird-link)"
        self.assertEqual(extract_markdown_links(text4), [("weird link!@#", "https://example.com/weird-link")])

        # Test ignoring image links
        text5 = "This is a ![not a link](https://example.com/image.jpg) but [this is a link](https://example.com)"
        print(f"I've ran this test!!!!")
        self.assertEqual(extract_markdown_links(text5), [("this is a link", "https://example.com")])

if __name__ == '__main__':
    unittest.main()
