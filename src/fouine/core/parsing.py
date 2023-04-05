import argparse

#######################################
# CLASS Parse Args
class ParseArgs:
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
        """__init__ method of `fouine.parsing.ParseArgs` class. Here arguments are defined.

        In this method each possible argument for `fouine` is declared using the `argparse.ArgumentParser.add_argument()` method.
        """

        self.parser = argparse.ArgumentParser(description='Extract data from an EWF image.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        self.parser.add_argument('-i', '--input',
                            default="./",
                            help='The path to the EWF image you want to analyze.\n')
        self.parser.add_argument('-o', '--output',
                            default="./Fouined",
                            help='The dir you want to save your results in.\n')
        self.parser.add_argument('-c', '--config',
                            default="./",
                            help='Where to find your specified config file.\n')
        self.parser.add_argument('-lf', '--logfile',
                            help='Where to save your logfile.\nBy default will be at /tmp/fouine-YEAR_MONTH_DAY:HOUR:MINUTES:SECONDS.log\n')                    
        self.parser.add_argument('-v', '--verbose',
                            action='count',
                            default=0,
                            help='Use this option to set verbose level, e.g -vvv -> lvl3.\n')
        self.parser.add_argument('-l', '--logging',
                            action='count',
                            default=0,
                            help='Use this option to set loglevel. Each occurence adds 10 to loglevel.\nhttps://www.logicmonitor.com/blog/python-logging-levels-explained\n')



    def run(self):

        """This method calls `argparse.ArgumentParser.parse_args()` to retrieve the argument list.
    
        """
        self.args = self.parser.parse_args()




#######################################
# CLASS Scoper
class Scoper:

    def __init__(self):
        pass


def find_scope(args):
    """From the config file, lists the artifacts that needs recovery, and the needed methods.

    """
    # TEST
    cfg_path = args.config
    img_path = args.input
    
    scoper = Scoper()
