from textnode import *
from htmlnode import *
from enum import Enum
import re

types_dict = {
    TextType.TEXT: None, 
    TextType.BOLD: "**",
    TextType.ITALIC: "*",
    TextType.CODE: "`",
    TextType.LINK: None,
    TextType.IMAGE: None
}

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

# regex patterns
re_markdown_images = re.compile(
    r"""!                               # ensures the match is preceded by !
    \[                                  # opening square bracket
    ([^\[\]]*?)                         # text (first capchering group)
    \]                                  # closing square bracket
    \(                                  # opening parenthese
    (.*?\.(?:jpg|jpeg|png|gif))         # url text (second capchering group)
    \)""",                              # closing parenthese
    re.VERBOSE
)
re_markdown_links = re.compile(
    r"""(?<!!)                          # ensures the match is not preceded by !
    \[                                  # opening square bracket
    ([^\[\]]*)                          # text (first capchering group)
    \]                                  # closing square bracket
    \(                                  # opening parenthese
    ([^\(\)]*)                          # url text (second capchering group)
    \)""",                              # closing parenthese 
    re.VERBOSE
)
re_MD_to_blocks = re.compile(
    r"[ ]*\n{2,}[ ]*"
)
re_heading = re.compile(
    r"^#{1,6}? .+"
) 
re_code = re.compile(
    r"^```[\w\W]+```$"
)
re_quote = re.compile(
    r"^>"
)
re_unordered_list = re.compile(
    r"^[(?:\+|\*|\-)] "
)
def ordered_list_filt(input):
    str = lambda x: r"^{}. ".format(int(x) + 1)
    return re.match(str(input[1]), input[0])
re_count_level = re.compile(
    r"^#{1,6}? "
)
re_strip_QUOTE_enum = re.compile(
    r"^\>(.*)", 
    re.MULTILINE
)
re_strip_OL_enum = re.compile(
    r"^\d*\.\s(.*)", 
    re.MULTILINE
)
re_strip_UL_enum = re.compile(
    r"^[\+|\*|\-]\s(.*)", 
    re.MULTILINE
)
re_find_title = re.compile(
    r"^#{1} (.+)",
    re.MULTILINE,
)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not old_nodes:
        return []
    if text_type not in TextType:
        raise Exception(f"{text_type} is invalid TextNode type")
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):    
    return re_markdown_images.findall(text)

def extract_markdown_links(text):    
    return re_markdown_links.findall(text)

def split_nodes_general_links(old_nodes, text_type):
    if not old_nodes:
        return []
    new_nodes = []
    match text_type:
        case TextType.IMAGE:
            func = extract_markdown_images
            str = lambda item: f"![{item[0]}]({item[1]})"
        case TextType.LINK:
            func = extract_markdown_links
            str = lambda item: f"[{item[0]}]({item[1]})"
        case _:
            return old_nodes
    for node in old_nodes:
        if node.text_type == text_type:
            new_nodes.append(node)
            break
        items = func(node.text)
        if not items:
            new_nodes.append(node)
        else:
            text = node.text
            for item in items:
                splited_text = text.split(str(item), 1)                
                if splited_text[0]:
                    new_nodes.append(
                        TextNode(
                            splited_text[0], 
                            TextType.TEXT
                        )
                    )
                new_nodes.append(
                    TextNode(
                        item[0], 
                        text_type, 
                        item[1]
                    )
                )
                text = splited_text[1]
            if text:
                new_nodes.append(
                    TextNode(
                        text, 
                        TextType.TEXT
                    )
                )
    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_general_links(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_general_links(old_nodes, TextType.LINK)

def text_to_textnodes(text):
    new_nodes = [
        TextNode(
            text,
            TextType.TEXT
        )
    ]
    try:
        for type in TextType:
            if types_dict[type] is not None:
                new_nodes = split_nodes_delimiter(
                    new_nodes, 
                    types_dict[type], 
                    type
                )
        new_nodes = split_nodes_image(new_nodes)
        new_nodes = split_nodes_link(new_nodes)
    except Exception as e:
        print(e)
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = re_MD_to_blocks.split(markdown)
    for block in blocks:
        block.lstrip(" \n")
        block.rstrip(" \n")
    return blocks

def get_block_type(block):
    if re_heading.match(block):
        return BlockType.HEADING
    if re_code.match(block):
        return BlockType.CODE
    lines = block.split("\n")
    len_lines = len(lines)
    filtered = list(filter(re_quote.match, lines))
    if len(filtered) == len_lines:
        return BlockType.QUOTE
    filtered = list(filter(re_unordered_list.match, lines))
    if len(filtered) == len_lines:
        return BlockType.UNORDERED_LIST
    filtered = list(
        filter(
            ordered_list_filt, 
            zip(
                lines, 
                range(len_lines)
            )
        )
    )
    if len(filtered) == len_lines:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    if not text:
        return []
    html_node = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        html_node.append(text_node_to_html_node(node))
    return html_node

def lines_to_children(lines, tag=None):
    html_nodes = []
    if tag == None:
        for line in lines:
            html_nodes.extend(text_to_children(line))
    else:
        for line in lines:
            html_nodes.append(ParentNode(tag, text_to_children(line)))
    return html_nodes

def heading_block_to_HTMLNode(block):
    level = re_count_level.match(block).span()[-1] - 1
    return ParentNode(f"h{level}", text_to_children(block.removeprefix("#" * level + " ")))

def code_block_to_HTMLNode(block):
    lines = block.removeprefix("```").removesuffix("```").split("\n")
    return ParentNode("code", lines_to_children(lines, "pre"))

def quote_block_to_HTMLNode(block):
    lines = re_strip_QUOTE_enum.findall(block)
    return ParentNode("blockquote", lines_to_children(lines, None))

def unordered_list_block_to_HTMLNode(block):
    lines = re_strip_UL_enum.findall(block)
    return ParentNode("ul", lines_to_children(lines, "li"))

def ordered_list_block_to_HTMLNode(block):
    lines = re_strip_OL_enum.findall(block)
    return ParentNode("ol", lines_to_children(lines, "li"))
    
def paragraph_block_to_HTMLNode(block):
    lines = block.split("\n")
    return ParentNode("p", lines_to_children(lines, None))

def markdown_to_html_node(markdown):
    if not markdown:
        return ParentNode()
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match get_block_type(block):
            case BlockType.HEADING:
                html_nodes.append(heading_block_to_HTMLNode(block))
            case BlockType.CODE:
                html_nodes.append(code_block_to_HTMLNode(block))
            case BlockType.QUOTE:
                html_nodes.append(quote_block_to_HTMLNode(block))            
            case BlockType.UNORDERED_LIST:
                html_nodes.append(unordered_list_block_to_HTMLNode(block))
            case BlockType.ORDERED_LIST:
                html_nodes.append(ordered_list_block_to_HTMLNode(block))
            case BlockType.PARAGRAPH:
                html_nodes.append(paragraph_block_to_HTMLNode(block))
    return ParentNode("div", html_nodes)

def extract_title(markdown):
    res = re_find_title.findall(markdown)
    if len(res) == 0:
        raise Exception("h1 header not found")
    if len(res) > 1:
        raise Exception("multiple h1 header found")
    return res[0]