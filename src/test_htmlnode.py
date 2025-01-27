import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is some text",["child1","child2"],{"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("p", "This is some text",["child1","child2"],{"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("a", "This is some text")
        node2 = HTMLNode("p", "This is some text")
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode("p", "This is some text",["child1","child2"],{"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("p", "This is some text",["child1","child2"],{"href": "https://www.google.com", "target": "_blank",})
        props = node.props_to_html()
        #print(f"props_to_html: {props}")
        self.assertEqual(node, node2)

    def test_not_eq2(self):
        node = HTMLNode("p", "This is some text as well",["child1","child2"])
        node2 = HTMLNode("p", "This is some text",["child1","child2"])
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
