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

    This is the main method.
    It takes care of calling `fouine.parsing.parser()` method, that will continue the execution.
    """

    print("Lancement de la Fouine...")
    try:
        ## INITIALIZATION
        # Parsing
        parser = parsing.ParseArgs()
        parser.run()
        # Logging setting
        logger = logs.set_logs(parser.args)
        logger.info("[X]   Fouine se réveille ...")
        fouine = core.Fouine('/home/njord/Desktop/Devs/2600/FOR/code/2600_Forensic_Tool/disks/disk.E01', logger)
        # Retrieve target artifacts list and the associated methods.
        targets = parsing.find_scope(parser.args)
        _helper.dir_create(targets)
        ## HERE PASS THE TARGETS (TUPLE LIST) TO CORE.CORE
        fouine.write_from_parser(targets)

    except (KeyboardInterrupt, EOFError):
        print("Here should close the APP")

    print("App opened and now closing!")


######################################
# ENTRYPOINT
if __name__ == "__main__":
    main()
