import re

r_images = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
r_links = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

# takes a raw markdown text and returns a tuple (alt, src)
def extract_markdown_images(text):
    return re.findall(r_images, text)

# returns a tuple (anchor text, url)
def extract_markdown_links(text):
    return re.findall(r_links, text)