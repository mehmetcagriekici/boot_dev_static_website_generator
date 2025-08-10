import unittest

from textnode import TextNode, TextType
from utils.split_nodes_delimiter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    # no delimiter
    def test_no_delimiter(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "", TextType.TEXT), [node])
    
    # unmatched delimiter
    def test_unmatched_delimiter(self):
        node = TextNode("This is *italic without a close", TextType.TEXT)

        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(cm.exception.args[0], "Unmatched delimiters, invalid syntax!")

    # multiple inline elements
    def test_multiple_inline_elements(self):
        node = TextNode("Mix *one* and *two* colors", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.BOLD), 
        [TextNode("Mix ", TextType.TEXT), TextNode("one", TextType.BOLD), TextNode(" and ", TextType.TEXT), TextNode("two", TextType.BOLD), TextNode(" colors", TextType.TEXT)])

    # delimiters at edges
    def test_delimiters_at_edges(self):
        node = TextNode("*start* or at the *end*", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.BOLD), [TextNode("start", TextType.BOLD), TextNode(" or at the ", TextType.TEXT), TextNode("end", TextType.BOLD)])

if __name__ == "__main__":
    unittest.main()