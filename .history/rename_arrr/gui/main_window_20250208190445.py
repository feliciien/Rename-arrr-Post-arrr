"""
Main GUI window for the Rename-arrr application
"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QPushButton, QLabel, QFileDialog, QProgressBar,
                           QTextEdit, QComboBox, QHBoxLayout, QCheckBox,
                           QListWidget, QToolBar, QAction)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import asyncio
import logging
from typing import Dict, List

from rename_arrr.core.renamer import MediaRenamer
from rename_arrr.core.scrapers.movie_scraper import MovieTVScraper

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set logging level to INFO for production
if os.getenv('ENV') == 'production':
    logger.setLevel(logging.INFO)

class RenameWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(list)
    log = pyqtSignal(str)
    
    def __init__(self, files: List[str], scraper: MovieTVScraper):
        super().__init__()
        self.files = files
        self.renamer = MediaRenamer()
        self.scraper = scraper
        
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
                    try:
                        # Fetch additional metadata
                        if metadata['type'] == 'movie':
                            movie_metadata = self.scraper.search_movie(metadata['title'])
                            if movie_metadata:
                                metadata.update(movie_metadata)
                        elif metadata['type'] == 'tv':
                            tv_metadata = self.scraper.search_tv_show(metadata['title'])
                            if tv_metadata:
                                metadata.update(tv_metadata)
                        
                        new_path = loop.run_until_complete(self.renamer.rename_file(file_path, metadata))
                        if new_path:
                            results.append({
                                'original': file_path,
                                'new': new_path,
                                'metadata': metadata
                            })
                    except Exception as rename_error:
                        logger.error(f"Failed to rename file {file_path}: {rename_error}")
                
                self.progress.emit(int(i / total * 100))
            
            # Clean up
            loop.close()
            
            self.finished.emit(results)
            
        except Exception as e:
            logger.error(f"Error during renaming: {str(e)}")
            self.log.emit(f"Error: {str(e)}")
            self.finished.emit([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rename-arrr")
        self.setMinimumSize(800, 600)
        
        # Create toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Add actions to toolbar
        add_files_action = QAction("Add Files", self)
        add_files_action.triggered.connect(self.add_files)
        toolbar.addAction(add_files_action)
        
        clear_action = QAction("Clear List", self)
        clear_action.triggered.connect(self.clear_files)
        toolbar.addAction(clear_action)
        
        toolbar.addSeparator()
        
        nfo_action = QAction("Generate NFO", self)
        nfo_action.triggered.connect(self.generate_nfo)
        toolbar.addAction(nfo_action)
        
        theme_action = QAction("Toggle Theme", self)
        theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(theme_action)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create file selection area
        file_layout = QVBoxLayout()
        
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
        self.media_type.addItems(["Auto Detect", "Movies", "TV Shows", "Anime", "Music"])
        options_layout.addWidget(QLabel("Media Type:"))
        options_layout.addWidget(self.media_type)
        
        # Scraper selection
        self.scraper_label = QLabel("Metadata Source:")
        self.scraper_combo = QComboBox()
        self.scraper_combo.addItems(["TVDB", "AniDB", "PosterDB", "MusicBrainz"])
        options_layout.addWidget(self.scraper_label)
        options_layout.addWidget(self.scraper_combo)
        
        # Add batch processing options
        self.batch_checkbox = QCheckBox("Batch Processing")
        options_layout.addWidget(self.batch_checkbox)
        
        layout.addLayout(options_layout)
        
        # Create progress bar
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # Create log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.start_btn = QPushButton("Start Renaming")
        self.start_btn.clicked.connect(self.start_renaming)
        layout.addWidget(self.start_btn)
        
        # Initialize worker
        self.worker = None
        self.scraper = MovieTVScraper(tmdb_api_key='YOUR_TMDB_API_KEY')
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.styleSheet() == "":
            # Apply dark theme
            self.setStyleSheet("""
                QWidget {
                    background-color: #2e2e2e;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #444444;
                    color: #ffffff;
                }
                QProgressBar {
                    background-color: #444444;
                    color: #ffffff;
                }
                QTextEdit {
                    background-color: #444444;
                    color: #ffffff;
                }
                QListWidget {
                    background-color: #444444;
                    color: #ffffff;
                }
            """)
        else:
            # Revert to light theme
            self.setStyleSheet("")

    def add_files(self):
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
        self.worker = RenameWorker(files, self.scraper)
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

    def generate_nfo(self):
        """Generate NFO files for selected media"""
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if not files:
            self.log_output.append("Please add some files first")
            return

        for file_path in files:
            # Generate NFO content
            nfo_content = "<nfo>\n"
            nfo_content += f"  <title>{os.path.basename(file_path)}</title>\n"
            nfo_content += "</nfo>\n"

            # Save NFO file
            nfo_path = os.path.splitext(file_path)[0] + ".nfo"
            with open(nfo_path, 'w') as nfo_file:
                nfo_file.write(nfo_content)
            self.log_output.append(f"Generated NFO for {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
