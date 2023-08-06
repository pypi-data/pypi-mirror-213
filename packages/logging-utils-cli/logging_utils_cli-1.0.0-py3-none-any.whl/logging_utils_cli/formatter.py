"""Log formatters for python logging."""

import logging
import termcolor


class TerminalFormatter(logging.Formatter):
    """Logging formatter with colors."""

    colors = {
        logging.DEBUG: "grey",
        logging.INFO: "cyan",
        logging.SUCCESS: "green",
        logging.WARNING: "yellow",
        logging.ERROR: "red",
        logging.CRITICAL: "red",
    }
    prefix = {
        logging.DEBUG: "[d]",
        logging.INFO: "[i]",
        logging.SUCCESS: "[i]",
        logging.WARNING: "[!]",
        logging.ERROR: "[!]",
        logging.CRITICAL: "[!]",
    }
    attrs = {
        logging.CRITICAL: ["bold"],
    }

    def __init__(self, fmt="%(message)s"):
        super().__init__(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    def format(self, record):
        return termcolor.colored(
            f"{self.prefix[record.levelno]} {super().format(record)}",
            color=self.colors[record.levelno],
            attrs=self.attrs.get(record.levelno),
        )
