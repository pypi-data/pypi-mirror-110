import functools
import hashlib
import os
import shutil
from os import stat_result
from typing import BinaryIO, Generator, List, TextIO, Union

from bacx.storage.engines.engine import StorageEngine

"""
TODO:
v sucasnosti je logika, ze sa stahovat mozu iba subory. Nie priecinky. Je to ok? (principialne nie)
Tyka sa aj veci ako `get_local_path`. 
"""


class LocalDrive(StorageEngine):
    """
    LocalDrive is storage engine, which resides on your physical drive, in `link` directory.
    Basically, it is wrapper for Python's builtin open() method.
    For details, about it's methods see help(LocalDrive) and help(StorageEngine).
    """

    def __init__(self, link: str = None, cache_path: str = None, other: dict = None, remote: dict = None):
        """See LocalDrive.__doc__ and StorageEngine.__doc__"""
        if not isinstance(link, str):
            raise TypeError(f"LocalDrive requires `link` argument to be a string path to base directory.")
        if not os.path.isdir(link):
            raise NotADirectoryError(f"Provided path to base directory (`link`) does not exists (got: `{link}`)")
        super().__init__(link=link, cache_path=cache_path, other=other, remote=remote)

    def get_real_path(self, path):
        """
        Path used by user is always relative to base directory, and target file must be inside base directory.
        Therefore path can't starts with `/`, can't contain `/../` and must starts with `link`.
        :return: `path` prefixed with path to base directory (`link`)
        """
        # TODO get_real_path(".") nie je aktualny pricinok ale appendne `.` To je ok?
        if path.startswith("/"):
            raise ValueError(f"LocalDrive path can't starts with `/`. " f"Path is always relative to base directory")
        path = os.path.join(self._link, path)
        if "/../" in path:
            raise ValueError(f"LocalDrive does not allow using super directory (`/../`).")
        return path

    def assert_file(function):
        """
        Checks, whether first argument of decorated function is path to a file.
        """

        @functools.wraps(function)
        def modified(self, path, *args, **kwargs):
            if not self.is_file(path):
                raise FileNotFoundError(f"File `{path}` does not exists.")
            return function(self, path, *args, **kwargs)

        return modified

    def assert_directory(function):
        """
        Checks, whether first argument of decorated function is path to a dictionary.
        """

        @functools.wraps(function)
        def modified(self, path, *args, **kwargs):
            if not self.is_dir(path):
                raise NotADirectoryError(f"Directory `{path}` does not exists.")
            return function(self, path, *args, **kwargs)

        return modified

    def assert_file_or_directory(function):
        """
        Asserts that first argument of decorated function is path to file or directory.
        """

        @functools.wraps(function)
        def modified(self, path, *args, **kwargs):
            if not (self.is_file(path) or self.is_dir(path)):
                raise FileNotFoundError(f"Item `{path}` is neither file, nor directory.")
            return function(self, path, *args, **kwargs)

        return modified

    def open(self, filepath, *args, **kwargs) -> Union[TextIO, BinaryIO]:
        return open(self.get_real_path(filepath), *args, **kwargs)

    @assert_file
    def get_local_path(self, filepath: str) -> str:
        return self.get_real_path(filepath)

    def mkdir(self, dir_name: str, mode=0o777) -> None:
        return os.mkdir(self.get_real_path(dir_name), mode)

    def mkdirs(self, dirpath: str, mode=0o777, exist_ok=False) -> None:
        return os.makedirs(self.get_real_path(dirpath), mode, exist_ok)

    def is_file(self, filepath: str) -> bool:
        return os.path.isfile(self.get_real_path(filepath))

    def is_dir(self, dirpath: str) -> bool:
        return os.path.isdir(self.get_real_path(dirpath))

    def exists(self, path: str) -> bool:
        return self.is_dir(path) or self.is_file(path)

    @assert_file
    def md5_sum(self, filepath: str) -> bytes:
        filepath = self.get_real_path(filepath)
        with open(filepath, "rb") as file:
            return hashlib.md5(file.read()).digest()

    def _listing_generator(self, base, prefix, depth, filter: str = StorageEngine.DIR_AND_FILE) -> Generator:
        if depth < 1:
            yield from []
        else:
            for item in os.listdir(os.path.join(base, prefix)):
                prefixed_path = os.path.join(prefix, item)
                absolute_path = os.path.join(base, prefixed_path)
                if os.path.isfile(absolute_path) and (
                    filter == StorageEngine.FILE or filter == StorageEngine.DIR_AND_FILE
                ):
                    yield prefixed_path
                elif os.path.isdir(absolute_path):
                    if filter == StorageEngine.DIR or filter == StorageEngine.DIR_AND_FILE:
                        yield prefixed_path
                    yield from self._listing_generator(base, prefixed_path, depth - 1, filter)

    @assert_directory
    def list(self, dirpath: str, filter: str = StorageEngine.DIR_AND_FILE, depth: int = 1) -> List[str]:
        return [*self._listing_generator(self.get_real_path(dirpath), "", depth, filter)]

    @assert_file_or_directory
    def stat(self, path: str) -> stat_result:
        return os.stat(self.get_real_path(path))

    @assert_file_or_directory
    def size(self, path: str) -> int:
        return os.path.getsize(self.get_real_path(path))

    @assert_directory
    def rmtree(self, dirpath: str) -> None:
        return shutil.rmtree(self.get_real_path(dirpath))

    @assert_directory
    def rmdir(self, dirpath: str) -> None:
        if len(self.list(dirpath)) > 0:
            raise OSError(f"Directory `{dirpath}` is not empty.")
        return os.rmdir(self.get_real_path(dirpath))

    @assert_file
    def delete(self, filepath: str) -> None:
        return os.remove(self.get_real_path(filepath))
