#!/usr/bin/env python3
import argparse
import logging
from datetime import datetime

from fouine.core import logs, parsing


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
        logs.set_logs(parser.args)

        # Retrieve target artifacts list and the associated methods.
        targets = parsing.find_scope(parser.args)

        ## HERE PASS THE TARGETS (TUPLE LIST) TO CORE.CORE
        # Core will then call modules (class or method or idk)

    except (KeyboardInterrupt, EOFError):
        print("Here should close the APP")

    print("App opened and now closing!")


######################################
# ENTRYPOINT
if __name__ == "__main__":
    main()
