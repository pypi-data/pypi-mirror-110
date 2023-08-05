import tempfile
from os import path
from typing import Iterator, KeysView, List

from yamale import YamaleError

from bacx.storage.engines.aws_drive import AwsDrive
from bacx.storage.engines.engine import StorageEngine
from bacx.storage.engines.gcloud_drive import GcloudDrive
from bacx.storage.engines.local_drive import LocalDrive
from bacx.utils.cache_manager import CacheManager
from bacx.utils.config import Config
from bacx.utils.dict_utils import get_nested_item
from bacx.utils.import_utils import import_from_module

# global dict and list of module-registered storage engines
# (this variable is used for example also in tests)
CUSTOM_ENGINE = "custom"
STORAGE_ENGINES_DICT = {"gcloud": GcloudDrive, "local": LocalDrive, "aws": AwsDrive}


class StorageManager:
    """
    Creates instance of the StorageManager according to configuration file (use path or config).
    :param path: string path to file with configuration
    :param config: dictionary with configuration
    :raises ValueError, KeyError, AttributeError:
    """

    SCHEMA_PATH = path.join(path.dirname(__file__), "schema.yaml")
    # manager keys&values:
    DEFAULT = "default"
    PATH = "path"
    CLEAN = "clean"
    ON_SHUTDOWN = "on_shutdown"
    KEYS_TO_CACHE = ("settings", "cache")
    VALUE_OF_DEFAULT_CACHE = {
        PATH: tempfile.gettempdir(),
        ON_SHUTDOWN: None,
    }
    KEYS_TO_CACHE_PATH = ("settings", "cache", "path")
    # storage keys:
    LINK = "link"
    OTHER = "other"
    REMOTE = "remote"
    CACHE_DIR = "cache_dir"
    IS_DEFAULT = "is_default"

    def _check_configuration_syntax(self, configuration: Config) -> None:
        """
        Checks, whether input configuration is valid.
        TODO: duplicity in is_default is not checked here
        :raise RuntimeError: if configuration is invalid
        """
        try:
            configuration.check_yamale_schema(self.SCHEMA_PATH)
        except YamaleError as error:
            raise RuntimeError(getattr(error, "message", str(error)))

    def _create_cache_manager(self, configuration: Config) -> CacheManager:
        """
        Setups cache manager according to StorageManager configuration. If cache is None, default
        cache manager will be returned (manager, which resides inside the OS specified temp folder)
        :return: CacheManager
        """
        if configuration.settings.cache is not None:
            return CacheManager(
                configuration.settings.cache.path,
                True if configuration.settings.cache.on_shutdown == self.CLEAN else False,
            )
        else:
            return CacheManager(tempfile.gettempdir())

    def _load_configuration(self, path: str = None, config: dict = None, keys: List[str] = None) -> Config:
        """
        Loads configuration from file or from configuration
        dictionary. Method also auto-fills default_storage values.
        :param path: path to yaml file with configuration
        :param config: configuration in dictionary
        :param keys: if desired configuration is nested (somewhere deep inside),
        you can specify key sequence, which points to your configuration.
        :return: Config
        :raise SyntaxError, if configuration does not satisfy StorageManager configuration schema.
        """
        config = Config(path=path) if config is None else Config(data=config)
        if keys is not None:
            config = Config(data=get_nested_item(config, keys))
        self._check_configuration_syntax(config)

        # autofill default cache settings:
        if config.settings.cache == self.DEFAULT:
            config = config.set_in(self.KEYS_TO_CACHE, self.VALUE_OF_DEFAULT_CACHE)
        if config.settings.cache is not None:
            if config.settings.cache.path == self.DEFAULT:
                config = config.set_in(self.KEYS_TO_CACHE_PATH, tempfile.gettempdir())
        return config

    def _create_engine(self, name: str, engine_config: Config) -> StorageEngine:
        """
        Creates and returns an instance of a storage manager.
        :param name: name of this engine
        :param engine_config: configuration for this engine
        """
        # get: engine_type, class_handle
        if engine_config.type == CUSTOM_ENGINE:
            class_handle = import_from_module(engine_config.module)
        else:
            class_handle = STORAGE_ENGINES_DICT[engine_config.type]
        # check possible errors:
        if not issubclass(class_handle, StorageEngine):
            raise ValueError(f"Class handling engine with name `{name}` is not a sub-class of StorageEngine.")
        if engine_config.get(self.IS_DEFAULT, False):
            if self._default_storage_name is not None:
                raise ValueError(f"Configuration file contains multiple default storages.")
            else:
                self._default_storage_name = name
        # check cache folder configuration:
        cache_path = engine_config.get(self.CACHE_DIR)
        if cache_path is not None:
            self._cache_manager.add_directory(cache_path)
        elif self._configuration.settings.cache is not None:
            cache_path = self._cache_manager.get_new_directory()
        # create storage engine instance:
        return class_handle(
            link=engine_config.get(self.LINK),
            cache_path=cache_path,
            other=engine_config.get(self.OTHER),
            remote=engine_config.get(self.REMOTE),
        )

    def __init__(self, path: str = None, config: dict = None, keys: List[str] = None):
        if (path is not None) + (config is not None) != 1:
            raise AttributeError(f"Invalid number of arguments: use path or config")
        self._default_storage_name = None
        self._storages = {}
        self._configuration = self._load_configuration(path, config, keys)
        self._cache_manager = self._create_cache_manager(self._configuration)
        self._storages = {
            name: self._create_engine(name, config) for name, config in self._configuration.storages.items()
        }

    def default_storage(self) -> StorageEngine:
        """Returns default storage engine, or None"""
        return self._storages.get(self._default_storage_name)

    def __getitem__(self, name: str) -> StorageEngine:
        """Returns storage engine with name 'name'"""
        return self._storages[name]

    def __contains__(self, name) -> bool:
        """Returns true, if Storage Manager contains engine with name 'name'"""
        return name in self._storages

    def storages(self) -> Iterator[StorageEngine]:
        """Returns iterator over storage engines."""
        return iter(self._storages.values())

    def storage_names(self) -> KeysView[str]:
        """Returns names of storage engines."""
        return self._storages.keys()

    def __iter__(self) -> Iterator[str]:
        """Returns iterator over names of storage engines."""
        return iter(self._storages.keys())
