import logging
import os

def setup_logger(log_dir="logs", log_file="rename_arrr.log"):
    """
    Sets up a logger with both console and file handlers.

    Args:
        log_dir (str): Directory where the log file will be stored.
        log_file (str): Name of the log file.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("RenameArrr")
    logger.setLevel(logging.DEBUG)

    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # File handler
    file_handler = logging.FileHandler(log_path, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger