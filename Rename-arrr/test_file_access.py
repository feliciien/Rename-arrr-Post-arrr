import os

folder_path = r"C:\Mac\Home\Desktop\Rename-arrr-Post-arrr\tests"
print(f"Testing folder access: {folder_path}")

if not os.path.exists(folder_path):
    print("ERROR: Folder does not exist!")
else:
    print("Folder exists. Listing files:")
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            print(f"File detected: {filename}")
        else:
            print(f"Skipping non-file: {filename}")