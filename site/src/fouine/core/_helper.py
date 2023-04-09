from enum import Enum
import re
import os
import pytsk3

from typing import Optional
from colorama import Fore, Style

SUPPORTED_FS = [
    b"TFS",
    b"NTFS",
    b"FAT",
    b"FAT12",
    b"FAT16",
    b"FAT32",
    b"EXT2",
    b"EXT3",
    b"EXT4",
    b"HFS",
    b"ISO",
    b"YAFFS",
    b"SWAP",
    b"FFS",
    b"data",
]
DEFAULT_USER = [b"All Users", b"Default", b"Default User", b"desktop.ini", b"Public"]

class Target:
    def __init__(self, name: Optional[str] = None, category: Optional[str] = None, 
                path: Optional[str] = None, file_mask: Optional[str] = None, 
                recursive: Optional[bool] = None, export_path: Optional[str] = None,
                comment: Optional[str] = None):
        self.name = name
        self.category = category
        self.path = path
        self.export_path = export_path
        self.file_mask = file_mask
        self.recursive = recursive
        self.comment = comment
    
    def __repr__(self):
        attrs = []
        for attr in self.__dict__:
            value = getattr(self, attr)
            if value is not None:
                if attr == "name":
                    attrs.append(Fore.BLUE + str(value) + Style.RESET_ALL)
                elif attr == "category":
                    attrs.append(Fore.GREEN + str(value) + Style.RESET_ALL)
                elif attr == "path":
                    attrs.append(Fore.YELLOW + str(value) + Style.RESET_ALL)
                elif attr == "export_path":
                    attrs.append(Fore.MAGENTA + str(value) + Style.RESET_ALL)
                elif attr == "file_mask":
                    attrs.append(Fore.CYAN + str(value) + Style.RESET_ALL)
                elif attr == "recursive":
                    attrs.append(Fore.RED + str(value) + Style.RESET_ALL)
            else:
                if attr == "name":
                    attrs.append(Fore.BLUE + str(None) + Style.RESET_ALL)
                elif attr == "category":
                    attrs.append(Fore.GREEN + str(None) + Style.RESET_ALL)
                elif attr == "path":
                    attrs.append(Fore.YELLOW + str(None) + Style.RESET_ALL)
                elif attr == "export_path":
                    attrs.append(Fore.MAGENTA + str(None) + Style.RESET_ALL)
                elif attr == "file_mask":
                    attrs.append(Fore.CYAN + str(None) + Style.RESET_ALL)
                elif attr == "recursive":
                    attrs.append(Fore.RED + str(None) + Style.RESET_ALL)
        return f"Target({', '.join(attrs)})"

class FS_TYPE_ENUM(Enum):
    DTECT = pytsk3.TSK_FS_TYPE_DETECT  # 0x00000000,
    NTFS = pytsk3.TSK_FS_TYPE_NTFS  # 0x00000001,
    FAT12 = pytsk3.TSK_FS_TYPE_FAT12  # 0x00000002,
    FAT16 = pytsk3.TSK_FS_TYPE_FAT16  # 0x00000004,
    FAT32 = pytsk3.TSK_FS_TYPE_FAT32  # 0x00000008,
    EXFAT = pytsk3.TSK_FS_TYPE_EXFAT  # 0x0000000a,
    FFS1 = pytsk3.TSK_FS_TYPE_FFS1  # 0x00000010,
    FFS1B = pytsk3.TSK_FS_TYPE_FFS1B  # 0x00000020,
    FFS2 = pytsk3.TSK_FS_TYPE_FFS2  # 0x00000040,
    EXT2 = pytsk3.TSK_FS_TYPE_EXT2  # 0x00000080,
    EXT3 = pytsk3.TSK_FS_TYPE_EXT3  # 0x00000100,
    SWAP = pytsk3.TSK_FS_TYPE_SWAP  # 0x00000200,
    RAW = pytsk3.TSK_FS_TYPE_RAW  # 0x00000400,
    ISO9660 = pytsk3.TSK_FS_TYPE_ISO9660  # 0x00000800,
    HFS = pytsk3.TSK_FS_TYPE_HFS  # 0x00001000,
    EXT4 = pytsk3.TSK_FS_TYPE_EXT4  # 0x00002000,
    YAFFS2 = pytsk3.TSK_FS_TYPE_YAFFS2  # 0x00004000,
    UNK = pytsk3.TSK_FS_TYPE_UNSUPP  # 0xffffffff


