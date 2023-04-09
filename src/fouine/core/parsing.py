import argparse
import os
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from fouine.core._helper import Target


class Parser:
    """An argument parser, based on `argparse`. Defines arguments, read them, then take appropriate action.

    Accepted options are:
        -i / --input
        -o / --output
        -c / --config
        -v / --verbose
        -l / --logging

    Attributes:
        parser (argparse.ArgumentParser): An `argparse` argument parser. It is used to define arguments or take actions on them.
    """

    def __init__(self):
        """__init__ method of `fouine.parsing.Parser` class. Here arguments are defined.

        In this method each possible argument for `fouine` is declared using the `argparse.ArgumentParser.add_argument()` method.
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
            default="./Fouined",
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
            action="count",
            default=0,
            help="Use this option to set verbose level, e.g -vvv -> lvl3.\n",
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


def extract_yaml(configfile_path, outdir, logger) -> list[Target]:
    """Receives the path of a .tkape, .yaml or .yml config file, and extract the contained rules.
    Args:
        configfile_path(str): The path of a .tkape, .yaml or .yml config file.
        outdir(str): The path of save directory (--output option).
    """

    print(f"extract received {outdir}")

    # Init rules list
    rules = list()

    # Load yaml file
    if not os.path.isfile(configfile_path):
        logger.warning(f"{configfile_path} is not a valid file!")
        return []
    stream = open(configfile_path, "r")
    configfile = yaml.load(stream, Loader=Loader)
    # Retrieve extraction rules from Targets field
    if configfile is None:
        logger.warning(f"{configfile} is None after yaml.load")
        return []

    for tmp in configfile["Targets"]:
        target = Target()
        for element, key in {"Path": 'path', "FileMask": 'file_mask',
                         "Name": "name", "Category": 'category',
                         "Recursive": 'recursive', "Comment": 'comment'}.items():
            try:
                if element == "Recursive":
                    if not tmp[element] and not tmp["Filemask"]:
                        setattr(target, 'filemask', ".*")
                setattr(target, key, tmp[element])
            except:
                pass
                #logger.debug(f"Have'not find arg {element} in tkape!")
        target.export_path = outdir
        rules.append(target)
    return rules


def find_scope(args, logger) -> list:
    """From the config file, lists the artifacts that needs recovery, and the needed methods."""

    # Establish a list of path to look for config files, based on --config option
    if "," in args.config:
        cfg_paths = args.config.split(",")
    else:
        cfg_paths = args.config

    logger.debug(f"Taking targets from {cfg_paths}")

    # Retrieves targets list from each config file.
    # The result is a list of 3 elements list. They hold the desired save path as 1st element, the artifact path as 2nd,
    # and wether it is a file or a directory that should be explored recursively as a 3rd element.
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
                    if file.rpartition("/")[:1].rpartition(".")[:1] in ("yml, " "yaml", "tkape"):
                        rules = extract_yaml(file, outdir)
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
                    f"[!] Non-existant config directory {dir}... It should be a yaml file with .yaml, .yml or .tkape file.\n    File Skipped. "
                )
                continue
            

        # Rules are extracted if path points to a config file with proper extension.
        if extension in ("yml", "yaml", "tkape"):
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
        # targets = DEFAULT_TARGETS
        pass
    
    return targets