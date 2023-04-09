# How to create your target files.

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


# What path to look for artifacts.

To understand how to build targets, you can look at __EricZimmerman__ [Kape Files](https://github.com/EricZimmerman/KapeFiles/tree/master/Targets).
They are supported by `Fouine`.

You can also look at [Velociraptor Targets.yaml](https://github.com/Velocidex/velociraptor/blob/master/artifacts/definitions/Windows/KapeFiles/Targets.yaml), which centralizes a lot of rules for extracting artifacts, from different authors.

Of course, you can also try to extract whatever path interests you!

