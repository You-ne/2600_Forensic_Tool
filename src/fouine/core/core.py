import pyewf
import pytsk3
from colorama import Fore, Style
from typing import Optional, Union

from tsk3_helper import *

class EwfImg(pytsk3.Img_Info):
  """
  A class to manage the image dump
  """
  def _get_partitions(self):
    return pytsk3.Volume_Info(self)
  
  def __init__(self, ewf_handle):
    self._ewf_handle = ewf_handle
    super(EwfImg, self).__init__(
        url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)
    self.partTable = self._get_partitions() 

  def close(self):
    self._ewf_handle.close()

  def read(self, offset, size):
    self._ewf_handle.seek(offset)
    return self._ewf_handle.read(size)

  def get_size(self):
    return self._ewf_handle.get_media_size()


class FilesystemHelper(pytsk3.FS_Info):
  def __repr__(self):
    return f"{Fore.MAGENTA}TYPE: {Fore.YELLOW} {self.fs_type}"

  def __init__(self, img, partition):
    super(FilesystemHelper, self).__init__(img, offset=(partition.start*512))
    self.fs_type = FS_TYPE_ENUM(self.info.ftype)
  def fstype(self, ):
    return self.fs_type.name

  def ls_dir(self, path:str='/'):
    directory = self.open_dir(path)
    return [file_handle.info.name.name for file_handle in directory]
  
  def read_file(self, file_path:str, raw:Optional[bool]=False):
    file = self.open(file_path)
    if raw:
      return file.read_random(0, file.info.meta.size)
    return file


class Fouine():
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
      return [volume for volume in self for fs in SUPPORTED_FS if fs in volume.desc]

    def __init__(self, partitions:list) -> None:
      super().__init__(partitions)
      self._tsk_fs = [
      b'TFS', b'NTFS', b'FAT', b'FAT12', b'FAT16', b'FAT32', b'EXT2', b'EXT3',
      b'EXT4', b'HFS+', b'ISO', b'UFS', b'APFS', b'data']
      try:
        self.fs_vols = self._list_vol_fs()
      except Exception as e:
        print(f"{e} \n {Fore.YELLOW} NOTE: Runtime Error can occur if your EWF image is incomplete{Style.RESET_ALL}")
      
    def __repr__(self):
      ret = ""
      for part in self:
        ret += f"{Fore.RED}{part.addr}  |  {Fore.BLUE}{part.start} - {part.start*512}\t\t{Fore.GREEN}{part.desc}{Style.RESET_ALL}\n"
      return ret
    
    @classmethod
    def from_volume_info(cls, volume):
      return cls([p for p in volume])

  def _export(self, data: Union[bytes,bytearray,str], path):
    with open(path, 'wb') as f:
      f.write(data)
  
  def _get_fs(self, part_idx=None) -> list:
    if part_idx:
      return [FilesystemHelper(self.img, part)
               for part in self.partition_table if int(p.addr) == part_idx]
    return [FilesystemHelper(self.img, part)
              for part in self.partition_table.fs_vols]

  def __init__(self, filename:str=None,) -> None:
    self.raw = filename
    self.filenames = pyewf.glob(self.raw) if self.raw else None
    self.handle = pyewf.handle()
    self.handle.open(self.filenames)
    self.img = EwfImg(self.handle)
    self.partition_table = self.PartitionTable.from_volume_info(self.img.partTable)
    self.filesystems = self._get_fs()

  def ls_users(self, filesystemID:Optional[int]=0):
    user_dir_ls = self.filesystems[filesystemID].ls_dir('/Users')[2:]
    return [user for e in user_dir_ls if (not 'efault' in e) and (not 'Public' in e) and (not 'All Users' in e)]

  def get_MFT(self, filesystemID:Optional[int]=0, 
              export: Optional[bool]=False, export_path: Optional[str]=None):
    if export:
      if export_path:
        self._export(self.filesystems[filesystemID].read_file('$MFT', raw=True), export_path)
        return
      raise ValueError("Export path was not specified dumbass")
    return self.filesystems[filesystemID].read_file('$MFT')
    pass

  def get_news(self,):
    pass

  def ripp_reg(self,):
    pass

  def dump_browsers(self,):
    pass

'''
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

'''