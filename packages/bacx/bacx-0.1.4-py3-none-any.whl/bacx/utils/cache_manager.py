import shutil
import tempfile
from os.path import isabs, isdir, join


class CacheManager:
    """
    Class for maintaining cache folders.
    Path to cache folders created through this class won't be overlapping, or issued multiple times.
    """

    def __init__(self, directory: str = None, clean: bool = False):
        """
        Creates cache manager class.
        :param directory: path to directory, where can be cached flies placed.
        Default temporary directory is directory provided by python.
        :raises: FileNotFoundError, if default_dir path does not exists.
        """
        self._clean_on_delete = clean
        self._directories = []
        if directory is not None:
            if not isdir(directory):
                raise FileNotFoundError(f"Folder {directory} does not exists.")
            if not isabs(directory):
                raise ValueError(f"Base directory must be absolute path (got: '{directory}').")
            else:
                self._base_directory = directory
        else:
            self._base_directory = tempfile.gettempdir()

    def is_already_used(self, directory: str) -> bool:
        """
        Checks, whether directory is not already used in this
        CacheManager instance.
        :return: true, if directory is already used. False otherwise.
        """
        for existing_dir in self._directories:
            if existing_dir.startswith(directory) or directory.startswith(existing_dir):
                return True
        return False

    def get_new_directory(self) -> str:
        """
        Creates temporary directory inside base directory (see CacheManager init).
        :return: string, absolute path to newly created temporary directory.
        """
        temp_dir = tempfile.mkdtemp(dir=self._base_directory)
        self._directories.append(temp_dir)
        return temp_dir

    def add_directory(self, directory: str, base: str = None) -> None:
        """
        Adds existing cache directory to CacheManager. Directory must exist and absolute
        path must be provided. If only directory name is provided, default base set in CacheManager
        will be used.
        :param directory: name of the directory (that base+name creates an absolute path to the directory),
        or absolute path to directory.
        :param base: absolute base
        :raises ValueError: if base is not absolute or if directory does not exists or if directory is
        already used as cache directory.
        """
        if base is not None:
            if not isabs(base):
                raise ValueError(f"Base must be absolute path.")
            directory = join(base, directory)
        elif not isabs(directory):
            raise ValueError(f"Directory must be specified by full path (got: {directory})")
        if not isdir(directory):
            raise ValueError(f"Directory '{directory}' does not exists.")
        if self.is_already_used(directory):
            raise ValueError(f"Directory '{directory}' is already used as cache directory.")
        self._directories.append(directory)

    def _remove_directory(self, directory: str) -> None:
        """
        Removes directory and it's files and sub directories.
        :param directory: absolute path to directory to be removed.
        :raises: FileNotFoundError
        """
        if directory not in self._directories:
            raise FileNotFoundError(f"Directory '{directory}' is not in this CacheManager.")
        else:
            shutil.rmtree(directory)
            self._directories.remove(directory)

    def _remove_all(self) -> None:
        """
        Removes all cache folders and their content.
        """
        for directory in [*self._directories]:
            self._remove_directory(directory)

    def __del__(self):
        if self._clean_on_delete:
            self._remove_all()
