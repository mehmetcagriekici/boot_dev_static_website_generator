import unittest

from textnode import TextNode, TextType
from utils.split_nodes_image_link import split_nodes_image, split_nodes_link

class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_image_at_the_end_of_the_text(self):
        node = TextNode("Some text ![alt](url)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([
            TextNode("Some text ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url")
        ], result)
    
    def test_multiple_images_with_no_texts_between(self):
        node = TextNode("![a](x)![b](y)![c](z)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([
            TextNode("a", TextType.IMAGE, "x"),
            TextNode("b", TextType.IMAGE, "y"),
            TextNode("c", TextType.IMAGE, "z"),
        ], result)

    def test_link_and_image_mixed(self):
        node = TextNode("Go to [site](url) for ![pic](img)", TextType.TEXT)
        result_link = split_nodes_link([node])
        result = split_nodes_image(result_link)
        self.assertListEqual([
            TextNode("Go to ", TextType.TEXT),
            TextNode("site", TextType.LINK, "url"),
            TextNode(" for ", TextType.TEXT),
            TextNode("pic", TextType.IMAGE, "img")
        ], result)

    def test_text_with_only_markdown_in_the_middle(self):
        node = TextNode("![img1](x) and then some words and [a link](y)", TextType.TEXT)
        result_link = split_nodes_link([node])
        result = split_nodes_image(result_link) 
        self.assertListEqual([
            TextNode("img1", TextType.IMAGE, "x"),
            TextNode(" and then some words and ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "y")
        ], result) 
            


if __name__ == "__main__":
    unittest.main()