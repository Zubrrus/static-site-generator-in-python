import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html1(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        text = '''<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'''
        self.assertEqual(node.to_html(), text)

    def text_eq(self):
        node1 = ParentNode(
            "div",
            [
                ParentNode("h1", LeafNode(None, "cookies")),
                ParentNode("h2", LeafNode("i", "pizza")),
                ParentNode("h3", LeafNode("b", "cheeseburger")),
            ],
            None
        )
        node2 = ParentNode(
            "div",
            [
                ParentNode("h1", LeafNode(None, "cookies")),
                ParentNode("h2", LeafNode("i", "pizza")),
                ParentNode("h3", LeafNode("b", "cheeseburger")),
            ],
            None
        )
        self.assertEqual(node1, node2)

    def test_to_html2(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        giga_node = ParentNode(
            "p",
            [
                node,
                node,
                node,
            ],
        )  
        text = '''<p>''' + \
        '''<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>''' + \
        '''<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>''' + \
        '''<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>''' + \
        '''</p>'''
        self.assertEqual(giga_node.to_html(), text)


if __name__ == "__main__":
    unittest.main()