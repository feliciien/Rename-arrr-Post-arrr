"""
Main entry point for Rename-arrr
"""
import sys
import os
import logging
from dotenv import load_dotenv
from gui.main_window import main as gui_main

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rename_arrr.log'),
        logging.StreamHandler()
    ]
)

def main():
    """Main entry point"""
    # Load environment variables
    load_dotenv()
    
    # Start GUI
    gui_main()

if __name__ == "__main__":
    main()
