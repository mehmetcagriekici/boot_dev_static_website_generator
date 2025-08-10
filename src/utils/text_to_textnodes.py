from utils.split_nodes_delimiter import split_nodes_delimiter
from utils.split_nodes_image_link import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

def text_to_text_nodes(text):
    initial_node = TextNode(text, TextType.TEXT)
    # split delimiters
    bold_stripped_nodes = split_nodes_delimiter([initial_node], "**", TextType.BOLD)

    italic_stripped_nodes = split_nodes_delimiter(bold_stripped_nodes, "_", TextType.ITALIC)
    
    code_stripped_nodes = split_nodes_delimiter(italic_stripped_nodes, "`", TextType.CODE)

    # split images
    images_stripped_nodes = split_nodes_image(code_stripped_nodes)
    # split links
    final_nodes = split_nodes_link(images_stripped_nodes)
    
    return final_nodes