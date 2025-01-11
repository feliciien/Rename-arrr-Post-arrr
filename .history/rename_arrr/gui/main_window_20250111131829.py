"""
Main GUI window for the Rename-arrr application
"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QPushButton, QLabel, QFileDialog, QProgressBar,
                           QTextEdit, QComboBox, QHBoxLayout, QCheckBox,
                           QListWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import asyncio
import logging
from typing import Dict, List

from rename_arrr.core.renamer import MediaRenamer

logger = logging.getLogger(__name__)

class RenameWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)
    log = pyqtSignal(str)
    
    def __init__(self, files: List[str]):
        super().__init__()
        self.files = files
        self.renamer = MediaRenamer()
        
    def run(self):
        """Run the renaming process"""
        try:
            # Get event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            results = []
            total = len(self.files)
            
            for i, file_path in enumerate(self.files, 1):
                # Process single file
                info = self.renamer._extract_info_from_filename(os.path.basename(file_path))
                if info:
                    metadata = {
                        'title': info['title'],
                        'year': info.get('year'),
                        'type': info['type'],
                        'season': info.get('season'),
                        'episode': info.get('episode'),
                        'artist': info.get('artist'),
                        'track': info.get('track')
                    }
                    new_path = loop.run_until_complete(self.renamer.rename_file(file_path, metadata))
                    if new_path:
                        results.append({
                            'original': file_path,
                            'new': new_path,
                            'metadata': metadata
                        })
                
                self.progress.emit(int(i / total * 100))
            
            # Clean up
            loop.close()
            
            self.finished.emit(results)
            
        except Exception as e:
            self.log.emit(f"Error: {str(e)}")
            self.finished.emit([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rename-arrr")
        self.setMinimumSize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create file selection area
        file_layout = QVBoxLayout()
        
        # Add file selection buttons
        btn_layout = QHBoxLayout()
        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.clicked.connect(self.add_files)
        self.clear_btn = QPushButton("Clear List")
        self.clear_btn.clicked.connect(self.clear_files)
        btn_layout.addWidget(self.add_files_btn)
        btn_layout.addWidget(self.clear_btn)
        file_layout.addLayout(btn_layout)
        
        # Add file list with drag-and-drop functionality
        self.file_list = QListWidget()
        self.file_list.setAcceptDrops(True)
        self.file_list.setDragDropMode(QListWidget.InternalMove)
        self.file_list.dragEnterEvent = self.dragEnterEvent
        self.file_list.dropEvent = self.dropEvent
        file_layout.addWidget(self.file_list)
        
        layout.addLayout(file_layout)
        
        # Create options
        options_layout = QHBoxLayout()
        
        # Media type selection
        self.media_type = QComboBox()
        self.media_type.addItems(["Auto Detect", "Movies", "TV Shows", "Music"])
        options_layout.addWidget(QLabel("Media Type:"))
        options_layout.addWidget(self.media_type)
        
        # Scraper selection
        self.scraper_label = QLabel("Scraper:")
        self.scraper_combo = QComboBox()
        self.scraper_combo.addItems(["AniDB", "TVDB", "PosterDB"])
        options_layout.addWidget(self.scraper_label)
        options_layout.addWidget(self.scraper_combo)
        
        layout.addLayout(options_layout)
        
        # Create progress bar
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # Create log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
        
        # Create start button
        self.start_btn = QPushButton("Start Renaming")
        self.start_btn.clicked.connect(self.start_renaming)
        layout.addWidget(self.start_btn)
        
        # Initialize worker
        self.worker = None
        
    def dragEnterEvent(self, event):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop event"""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path:
                self.file_list.addItem(file_path)
                self.log_output.append(f"Added {file_path} via drag-and-drop")

        """Open file selection dialog"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Media Files",
            "",
            "Media Files (*.mp3 *.mp4 *.mkv *.avi *.mov *.flac);;All Files (*.*)"
        )
        if files:
            self.file_list.addItems(files)
            self.log_output.append(f"Added {len(files)} files to the list")
            
    def clear_files(self):
        """Clear the file list"""
        self.file_list.clear()
        self.log_output.append("Cleared file list")
            
    def start_renaming(self):
        """Start the renaming process"""
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if not files:
            self.log_output.append("Please add some files first")
            return
            
        # Disable UI elements
        self.start_btn.setEnabled(False)
        self.add_files_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)
        self.progress.setValue(0)
        
        # Create and start worker
        self.worker = RenameWorker(files)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.process_finished)
        self.worker.log.connect(self.log_message)
        self.worker.start()
        
    def update_progress(self, value):
        """Update progress bar"""
        self.progress.setValue(value)
        
    def process_finished(self, results):
        """Handle process completion"""
        # Re-enable UI elements
        self.start_btn.setEnabled(True)
        self.add_files_btn.setEnabled(True)
        self.clear_btn.setEnabled(True)
        
        # Log results
        if results:
            self.log_output.append("\nRenaming completed successfully!")
            for result in results:
                self.log_output.append(f"\nRenamed: {result['original']} -> {result['new']}")
        else:
            self.log_output.append("\nNo files were renamed")
            
    def log_message(self, message):
        """Add message to log output"""
        self.log_output.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
