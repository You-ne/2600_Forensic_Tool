import datetime
import logging
from functools import wraps
from typing import Optional

from colorama import Fore, Style


class ColorFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        if levelname == "DEBUG":
            color = Fore.BLUE
        elif levelname == "INFO":
            color = Fore.GREEN
        elif levelname == "WARNING":
            color = Fore.YELLOW
        elif levelname == "ERROR":
            color = Fore.RED
        elif levelname == "CRITICAL":
            color = Style.BRIGHT + Fore.RED
        else:
            color = ""
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


def set_logs(args) -> logging.logger:
    """Sets the `logging` module with correct values from cli arguments.

    Receives the arguments from the `fouine.core.parsing.ParseArgs`
    and uses them to set the `logging` module.

    Notably, it sets the logfile location and the log level.

    Args:
        args (Namespace): Arguments received from argparse.ArgumentParser.parseàargs() method.
    """

    ## Set log file location
    if args.logfile:
        logname = args.logfile
    else:
        logname = datetime.now().strftime("/tmp/fouine-%Y_%m_%d:%H:%M:%S.log")

    ## Set correct loglevel
    # Default loglevel is 0
    loglevel = 0
    # Sets logging to a loglevel of 10,20,30,40,50
    if args.logging > 1:
        if args.logging > 5:
            args.logging = 5
        loglevel = 60 - args.logging * 10

    ## Configure `logging` module
    logging.basicConfig(
        level=loglevel,
        format="%(levelname)s %(message)s",
        filename=logname,
        handlers=[logging.FileHandler(logname), logging.StreamHandler()],
    )
    logger = logging.getLogger()
    color_handler = logging.StreamHandler()
    color_handler.setFormatter(ColorFormatter())
    logger.addHandler(color_handler)
    return logger


def log_msg(
    logger,
    statement: str,
    logret: Optional[bool] = False,
    attribute: Optional[str] = None,
):
    """Decorator that logs a message after a function call, optionally logging the return value.
        It must be runned inside a class if you want to use attribute feature

    Args:
        statement (str): _description_
        logret (Optional[bool], optional): Should print return value ?. Defaults to False.
        attribute (str, optional): Attribute to be printed. Defaults to None.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if logret and attribute:
                logger.debug(statement.format(getattr(args[0], attribute), logret))
            elif logret:
                logger.debug(statement.format(result))
            else:
                logger.debug(statement)
            return result

        return wrapper

    return decorator
