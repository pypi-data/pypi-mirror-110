import re


class Namedict(dict):
    __doc__ = """
    Converts (non-recursively) dictionary to Namedict dictionary.
    Note: if you need recursive constructor, use instance = Namedict.from_obj(nested_dicts)
    Keys, in input dictionary must:
    1) be strings
    2) match __attribute_check regex, for example: abc, ab-c, a123, a-_B__C1x64-_-_    
    3) must starts with letter (upper/lower case)
    Key can't be a string, which is in dir(Namedict).
    Values can be accessed by:
    1) getitem: instance['key']
    2) or by namespace: instance.key
    If key contains dash, namespace key will use underscore.
    For example: inst['a_b-2'] == inst.a_b_2
    :param data: dictionary to be converted.
    Accepts dict-style arguments: Namedict(key1=val, key2=val2 ...)
    """
    _MODIFY_ERROR = ValueError("Namedict object can't be modified")
    _attribute_check = re.compile("^[A-Za-z][A-Za-z0-9_]*$")

    def __getattr__(self, item):
        if item in self._attributes:
            return self[self._attributes[item]]
        raise AttributeError(f"Namedict object has no attribute '{item}'")

    def __setattr__(self, key, value):
        if self._locked:
            raise self._MODIFY_ERROR
        return super().__setattr__(key, value)

    def __setitem__(self, key, value):
        if self._locked:
            raise self._MODIFY_ERROR
        super().__setitem__(key, value)

    def __delitem__(self, key):
        raise self._MODIFY_ERROR

    def __delattr__(self, item):
        raise self._MODIFY_ERROR

    def pop(self, key):
        raise self._MODIFY_ERROR

    def popitem(self):
        raise self._MODIFY_ERROR

    def update(self, __m, **kwargs):
        if self._locked:
            raise self._MODIFY_ERROR
        return super().update(__m, **kwargs)

    def clear(self) -> None:
        raise self._MODIFY_ERROR

    def to_obj(nd_whatever):
        """
        This function recursively converts Namedict dictionary back to python dictionary.
        Function can be used:
            - python_dict = Namedict.to_obj(namedict_instance)
            - python_dict = namedict_instance.to_obj()
        :return: python dictionary equivalent to Namedict instance, which is being converted
        """
        if isinstance(nd_whatever, dict):
            return {key: Namedict.to_obj(val) for key, val in nd_whatever.items()}
        if isinstance(nd_whatever, list):
            return [Namedict.to_obj(item) for item in nd_whatever]
        if isinstance(nd_whatever, tuple):
            return tuple(Namedict.to_obj(item) for item in nd_whatever)
        return nd_whatever

    @staticmethod
    def from_obj(data, _check_dict=True):
        """
        This function will recursively convert input data (must be dictionary).
        :param data:
        :return: Namedict representing input data
        :raise TypeError: if input data is not dictionary
        """
        if _check_dict and not isinstance(data, dict):
            raise TypeError(f"Namedict must be constructed from dictionary (got: {type(data)})")
        if isinstance(data, dict):
            return Namedict({key: Namedict.from_obj(val, False) for key, val in data.items()})
        if isinstance(data, list):
            return [Namedict.from_obj(item, False) for item in data]
        if isinstance(data, tuple):
            return tuple(Namedict.from_obj(item, False) for item in data)
        return data

    def _check_key_and_save_alias(self, key: str) -> str:
        """
        Checks, if input key is valid string, and it's 'dash-underscore' escaped
        version can be used in Namedict namespace. Saves escaped key to namespace (attributes)
        and returns input key.
        :param key: key to be checked, converted and saved
        :return: input key (unmodified)
        :raise TypeError: if key is not string
        :raise KeyError: if invalid key
        """
        if not isinstance(key, str):
            raise TypeError(f"Dictionary key must be string (got: {type(key)})")
        alias_key = key.replace("-", "_")
        if self._attribute_check.match(alias_key) is None:
            raise KeyError(f"Key {key} has invalid format (see doc)")
        if alias_key in dir(self):
            raise KeyError(
                f'Key {key} ({alias_key} after "dash-to-underscore" substitution) '
                f"can't be used, because it is reserved string in Namedict class"
            )
        if alias_key in self._attributes:
            raise KeyError(
                f'Key {key} ({alias_key} after "dash-to-underscore" substitution) ' f"collides with another key"
            )
        else:
            self._attributes[alias_key] = key
        return key

    def __init__(self, dictionary: dict = None, **kwargs) -> None:
        # create attributes dictionary, init self array and lock:
        self.__dict__["_locked"] = False
        self._attributes = {}
        dictionary = {**(dictionary or {}), **kwargs}
        super().__init__({self._check_key_and_save_alias(key): val for key, val in dictionary.items()})
        self._locked = True
