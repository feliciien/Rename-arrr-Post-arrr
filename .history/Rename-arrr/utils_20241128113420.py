import logging
import os
import sys

def setup_logger():
    """
    Sets up the logger to log messages to a file and the console.
    """
    logger = logging.getLogger('RenameArrrLogger')
    logger.setLevel(logging.DEBUG)  # Capture all levels of log messages

    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # File handler - logs all messages
    log_file = os.path.join(log_dir, 'rename_arrr.log')
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(file_formatter)
    logger.addHandler(fh)

    # Console handler - logs DEBUG and above
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)

    return logger