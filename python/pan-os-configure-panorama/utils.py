import logging


class Logger:
    """
        A singleton Logger class for managing application-wide logging.

        This class implements a thread-safe singleton pattern for logging, providing
        methods to set log levels and log messages at various severity levels.

        Attributes:
            logger (logging.Logger): The underlying Logger instance.

        Error:
            None explicitly raised, but warns on invalid log levels.

        Return:
            Logger: The singleton instance of the Logger class.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger('palo_alto_config')
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            cls._instance.logger.addHandler(handler)
            cls._instance.logger.setLevel(logging.INFO)  # Default level
        return cls._instance

    def set_level(self, log_level: str):
        level = logging.getLevelName(log_level.upper())
        if isinstance(level, int):
            self.logger.setLevel(level)
        else:
            self.logger.warning(f"Invalid log level: {log_level}. Defaulting to INFO.")
            self.logger.setLevel(logging.INFO)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)


logger = Logger()


def set_log_level(log_level: str):
    logger.set_level(log_level)
