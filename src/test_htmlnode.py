import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_url(self):
        node = HTMLNode(tag="a", text="link", props={"href":"https://boot.dev"})
        print(node)
        self.assertEqual(node.props_to_html(), 'href="https://boot.dev"')

    def test_url_2(self):
        node = HTMLNode(tag="a", text="link", props={"href":"https://boot.dev"})
        self.assertEqual(node.__repr__(), 'HTMLNode(tag="a", text="link", children=None, props={\'href\': \'https://boot.dev\'})')

if __name__ == "__main__":
    unittest.main()
