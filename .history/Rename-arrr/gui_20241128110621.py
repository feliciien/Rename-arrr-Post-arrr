import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QLineEdit, QMessageBox, QProgressBar, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import QThread, pyqtSignal
from renamer import rename_files, extract_title_year
from utils import setup_logger

# Set up the logger
logger = setup_logger()

class RenameThread(QThread):
    progress_update = pyqtSignal(int)
    file_renamed = pyqtSignal(str, str)
    error_occurred = pyqtSignal(str)

    def __init__(self, folder_path, files):
        super().__init__()
        self.folder_path = folder_path
        self.files = files
        self._is_running = True

    def run(self):
        total_files = len(self.files)
        for index, filename in enumerate(self.files, start=1):
            if not self._is_running:
                break
            try:
                title, year = extract_title_year(filename)
                new_filename = rename_files(self.folder_path, filename, title, year)
                self.file_renamed.emit(filename, new_filename)
            except Exception as e:
                error_message = f"Failed to rename '{filename}': {e}"
                logger.error(error_message)
                self.error_occurred.emit(error_message)
            progress = int((index / total_files) * 100)
            self.progress_update.emit(progress)

    def stop(self):
        self._is_running = False

class RenameArrrGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.rename_thread = None

    def init_ui(self):
        self.setWindowTitle('Rename...arrr')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Folder selection
        self.label = QLabel('Select the folder containing files:', self)
        layout.addWidget(self.label)

        self.path_input = QLineEdit(self)
        layout.addWidget(self.path_input)

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)

        # File list
        self.file_list_label = QLabel('Files in Selected Folder:', self)
        layout.addWidget(self.file_list_label)

        self.file_list = QListWidget(self)
        layout.addWidget(self.file_list)

        # Rename button
        self.rename_button = QPushButton('Rename Files', self)
        self.rename_button.clicked.connect(self.rename_files_action)
        layout.addWidget(self.rename_button)

        # Progress bar
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            print(f"DEBUG: Selected folder: {folder}")  # Debug output
            self.path_input.setText(folder)
            self.populate_file_list(folder)

    def populate_file_list(self, folder_path):
        """
        Populates the file list widget with all files from the selected folder.
        """
        self.file_list.clear()
        logger.info(f"Populating file list for folder: {folder_path}")
        print(f"DEBUG: Populating file list for folder: {folder_path}")  # Debug output

        if not os.path.exists(folder_path):
            logger.error(f"Folder does not exist: {folder_path}")
            QMessageBox.critical(self, 'Error', f"The folder does not exist: {folder_path}")
            return

        try:
            files_found = False
            for filename in os.listdir(folder_path):
                full_path = os.path.join(folder_path, filename)
                print(f"DEBUG: Checking file: {full_path}")  # Debug output
                if os.path.isfile(full_path):  # Only add files, skip directories
                    print(f"DEBUG: Adding file: {filename}")  # Debug output
                    self.file_list.addItem(QListWidgetItem(filename))
                    files_found = True

            if not files_found:
                logger.warning(f"No files found in: {folder_path}")
                QMessageBox.information(self, 'No Files Found', 'No files found in the selected folder.')
        except Exception as e:
            logger.error(f"Error populating file list: {e}")
            QMessageBox.critical(self, 'Error', f"An error occurred while reading the folder: {e}")

    def rename_files_action(self):
        folder_path = self.path_input.text()
        if not folder_path:
            QMessageBox.warning(self, 'Input Error', 'Please select a folder.')
            return

        files_to_rename = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if not files_to_rename:
            QMessageBox.information(self, 'No Files', 'No files found to rename.')
            return

        self.rename_button.setEnabled(False)
        self.browse_button.setEnabled(False)

        self.rename_thread = RenameThread(folder_path, files_to_rename)
        self.rename_thread.progress_update.connect(self.update_progress)
        self.rename_thread.file_renamed.connect(self.update_file_list)
        self.rename_thread.error_occurred.connect(self.show_error)
        self.rename_thread.finished.connect(self.rename_finished)
        self.rename_thread.start()

    def update_progress(self, value):
        self.progress.setValue(value)

    def update_file_list(self, old_filename, new_filename):
        for index in range(self.file_list.count()):
            item = self.file_list.item(index)
            if item.text() == old_filename:
                item.setText(new_filename)
                break

    def show_error(self, message):
        QMessageBox.critical(self, 'Error', message)

    def rename_finished(self):
        self.rename_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        QMessageBox.information(self, 'Renaming Completed', 'File renaming process has completed.')
        self.progress.setValue(0)

# FIXED INDENTATION ISSUE
def main():
    app = QApplication(sys.argv)
    gui = RenameArrrGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()