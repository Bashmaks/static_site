import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        self.assertEqual(node.url, "https://boot.dev")

    def test_url_2(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.url, None)

if __name__ == "__main__":
    unittest.main()
