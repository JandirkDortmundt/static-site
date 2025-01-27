import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(tag="p", value="This is some text",props={"href": "https://www.google.com"})
        node2 = LeafNode(tag="p", value="This is some text",props={"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = LeafNode(tag="a", value="This is some text")
        node2 = LeafNode(tag="p", value="This is some text")
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = LeafNode(tag="p", value="This is some text",props={"href": "https://www.google.com"})
        node2 = LeafNode(tag="p", value="This is some text",props={"href": "https://www.google.com"})
        props = node.props_to_html()
        self.assertEqual(node, node2)

    def test_not_eq2(self):
        node = LeafNode(tag="p", value="This is some text as well")
        node2 = LeafNode(tag="p", value="This is some text")
        self.assertNotEqual(node, node2)

def test_value_is_none(self):
    with self.assertRaises(ValueError):
        LeafNode(tag="p", value=None)


if __name__ == "__main__":
    unittest.main()
