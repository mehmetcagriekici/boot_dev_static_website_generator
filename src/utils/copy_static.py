import os, shutil

# Write a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public)
def copy_static():
    path_to_public = "public"
    path_to_static = "static"

    # It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
    if os.path.exists(path_to_public):
        # remove the public directory
        shutil.rmtree(path_to_public)
 
    # create a new public directory
    os.makedirs(path_to_public, exist_ok=True)

    # It should copy all files and subdirectories, nested files, etc.
    copy_static_content(path_to_static, path_to_public)


# recursive function to get the files from a folder
def copy_static_content(path, target):
    # get the path contents
    contents = os.listdir(path)
    # iterate over the contents
    for content in contents:
        # join the content path with the path
        content_path = os.path.join(path, content)
        # if content path is file copy it to the target
        if os.path.isfile(content_path):
            shutil.copy2(content_path, target)
            print(f"Copying {content_path} to {target}")
        else:
            # create a directory in the target
            dir_path = os.path.join(target, content)
            os.makedirs(dir_path, exist_ok=True)
            # recursively call the function with the updated target
            copy_static_content(content_path, dir_path)



