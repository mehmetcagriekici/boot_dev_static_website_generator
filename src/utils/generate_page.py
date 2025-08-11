import os
from utils.markdown_to_html_node import markdown_to_html_node
from utils.extract_title import extract_title

def generate_page(from_path, template_path, dest_path, base_path):
    # Print a message like "Generating page from from_path to dest_path using template_path".
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file at from_path and store the contents in a variable.
    markdown_file = open(from_path)
    markdown = markdown_file.read()

    # Read the template file at template_path and store the contents in a variable.
    template_file = open(template_path)
    template = template_file.read()

    # Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
    html_string = markdown_to_html_node(markdown).to_html()

    # Use the extract_title function to grab the title of the page.
    page_title = extract_title(markdown)

    # Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    new_template = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_string).replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')

    # Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.
    if not os.path.dirname(dest_path):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as file:
        file.write(new_template)
    

    
    
