#!/bin/bash

poetry install --with dev,docs

files=$(find "./configs" -type f)
args=$(printf '"%s",' $files)
args=${args%?}
echo "$args"
fouine --input /home/njord/Desktop/Devs/2600/FOR/code/2600_Forensic_Tool/disks/disk.E01 \
	--config "./configs/RegistryHiveUser.yaml","./configs/ChromeFileSystem.yaml","./configs/EdgeFileSystem.yaml","./configs/$MFT.yaml","./configs/$MFTMirr.yaml","./configs/Edge.yaml","./configs/$Boot.yaml","./configs/EventLogs.yaml","./configs/EdgeChromum.yaml","./configs/Firefox.yaml","./configs/ChromeExtensions.yaml","./configs/Chrome.yaml","./configs/RegistryHiveSystem.yaml","./configs/InternetExplorer.yaml","./configs/LogFiles.yaml","./configs/GroupPolicy.yaml","./configs/$LogFile.yaml"
