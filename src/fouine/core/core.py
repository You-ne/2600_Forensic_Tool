import os
import re
import logging
from typing import Optional, Union

import pyewf
import pytsk3
from ._helper import (
    DEFAULT_USER,
    FILE_TYPE_ENUM,
    FS_TYPE_ENUM,
    SUPPORTED_FS,
    HKEYArtefacts,
    WindowsBrowser,
    WindowsNews,
    Target,
)
from colorama import Fore, Style


class File:
    def __init__(self, file: pytsk3.File) -> None:
        self.file = file
        self.raw_data = self.file.read_random(0, self.file.info.meta.size)

    def is_directory(self):
        try:
            self.file.as_direcory()
            return True
        except OSError:
            return False


class HKEY:
    def __init__(
        self, name: Union[str, bytes], path: Union[str, bytes], file: Optional[File]
    ) -> None:
        self.name = name
        self.path = path
        self.file = file if file else None

    def __repr__(
        self,
    ):
        return f"{Fore.LIGHTGREEN_EX}{self.name} {Fore.YELLOW}{self.path}\n"


class EwfImg(pytsk3.Img_Info):
    def _get_partitions(self):
        """
        The _get_partitions function is a helper function that returns the partitions of the image.
        It is used by other functions in this class to get information about each partition.

        :param self: Used to Reference the object that is calling the function.
        :return: A volume_info object.

        :doc-author: Telio
        """
        return pytsk3.Volume_Info(self)

    def __init__(self, ewf_handle):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the object and makes it ready for use.

        :param self: Used to Represent the instance of the class.
        :param ewf_handle: Used to Pass in the ewf_handle object.
        :return: An object of type pytsk3.

        :doc-author: Telio
        """
        self._ewf_handle = ewf_handle
        super(EwfImg, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)
        self.partTable = self._get_partitions()

    def close(self):
        """
        The close function closes the EWF file handle.

        :param self: Used to Represent the instance of the class.
        :return: None.

        :doc-author: Telio
        """
        self._ewf_handle.close()

    def read(self, offset, size):
        """
        The read function is called by the pytsk3.Img_Info class to read data from
        the EWF file. The offset and size parameters are passed in as integers, and
        the function returns a string of bytes.
        :param self: Used to Represent the instance of the class.
        :param offset: Used to Set the position of the file pointer.
        :param size: Used to Determine how many bytes to read from the file.
        :return: The data read from the offset and size.

        :doc-author: Telio
        """
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        """
        The get_size function returns the size of the media image.

            :returns: The size of the media image in bytes.

        :param self: Used to Refer to the object itself.
        :return: The size of the media image.

        :doc-author: Telio
        """
        return self._ewf_handle.get_media_size()


class FilesystemHelper(pytsk3.FS_Info):
    def __repr__(self):
        """
        The __repr__ function is used to compute the "official" string representation of an object.
        This is how you would make an object of the class. The goal of __repr__ is to be unambiguous.

        :param self: Used to Represent the instance of the class.
        :return: The type of the file system.

        :doc-author: Telio
        """
        return f"{Fore.MAGENTA}TYPE: {Fore.YELLOW} {self.fs_type}"

    def __init__(self, img, partition):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the object by assigning values to its attributes.
        The self parameter refers to the instance of this class, and is used to access or assign attributes.

        :param self: Used to Represent the instance of the class.
        :param img: Used to Pass the image file to the super class.
        :param partition: Used to Determine the offset of the filesystem.
        :return: The super function.

        :doc-author: Telio
        """
        super(FilesystemHelper, self).__init__(img, offset=(partition.start * 512))
        self.fs_type = FS_TYPE_ENUM(self.info.ftype)

    def fstype(
        self,
    ):
        """
        The fstype function returns the name of the filesystem type.

        :param self: Used to Represent the instance of the class.
        :param : Used to Return the name of the file system type.
        :return: The name of the filesystem type.

        :doc-author: Telio
        """
        return self.fs_type.name

    def ls(self, path: str = "/"):
        """
        The ls function takes a path as an argument and returns the names of all files in that directory.
        If no path is given, it defaults to the root directory.

        :param self: Used to Represent the instance of the class.
        :param path:str='/': Used to Set a default value for the path parameter.
        :return: A list of all files and directories in the given directory.

        :doc-author: Telio
        """
        directory = self.open_dir(path)
        return [file_handle.info.name.name for file_handle in directory]

    def read_file(self, file_path: str) -> File:
        """
        The read_file function reads a file from the filesystem.

        Args:
          file_path (str): The path to the file to read.

          raw (Optional[bool]): If True, return the raw bytes of the file instead of an open File object. Defaults to False.

            Returns:
              Union[File, bytes]: Either an open File object or a byte string containing all data in the requested file.

        :param self: Used to Represent the instance of the class.
        :param file_path:str: Used to Specify the path of the file to be read.
        :param raw:Optional[bool]=False: Used to Specify whether or not to read the file as raw data.
        :return: A file object.

        :doc-author: Telio
        """
        return File(self.open(file_path))


