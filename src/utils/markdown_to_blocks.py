def markdown_to_blocks(markdown):
    # list to store final blocks
    result = []
    blocks = markdown.split("\n\n")

    # iterate over the blocks
    for block in blocks:
        # trim the block
        trimmed_block = block.strip()
        # filter out the possible empty blocks
        if trimmed_block:                    
            # add block to the result    
            result.append(trimmed_block)
       
    return result