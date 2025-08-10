import os
from utils.generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # check if the dir_path_content is a directory
    if os.path.isfile(dir_path_content):
        # ensure that path exist
        os.makedirs(os.path.dirname(dest_dir_path), exist_ok=True)
        # generate a page
        generate_page(dir_path_content, template_path, dest_dir_path.replace(".md", ".html"))  
    else:
        # create a folder in the destination
        os.makedirs(dest_dir_path, exist_ok=True)
      
        # iterate over the directory contents
        content_list = os.listdir(dir_path_content)
        for content in content_list:
            new_content_path = os.path.join(dir_path_content, content)
            new_dest_path = os.path.join(dest_dir_path, content)

            # recursively call the function on the current folder
            generate_pages_recursive(new_content_path, template_path, new_dest_path)




    