class FILE_TYPE_ENUM(Enum):
    UNKNOWN = pytsk3.TSK_FS_NAME_TYPE_UNDEF  # Unknown type.
    PIPE = pytsk3.TSK_FS_NAME_TYPE_FIFO  # Named pipe.
    CHR_DEV = pytsk3.TSK_FS_NAME_TYPE_CHR  # Character device.
    DIR = pytsk3.TSK_FS_NAME_TYPE_DIR  # Directory.
    BLK_DEV = pytsk3.TSK_FS_NAME_TYPE_BLK  # Block device.
    FILE = pytsk3.TSK_FS_NAME_TYPE_REG  # Regular file.
    LINK = pytsk3.TSK_FS_NAME_TYPE_LNK  # Symbolic link.
    SOCKET = pytsk3.TSK_FS_NAME_TYPE_SOCK  # Socket.
    SHADOW_I = pytsk3.TSK_FS_NAME_TYPE_SHAD  # Shadow inode (solaris)
    WHT = pytsk3.TSK_FS_NAME_TYPE_WHT  # Whiteout (openbsd)
    VIRT_FILE = pytsk3.TSK_FS_NAME_TYPE_VIRT  # Special (TSK added "Virtual" files)
    VIRT_DIR = pytsk3.TSK_FS_NAME_TYPE_VIRT_DIR  # Special (TSK added "Virtual" directories)


class HKEYArtefacts(Enum):
    HKEY_LOCAL_MACHINE_SAM = b"/Windows/System32/config/SAM"
    HKEY_LOCAL_MACHINE_SOFTWARE = b"/Windows/System32/config/SOFTWARE"
    HKEY_LOCAL_MACHINE_SYSTEM = b"/Windows/System32/config/SYSTEM"
    HKEY_USERS_NT = b"/Users/<username>/NTUSER.DAT"
    HKEY_USERS_DEFAULT = b"/Windows/System32/config/DEFAULT"
    HKEY_USERS_SID = b"/Windows/System32/config/SID"

    def __init__(self, path):
        self._path_template = path

    def get_path(self, username=None):
        if self is not HKEYArtefacts.HKEY_USERS_NT:
            return self._path_template
        else:
            if username is None:
                raise ValueError("Username is required for HKEY_USERS_NT.")
            else:
                return self._path_template.replace(b"<username>", username)

    
class WindowsNews(Enum):
    WINDOWS_APPLICATION_LOG = {
        "Windows 7": "/Windows/System32/Winevt/Logs/Application.evtx",
        "Windows 10/11": "/Windows/System32/winevt/Logs/Application.evtx",
    }
    WINDOWS_SETUP_LOG = {
        "Windows 7": "/Windows/Panther/setupact.log",
        "Windows 10/11": "/Windows/Panther/setupact.log",
    }
    WINDOWS_FORWARDED_EVENTS = {
        "Windows 7": "Not available",
        "Windows 10/11": "/Windows/System32/winevt/Logs/ForwardedEvents.evtx",
    }
    WINDOWS_HARDWARE_EVENTS_LOG = {
        "Windows 7": "/Windows/System32/Winevt/Logs/Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx",
        "Windows 10/11": "/Windows/System32/Winevt/Logs/Microsoft-Windows-DriverFrameworks-UserMode%4Operational.evtx",
    }
    WINDOWS_INTERNET_EXPLORER_LOG = {
        "Windows 7": "/Windows/Logs/IE/IE*.log",
        "Windows 10/11": "Not available (Internet Explorer is no longer supported in Windows 10/11)",
    }
    WINDOWS_POWERSHELL_LOG = {
        "Windows 7": "/Windows/System32/Winevt/Logs/Microsoft-Windows-PowerShell%4Operational.evtx",
        "Windows 10/11": "/Windows/System32/Winevt/Logs/Microsoft-Windows-PowerShell%4Operational.evtx",
    }
    WINDOWS_SETUP_ACTIONS_LOG = {
        "Windows 7": "/Windows/Panther/setupact.log",
        "Windows 10/11": "/Windows/Panther/setupact.log",
    }
    WINDOWS_SYSTEM_LOG = {
        "Windows 7": "/Windows/System32/Winevt/Logs/System.evtx",
        "Windows 10/11": "/Windows/System32/winevt/Logs/System.evtx",
    }
    WINDOWS_SECURITY_LOG = {
        "Windows 7": "/Windows/System32/Winevt/Logs/Security.evtx",
        "Windows 10/11": "/Windows/System32/winevt/Logs/Security.evtx",
    }
    WINDOWS_TASK_SCHEDULER_LOG = {
        "Windows 7": "/Windows/System32/Winevt/Logs/Microsoft-Windows-TaskScheduler%4Operational.evtx",
        "Windows 10/11": "/Windows/System32/winevt/Logs/Microsoft-Windows-TaskScheduler%4Operational.evtx",
    }


