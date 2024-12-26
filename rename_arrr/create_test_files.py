import os

def create_test_files(folder_path):
    """
    Creates sample test files in the specified folder for testing purposes.
    """
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # List of sample file names to create
    sample_files = {
        "movies": [
            "Inception.2010.1080p.BluRay.mp4",
            "The.Matrix.1999.720p.WEB-DL.mkv",
            "Interstellar_2014_4K_BluRay.avi",
            "The.Godfather.1972.REMASTERED.mov",
            "Parasite-2019-1080p.mp4",
            "Random.Documentary.2022.1080p.mkv",
            "TestFile_Without_Year.mp4"
        ],
        "tv_shows": [
            "Breaking.Bad.S01E01.720p.WEB-DL.mkv",
            "Game.of.Thrones.S08E06.1080p.HDTV.mp4",
            "The.Office.US.S03E15.BluRay.avi",
            "Stranger.Things.S04E01.4K.WEB-DL.mkv",
            "Better.Call.Saul.S06E13.1080p.AMZN.mp4",
            "The.Last.of.Us.S01E09.HDR.2160p.mkv"
        ],
        "anime": [
            "[HorribleSubs] One Piece - 1000 [1080p].mkv",
            "[Subsplease] Attack on Titan - 75 [720p].mp4",
            "[Erai-raws] Demon Slayer - 26 [1080p].mkv",
            "[Judas] Jujutsu Kaisen - 24 [4K].mp4",
            "[Commie] Steins;Gate - 24 [BD 1080p].mkv",
            "My Hero Academia S05E25 [1080p].mp4"
        ]
    }

    # Create subdirectories and files
    for category, files in sample_files.items():
        category_path = os.path.join(folder_path, category)
        os.makedirs(category_path, exist_ok=True)
        
        for file_name in files:
            file_path = os.path.join(category_path, file_name)
            with open(file_path, "w") as f:
                f.write("")  # Create an empty file
            print(f"Created test file: {file_path}")

    # Notify user when done
    total_files = sum(len(files) for files in sample_files.values())
    print(f"\nCreated {total_files} test files across {len(sample_files)} categories in {folder_path}.")

if __name__ == "__main__":
    # Define the folder path for test files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    test_folder = os.path.join(project_root, "test_files")
    
    # Create test files
    create_test_files(test_folder)