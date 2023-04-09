#!/usr/bin/env python3
import argparse
import logging
from datetime import datetime
from colorama import Fore, Style

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
        try:
            fouine = core.Fouine(parser.args.input, logger)
        except Exception as e:
            print(f"{e} {Fore.LIGHTRED_EX}\nYour input file disk must not be correct please verify!{Style.RESET_ALL}")
            return
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
        logger.debug(targets)
        fouine.write_from_parser(targets)

    except (KeyboardInterrupt, EOFError):
        print("Here should close the APP")

    print("App opened and now closing!")


######################################
# ENTRYPOINT
if __name__ == "__main__":
    main()
