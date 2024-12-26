import os

folder_path = r"C:\Mac\Home\Desktop\Rename-arrr-Post-arrr\tests"

if os.path.exists(folder_path):
    print(f"Listing files in folder: {folder_path}")
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            print(f"File: {filename}")
        else:
            print(f"Skipping non-file: {filename}")
else:
    print(f"Folder does not exist: {folder_path}")