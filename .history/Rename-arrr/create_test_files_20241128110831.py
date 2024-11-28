import os

def create_test_files(folder_path):
    """
    Creates sample test files in the specified folder for testing purposes.
    """
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    # List of sample file names to create
    sample_files = [
        "Inception.2010.1080p.BluRay.mp4",
        "The.Matrix.1999.720p.WEB-DL.mkv",
        "Interstellar_2014_4K_BluRay.avi",
        "The.Godfather.1972.REMASTERED.mov",
        "Parasite-2019-1080p.mp4"
    ]

    for file_name in sample_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w") as f:
            f.write("")  # Create an empty file
        print(f"Created test file: {file_path}")

if __name__ == "__main__":
    # Define the folder path
    test_folder = r"C:\Mac\Home\Desktop\Rename-arrr-Post-arrr\tests"
    create_test_files(test_folder)