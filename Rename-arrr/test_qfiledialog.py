from PyQt5.QtWidgets import QApplication, QFileDialog
import sys

def test_file_dialog():
    app = QApplication(sys.argv)
    folder = QFileDialog.getExistingDirectory(None, 'Select Folder')
    if folder:
        print(f"Selected folder: {folder}")
    else:
        print("No folder selected.")

if __name__ == "__main__":
    test_file_dialog()