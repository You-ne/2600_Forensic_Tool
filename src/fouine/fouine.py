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
        logger = logs.set_logs(parser.args)
        logger.info("[X] Parsing arguments...")
        # Logging setting
        logger.info(parser.args)
        #fouine = core.Fouine(parser.args.input, logger)
        logger.info("Lancement de la Fouine...")
        # Retrieve target artifacts list
        targets = parsing.find_scope(parser.args, logger)
        # Create the directory tree needed to hold extracted data
        #_helper.dir_create(targets)
        ## HERE PASS THE TARGETS (TUPLE LIST) TO CORE.CORE
        #fouine.write_from_parser(targets)

    except (KeyboardInterrupt, EOFError):
        print("Here should close the APP")

    print("App opened and now closing!")


######################################
# ENTRYPOINT
if __name__ == "__main__":
    main()
