# Rename-arrr/gui.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QLineEdit, QMessageBox, QProgressBar
)
from renamer import rename_files

class RenameArrrGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Rename...arrr')
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        self.label = QLabel('Select the folder containing media files:', self)
        layout.addWidget(self.label)
        
        self.path_input = QLineEdit(self)
        layout.addWidget(self.path_input)
        
        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)
        
        self.rename_button = QPushButton('Rename Files', self)
        self.rename_button.clicked.connect(self.rename_files_action)
        layout.addWidget(self.rename_button)
        
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        
        self.setLayout(layout)
    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            self.path_input.setText(folder)
    
    def rename_files_action(self):
        folder_path = self.path_input.text()
        if not folder_path:
            QMessageBox.warning(self, 'Input Error', 'Please select a folder.')
            return
        try:
            renamed_files = rename_files(folder_path)
            self.progress.setValue(100)
            QMessageBox.information(
                self, 'Success', f'Renamed {len(renamed_files)} files successfully.'
            )
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = RenameArrrGUI()
    gui.show()
    sys.exit(app.exec_())