from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # store the new nodes
    new_nodes = []

    # loop over the given nodes
    for old_node in old_nodes:
        # only text type text nodes with a delimiter
        if not delimiter or delimiter not in old_node.text or not old_node.text_type or old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        else:
            # store the parts after split
            new_parts = []
                
            # split the parts
            parts = old_node.text.split(delimiter)

            # check for unmatched delimiters
            if len(parts) % 2 == 0:
                raise Exception("Unmatched delimiters, invalid syntax!") 

            # check if the index is even or odd - text/delimiter
            for i in range(len(parts)):
                if i % 2 == 0:
                    # text
                    if parts[i].strip():
                        new_parts.append(TextNode(parts[i], TextType.TEXT))
                else:
                    # check if delimiter is empty
                    if parts[i].strip():      
                        new_parts.append(TextNode(parts[i], text_type))
                    
            # extend the new nodes
            new_nodes.extend(new_parts)

    return new_nodes

       
        