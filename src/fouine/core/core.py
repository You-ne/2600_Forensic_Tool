import pyewf
import pytsk3


class EwfImg(pytsk3.Img_Info):
  """
  A class to manage the image dump
  """
  def _get_partitions(self):
    return pytsk3.Volume_Info(self)
  
  def __init__(self, ewf_handle):
    self._tsk_fs = ['TFS', 'NTFS', 'FAT', 'FAT12', 'FAT16', 'FAT32', 'EXT2', 'EXT3', 'EXT4', 'HFS+', 'ISO', 'UFS', 'APFS', 'data']
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

  def list_fs(self):
    return [volume for volume in self.partTable for fs in self._tsk_fs if fs in str(volume.desc)]
      


class Fouine():
  """
    Take a file name in argument and return an object to work with EWF disk from a forensic point of view
  """
  def __init__(self, filename:str=None,) -> None:
    self.raw = filename
    self.filenames = pyewf.glob(self.raw) if self.raw else None
    self.handle = pyewf.handle()
    self.handle.open(self.filenames)
    self.img = EwfImg(self.handle)
    self.partition_table = self.img.partTable



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