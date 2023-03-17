#!/usr/bin/env python3
import logging
from datetime import datetime


def main():
    try:
        logname = datetime.now().strftime("/tmp/log%Y_%m_%d_%H:%M:%S.log")
        logging.basicConfig(filename=logname, level=logging.INFO)
        print("App opened and noow closing!")
        # Put the rest of the app here

    except (KeyboardInterrupt, EOFError):
        print("Here should close the APP")


if __name__ == '__main__':
    main()
