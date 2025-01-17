import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        text = ''' href="https://www.google.com" target="_blank"'''
        self.assertEqual(node.props_to_html(), text)

    def test_values(self):
        node = HTMLNode(
            "div",
            "o, hello where",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "o, hello where",
        )

    def test_repr(self):
        node = HTMLNode(
            "h1",
            "Header1",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(h1, Header1, children: None, {'class': 'primary'})",
        )

if __name__ == "__main__":
    unittest.main()