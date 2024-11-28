def populate_file_list(self, folder_path):
    """
    Populates the file list widget with all files from the selected folder.
    """
    self.file_list.clear()
    print(f"DEBUG: Populating file list for folder: {folder_path}")

    if not os.path.exists(folder_path):
        print(f"DEBUG: Folder does not exist: {folder_path}")
        QMessageBox.critical(self, 'Error', f"The folder does not exist: {folder_path}")
        return

    try:
        files_found = False
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            print(f"DEBUG: Checking file: {full_path}")
            if os.path.isfile(full_path):  # Ensure it's a file
                print(f"DEBUG: Adding file: {filename}")
                self.file_list.addItem(QListWidgetItem(filename))
                files_found = True

        if not files_found:
            print(f"DEBUG: No files found in folder: {folder_path}")
            QMessageBox.information(self, 'No Files Found', 'No files found in the selected folder.')
    except Exception as e:
        print(f"DEBUG: Error reading folder: {e}")
        QMessageBox.critical(self, 'Error', f"An error occurred while reading the folder: {e}")