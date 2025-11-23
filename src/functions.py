import re
import os
import shutil

from my_types import TextType, BlockType
from textnode import TextNode
from leafnode import LeafNode
from parentnode import ParentNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def split_node(node):
        text_blocks = node.text.split(delimiter)
        if len(text_blocks) % 2 == 0:
            raise ValueError('invalid Markdown syntax')
        new_nodes = []
        for i,text in enumerate(text_blocks):
            if i % 2 == 0:
                new_nodes.append(TextNode(text, text_type=TextType.TEXT))
            else:
                new_nodes.append(TextNode(text=text, text_type=text_type))
        return new_nodes
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            new_nodes.extend(split_node(node))
    return new_nodes

def extract_markdown_images(text):
    img_re = re.compile(r"!\[(?P<alt>.*?)\]\((?P<src>.*?)\)")
    return img_re.findall(text)

def extract_markdown_links(text):
    url_re = re.compile(r"\[(?P<text>.*?)\]\((?P<url>.*?)\)")
    return url_re.findall(text)

def _split_nodes_with_url(old_nodes, node_type):
    if node_type is TextType.IMAGE:
        extract_fun = extract_markdown_images
        prefix = "!"
    elif node_type is TextType.LINK:
        extract_fun = extract_markdown_links
        prefix = ""
    else:
        raise ValueError("Invalid node type!")
    def split_node(node):
        result = []
        text = node.text
        for alt, link in extract_fun(text):
            before, text = text.split(f"{prefix}[{alt}]({link})", 1)
            if len(before) > 0:
                result.append(TextNode(text=before, text_type=TextType.TEXT))
            result.append(TextNode(text=alt, text_type=node_type, url=link))
        if len(text) > 0:
            result.append(TextNode(text=text, text_type=TextType.TEXT))
        return result
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            new_nodes.extend(split_node(node))
    return new_nodes

def split_nodes_image(old_nodes):
    return _split_nodes_with_url(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return _split_nodes_with_url(old_nodes, TextType.LINK)

def text_to_textnodes(text):
    types = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE
        }
    nodes = split_nodes_image([TextNode(text=text, text_type=TextType.TEXT)])
    nodes = split_nodes_link(nodes)
    for delimiter, text_type in types.items():
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    return nodes

def markdown_to_blocks(markdown):
    blocks = [block.strip().strip("\n") for block in markdown.split("\n\n")]
    return [block for block in blocks if len(block) > 0]
    
def block_to_block_type(markdown):
    mapper = {
        BlockType.HEADING: re.compile("^#{1,6}.*", re.MULTILINE),
        BlockType.CODE: re.compile(r'^```(\n|.)*?```$', re.MULTILINE),
        BlockType.QUOTE: re.compile("^>.+", re.MULTILINE),
        BlockType.UNORDERED_LIST: re.compile("^- .*"),
        BlockType.ORDERED_LIST: re.compile(r'^\d+\. .*'),
        }
    for block_type, tmp_re in mapper.items():
        if tmp_re.match(markdown):
            return block_type
    return BlockType.PARAGRAPH

def text_to_children(text):
    nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, nodes))

def paragraph_block_to_node(block):
    lines = [line for line in block.split("\n") if len(line) > 0]
    tmp = " ".join(lines)
    children = text_to_children(tmp)
    return ParentNode(tag="p", children=children)

def heading_block_to_node(block):
    tmp_re = re.compile("^(?P<level>#{1,6}).*")
    m = tmp_re.match(block)
    level = len(m.group("level"))
    return LeafNode(tag=f"h{level}", value=block.lstrip('#'))

def quote_block_to_node(block):
    lines = [line.lstrip(">").strip() for line in block.split("\n")]
    return LeafNode(tag="blockquote", value="\n".join(lines))

def unordered_list_block_to_node(block):
    tmp = lambda x: LeafNode(tag="li", value=x)
    lines = [line.lstrip("-").strip() for line in block.split("\n")]
    return ParentNode(tag="ul", children=map(tmp, lines))

def ordered_list_block_to_node(block):
    tmp = lambda x: LeafNode(tag="li", value=x)
    lines = [line.split(".", 1)[-1].strip() for line in block.split("\n")]
    return ParentNode(tag="ol", children=map(tmp, lines))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                nodes.append(paragraph_block_to_node(block))
            case BlockType.HEADING:
                nodes.append(heading_block_to_node(block))
            case BlockType.CODE:
                node = LeafNode(tag="code", value=block.strip('`').lstrip("\n"))
                nodes.append(ParentNode(tag="pre", children=[node]))
            case BlockType.QUOTE:
                nodes.append(quote_block_to_node(block))
            case BlockType.UNORDERED_LIST:
                nodes.append(unordered_list_block_to_node(block))
            case BlockType.ORDERED_LIST:
                nodes.append(ordered_list_block_to_node(block))
    return ParentNode(tag="div", children=nodes)

def extract_title(markdown):
    lines = [line.strip() for line in markdown.split("\n")]
    lines = [line for line in lines if len(line) > 0]
    header = next((line.lstrip("# ") for line in lines if line.startswith("# ")), None)
    if header is None:
        raise Exception("Header h1 not found in text")
    return header.strip()


#%% file operations
def copy_tree(source, destination):
    # check folders
    if not os.path.exists(source):
        raise Exception("Source not found")
    if not os.path.exists(destination):
        os.mkdir(destination)
    else:
        # clear content of destination
        content = os.listdir(destination)
        for filename in content:
            dst = os.path.join(destination, filename)
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
    # copy content of source to destination
    content = os.listdir(source)
    for filename in content:
        src = os.path.join(source, filename)
        dst = os.path.join(destination, filename)
        if os.path.isdir(src):
            os.mkdir(dst)
            copy_tree(src, dst)
        else:
            shutil.copy(src, dst)
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    content = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    with open(dest_path, 'w') as f:
        f.write(content)