class Fouine:
    """
    Take a file name in argument and return an object to work with EWF disk from a forensic point of view
    self.handle is a pyewf.handle class
    self.img is the ewf image binding derived from EwfImg class
    self.partition_table is a custom list of partitions
    self.filesystems is a list of filesystems
    """

    class PartitionTable(list):
        """
        Class for handling partitions tables
        """

        def _list_vol_fs(self) -> list:
            """
            The _list_vol_fs function is a generator that returns a list of all volumes
            that have one of the supported filesystems in their description.  This is used
            to determine which volumes are available for mounting.

            :param self: Used to Access the class attributes.
            :return: A list of volumes that have a filesystem in the supported_fs list.

            :doc-author: Telio
            """
            return [volume for volume in self for fs in SUPPORTED_FS if fs in volume.desc]

        def __init__(self, partitions: list) -> None:
            """
            The __init__ function is the first function that is called when you create a new instance of a class.
            It's job is to initialize all of the attributes for an object.

            :param self: Used to Represent the instance of the class.
            :param partitions:list: Used to Pass the list of partitions to the parent class.
            :return: None.

            :doc-author: Telio
            """

            super().__init__(partitions)
            self._tsk_fs = [
                b"TFS",
                b"NTFS",
                b"FAT",
                b"FAT12",
                b"FAT16",
                b"FAT32",
                b"EXT2",
                b"EXT3",
                b"EXT4",
                b"HFS+",
                b"ISO",
                b"UFS",
                b"APFS",
                b"data",
            ]
            try:
                self.fs_vols = self._list_vol_fs()
            except Exception as e:
                print(
                    f"{e} \n {Fore.YELLOW} NOTE: Runtime Error can occur if your EWF image is incomplete{Style.RESET_ALL}",
                )

        def __repr__(self):
            """
            The __repr__ function is used to return a string representation of the object.
            This is useful for debugging and logging purposes, as well as for interactive use in the Python shell.
            The __repr__ function should return a string that can be parsed by eval() to recreate an equivalent object.

            :param self: Used to Represent the instance of the class.
            :return: A string representation of the object.

            :doc-author: Telio
            """
            ret = ""
            for part in self:
                ret += f"{Fore.RED}{part.addr}  |  {Fore.BLUE}{part.start} - {part.start*512}\t\t{Fore.GREEN}{part.desc}{Style.RESET_ALL}\n"
            return ret

        @classmethod
        def from_volume_info(cls, volume):
            """
            The from_volume_info function is a class method that takes in a volume and returns an instance of the VolumeInfo class.
            The volume is iterated over, and each page is added to the list of pages for this instance.

            :param cls: Used to Create a new instance of the class.
            :param volume: Used to Create a list of pages.
            :return: A list of pages.

            :doc-author: Telio
            """
            return cls([p for p in volume])

    def __init__(
        self,
        filename: str,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines all of its attributes.
        The __init__ function takes in a filename as an argument, which it then uses to open a handle to that file using pyewf's open() method.
        It then creates an EwfImg object from that handle (which is used for reading data from disk), and gets its partition table using EwfImg's partTable attribute.

        :param self: Used to Represent the instance of the class.
        :param filename:str=None: Used to Specify the filename of the image.
        :param : Used to Store the filename of the image.
        :return: None.

        :doc-author: Telio
        """
        self.raw = filename
        self.logger = logger
        self.filenames = pyewf.glob(self.raw) if self.raw else None
        self.handle = pyewf.handle()
        self.handle.open(self.filenames)
        self.img = EwfImg(self.handle)
        self.partition_table = self.PartitionTable.from_volume_info(self.img.partTable)
        self.filesystems = self._get_fs()
        self.system_users = []
        self.available_hkeys = []
        try:
            self.list_users()
        except:
            pass

    def _get_file(self, filename, filesystemID: int = 0) -> File:
        return self.filesystems[filesystemID].read_file(filename)

    def _ls(self, path, filesystemID: int = 0) -> list:
        try:
            return self.filesystems[filesystemID].ls(path)
        except:
            self.logger.warning(f"PATH NOT FOUND {path} on  fs {filesystemID}")
            return -1
    def _write_data(self, data: Union[bytes, bytearray, str], path):
        """
        The _export function is used to export data from the database.

        The _export function is called by the export_data function, which is a public API method. The _export function takes two arguments:

          1) data - This argument should be a bytes-like object (bytes, bytearray or str). It represents the data that will be exported to disk.

          2) path - This argument should be a string representing an absolute filepath on disk where you want your exported file to go.

        :param self: Used to Access the class attributes.
        :param data:Union[bytes: Used to Specify the type of data that is going to be passed in.
        :param bytearray: Used to Convert the data to bytes.
        :param str]: Used to Specify the type of data that can be passed to the function.
        :param path: Used to Specify the path of the file to be written.
        :return: Nothing.

        :doc-author: Telio
        """
        with open(path, "wb") as f:
            f.write(data)

    def _find_file_in_dir(self, path: str, rexpr: str, filesystemID: int = 0):
        self.logger.debug(f"REGEX: {rexpr}")
        rexpr = rexpr.replace('.', '\.')
        rexpr = rexpr.replace('*', '.*')
        self.logger.debug(f"REGEX UPDATE: {rexpr}")
        rexpr = re.compile(rexpr)
        dir = self._ls(path)
        if dir == -1:
            return -1
        return [file for file in dir if rexpr.match(file.decode())]

    def _get_fs(self, part_idx=None) -> list:
        """
        The _get_fs function is a helper function that returns a list of FilesystemHelper objects.
        It takes an optional argument, part_idx, which is the index of the partition to be returned.
        If no part_idx is given, it will return all partitions in the image.

        :param self: Used to Access the instance of the class.
        :param part_idx=None: Used to Specify a default value for the part_idx parameter.
        :return: A list of filesystemhelper objects.

        :doc-author: Telio
        """
        if part_idx:
            return [
                FilesystemHelper(self.img, part)
                for part in self.partition_table
                if int(part.addr) == part_idx
            ]
        return [FilesystemHelper(self.img, part) for part in self.partition_table.fs_vols]

    def _enumerate_available_hkeys(self, filesystemID: int = 0) -> None:
        if not self.system_users:
            self.list_users(filesystemID)
        for hkey in HKEYArtefacts:
            try:
                if hkey.name == "HKEY_USERS_NT":
                    for u in self.system_users:
                        path = hkey.get_path(u)
                        file = self._get_file(
                            filesystemID=filesystemID, filename=path.decode("ascii")
                        )
                        HK = HKEY(hkey.name, path, file)
                else:
                    path = hkey.get_path("")
                    file = self._get_file(filesystemID=filesystemID, filename=path.decode("ascii"))
                    HK = HKEY(hkey.name, path, file)
            except:
                continue
            self.available_hkeys.append(HK)
        return self.available_hkeys

    def write_file(
        self,
        ewf_path: str,
        host_path: str,
        filesystemID: int = 0,
    ) -> int:
        try:
            file = self._get_file(filesystemID=filesystemID, filename=ewf_path)
        except Exception as e:
            print(f"{e}  -  Can't access requested file on EWF image!")
            return -1
        try:
            self._write_data(file.raw_data, host_path)
        except Exception as e:
            print(f"{e}  -  We were not able to export data to host!")
            return -2
        return 0

    def expand_path(self, path: str) -> list:
        if not "*" in path:
            return [path]

        parts = path.split("*")
        base_dir = parts[0]
        print(f"BD: {base_dir} - PARTS: {parts}")
        lsdir = self._ls(base_dir)
        if lsdir == -1:
            return []
        subdirs = [d for d in lsdir if self._get_file(d).is_directory()]
        for subdir in subdirs:
            rest_path = "*".join(parts[1:])
            new_path = base_dir + subdir + rest_path
            print(new_path)
            results += self.expand_path(new_path)
        return results

    def _format_tkap_path(self, path: str):
        paths = []
        path = path.replace("\\", "/")
        path = path.replace("//", "/")
        path = path.replace("C:", "")
        self.logger.debug(path)

        if "%user%" in path:
            for u in self.system_users:
                self.logger.debug(f"user: {u}")
                paths.append(path.replace("%user%", u.decode()))
            self.logger.debug(f"FMTWINDWS RET: {paths}")
            return paths
        paths.append(path)

        for path in paths:
            paths.remove(path)
            tmp = self.expand_path(path)
            paths.extend(tmp)
        self.logger.debug(f"FMTTKAP RET: {paths}")
        return paths

    def write_from_parser(self, arglist: list[Target], filesystemID: int = 0) -> None:
        for scope in arglist:
            for target in scope:
                ewf_files = []
                paths = self._format_tkap_path(target.path)
                for path in paths:
                    if target.recursive:
                        self.logger.debug(f"RECURSE: {target}\n\n{path}")
                        flist = self._find_file_in_dir(path, "*", filesystemID)
                    else:
                        self.logger.debug(f"FILEMASK: {target}\n\n{path}")
                        flist = self._find_file_in_dir(path, target.file_mask, filesystemID)
                        self.logger.debug(f"return {flist} path {path}, name {target.name}, fsid {filesystemID}")
                    if flist == -1:
                      self.logger.debug(f"FLIST: {flist}")
                      continue
                    self.logger.debug(f"Found {len(flist)} corresponding files: {flist} at {path}")

                    for f in flist:
                        ewf_path = path + f.decode()
                        ewf_files.append(ewf_path)
                for ewf_f in ewf_files:
                    export_path = target.export_path + ewf_f
                    export_dir, s, tmp = export_path.rpartition('/')
                    self.logger.debug(f"Attempting to write {ewf_f} at\n\n {export_path}\n")
                    if not os.path.exists(export_dir):
                        try :
                          os.makedirs(export_dir,  0o740)
                        except Exception as e:
                            self.logger.error(f"{e}  -  WE WERE NOT ABLE TO CREATE DIR {export_dir}")
                    self.logger.debug(f"f: {ewf_f},\n ep: {export_path},\n fsid {filesystemID}")
                    self.write_file(ewf_f, export_path, filesystemID)

    def list_users(self, filesystemID: int = 0) -> list[bytes]:
        user_ls = self.filesystems[filesystemID].ls("/Users")[2:]
        self.system_users = [u for u in user_ls if u not in DEFAULT_USER]
        return self.system_users

    def get_hkeys_files(
        self,
        filesystemID: int = 0,
        filter: Optional[list[str]] = False,  # filter should be a list of hkey.name values
        export: Optional[bool] = False,
        export_path: Optional[str] = False,
    ) -> list[dict]:
        if not self.available_hkeys:
            self._enumerate_available_hkeys(filesystemID)
        print("start")
        for hkey in self.available_hkeys:
            print("c")
            if filter:
                if hkey.name in filter:
                    continue
            print(f"-{export_path}- t: {type(export_path)} {export_path is True}")
            if export:
                print(f"test export {export_path}")
                try:
                    if export_path == "" or ".":
                        if not os.path.exists("./_FOUINE_EXPORTS"):
                            os.mkdir("_FOUINE_EXPORTS")
                        self._write_data(
                            hkey.file.raw_data,
                            f"./_FOUINE_EXPORTS/{hkey.name}",
                        )
                    else:
                        self._write_data(hkey.file.raw_data, f"{export_path}/{hkey.name}")
                except Exception as e:
                    print(f"{e}  -  We were not able to export data to host!")
        return self.available_hkeys

    def get_MFT(
        self,
        filesystemID: int = 0,
        export: Optional[bool] = False,
        export_path: Optional[str] = None,
    ) -> File:
        """
        The get_MFT function is used to retrieve the MFT from a specified filesystem.
        The function takes two optional arguments:
          - export (bool): If set to True, the function will export the raw MFT data as a binary file.
          - export_path (str): The path where you want to save your exported file. This argument is required if you specify 'export' as True.

        :param self: Used to Refer to the object itself.
        :param filesystemID:Optional[int]=0: Used to Specify the filesystem to use.
        :param export:Optional[bool]=False: Used to Determine whether or not the user wants to export the file.
        :param export_path:Optional[str]=None: Used to Specify the path to export the mft file to.
        :return: The mft of the specified filesystem.

        :doc-author: Telio
        """
        file = self._get_file(filesystemID=filesystemID, filename="$MFT")
        if export:
            if export_path:
                self._write_data(
                    file.raw_data,
                    export_path,
                )
                return file
            raise ValueError("Export path was not specified dumbass")
        return file


"""
  Il faut réaliser un outil en Python pour extraire les fichiers intéressants pour le forensic, d'une image disque au format EWF, celle utilisée en cours par exemple.

  Vous devez extraire au minimum :

  - les fichiers du registre système et les ruches utilisateur,
  - Les navigateurs Internet Edge, Internet Explorer, Firefox et Chrome,
  - les journaux Windows Security et System au minimum,
  - et la MFT

  La liste des fichiers à extraire devra être au format yaml, notamment pour indiquer les outils / commandes à utiliser par la suite (B.2).
  Il ne s'agit pas d'être exhaustif, mais de prendre en compte les données sources étudiées en cours.
  Il est conseillé d'utiliser des expressions régulières, mais seuls les fichiers prévus doivent être extraits.

  Il est également conseillé d'utiliser, en back end, les commandes The Sleuth Kit suivantes: mmls, fls et icat

  On restreindra l'outil aux fichiers à extraire venant dune image Windows 7 à Windows 11.

  L'outil devra fonctionner sous Windows ou Linux, avec Python 3.

"""
