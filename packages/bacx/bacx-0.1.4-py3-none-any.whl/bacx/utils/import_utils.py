from importlib import import_module
from importlib.util import module_from_spec, spec_from_file_location
from os.path import basename, splitext
from types import ModuleType
from typing import Any


def _get_attribute(module: ModuleType, attribute: str, namespace: dict = None) -> Any:
    if attribute not in dir(module):
        raise KeyError(f"Attribute '{attribute}' not found.")
    if namespace is not None:
        if attribute in namespace:
            raise ImportError(f"Name '{attribute}' is already used in given namespace.")
        namespace[attribute] = module.__dict__[attribute]
    return module.__dict__[attribute]


def import_from_module(package: str, attribute: str = None, namespace: dict = None):
    """
    Function dynamically imports module, looks for desired attribute and returns handle
    to this attribute (variable value, reference to class, or reference to function). Desired
    attribute can be added to namespace via 'namespace' argument.
    Example:
        >>>ForExampleSomeClass = import_from_module('package.my_module.ForExampleSomeClass')
        Or:
        >>>AnotherAttribute = import_from_module('package.my_module', 'AnotherAttribute')
        Import to current global namespace:
        >>>var = import_from_module('package.my_module.var', namespace=globals())
    :param package: python package path like 'package.subpackage.module.attribute'
    :param attribute: optional, name of the attribute. If not provided,
    attribute name will be extracted from package string.
    :param namespace: optional, namespace, to which loaded attribute should be add
    :raises ImportError: if namespace is provided, and it already contains attribute with 'attribute'
    :raises KeyError: if module does not contain attribute with 'attribute'
    :returns: handle to desired attribute
    """
    if attribute is None:
        package, attribute = package.rsplit(".", 1)
    module = import_module(package)
    return _get_attribute(module, attribute, namespace)


def import_from_file(path: str, attribute: str, namespace: dict = None):
    """
    Function dynamically imports content of python script, looks for desired attribute and returns handle
    to this attribute (variable value, reference to class, or reference to function). Desired
    attribute can be added to namespace via 'namespace' argument.
    Example:
        Let's have a script in /home/user/script.py:
        >class foo:
        >  def bar():
        >    return 47
        >
        Import foo from script.py using:
        >>>foo_handle = import_from_file(path='/home/user/script.py', attribute='foo')
        >>>f = foo_handle()
        >>>f.bar() # will return 47
        Import to current global namespace:
        >>>import_from_file('foo', '/home/user/script.py', namespace=globals())
        >>>f = foo()
        >>>f.bar() # will return 47
    :param path: path to python module, which holds desired attribute
    :param attribute: name of the attribute, which should be loaded from module
    :param namespace: optional, namespace, to which loaded attribute should be add
    :raises ImportError: if namespace is provided, and it already contains attribute with 'attribute'
    :raises KeyError: if module does not contain attribute with 'attribute'
    :returns: handle to desired attribute
    """
    module_name, _ = splitext(basename(path))
    spec = spec_from_file_location(module_name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return _get_attribute(module, attribute, namespace)
