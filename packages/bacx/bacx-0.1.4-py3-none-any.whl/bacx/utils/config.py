import io
import json
from functools import reduce

import yamale
import yaml

from bacx.utils import dict_utils
from bacx.utils.namedict import Namedict


class Config(Namedict):
    @staticmethod
    def from_obj(data, _check_dict=True):
        return Config(data=data)

    def set_in(self, *args) -> "Config":
        """
        Substitute (one or multiple substitutions) and return new Config.
        :param args: sequence of k substitution, in total 2*k arguments.
        Each substitution is defined by key, and new_value. Key may be direct key to this
        Config instance, or list of keys, which will be used to address substitution.
        Example: set_in('key', 'value')
        Multiple substitutions are processed from left to right:
            set_in('key_first_subst', 'val_first_subst',
                ['key2', 'key2_deeper'], 'val_second_subst').
        :return: new Config with desired substitutions
        """
        # convert to dict, which can be modified:
        data = self.to_obj()
        # iterate through substitutions:
        for keys, value in zip(args[::2], args[1::2]):
            # apply key(s):
            data_ptr = data
            if isinstance(keys, (list, tuple)):
                data_ptr = reduce(lambda dat, idx: dat[idx], keys[:-1], data)
                keys = keys[-1]
            if keys not in data_ptr:
                raise KeyError(f"Can't replace value '{value}': key '{keys}' is not in '{data_ptr}'.")
            data_ptr[keys] = value
        # construct new Config:
        return Config(data=data)

    def merge_config(self, *args: dict) -> "Config":
        """
        Merges configurations with current Config and returns merged Config.
        :param args: one or multiple configurations, which are being to merged to
        this Config. Precedence is from the left to right. Current Config
        instance (self) has lowest priority.
        Configurations must be python dictionaries (Config or Namedict).
        :return: new, merged Config.
        """
        # convert to dict, which can be modified:
        first_config = self.to_obj()
        for second_config in args:
            first_config = dict_utils.deep_dict_merge(
                first_config, second_config if type(second_config) is dict else second_config.to_obj()
            )
        # construct new Config:
        return Config(data=first_config)

    def check_yamale_schema(self, path: str = None) -> None:
        """
        Checks, whether config instance is according to yamale schema.
        :param path: path to schema
        :return:
        """
        yamale.validate(yamale.make_schema(path), yamale.make_data(content=json.dumps(self)))

    def __init__(self, file: io.IOBase = None, path: str = None, data: dict = None) -> None:
        """
        Creates namedict-like dictionary from yaml file (defined by file pointer or file path)
        or from python dictionary.
        :param file: file pointer to yaml file
        :param path: path to yaml file
        :param data: dictionary to be converted to config
        """
        # use file or data:
        if (file is not None) + (path is not None) + (data is not None) != 1:
            raise AttributeError(f"Invalid number of arguments: use file, path or data.")
        if file is not None:
            data = yaml.safe_load(file)
        elif path is not None:
            with open(path, "r") as file:
                data = yaml.safe_load(file)
        if not isinstance(data, dict):
            raise ValueError(f"Input file must be a yaml dictionary.")
        super().__init__({key: Namedict.from_obj(val, _check_dict=False) for key, val in data.items()})
