# How to launch

After installation with `poetry install`, or `pip install ./pkg` if you have a binary distribution;
you can launch Fouine with `fouine`.

Multiple options can be provided:
"""

    -i / --input    -> Path where EWF shall be found. (By default:)
    -o / --output   -> Path where extracted artifacts should be saved.
    -c / --config   -> Path where config file are to be found.
    -v / --verbose  -> Wether logging info should be printed in stdout. If not, it is only recorded in logfiles.
    -l / --logging  -> Each 'l' increases the logging level.
    -lf / --logfile -> Where to save your logfile. By default will be at /tmp/fouine-YEAR_MONTH_DAY:HOUR:MINUTES:SECONDS.log
"""