#!/usr/bin/pyenv python3

"""
Module to obtain file metadata and perform basic operations on files such as
opening, hashing, and typing.  File objects are enhanced Path objects.
"""

import datetime
import hashlib
import magic
from pathlib import Path


class File(Path):
    """
    Base class for file information and actions common to all file types.
    """
    # hack needed to inherit from pathlib
    _flavour = Path('.')._flavour

    def __init__(self, path: str) -> None:
        """
        Initializes File() object from a string or a Path object
        with basic file information, e.g, name, size date stamps, etc.  Files
        are not automatically typed, or hashed as this can take substantial time
        and may not be needed in all circumstances.
        """
        super().__init__()
        self.relative_path = str(path)
        self.absolute_path = str(self.absolute())
        self.extension = self.suffix
        self.status = self.__get_status()
        self.size = self.status.st_size
        self.blocks = self.status.st_blocks
        self.blocksize = self.status.st_blksize
        self.modified = self.__get_date(self.status.st_mtime)
        self.accessed = self.__get_date(self.status.st_atime)
        self.changed = self.__get_date(self.status.st_ctime)
        self.created = self.__get_date(self.status.st_birthtime)
        self.mode = self.status.st_mode
        self.inode = self.status.st_ino
        self.uid = self.status.st_uid
        self.gid = self.status.st_gid
        self.device = self.status.st_dev
        self.hardlinks = self.status.st_nlink
        self.md5 = None
        self.sha1 = None
        self.sha256 = None
        self.file_type = None
        self.mime_type = None

    @classmethod
    def __get_date(cls, ts: float) -> datetime:
        """Private method to return a timezone aware datetime object."""
        # todo: allow timezone conversion
        ts = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
        return ts

    def __get_hash(self, hasher) -> str:
        """Private method to return hash digest based on supplied hasher
        digest, eg, hashlib.md5()."""
        with self.open('rb') as file:
            while True:
                # break into 64k chunks for more efficient hashing
                data = file.read(65536)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()

    def __get_magic(self, mime: bool = False) -> str:
        """Private method to return file type."""
        if self.is_dir() and mime:
            return "binary"
        elif self.is_dir():
            return "directory"
        else:
            return magic.from_file(str(self), mime)

    def __get_status(self):
        """Private method to return file stats."""
        if self.is_symlink():
            return self.lstat()
        else:
            return self.stat()

    def get_md5(self) -> str:
        """Returns and stores the hexadecimal MD5 hash digest attribute of the
        file."""
        hasher = hashlib.md5()
        self.md5 = self.__get_hash(hasher)
        return self.md5

    def get_sha1(self) -> str:
        """Returns and stores the hexadecimal SHA1 hash digest attribute of the
        file."""
        hasher = hashlib.sha1()
        self.sha1 = self.__get_hash(hasher)
        return self.sha1

    def get_sha256(self) -> str:
        """Return and store the hexadecimal SHA256 hash digest attribute of the
        file."""
        hasher = hashlib.sha256()
        self.sha256 = self.__get_hash(hasher)
        return self.sha256

    def get_file_type(self) -> str:
        """Return and store the file type attribute as detected by
        python-magic."""
        self.file_type = self.__get_magic()
        return self.file_type

    def get_mime_type(self) -> str:
        """Return and store the mime type attribute as detected by
        python-magic."""
        self.mime_type = self.__get_magic(mime=True)
        return self.mime_type

    def print_status(self) -> None:
        string = (
            f'  File: {self.absolute_path}\n'
            f'  Size: {self.size}\tBlocks: {self.blocks}\tBlock Sz: {self.blocksize}\n'
            f'Device: {self.device}\tInode: {self.inode}\tLinks: {self.hardlinks}\n'
            f'  Mode: {self.mode}\tUID: {self.uid}\tGID: {self.gid}\n'
            f'Access: {self.accessed}\n'
            f'Modify: {self.modified}\n'
            f'Change: {self.changed}\n'
            f'Create: {self.created}'
        )
        print(string)
        return


def get_files(path: str, pattern: str = '*', recursive: bool = True):
    """
    Return generator of File objects from path matching pattern, with optional
    recursion into subdirectories.  If path is a file, the File object for that
    path is returned.
    """
    p = File(path)

    if p.is_file():
        return p
    if recursive:
        for f in p.rglob(pattern):
            yield File(f)
    for f in p.glob(pattern):
        yield File(f)
