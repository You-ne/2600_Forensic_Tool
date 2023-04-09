#!/usr/bin/env python3
import argparse
import logging
from datetime import datetime
from prompt_toolkit import prompt

from fouine.core import ( _helper
                         , core
                         ,logs
                         , parsing
)


######################################
# MAIN
def main():
    """Program entrypoint.

    This is the main.
    It takes care of calling `fouine.parsing.parser()` method, that will continue the execution.
    """
    
    try:
        ## INITIALIZATION
        # Parsing
        
        parser = parsing.Parser()
        parser.run()
        # Logging setting
        logger = logs.set_logs(parser.args)
        fouine = core.Fouine(parser.args.input, logger)
        # Retrieve target artifacts list
        targets = parsing.find_scope(parser.args, logger)
        #_helper.dir_create(targets)
        fs_number = len(fouine.filesystems)
        logger.info(f"DETECTED {fs_number} filesystems")
        if fs_number != 1:
            logger.warning(f"More than 1 filesystem detected, please choose one:")
            logger.info(f"PARTITION TABLE : \n")
            print(fouine.partition_table)
            logger.info("FILESYSTEMS: ")
            [print(fs) for fs in fouine.filesystems]
            fs_number = int(input("Please enter a filesystem number:  "))
        if type(fs_number) != int:
            logger.warning(f"Wrong fs number {fs_number}")
            return
        if fs_number < 0:
            logger.warning(f"Wrong fs number {fs_number}")
            return
        if fs_number > len(fouine.filesystems):
            logger.warning(f"Wrong fs number {fs_number}")
            return
        fouine.write_from_parser(targets)

    except (KeyboardInterrupt, EOFError):
        print("Here should close the APP")

    print("App opened and now closing!")


######################################
# ENTRYPOINT
if __name__ == "__main__":
    main()
