from functools import reduce
from textnode import TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Implementation failed!")
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        return reduce(lambda attrs, key: attrs + f'{key}="{self.props[key]}" ' , self.props.keys(), "").strip()
    
    def __repr__(self):
        return f"tag: {self.tag + ", " if self.tag else ""}value: {self.value + ", " if self.value else ""}children: {self.children + ", " if self.children else ""}props: {self.props if self.props else ""}"
 
class LeafNode(HTMLNode):
    # self closing dict
    SELF_CLOSING_TAGS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 
    'link', 'meta', 'param', 'source', 'track', 'wbr'
    }

    # cannot have children, must have a value, might have props, if not tag, pure string
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
    
    def to_html(self):
        # check if the node has a value
        if self.value is None:
            raise ValueError("Leaf nodes must have values")
        
        # check if the node is just a text
        if not self.tag:
            return str(self.value)
        
        # check if node has props
        leaf_props = ""
        if self.props:
            leaf_props = self.props_to_html()

        #check if self closing
        if self.tag in self.SELF_CLOSING_TAGS:
            return f'<{self.tag}{" " + self.props_to_html() if self.props else ""} />'
        
        # leaf node HTML
        return f"<{self.tag}{" " + leaf_props if leaf_props else ""}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    # cannot have a value, must have children and a tag, might have props
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    # create HTML
    def to_html(self):
        # check if the node has a tag
        if not self.tag:
            raise ValueError("Parent nodes must have a tag")
        
        # check if the node has children
        if not self.children:
            raise ValueError("Parent nodes must have children")
        
        # check if node has props
        parent_props = ""
        if self.props:
            parent_props = self.props_to_html()

        # result of recursions nested inside the parent
        children_html = ""

        # iterate over each children and recursively call to_html on them, concatenating the results injecting them to the html result
        for child in self.children:
            children_html += child.to_html()

        # final result
        return f'<{self.tag}{" " + parent_props if parent_props else ""}>{children_html}</{self.tag}>'
    
# convert text node to an html node
def text_node_to_html_node(text_node, make_inline=True):
    # inline
    inline_text = text_node.text.replace("\n", " ") if make_inline else text_node.text
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=inline_text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=inline_text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=inline_text)
        case TextType.CODE:
            return LeafNode(tag="code", value=inline_text)
        case TextType.LINK:
            return LeafNode(tag="a", value=inline_text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt":inline_text})
        case _:
            raise Exception("Invalid text type!")