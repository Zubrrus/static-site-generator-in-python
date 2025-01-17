import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html1(self):
        node = LeafNode("p", "This is a paragraph of text.")
        text = '''<p>This is a paragraph of text.</p>'''
        self.assertEqual(node.to_html(), text)


    def test_to_html2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        text = '''<a href="https://www.google.com">Click me!</a>'''
        self.assertEqual(node.to_html(), text)


    def test_to_html3(self):
        node = LeafNode("b", "Bold text")
        text = '''<b>Bold text</b>'''
        self.assertEqual(node.to_html(), text)   


    def test_to_html4(self):
        node = LeafNode(None, "Normal text")
        text = '''Normal text'''
        self.assertEqual(node.to_html(), text)


if __name__ == "__main__":
    unittest.main()