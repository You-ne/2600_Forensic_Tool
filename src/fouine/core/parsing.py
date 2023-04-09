import argparse
import os
import time

import yaml

try:
    from yaml import CDumper as Dumper, CLoader as Loader
except ImportError:
    from yaml import Loader, Dumper

from fouine.core._defcfg import DEFAULT_CONFIG
from fouine.core._helper import Target


class Parser:
    """An argument parser, based on `argparse`. Defines arguments, read them, then take appropriate action.

    Accepted options are:
        -i / --input
        -o / --output
        -c / --config
        -v / --verbose
        -l / --logging
        -lf / --logfile

    Attributes:
        parser (argparse.ArgumentParser): An `argparse` argument parser. It is used to define arguments or take actions on them.
    """

    def __init__(self):
        """__init__ method of `fouine.parsing.Parser` class. Here arguments are defined.

        In this method each possible argument for `fouine` is declared using the `argparse.ArgumentParser.add_argument()` method.

        Args:
            self (fouine.core.parsing.Parser): self
        """

        self.parser = argparse.ArgumentParser(
            description="Extract data from an EWF image.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        self.parser.add_argument(
            "-i",
            "--input",
            default="./",
            help="The path to the EWF image you want to analyze.\n",
        )
        self.parser.add_argument(
            "-o",
            "--output",
            default="./Fouined/",
            help="The dir you want to save your results in.\n",
        )
        self.parser.add_argument(
            "-c",
            "--config",
            default="./",
            help="Where to find your specified config file.\n",
        )
        self.parser.add_argument(
            "-lf",
            "--logfile",
            help="Where to save your logfile.\nBy default will be at /tmp/fouine-YEAR_MONTH_DAY:HOUR:MINUTES:SECONDS.log\n",
        )
        self.parser.add_argument(
            "-v",
            "--verbose",
            default=False,
            help="Use this option to activate verbose output on stdout.\n",
        )
        self.parser.add_argument(
            "-l",
            "--logging",
            action="count",
            default=0,
            help="Use this option to set loglevel. Each occurence adds 10 to loglevel.\nhttps://www.logicmonitor.com/blog/python-logging-levels-explained\n",
        )

    def run(self):
        """This method calls `argparse.ArgumentParser.parse_args()` to retrieve the argument list."""
        self.args = self.parser.parse_args()


def extract_yaml(configfile_path: str, outdir: str, logger) -> list[Target]:
    """Receives the path of a .tkape, .yaml or .yml config file, and extract the contained rules.

    It will first check that the path points to an exitsing file, then try to load it using yaml.load().
    If the loading fails, a log message will be recorded and an empty list returned.

    Otherwise, the .yaml content will be explored, and the values needed to build fouine.core._helper.Target() objects retrieved.

    Args:
        configfile_path(str): The path of a .tkape, .yaml or .yml config file.
        outdir(str): The path of save directory (--output option).
    """

    # Init rules list
    rules = list()

    # Load yaml file
    if not os.path.isfile(configfile_path):
        logger.warning(f"{configfile_path} config file doesn't exist!\n File is skipped!")
        return []
    stream = open(configfile_path, "r")
    configfile = yaml.load(stream, Loader=Loader)
    # Retrieve extraction rules from Targets field
    if configfile is None:
        logger.warning(
            f"No configfile retrieved after yaml.load on {configfile_path}. Check that it is a correct yaml file !"
        )
        return []

    try:
        for tmp in configfile["Targets"]:
            target = Target()
            for element, key in {
                "Path": "path",
                "FileMask": "file_mask",
                "Name": "name",
                "Category": "category",
                "Recursive": "recursive",
                "Comment": "comment",
            }.items():
                try:
                    if element == "Recursive":
                        logger.debug(f"{tmp[element]}  {element}")
                        logger.debug(target)
                        if tmp[element] == False:
                            setattr(target, "filemask", ".*")
                    setattr(target, key, tmp[element])

                except:
                    pass
                    # logger.debug(f"Have'not find arg {element} in tkape!")
            target.export_path = outdir
            rules.append(target)
    except:
        logger.warning(
            "That .yaml file was not a proper configuration file. Refer to documentation for more information."
        )
    return rules


def find_scope(args, logger) -> list:
    """From the --config argument, will list all configuration files and call extract_yaml on them to retrieve extraction rules.

    First, it will figure out if it received multiple paths from --config.
    In this case, it will put them in a list.
    If only one path was given, it will be stored in a list nonetheless.

    The function will then separate the rightmost part of the given paths,
    using / as a delimiter, one path by one.

    Then, it can act on it in three ways:
        - If it is a directory, it will explore it (non-recursively) and look for config files using the same process.\n
        - If it is a yml, yaml or tkape file, it will extract the rules contained in it.\n
        - If it is a file with the wrong extension, or if the path doesn't exits, it will skip it and continue.\n”

    Args:
        args (Namespace): The arguments given to fouine by the user.
        logger (logging.Logger): The logger initialized in fouine.logs.set_logs().
    """

    # Establish a list of path to look for config files, based on --config option
    if "," in args.config:
        cfg_paths = args.config.split(",")
    else:
        cfg_paths = list()
        cfg_paths.append(args.config)

    logger.debug(f"Taking targets from {cfg_paths}")

    # Retrieves targets list from each config file.
    targets = list()
    outdir = args.output
    for path in cfg_paths:
        last_path_elem = path.rpartition("/")[-1]
        extension = last_path_elem.rpartition(".")[-1]

        if extension is last_path_elem:
            if os.path.isdir(path):
                dir_files = os.listdir(path)
                for file in dir_files:
                    # Extension check
                    filename = file.rpartition("/")[-1]
                    if filename.rpartition(".")[-1] in ("yml", "yaml", "tkape"):
                        rules = extract_yaml(path + "/" + file, outdir, logger)
                        if rules != []:
                            targets.append(rules)
                    # Wrong extension warning
                    else:
                        logger.warning(
                            f"[!] Wrong extension for the config file {file}... It should be a yaml file with .yaml, .yml or .tkape file.\n    File Skipped. "
                        )
                        continue
            else:
                logger.warning(
                    f"[!] Non-existant config directory {dir}...\n    Directory Skipped. "
                )
                continue

        # Rules are extracted if path points to a config file with proper extension.
        elif extension in ("yml", "yaml", "tkape"):
            rules = extract_yaml(path, outdir, logger)
            if rules != []:
                targets.append(rules)

        # Skip file and alert if wrong file extension
        else:
            logger.warning(
                f"[!] Wrong extension for the config file {path}...\n    Directory Skipped. "
            )
            continue

    if not targets:
        logger.warning("Loading default configS")
        def_conf = DEFAULT_CONFIG(args.output)
        targets = def_conf.Targets

    return targets
