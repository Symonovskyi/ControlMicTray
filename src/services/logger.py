import logging

# Global logger instance, typically named after the module
logger = logging.Logger(__name__)


# Adding console handler with formatter and customizing it.
console_handler = logging.StreamHandler()
console_handler.set_name("MainConsoleLogger")

# console_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
console_formatter = logging.Formatter('%(asctime)s -> %(message)s')
console_handler.setFormatter(console_formatter)

logger.addHandler(console_handler)
