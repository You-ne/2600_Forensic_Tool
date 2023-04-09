#!/bin/bash

poetry install --with dev,docs

files=$(find "./configs" -type f)
args=$(printf '"%s",' $files)
args=${args%?}
echo "$args"

fouine --input /home/njord/Desktop/Devs/2600/FOR/code/2600_Forensic_Tool/disks/disk.E01 --output ./Fouined
