import argparse
import os
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


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






def extract_yaml(configfile_path, outdir)->list:
    """Receives the path of a .tkape, .yaml or .yml config file, and extract the contained rules.
    Args:
        configfile_path(str): The path of a .tkape, .yaml or .yml config file.
        outdir(str): The path of save directory (--output option).
    """
    
    # Init rules list
    rules = list()

    # Load yaml file
    stream = open(configfile_path, 'r')
    configfile = yaml.load(stream, Loader=Loader)
    
    # Retrieve extraction rules from Targets field
    for target in configfile["Targets"]:
        path = target["Path"]
        if target["FileMask"]:
            path = path+target["FileMask"]
        if target["Recursive"]:
            rules.append([outdir, path[2:].replace("\\", "/"), "Recursive"])
        else:
            rules.append([outdir, path[2:].replace("\\", "/"), "\0"])

    return(rules)



def find_scope(config, logger)->list:
    """From the config file, lists the artifacts that needs recovery, and the needed methods.
    """
    
    # Establish a list of path to look for config files, based on --config option
    if "," in config:
        cfg_paths = config.split(",")
    else:
        cfg_paths = config
       
    
    print(f"Taking targets from {cfg_paths}")

    # Retrieves targets list from each config file.
    # The result is a list of 3 elements list. They hold the desired save path as 1st element, the artifact path as 2nd,
    # and wether it is a file or a directory that should be explored recursively as a 3rd element.
    targets = list()
    for path in cfg_paths:
        
        # Rules are extracted if path points to a config file with proper extension.
        if extension:=path.rpartition("/")[:1].rpartition(".")[:1] in ("yml, ""yaml", "tkape"):
            rules = extract_yaml(path)
            targets.append(rules)

        # If path points to a directory, file are checked for proper extensio nthen rules are extracted.
        elif extension == "":
            dir_files = os.listdir(path)
            for file in dir_files:
                # Extension check
                if file.rpartition("/")[:1].rpartition(".")[:1] in ("yml, ""yaml", "tkape"):
                    rules = extract_yaml(file)
                    targets.append(rules)
                # Wrong extension warning
                else:
                    logger.warning(f"[!] Wrong extension for the config file {file}... It should be a yaml file with .yaml, .yml or .tkape file.\n    File Skipped. ")
                    continue

            """
            stream = open(configfile, 'r')
            tmp_conf = yaml.load(stream, Loader=Loader)

            for entry in tmp_conf["Targets"]:
                path = entry["Path"]
                if entry["FileMask"]:
                    path = path+entry["FileMask"]
                if entry["Recursive"]:
                    targets.append([args.output, path[2:].replace("\\", "/"), "Recursive"])
                else:
                    targets.append([args.output, path[2:].replace("\\", "/"), "\0"])
            """
        
        # Skip file and alert if wrong file extension
        else:
            logger.warning(f"[!] Wrong extension for the config file {path}... It should be a yaml file with .yaml, .yml or .tkape file.\n    File Skipped. ")
            continue
    
    if not targets:
        #targets = DEFAULT_TARGETS
        pass
    
    return(targets)