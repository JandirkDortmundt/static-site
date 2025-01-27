import unittest

from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):

    def test_single_child(self):
        child = LeafNode(tag="span", value="Child text")
        parent = ParentNode(tag="div", children=[child])
        self.assertEqual(parent.to_html(), "<div><span>Child text</span></div>")

    def test_multiple_children(self):
        child1 = LeafNode(tag="p", value="Paragraph 1")
        child2 = LeafNode(tag="p", value="Paragraph 2")
        parent = ParentNode(tag="div", children=[child1, child2])
        self.assertEqual(
            parent.to_html(),
            "<div><p>Paragraph 1</p><p>Paragraph 2</p></div>"
        )

    def test_with_props(self):
        child = LeafNode(tag="span", value="Child text")
        parent = ParentNode(tag="div", children=[child], props={"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>Child text</span></div>')

    def test_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div", children=[]).to_html()

    def test_no_tag(self):
        child = LeafNode(tag="span", value="Child text")
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=[child]).to_html()

    def test_nested_structure(self):
        grandchild = LeafNode(tag="b", value="Bold text")
        child = ParentNode(tag="p", children=[grandchild])
        parent = ParentNode(tag="div", children=[child])
        self.assertEqual(
            parent.to_html(),
            "<div><p><b>Bold text</b></p></div>"
        )

    def test_child_without_tag(self):
        child = LeafNode(value="Just text")
        parent = ParentNode(tag="div", children=[child])
        self.assertEqual(parent.to_html(), "<div>Just text</div>")

if __name__ == "__main__":
    unittest.main()
