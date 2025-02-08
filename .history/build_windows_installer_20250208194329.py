import os
import PyInstaller.__main__

# Get the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths for additional files
license_file = os.path.join(base_dir, 'rename_arrr', 'license_manager.py')

# PyInstaller configuration
PyInstaller.__main__.run([
    '--name=RenameArrr',
    '--onefile',
    '--windowed',
    '--add-data={}{}*{}'.format(os.path.join(base_dir, 'rename_arrr'), os.pathsep, os.pathsep),
    '--hidden-import=PyQt5',
    '--hidden-import=requests',
    '--hidden-import=beautifulsoup4',
    '--hidden-import=aiohttp',
    '--hidden-import=lxml',
    '--hidden-import=cloudscraper',
    '--hidden-import=selenium',
    '--hidden-import=playwright',
    '--hidden-import=python-dotenv',
    '--hidden-import=aiofiles',
    '--hidden-import=pyyaml',
    '--hidden-import=tqdm',
    '--hidden-import=tvdb-v4-official',
    '--hidden-import=musicbrainzngs',
    '--hidden-import=tmdbv3api',
    '--hidden-import=imdbpy',
    'run_gui.py',
])
