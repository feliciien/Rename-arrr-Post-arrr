import os
import shutil
import unittest
from renamer import extract_title_year, rename_files

class TestRenamer(unittest.TestCase):
    def setUp(self):
        # Create a temporary test folder
        self.test_folder = "test_files_temp"
        os.makedirs(self.test_folder, exist_ok=True)

        # Create test files
        self.files = [
            "Inception.2010.1080p.BluRay.mp4",
            "Parasite.2019.1080p.mp4",
            "The.Matrix.1999.720p.WEB-DL.mkv",
            "Random.Documentary.2022.1080p.mkv",
            "TestFile_Without_Year.mp4"
        ]
        for file in self.files:
            open(os.path.join(self.test_folder, file), 'w').close()

    def tearDown(self):
        # Clean up test folder
        shutil.rmtree(self.test_folder)

    def test_extract_title_year(self):
        self.assertEqual(extract_title_year("Inception.2010.1080p.BluRay.mp4"), ("Inception", "2010"))
        self.assertEqual(extract_title_year("TestFile_Without_Year.mp4"), ("TestFile_Without_Year", "Unknown"))

    def test_rename_files(self):
        renamed_files = []
        for file in self.files:
            title, year = extract_title_year(file)
            new_filename = rename_files(self.test_folder, file, title, year)
            renamed_files.append(new_filename)

        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "Inception (2010).mp4")))
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "Parasite (2019).mp4")))
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "The.Matrix (1999).mkv")))
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "Random.Documentary (2022).mkv")))
        self.assertTrue(os.path.exists(os.path.join(self.test_folder, "TestFile_Without_Year (Unknown).mp4")))

if __name__ == "__main__":
    unittest.main()