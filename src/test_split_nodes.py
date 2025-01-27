import unittest
from textnode import TextNode, TextType
from node_utils import split_nodes_image, split_nodes_link

class TestMarkdownSplitting(unittest.TestCase):
    def test_split_nodes_image(self):
        # Single image
        node = TextNode("Image: ![duck](duck.jpg)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("Image: ", TextType.TEXT),
            TextNode("duck", TextType.IMAGES, "duck.jpg")
        ])

        # Multiple images
        node = TextNode("Images: ![duck](duck.jpg) and ![cat](cat.jpg)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("Images: ", TextType.TEXT),
            TextNode("duck", TextType.IMAGES, "duck.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("cat", TextType.IMAGES, "cat.jpg")
        ])

        # No images
        node = TextNode("No images here", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

        # Non-text node
        node = TextNode("Already an image", TextType.IMAGES, "image.jpg")
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_split_nodes_link(self):
        # Single link
        node = TextNode("Link: [boot dev](https://boot.dev)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("Link: ", TextType.TEXT),
            TextNode("boot dev", TextType.LINKS, "https://boot.dev")
        ])

        # Multiple links
        node = TextNode("Links: [boot dev](https://boot.dev) and [youtube](https://youtube.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("Links: ", TextType.TEXT),
            TextNode("boot dev", TextType.LINKS, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("youtube", TextType.LINKS, "https://youtube.com")
        ])

        # No links
        node = TextNode("No links here", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

        # Non-text node
        node = TextNode("Already a link", TextType.LINKS, "https://example.com")
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_mixed_nodes(self):
        # Mixed nodes in list
        nodes = [
            TextNode("Image: ![duck](duck.jpg)", TextType.TEXT),
            TextNode("Already an image", TextType.IMAGES, "image.jpg"),
            TextNode("Link: [boot dev](https://boot.dev)", TextType.TEXT)
        ]
        
        image_result = split_nodes_image(nodes)
        self.assertEqual(image_result, [
            TextNode("Image: ", TextType.TEXT),
            TextNode("duck", TextType.IMAGES, "duck.jpg"),
            TextNode("Already an image", TextType.IMAGES, "image.jpg"),
            TextNode("Link: [boot dev](https://boot.dev)", TextType.TEXT)
        ])

        link_result = split_nodes_link(nodes)
        self.assertEqual(link_result, [
            TextNode("Image: ![duck](duck.jpg)", TextType.TEXT),
            TextNode("Already an image", TextType.IMAGES, "image.jpg"),
            TextNode("Link: ", TextType.TEXT),
            TextNode("boot dev", TextType.LINKS, "https://boot.dev")
        ])

if __name__ == '__main__':
    unittest.main()
