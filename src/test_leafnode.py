import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(tag=None, value="test")
        self.assertEqual(node.to_html(), "test")

    def test_url(self):
        node = LeafNode(tag="a", value="link", props={"href":"https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">link</a>')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

if __name__ == "__main__":
    unittest.main()
