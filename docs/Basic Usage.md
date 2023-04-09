# How to call Fouine ?

After installation with `poetry install`, or `pip install ./pkg` if you have a binary distribution;
you can launch Fouine with `fouine`.

Multiple options can be provided:

```text
    -h / --help     -> Display help in the CLI.
    -i / --input    -> Path where EWF shall be found. (By default: ./)
    -o / --output   -> Path where extracted artifacts should be saved. (By default: ./Fouined)
    -c / --config   -> Path where config file are to be found. (By default: ./)
    -v / --verbose  -> Wether logging info should be printed in stdout. If not, it is only recorded in logfiles. (By default: False)
    -l / --logging  -> Each 'l' increases the logging level. (By default: 0)
    -lf / --logfile -> Where to save your logfile. (By default: /tmp/fouine-YEAR_MONTH_DAY:HOUR:MINUTES:SECONDS.log)
```



# What to feed Fouine ??

You can specify multiple sources for your config files, like this:

`fouine -c "./source1","./source2","./source3"`

Each source can be either a directory or a yaml file.
Directories will be explored non-recursively, seaching for yaml files.

Each yaml file must follow a certain structure to be accepted.

```yaml
Targets:
    -
        Name:       (str) The target name.
        Category:   (str) The target category.
        Path:       (str) The path where the target should be looked for.
        FileMask:   (str) The mask to be applied in the target directory to find the target artifacts.
        Recursive:  (bool) Wethet the target directory shall be explored recursively.
    -
        ...
```

# Thanks Fouine <3

&#9825 &#128063 &#9825

