import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    #
    node = HTMLNode(tag="button", value="move right", props={"onclick":"moveright"})
    node2 = HTMLNode(tag="p", value="success")
    node3 = HTMLNode(tag="a", props={"href":"https://boot.dev", "target": "_blank"})
    
    #
    leafNode = LeafNode("p", "Hello, world!")
    leafNode2 = LeafNode("button", "click here", props={"onclick": "onclick"})
    leafNode3 = LeafNode("a", "boot.dev", props={"href": "https://boot.dev", "target": "_blank"})

    #
    def test_props_to_html_one(self):
        self.assertEqual(self.node.props_to_html(), 'onclick="moveright"')
    
    def test_props_to_html_two(self):
        self.assertEqual(self.node2.props_to_html(), "")
    
    def test_props_to_html_three(self):
        self.assertEqual(self.node3.props_to_html(), 'href="https://boot.dev" target="_blank"')

    #
    def test_leaf_to_html_p(self):
        self.assertEqual(self.leafNode.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_button(self):
        self.assertEqual(self.leafNode2.to_html(), '<button onclick="onclick">click here</button>')

    def test_leaf_to_html_a(self):
        self.assertEqual(self.leafNode3.to_html(), '<a href="https://boot.dev" target="_blank">boot.dev</a>')

    #
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    # Boots
    def test_deeply_nested_madness(self):
        # 5 levels deep - like Russian nesting dolls!
        innermost = LeafNode("strong", "DEEP")
        level4 = ParentNode("em", [innermost])
        level3 = ParentNode("span", [level4])
        level2 = ParentNode("div", [level3])
        level1 = ParentNode("section", [level2])
    
        expected = "<section><div><span><em><strong>DEEP</strong></em></span></div></section>"
        self.assertEqual(level1.to_html(), expected)

    def test_sibling_chaos(self):
        # Multiple children at each level
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode(None, " and ")
        leaf3 = LeafNode("i", "Italic")
    
        child1 = ParentNode("span", [leaf1, leaf2])
        child2 = ParentNode("div", [leaf3])
        child3 = LeafNode("br", "")  # self-closing
    
        parent = ParentNode("p", [child1, child2, child3])
    
        expected = "<p><span><b>Bold</b> and </span><div><i>Italic</i></div><br /></p>"
        self.assertEqual(parent.to_html(), expected)

    def test_the_kitchen_sink(self):
        # Everything at once - props, nesting, multiple children
        deep_leaf = LeafNode("code", "print('hello')")
        deep_parent = ParentNode("pre", [deep_leaf], {"class": "code-block"})
    
        text1 = LeafNode(None, "Here's some code: ")
        text2 = LeafNode(None, " Pretty neat!")
        link = LeafNode("a", "Click me", {"href": "https://boot.dev"})
    
        container = ParentNode("div", [text1, deep_parent, text2, link], {"id": "main"})
    
        expected = '<div id="main">Here\'s some code: <pre class="code-block"><code>print(\'hello\')</code></pre> Pretty neat!<a href="https://boot.dev">Click me</a></div>'
        self.assertEqual(container.to_html(), expected)

    def test_empty_leaf_sandwich(self):
        # Mix of empty and non-empty leaf nodes
        empty1 = LeafNode(None, "")
        content = LeafNode("span", "Content")
        empty2 = LeafNode(None, "")
    
        parent = ParentNode("div", [empty1, content, empty2])
        expected = "<div><span>Content</span></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_recursive_nightmare(self):
        # ParentNodes all the way down with mixed content
        bottom = LeafNode("small", "tiny text")
        level3 = ParentNode("sup", [bottom])
        level2 = ParentNode("strong", [LeafNode(None, "LOUD "), level3])
        level1 = ParentNode("em", [LeafNode(None, "emphasis with "), level2])
        top = ParentNode("p", [LeafNode(None, "This is "), level1, LeafNode(None, "!")])
    
        expected = "<p>This is <em>emphasis with <strong>LOUD <sup><small>tiny text</small></sup></strong></em>!</p>"
        self.assertEqual(top.to_html(), expected)

    #
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "some_link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "some_link"})
    
    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "some_src")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "some_src", "alt": "This is an image node"})

if __name__ == "__main__":
    unittest.main()