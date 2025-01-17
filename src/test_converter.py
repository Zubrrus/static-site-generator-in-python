import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from converter import *


class TestTextNode(unittest.TestCase):
    def test_TEXT_text_node_to_html_node(self):
        node = TextNode("TEXT", TextType.TEXT)
        leaf_node = LeafNode(None, "TEXT")
        self.assertEqual(text_node_to_html_node(node), leaf_node)

    def test_BOLD_text_node_to_html_node(self):
        node = TextNode("BOLD", TextType.BOLD)
        leaf_node = LeafNode("b", "BOLD")
        self.assertEqual(text_node_to_html_node(node), leaf_node)

    def test_ITALIC_text_node_to_html_node(self):
        node = TextNode("ITALIC", TextType.ITALIC)
        leaf_node = LeafNode("i", "ITALIC")
        self.assertEqual(text_node_to_html_node(node), leaf_node)

    def test_CODE_text_node_to_html_node(self):
        node = TextNode("CODE", TextType.CODE)
        leaf_node = LeafNode("code", "CODE")
        self.assertEqual(text_node_to_html_node(node), leaf_node)

    def test_LINK_text_node_to_html_node(self):
        node = TextNode("LINK", TextType.LINK, "http://example.com")
        leaf_node = LeafNode("a", "LINK", {"href": "http://example.com"})
        self.assertEqual(text_node_to_html_node(node), leaf_node)

    def test_IMAGE_text_node_to_html_node(self):
        node = TextNode("IMAGE", TextType.IMAGE, "http://example.com")
        leaf_node = LeafNode("img", "", {"src": "http://example.com", "alt": "IMAGE"})
        self.assertEqual(text_node_to_html_node(node), leaf_node)

    def test_DEFAULF_text_node_to_html_node(self):
        wrong_type = "IMAG"
        node = TextNode("IMAGE", wrong_type, "http://example.com")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_split_nodes_delimiter1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        out = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        res = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(res, out)

    def test_split_nodes_delimiter2(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        out = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        res = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(res, out)

    def test_split_nodes_delimiter3(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", "bald")

    def test_split_nodes_delimiter4(self):
        node = TextNode("This is text with a **bolded phrase* in the middle", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text), 
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_split_nodes_link1(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        res = split_nodes_link([node])
        out = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),                           
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(res, out)

    def test_split_nodes_link2(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev) just to links",
            TextType.TEXT,
        )
        res = split_nodes_link([node])
        out = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),                          
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(" just to links", TextType.TEXT),
        ]
        self.assertEqual(res, out)

    def test_split_nodes_image1(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) " +\
            "and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
        node = TextNode(
            text,
            TextType.TEXT,
        )
        res = split_nodes_image([node])
        out = [
            TextNode("This is text with an ", TextType.TEXT), 
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), 
            TextNode(" and another ", TextType.TEXT), 
            TextNode("second image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ]
        self.assertEqual(res, out)

    def test_split_nodes_image2(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) "+\
                "and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and some text",
            TextType.TEXT,
        )
        res = split_nodes_image([node])
        out = [
            TextNode("This is text with an ", TextType.TEXT), 
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), 
            TextNode(" and another ", TextType.TEXT), 
            TextNode("second image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"), 
            TextNode(" and some text", TextType.TEXT),
        ]
        self.assertEqual(res, out)

    def test_split_nodes_image3(self):
        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            TextType.TEXT,
        )
        res = split_nodes_image([node])
        out = [
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        ]
        self.assertEqual(res, out) 

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image]" +\
            "(https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        res = text_to_textnodes(text)
        out = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(res, out) 

    def test_markdown_to_blocks(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n" +\
        "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        res = markdown_to_blocks(markdown)
        out = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(res, out) 

    def test_HEADING_get_block_type1(self):
        block = "#"
        self.assertNotEqual(get_block_type(block), BlockType.HEADING)

    def test_HEADING_get_block_type2(self):
        block = "####### not a heading"
        self.assertNotEqual(get_block_type(block), BlockType.HEADING)

    def test_HEADING_get_block_type3(self):
        block = "##not a heading"
        self.assertNotEqual(get_block_type(block), BlockType.HEADING)

    def test_HEADING_get_block_type4(self):
        block = "# actual heading"
        self.assertEqual(get_block_type(block), BlockType.HEADING) 

    def test_CODE_get_block_type1(self):
        block = "```code``"
        self.assertNotEqual(get_block_type(block), BlockType.CODE)

    def test_CODE_get_block_type2(self):
        block = "```sudo apt upgrade```"
        self.assertEqual(get_block_type(block), BlockType.CODE) 

    def test_CODE_get_block_type3(self):
        block = "```for item in items:\nprint(item)```"
        self.assertEqual(get_block_type(block), BlockType.CODE) 

    def test_QUOTE_get_block_type1(self):
        block = "> first line\n>second line (no space)\n>\n>third is empty"
        self.assertEqual(get_block_type(block), BlockType.QUOTE) 

    def test_QUOTE_get_block_type2(self):
        block = "> first line\n>second line (no space)\n>\nnot a quot actually"
        self.assertNotEqual(get_block_type(block), BlockType.QUOTE) 

    def test_UNORDERED_LIST_get_block_type1(self):
        block = "* list 1\n- list 2\n* list 3" #not an unordered lists
        self.assertNotEqual(get_block_type(block), BlockType.UNORDERED_LIST)

    def test_UNORDERED_LIST_get_block_type1(self):
        block = "* list 1\n* list 2\n list 3" #not an unordered lists
        self.assertNotEqual(get_block_type(block), BlockType.UNORDERED_LIST)

    def test_UNORDERED_LIST_get_block_type1(self):
        block = "* list 1\n*list 2\n *list 3" #not an unordered lists
        self.assertNotEqual(get_block_type(block), BlockType.UNORDERED_LIST)

    def test_UNORDERED_LIST_get_block_type2(self):
        block = "* list 1\n* list 2\n* list 3"
        self.assertEqual(get_block_type(block), BlockType.UNORDERED_LIST)

    def test_UNORDERED_LIST_get_block_type3(self):
        block = "+ list 1\n+ list 2\n+ list 3"
        self.assertEqual(get_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_UNORDERED_LIST_get_block_type4(self):
        block = "- list 1\n- list 2\n- list 3"
        self.assertEqual(get_block_type(block), BlockType.UNORDERED_LIST)

    def test_ORDERED_LIST_get_block_type1(self):
        block = "1. list 1\n3. list 2\n4. list 3" #not an ordered lists
        self.assertNotEqual(get_block_type(block), BlockType.ORDERED_LIST)

    def test_ORDERED_LIST_get_block_type2(self):
        block = "- list 1\n1. list 2\n2. list 3" #not an ordered lists
        self.assertNotEqual(get_block_type(block), BlockType.ORDERED_LIST)

    def test_ORDERED_LIST_get_block_type3(self):
        block = "1. list 1\n2. list 2\n3.list 3" #not an ordered lists
        self.assertNotEqual(get_block_type(block), BlockType.ORDERED_LIST)

    def test_ORDERED_LIST_get_block_type3(self):
        block = "1 list 1\n2. list 2\n3. list 3" #not an ordered lists
        self.assertNotEqual(get_block_type(block), BlockType.ORDERED_LIST)

    def test_ORDERED_LIST_get_block_type4(self):
        block = "2. list 1\n3. list 2\n4. list 3" #not an ordered lists
        self.assertNotEqual(get_block_type(block), BlockType.ORDERED_LIST)

    def test_ORDERED_LIST_get_block_type4(self):
        block = "1. list 1\n2. list 2\n3. list 3"
        self.assertEqual(get_block_type(block), BlockType.ORDERED_LIST)

    def test_HEADERS_markdown_to_html_node(self):
        markdown = "# cookies\n\n## *pizza*\n\n### **cheeseburger**"
        res = markdown_to_html_node(markdown)
        out = ParentNode(
            "div",
            [
                ParentNode("h1", [LeafNode(None, "cookies")]),
                ParentNode("h2", [LeafNode("i", "pizza")]),
                ParentNode("h3", [LeafNode("b", "cheeseburger")]),
            ],
            None
        )
        self.assertEqual(res, out) # cool

    def test_QUOTE_markdown_to_html_node1(self):
        markdown = ">From iron cometh strength!\n>From strength cometh will!\n" +\
            ">From will cometh faith!\n>From faith cometh honour!\n>From honour cometh iron!"
        res = markdown_to_html_node(markdown)
        out = ParentNode(
            "div",
            [
                ParentNode(
                    "blockquote", [
                        LeafNode(None, "From iron cometh strength!"),
                        LeafNode(None, "From strength cometh will!"),
                        LeafNode(None, "From will cometh faith!"),
                        LeafNode(None, "From faith cometh honour!"),
                        LeafNode(None, "From honour cometh iron!"),
                    ]
                ),
            ],
            None
        )
        self.assertEqual(res, out) # cool

    def test_QUOTE_markdown_to_html_node2(self):
        markdown = ">From **iron** cometh strength!\n>From strength cometh will!\n" +\
            ">From will cometh faith!\n>From faith cometh honour!\n>From honour cometh **iron**!"
        res = markdown_to_html_node(markdown)
        out = ParentNode(
            "div",
            [
                ParentNode(
                    "blockquote", [
                        LeafNode(None, "From "),
                        LeafNode("b", "iron"),
                        LeafNode(None, " cometh strength!"),
                        LeafNode(None, "From strength cometh will!"),
                        LeafNode(None, "From will cometh faith!"),
                        LeafNode(None, "From faith cometh honour!"),
                        LeafNode(None, "From honour cometh "),
                        LeafNode("b", "iron"),
                        LeafNode(None, "!"),
                    ]
                ),
            ],
            None
        )
        self.assertEqual(res, out) # cool

    def test_CODE_markdown_to_html_node(self):
        markdown = "```for item in items:\nprint(item)```"
        res = markdown_to_html_node(markdown)
        out = ParentNode(
            "div",
            [
                ParentNode(
                    "code",
                    [
                        ParentNode("pre", [LeafNode(None, "for item in items:")]),
                        ParentNode("pre", [LeafNode(None, "print(item)")])
                    ],
                    None
                )
            ]
        )
        self.assertEqual(res, out) # cool

    def test_ORDERED_LIST_markdown_to_html_node(self):
        markdown = "1. **sun**\n2. **moon**"
        res = markdown_to_html_node(markdown)
        out = ParentNode(
            "div",
            [
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", [LeafNode("b", "sun")]),
                        ParentNode("li", [LeafNode("b", "moon")])
                    ],
                    None
                )
            ]
        )
        self.assertEqual(res, out) # cool

    def test_UNORDERED_list_markdown_to_html_node1(self):
        markdown = "+ **sun**\n+ **moon**"
        res = markdown_to_html_node(markdown)
        out = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode("b", "sun")]),
                        ParentNode("li", [LeafNode("b", "moon")])
                    ],
                    None
                )
            ]
        )
        self.assertEqual(res, out) # cool

    def test_UNORDERED_list_markdown_to_html_node2(self):
        markdown = "* **sun**\n* **moon**"
        res = markdown_to_html_node(markdown)
        out = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode("b", "sun")]),
                        ParentNode("li", [LeafNode("b", "moon")])
                    ],
                    None
                )
            ]
        )
        self.assertEqual(res, out) # cool

    def test_UNORDERED_list_markdown_to_html_node3(self):
        markdown = "- **sun**\n- **moon**"
        res = markdown_to_html_node(markdown)
        out = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode("b", "sun")]),
                        ParentNode("li", [LeafNode("b", "moon")])
                    ],
                    None
                )
            ]
        )
         # cool

    def test_PARAGRAPH_list_markdown_to_html_node(self):
        markdown = "1. **sun**\n- **moon**\nsample text"
        res = markdown_to_html_node(markdown)
        out = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "1. "),
                        LeafNode("b", "sun"),
                        LeafNode(None, "- "),
                        LeafNode("b", "moon"),
                        LeafNode(None, "sample text")
                    ],
                    None
                )
            ]
        )
        self.assertEqual(res, out) # cool

    def test_extract_title1(self):
        markdown = "# title1\n\n## title2\n\n### title3\n\nsome sample text\nanother line"
        res = extract_title(markdown)
        out = "title1"
        self.assertEqual(res, out)

    def test_extract_title2(self):
        markdown = "## title1\n\n## title2\n\n### title3\n\nsome sample text\nanother line"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title3(self):
        markdown = "# title1\n\n# title2\n\n### title3\n\nsome sample text\nanother line"
        with self.assertRaises(Exception):
            extract_title(markdown)
  
if __name__ == "__main__":
    unittest.main()
