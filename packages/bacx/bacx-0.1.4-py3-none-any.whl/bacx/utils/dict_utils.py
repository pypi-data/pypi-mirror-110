import logging
from functools import reduce
from typing import Any, Iterable, Union

logger = logging.getLogger(__name__)


def map_values(mapper: callable, data: Any) -> Any:
    """
    Traverse through the structured data and call mapper on each processed value.
    `mapper` is applied after the sub-structure is processed to prevent infinite recursion using mappers like x -> [x].
    :return: deep copy of the structure with mapped values
    """
    if isinstance(data, dict):
        return mapper(type(data)({key: map_values(mapper, value) for key, value in data.items()}))
    if isinstance(data, list):
        return mapper(type(data)([map_values(mapper, value) for value in data]))
    if isinstance(data, tuple):
        return mapper(type(data)(map_values(mapper, value) for value in data))
    return mapper(data)


def replace_values_recursive(data, old_val, new_val):
    """
    Replaces all values in input data structure by desired value and returns modified data structure.
    :param data: list, tuple or directory
    :param old_val: value to be replaced
    :param new_val: replacing value
    :return: deep copy of the structure with replaced values
    """

    def replacer(value):
        return new_val if value == old_val else value

    return map_values(replacer, data)


def deep_dict_merge(first, second):
    """
    Merges two dictionaries. Accepts also types derived from python dictionary.
    Second dictionary has higher priority than the first.
    :param first:
    :param second:
    :return: new copy of first and second dictionary, with merged content
    """
    if isinstance(first, dict) and isinstance(second, dict):
        result = {**first}
        for key, val in second.items():
            if key in first:
                val = deep_dict_merge(first[key], val)
            result[key] = val
        # second operand has higher priority, so over-write first's argument type
        return type(second)(result)
    return second


def get_nested_item(data: Union[dict, tuple, list], keys: Iterable[Any]) -> Any:
    return reduce(lambda dat, idx: dat[idx], keys, data)


def replace_prefixed_values(data: Any, prefix: str, value_map: dict, warn_missing: bool = True) -> Any:
    """
    Replace all strings of form '<prefix><value>' to 'value_map[<value>]' in data.
    Example:
    >>>replace_prefixed_values({"key": "file://hello"}, "file://", {"hello": "gs://world"}}
    >>>-> {"key": "gs://world"}
    :return: deep copy of `data` with replaced values
    """

    def replacer(value):
        if isinstance(value, str) and value.startswith(prefix):
            new_value = value[len(prefix) :]
            if new_value in value_map:
                return value_map[new_value]
            if warn_missing:
                logger.warning(f"Value {value} starts with {prefix} but is missing in value_map.")
        return value

    return map_values(replacer, data)


""" 
TODO:
    def map_items():
    def map_keys():
"""
