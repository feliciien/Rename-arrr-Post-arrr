# utils.py

import logging
import os

def setup_logger():
    """
    Sets up a logger that logs messages to 'app.log'.
    """
    logger = logging.getLogger('RenameArrrLogger')
    logger.setLevel(logging.DEBUG)

    # Create handlers
    log_file = os.path.join(os.path.dirname(__file__), 'app.log')
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)  # Only output errors to the console

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger