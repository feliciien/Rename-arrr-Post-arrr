import os

def create_test_files(folder_path):
    """
    Creates sample test files in the specified folder for testing purposes.
    """
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # List of sample file names to create
    sample_files = [
        "Inception.2010.1080p.BluRay.mp4",
        "The.Matrix.1999.720p.WEB-DL.mkv",
        "Interstellar_2014_4K_BluRay.avi",
        "The.Godfather.1972.REMASTERED.mov",
        "Parasite-2019-1080p.mp4",
        "Random.Documentary.2022.1080p.mkv",
        "TestFile_Without_Year.mp4"
    ]

    # Create the sample files
    for file_name in sample_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w") as f:
            f.write("")  # Create an empty file
        print(f"Created test file: {file_path}")

    # Notify user when done
    print(f"Created {len(sample_files)} test files in {folder_path}.")

if __name__ == "__main__":
    # Define the folder path for test files
    test_folder = r"C:\Mac\Home\Desktop\Rename-arrr-Post-arrr\tests"
    
    # Create test files
    create_test_files(test_folder)