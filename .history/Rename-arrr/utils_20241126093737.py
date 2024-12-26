import logging
import os

def setup_logger():
    """
    Sets up a logger for the Rename-arrr application.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a logger instance
    logger = logging.getLogger('Rename-arrr')
    logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG for detailed logs

    # Create a logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Log file path
    log_file = os.path.join(log_dir, 'rename_arrr.log')

    # Create a file handler for logging to a file
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)  # Log all levels to the file

    # Create a console handler for logging errors to the console
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)  # Only show ERROR level logs on the console

    # Create a formatter for log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Add the formatter to both handlers
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger