import logging
from datetime import datetime

def set_logs(args):
    """Sets the `logging` module with correct values from cli arguments.

    Receives the arguments from the `fouine.core.parsing.ParseArgs`
    and uses them to set the `logging` module.

    Notably, it sets the logfile location and the log level.

    Args:
        args (Namespace): Arguments received from argparse.ArgumentParser.parseàargs() method.
    """

    ## Set log file location
    if args.logfile:
        logname=args.logfile
    else:
        logname = datetime.now().strftime("/tmp/fouine-%Y_%m_%d:%H:%M:%S.log")
    
    ## Set correct loglevel
    # Default loglevel is 0
    loglevel = 0
    # Sets logging to a loglevel of 10,20,30,40,50
    if args.logging>1: 
        if args.logging>5:
            args.logging = 5
        loglevel = 60-args.logging*10
        
    ## Configure `logging` module
    logging.basicConfig(filename=logname, level=args.logging)