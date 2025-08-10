import unittest
from utils.block_to_block_type import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        p = "This is a normal paragraph block!"
        result = block_to_block_type(p)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_heading(self):
        h = "### This is a heading!"
        result = block_to_block_type(h)
        self.assertEqual(result, BlockType.HEADING)

    def test_code(self):
        c = "``` this is some code here ```"
        result = block_to_block_type(c)
        self.assertEqual(result, BlockType.CODE)

    def test_quote(self):
        q = "> This is a quote" \
        "> This is another quote!"
        result = block_to_block_type(q)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unorderedlist(self):
        u = "- This is an unordered list" \
        "- With some elements" \
        "- And some other elements"
        result = block_to_block_type(u)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_orderedlist(self):
        o = "1. This is an ordered list" \
        "2. With some elements" \
        "3. And with some other elements"
        result = block_to_block_type(o)
        self.assertEqual(result, BlockType.ORDERED_LIST)

if __name__ == "__main__":
    unittest.main()