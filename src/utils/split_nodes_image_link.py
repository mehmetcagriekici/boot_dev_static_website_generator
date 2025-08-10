from utils.extract_markdown_images_links import extract_markdown_images, extract_markdown_links

from textnode import TextNode, TextType


# function to split text nodes based on image markdowns
def split_nodes_image(old_nodes):
    return split_nodes_common(old_nodes, extract_markdown_images, lambda alt, src: f"![{alt}]({src})", TextType.IMAGE)                      

# function to split text nodes based on link markdowns
def split_nodes_link(old_nodes):
    return split_nodes_common(old_nodes, extract_markdown_links, lambda text, href: f"[{text}]({href})",TextType.LINK )

def split_nodes_common(old_nodes, target_function, target_structure, target_type):
    new_nodes = []

    # iterate over the old nodes
    for node in old_nodes:
        # skip non text nodes
        if node.text_type != TextType.TEXT:
            # add it directly to the new nodes
            new_nodes.append(node)
            continue

        # control text -> target removed
        temp_text = node.text

        # loop over the temp text until there are no targets in it
        while True:
            targets = target_function(temp_text)
            # break condition
            if not targets:
                # add the leftover to the new nodes as a pure text node
                if temp_text:
                    new_nodes.append(TextNode(temp_text, TextType.TEXT))
                break
            
            # handle the first target
            target = targets[0]
            # will be used to split the temp text
            target_demiliter = target_structure(target[0], target[1])
            # split once -> [left_text?, rest]
            texts = temp_text.split(target_demiliter, 1)
            left_text = texts[0]
            rest_text = texts[1] if len(texts) > 1 else ""

            # if there is a left text add it to the new nodes as a pure text node
            if left_text:
                new_nodes.append(TextNode(left_text, TextType.TEXT))

            # add the target to the new nodes
            new_nodes.append(TextNode(target[0], target_type, target[1]))

            # update the temp text
            temp_text = rest_text

    return new_nodes