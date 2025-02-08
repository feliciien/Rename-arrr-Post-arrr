#!/usr/bin/env python3

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QAction, QToolBar, QFileDialog, QListWidget, QStatusBar,
    QMessageBox, QTabWidget
)
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Rename...arrr')
        self.setGeometry(100, 100, 800, 600)

        # Set window icon
        self.setWindowIcon(QIcon('icons/app_icon.png'))

        # Create the menu bar
        menubar = self.menuBar()

        # Add menus to the menu bar
        file_menu = menubar.addMenu('File')
        help_menu = menubar.addMenu('Help')

        # Add actions to the File menu
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create the toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Add toolbar actions
        open_action = QAction(QIcon('icons/open_folder.png'), 'Add Files', self)
        open_action.triggered.connect(self.open_files)
        toolbar.addAction(open_action)

        rename_action = QAction(QIcon('icons/rename.png'), 'Rename Files', self)
        rename_action.triggered.connect(self.rename_files)
        toolbar.addAction(rename_action)

        settings_action = QAction(QIcon('icons/settings.png'), 'Settings', self)
        settings_action.triggered.connect(self.open_settings)
        toolbar.addAction(settings_action)

        # Set up main layout
        main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(main_layout)

        # Add file list and preview area
        content_layout = QHBoxLayout()

        self.file_list = QListWidget()
        content_layout.addWidget(self.file_list)

        self.preview_label = QLabel('Preview will be shown here.')
        content_layout.addWidget(self.preview_label)

        main_layout.addLayout(content_layout)

        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Initialize License Manager
        from license_manager import LicenseManager
        self.license_manager = LicenseManager()

    def open_files(self):
        """Open file dialog to select files."""
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Media Files", "", "All Files (*)", options=options
        )
        if files:
            self.file_list.addItems(files)

    def rename_files(self):
        """Perform the rename operation."""
        if not self.license_manager.can_rename():
            QMessageBox.warning(
                self,
                'License Limit Reached',
                'You have reached the maximum number of renames allowed in the trial version.'
            )
            return

        # Placeholder for rename logic
        selected_files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if selected_files:
            # Simulate renaming files
            self.license_manager.increment_rename_count()
            QMessageBox.information(
                self,
                'Rename Successful',
                'Selected files have been renamed.'
            )
            self.status_bar.showMessage(f'Renamed {len(selected_files)} files.')
        else:
            QMessageBox.warning(
                self,
                'No Files Selected',
                'Please add files to rename.'
            )

    def open_settings(self):
        """Open the settings dialog."""
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.setGeometry(150, 150, 600, 400)

        # Create tabs for settings categories
        tabs = QTabWidget()
        tabs.addTab(GeneralSettingsTab(), 'General')
        tabs.addTab(AdvancedSettingsTab(), 'Advanced')
        tabs.addTab(LicenseSettingsTab(), 'License')

        self.setCentralWidget(tabs)

class GeneralSettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('General settings will be implemented here.')
        layout.addWidget(label)
        self.setLayout(layout)

class AdvancedSettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('Advanced settings will be implemented here.')
        layout.addWidget(label)
        self.setLayout(layout)

class LicenseSettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.license_label = QLabel('License status will be shown here.')
        layout.addWidget(self.license_label)
        self.setLayout(layout)
        self.update_license_status()

    def update_license_status(self):
        from license_manager import LicenseManager
        lm = LicenseManager()
        if lm.unlimited:
            self.license_label.setText('License Status: Activated (Unlimited Renames)')
        else:
            remaining = lm.remaining_renames()
            self.license_label.setText(f'License Status: Trial ({remaining} renames remaining)')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
