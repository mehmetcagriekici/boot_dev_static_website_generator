from enum import Enum
import re

# supported markdown types
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
         # Headings start with 1-6 # characters, followed by a space and then the heading text.
        if re.fullmatch(r"^(#{1,6})\s+(.*)$", block):
            return BlockType.HEADING
        
        # Code blocks must start with 3 backticks and end with 3 backticks.
        if re.fullmatch(r'```(?:[ \t]*\w+)?[\s\S]*?```', block):
            return BlockType.CODE
        
        # Every line in a quote block must start with a > character.
        if re.fullmatch(r"^(>.*\n?)*$", block):
            return BlockType.QUOTE
        
         # Every line in an unordered list block must start with a - character, followed by a space.
        if re.fullmatch(r'(- .*(?:\r?\n)?)+', block):
            return BlockType.UNORDERED_LIST
        
         # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
        if is_ordered_list(block):
            return BlockType.ORDERED_LIST

        # If none of the above conditions are met, the block is a normal paragraph.
        return BlockType.PARAGRAPH
        
# helper function to check if the list correctly ordered
def is_ordered_list(block):
    lines = block.split("\n")
    # loop over the lines
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}"):
            return False
    
    return re.fullmatch(r'(?:\d+\. .*(?:\r?\n)?)+', block)
    