class WindowsBrowser(Enum):
    INTERNET_EXPLORER_HISTORY = {
        "Windows 7": "/Users/%(user)/AppData/Local/Microsoft/Windows/History/",
        "Windows 10/11": "Not available (Internet Explorer is no longer supported in Windows 10/11)",
    }
    INTERNET_EXPLORER_CACHE = {
        "Windows 7": "/Users/%(user)/AppData/Local/Microsoft/Windows/Temporary Internet Files/",
        "Windows 10/11": "Not available (Internet Explorer is no longer supported in Windows 10/11)",
    }
    INTERNET_EXPLORER_COOKIES = {
        "Windows 7": "/Users/%(user)/AppData/Roaming/Microsoft/Windows/Cookies/",
        "Windows 10/11": "Not available (Internet Explorer is no longer supported in Windows 10/11)",
    }
    FIREFOX_PROFILE_FOLDER = {
        "Windows 7": "/Users/%(user)/AppData/Roaming/Mozilla/Firefox/Profiles/",
        "Windows 10/11": "/Users/%(user)/AppData/Roaming/Mozilla/Firefox/Profiles/",
    }
    CHROME_PROFILE_FOLDER = {
        "Windows 7": "/Users/%(user)/AppData/Local//Google//Chrome//User Data//Default/",
        "Windows 10/11": "/Users/%(user)/AppData/Local//Google//Chrome//User Data//Default/",
    }
    EDGE_HISTORY = {
        "Windows 7": "Not available (Microsoft Edge is not supported in Windows 7)",
        "Windows 10/11": "/Users/%(user)/AppData//Local//Microsoft//Edge//User Data/Default/History",
    }
    EDGE_CACHE = {
        "Windows 7": "Not available (Microsoft Edge is not supported in Windows 7)",
        "Windows 10/11": "/Users/%(user)/AppData/Local/Microsoft/Edge/User Data/Default/Cache",
    }
    EDGE_COOKIES = {
        "Windows 7": "Not available (Microsoft Edge is not supported in Windows 7)",
        "Windows 10/11": "/Users/%(user)/AppData/Local/Microsoft/Edge/User Data/Default/Cookies",
    }


def expand_path(path) -> list:
    if '*' not in path:
        return [path]
    else:
        parts = path.split('*')
        base_dir = parts[0]
        subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
        results = []
        for subdir in subdirs:
            rest_path = '*'.join(parts[1:])
            sub_path = os.path.join(base_dir, subdir, rest_path)
            results += expand_path(sub_path)
        return results


def dir_create(targets: list[Target]) -> None:
    """Creates the directory structure to store the retrieved artifacts.

    This function receives the target artifacts list. It will iterate on it, and will create a directory
    mimicing the name of the original artifact directory, every time the directory is not arlready existing.
    The created directories will be under a parent directory corresponding to the --output option.

    Args:
        targets(list): List of target artifacts.  Each element is itself a list, with the desired output directry as 1st element; the 2nd being the path of the desired artifact.
    """
    mode = 0o740

    for scope in targets:
        for target in scope:
            print(f"{target.export_path} {target.path}")
            paths = expand_path(target.path)
            for suffix in paths:
                path = target.export_path+suffix
                path = path.rpartition("/")[:1]
                path = str(path[0])

                # Creates the directories if not already existing
                if os.path.exists(path):
                    continue
                else:
                    os.makedirs(path, mode)


