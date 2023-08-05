import os
from os import stat_result
from typing import BinaryIO, List, TextIO, Union


def hook_file_close(file, callback, *args, close_first: bool = True, **kwargs):
    """
    Hooks `callback` call to `close()` method of given `file`.
    :param args: arguments for `callback`
    :param close_first: call `callback` after or before file `close()`.
    If True (default), then when `file.close()` will be called, file will be closed and then callback
    will be called. If False, callback will be called before file close.
    :param kwargs: key-value arguments for `callback`
    :return: original `file` with modified `close()` method.
    """
    original_close = file.close

    def new_close(*orig_args, **orig_kwargs):
        if close_first:
            original_close(*orig_args, **orig_kwargs)
            return callback(*args, **kwargs)
        else:
            callback(*args, **kwargs)
            return original_close(*orig_args, **orig_kwargs)

    file.close = new_close
    return file


class StorageEngine:
    """
    StorageEngine implements interface for storage engines and default behaviour for some methods.
    Key method is `open()`. If storage engine implements `open()`, some of
    these methods will be working in default behaviour (e.g. `download_to_file` will read using
    implemented `open()` method and write to physical drive).
    See StorageEngine.__init__.__doc__
    """

    DIR = "dir"
    FILE = "file"
    DIR_AND_FILE = "dir_and_file"

    def __init__(self, link: str = None, cache_path: str = None, other: dict = None, remote: dict = None):
        """
        See StorageEngine.__doc__
        :param link: path to folder, where files are stored (mounting point)
        :param cache_path: path to folder, where files can be cached
        :param other: dictionary with additional arguments
        :param remote: dictionary with remote (cloud) connection details
        """
        self._link = link
        self._cache_path = cache_path
        self._other = other
        self._remote = remote

    def delete(self, filepath: str) -> None:
        """
        Removes file.
        :raise FileNotFoundError: if file does not exists
        :raise IsADirectoryError: if object is directory and not file
        """
        raise NotImplementedError

    def rmdir(self, dirpath: str) -> None:
        """
        Removes empty directory.
        :raise FileNotFoundError: if directory does not exists
        :raise OSError: if directory is not empty
        """
        raise NotImplementedError

    def rmtree(self, dirpath: str) -> None:
        """
        Removes directory recursively.
        :raise FileNotFoundError: if directory does not exists
        """
        raise NotImplementedError

    def size(self, path: str) -> int:
        """
        :return: size of file (for directory it is zero constant).
        :raise FileNotFoundError: if object does not exists
        """
        raise NotImplementedError

    def stat(self, path: str) -> stat_result:
        """
        :return: stat details for file system object
        :raise: FileNotFoundError: if object does not exists
        """
        raise NotImplementedError

    def list(self, dirpath: str, filter: str = DIR_AND_FILE, depth: int = 1) -> List[str]:
        """
        Returns list of file system object names (files, directories). If depth > 1, lists also
        objects in directories to depth (e.g. if depth=2, list also directories in `dirpath`).
        Records from sub-directories will be prefixed with their path, relative to `dirpath`.
        :param filter: DIR-only directories, FILE-only files, DIR_AND_FILE-all (default)
        :param depth: max dept to which subdirectories will be listed (default is 1, only current directory)
        :return: list of file system object names in current directory (and recursive, if depth > 1)
        :raise FileNotFoundError: if directory does not exists
        """
        raise NotImplementedError

    def md5_sum(self, filepath: str) -> bytes:
        """
        :return: string md5 sum of file in binary format
        :raise FileNotFoundError: if file does not exists
        """
        raise NotImplementedError

    def exists(self, path: str) -> bool:
        """
        :return: true, if file system object (file or directory) exists.
        :raise FileNotFoundError: if object does not exists
        """
        raise NotImplementedError

    def is_file(self, filepath: str) -> bool:
        """
        :return: True, if `filepath` is path to a file. False otherwise.
        """
        raise NotImplementedError

    def is_dir(self, dirpath: str) -> bool:
        """
        :return: True, if 'dirpath' is path to directory. False otherwise.
        """
        raise NotImplementedError

    def mkdir(self, dir_name: str, mode=None) -> None:
        """
        Creates directory.
        :raise FileExistsError: if directory already exists
        :raise FileNotFoundError: if some directory within dirpath does not exists
        """
        raise NotImplementedError

    def mkdirs(self, dirpath: str, mode=None, exist_ok=False) -> None:
        """
        Creates directory recursively.
        :param exist_ok: if False, a FileExistsError is raised if the target directory already exists
        """
        raise NotImplementedError

    def mkfile(self, filepath: str) -> None:
        """
        Creates empty file.
        :raise FileExistsError: if file already exists
        """
        self.open(filepath, "x").close()

    def open(self, filepath: str, mode: str = "rw", *args, **kwargs) -> Union[TextIO, BinaryIO]:
        """
        Opens file and returns it's file pointer.
        :raise FileNotFoundError: if file does not exists
        :raise OSError: if file can't be opened
        """
        raise NotImplementedError

    def read_as_text(self, filepath: str) -> str:
        """
        :return: content of file in string
        :raise FileNotFoundError: if file does not exists
        """
        return self.open(filepath, "r").read()

    def read_as_bytes(self, filepath: str) -> bytes:
        """
        :return: content of file in bytes
        :raise FileNotFoundError: if file does not exists
        """
        return self.open(filepath, "rb").read()

    def download_to_file(self, filepath: str, local_path: str, exist_ok: bool = True) -> None:
        """
        Downloads file and writes it to 'local_path'.
        If storage is local (not cloud), download means copy (copy from `filepath` to `local_path`)
        :param local_path: path to directory or full path to file, where remote file will be written.
        :raise FileNotExistsError: if 'filepath' does not exists
        :raise FileExistsError: if exists_ok is False, and local_file exists (or exists_ok is False and name of the
        file to be downloaded exists in local_dir)
        """
        if os.path.isdir(local_path):
            local_path = os.path.join(local_path, os.path.basename(filepath))
        if exist_ok is False and os.path.isfile(local_path):
            raise FileExistsError(f"File `{os.path.basename(local_path)}` already exists.")
        with open(local_path, "wb") as out_file:
            in_file = self.open(filepath, "rb")
            out_file.write(in_file.read())
            in_file.close()

    def get_local_path(self, filepath: str) -> str:
        """
        :return: path to cached file from 'filepath'. If file is not cached, empty string is returned.
        :raise FileNotExistsError: if 'filepath' does not exists
        """
        raise NotImplementedError

    def upload_from_file(self, filepath: str, local_filepath: str) -> None:
        """
        Writes file from local_filepath to filepath.
        If storage is local (not cloud), upload means copy (copy from `local_file` to `filepath`)
        :raise FileNotExistsError: if 'local_filepath' does not exists
        """
        with open(local_filepath, "rb") as in_file:
            out_file = self.open(filepath, "wb")
            out_file.write(in_file.read())
            out_file.close()

    def write_as_text(self, filepath: str, content: str) -> None:
        """
        Writes `content` (string) to file in `filepath`
        """
        file = self.open(filepath, "w")
        file.write(content)
        file.close()

    def write_as_bytes(self, filepath: str, content: bytes) -> None:
        """
        Writes `content` (binary data) to file in `filepath`
        """
        file = self.open(filepath, "wb")
        file.write(content)
        file.close()
