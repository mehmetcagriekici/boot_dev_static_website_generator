from utils.markdown_to_blocks import markdown_to_blocks

# extract_title("# Hello") should return "Hello" (strip the # and any leading or trailing whitespace)
def extract_title(markdown):
    h1 = None
    # It should pull the h1 header from the markdown file (the line that starts with a single #) and return it
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            h1 = block.split("# ")[1]

    # If there is no h1 header, raise an exception
    if not h1:
        raise Exception("The document must contain a h1 header!")
    
    return h1