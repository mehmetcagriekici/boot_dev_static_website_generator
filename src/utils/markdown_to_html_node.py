import re

from utils.markdown_to_blocks import markdown_to_blocks
from utils.block_to_block_type import block_to_block_type, BlockType
from utils.text_to_textnodes import text_to_text_nodes
from htmlnode import ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

# converts a full markdown document into a single parent HTMLNode
def markdown_to_html_node(markdown):
    # split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    children = []

    # loop over each block
    for block in blocks:
        # determine the type of the block
        block_type = block_to_block_type(block)

        # based on the type of the block create a new HTMLNode with the proper data
        new_node = None
        # stores the text nodes
        text_nodes = []

        # convert blocks to text nodes except for code blocks
        if block_type != BlockType.CODE:
            text_nodes.extend(text_to_text_nodes(block))
        else:
            code_content = block.replace("```", "").lstrip()
            text_nodes.append(TextNode(code_content, TextType.TEXT))
        
        # Paragraphs should be surrounded by a <p> tag.
        if block_type == BlockType.PARAGRAPH:
            paragraph_nodes = convert_to_html_node(text_nodes)
            new_node = ParentNode(tag="p", children=paragraph_nodes)

        # Headings should be surrounded by a <h1> to <h6> tag, depending on the number of # characters.
        if block_type == BlockType.HEADING:
            level = len(block.split(" ")[0])
            heading_nodes = convert_to_html_node(text_nodes, delimiter=r"#")
            new_node = ParentNode(tag=f"h{level}", children=heading_nodes)
        
        # Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.
        if block_type == BlockType.CODE:
            code_nodes = convert_to_html_node(text_nodes, make_inline=False)
            child_code = ParentNode(tag="code", children=code_nodes)
            new_node = ParentNode(tag="pre", children=[child_code])
        
        # Quote blocks should be surrounded by a <blockquote> tag.
        if block_type == BlockType.QUOTE:
            quote_nodes = convert_to_html_node(text_nodes, delimiter=r">")
            new_node = ParentNode(tag="blockquote", children=quote_nodes)
        
        # Unordered list blocks should be surrounded by a <ul> tag, and each list item should be surrounded by a <li> tag.
        if block_type == BlockType.UNORDERED_LIST:
            ul_li_nodes = []
            li_blocks = block.split("\n")
            # iterate over the each block and convert them to text nodes
            for li_block in li_blocks:
                li_text_nodes = text_to_text_nodes(li_block)
                # convert li textnodes to li html node
                li_nodes = convert_to_html_node(li_text_nodes, delimiter=r"-")
                li_node = ParentNode(tag="li", children=li_nodes)
                ul_li_nodes.append(li_node)
            new_node = ParentNode(tag="ul", children=ul_li_nodes)
                                
        # Ordered list blocks should be surrounded by a <ol> tag, and each list item should be surrounded by a <li> tag.
        if block_type == BlockType.ORDERED_LIST:
            ol_li_nodes = []
            li_blocks = block.split("\n")
            # iterate over the each block and convert them to text nodes
            for li_block in li_blocks:
                li_text_nodes = text_to_text_nodes(li_block)
                # convert li textnodes to li html node
                li_nodes = convert_to_html_node(li_text_nodes, delimiter=r'^\d+\. ')
                li_node = ParentNode(tag="li", children=li_nodes)
                ol_li_nodes.append(li_node)
            new_node = ParentNode(tag="ol", children=ol_li_nodes)

        if new_node:
            children.append(new_node)
    
    # make all the block nodes children under a single parent HTML node(div) and return it
    return ParentNode(tag="div", children=children)

# converts text nodes to html nodes
def convert_to_html_node(text_nodes, delimiter=None, make_inline=True):
    html_nodes = []

    # iterate over the text nodes
    for text_node in text_nodes:
        new_text = text_node.text
        # remove the deimiter from the text node text
        if delimiter:
            new_text = re.sub(delimiter, "", text_node.text).strip()

        new_text_node = TextNode(new_text, text_node.text_type, text_node.url)

        # convert text node to html node
        html_node = text_node_to_html_node(new_text_node, make_inline)
        html_nodes.append(html_node)

    return html_nodes
    