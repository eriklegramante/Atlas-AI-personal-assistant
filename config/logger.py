import logging
from logging.handlers import RotatingFileHandler
from config.settings import settings

LOGS_DIR = settings.BASE_PATH / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE_PATH = LOGS_DIR / "atlas.log"


class CustomFormatter(logging.Formatter):
    """A custom ANSI-colorized logging formatter optimized for Linux terminal readability.

    This class overrides the standard logging formatter to dynamically inject
    terminal escape sequences based on the severity level of the log record.

    Attributes:
        grey (str): ANSI escape sequence for debug log colorization.
        cyan (str): ANSI escape sequence for informational log colorization.
        yellow (str): ANSI escape sequence for warning log colorization.
        red (str): ANSI escape sequence for error log colorization.
        bold_red (str): ANSI escape sequence for critical systemic failures.
        reset (str): ANSI escape sequence to restore default terminal styling.
        log_format (str): The structural format template for string messages.
        FORMATS (dict): Maps logging levels to their respective colorized formats.
    """

    grey = "\x1b[38;20m"
    cyan = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    log_format = (
        "%(asctime)s - [%(levelname)s] - (%(filename)s:%(lineno)d) - %(message)s"
    )

    FORMATS = {
        logging.DEBUG: grey + log_format + reset,
        logging.INFO: cyan + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Formats a LogRecord instance into a color-coded string.

        Args:
            record (logging.LogRecord): The raw log record populated by the framework.

        Returns:
            str: The fully evaluated text line containing timestamps and severity metadata.
        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logger() -> logging.Logger:
    """Configures and initializes the ATLAS central logging architecture.

    Establishes a dual-stream logging pipeline consisting of an ANSI-colorized
    stdout console interface and an asynchronous-safe file rotating engine.
    Ensures single-instance registration via handler checks to eliminate duplication.

    Args:
        None

    Returns:
        logging.Logger: A configured singleton-like logger instance mapped to 'ATLAS'.

    Raises:
        ValueError: If the environment configuration specifies an invalid log level name.
        OSError: If the underlying OS denies write access to the targeted log directory.
    """
    numeric_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logger = logging.getLogger("ATLAS")
    logger.setLevel(numeric_level)

    if logger.hasHandlers():
        return logger

    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(numeric_level)

    file_formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - (%(filename)s:%(lineno)d) - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
