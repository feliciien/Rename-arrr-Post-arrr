# Rename-arrr/utils.py

import logging
import os

def setup_logger():
    """
    Sets up the logger for the application.
    
    :return: Configured logger instance.
    """
    logger = logging.getLogger('Rename-arrr')
    logger.setLevel(logging.INFO)
    
    # Create log directory if it doesn't exist
    log_directory = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_directory, exist_ok=True)
    
    # Create file handler
    log_file = os.path.join(log_directory, 'rename_arrr.log')
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    
    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Create formatter and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger