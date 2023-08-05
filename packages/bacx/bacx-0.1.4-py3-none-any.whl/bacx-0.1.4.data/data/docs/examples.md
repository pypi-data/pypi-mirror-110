## Bacx documentation

* [Namedict](#namedict)
* [Config](#config)
* [Storage manager](#Storage-manager)
* [Local storage engine](#Local-storage-engine)
* [Aws storage engine](#Aws-storage-engine)

### Namedict:

Namedict is an immutable python dictionary, which supports key access by attribute call. Namedict can be crated by
non-recursive constructor `Namedict()` or by recursive static method `Namedict.from_obj()`:

```python
from bacx.utils.namedict import Namedict

# Only first layer keys:
nd = Namedict({'a': 1, 'b': {'c': 2}})
nd.a  # returns 1
nd.b.c  # this would fail
# Recursive:
nd = Namedict.from_obj({'a': 1, 'b': {'c': 2}})
nd.b.c  # returns 2
```

Namedict instance can't be modified, but it can be converted back to python dictionary, modified, and converted back to
Namedict:

```python
from bacx.utils.namedict import Namedict

nd = Namedict.from_obj({'a': 1, 'b': {'c': 2}})
dic = nd.to_obj()
dic['b']['c'] = 3
nd = Namedict.from_obj(dic)
nd.b.c  # returns 3
```

Namedict supports also python dictionary like access:

```python
nd['key']
```

As Namedict keys can be accessed as attribute, they can contain only letters, numbers, underscores, and they can't be
strings reserved in Namespace class (for example 'from_obj'). More precisely, they must satisfy this regex:

```regexp
"^[A-Za-z][A-Za-z0-9_]*$"
```

### Config:

Config is Namedict (see above), which can be created from yaml file:

```python
from bacx.utils.config import Config

# three options:
with open('conf.yaml', 'r') as file:
    cf = Config(file)
cf = Config(path='conf.yaml')
cf = Config(data={'a': 1, 'b': {'c': 2}})

```

Config supports also [yamale](https://github.com/23andMe/Yamale) schema checking:

```python
from bacx.utils.config import Config

cf = Config(path='config.yaml')
try:
    cf.check_yamale_schema(path="/path/to/schema.yaml")
except ValueError as e:
    print("Config does not satisfy yamale schema.")
```

Moreover, values in Config can be replaced by calling `set_in(...)` method. New Config will be returned:

```python
from bacx.utils.config import Config

cf1 = Config(data={'a': 1, 'b': {'c': 2}})
cf2 = cf1.set_in('a', 10)
cf2.a  # returns 10

# for more details see:
print(Config.set_in.__doc__)
```

Config supports also merging functionality:

```python
from bacx.utils.config import Config

cf1 = Config(data={'a': 1, 'b': {'c': 10}})
cf2 = Config(data={'a': 2, 'b': {'c': 11, 'd': 12}})
cf3 = Config(data={'a': 3, 'b': {'e': 13}})
dic = {'b': {'c': 2.5, 'f': 14}}
cf4 = cf1.merge_config(cf2, cf3, dic)
cf4.a  # returns 3
cf4.b  # returns {'c': 2.5, 'd': 12, 'e': 13, 'f': 14}

# for more details see:
print(Config.merge_config.__doc__)
```

### Storage manager:

To learn more, see documentation in code. For example:
```python
from bacx.storage.manager import StorageManager
help(StorageManager)
```

### Local storage engine
Local storage engine resides on physical drive. Example of configuration may looks like:
```yaml
version: 1
settings:
  cache: null
storages:
  my_local_files:
    type: local
    link: /home/wynxel/cxeng/bacx/tmp/dirrr
    is_default: True
```

Create storage manager instance:
```python
from bacx.storage.manager import StorageManager
stor_man = StorageManager("configuration.yml")
```

#### Some examples:
Listing directory:
```python
stor_man['my_local_files'].list(".", depth=10)
#>>> ['dir1', 'dir1/file1', 'haluska.sh']
stor_man['my_local_files'].stat("dir1")
#>>> os.stat_result(st_mode=16893, ..., st_ctime=1623749155)
stor_man['my_local_files'].exists("dir1/file1")
#>>> True
stor_man['my_local_files'].is_file("dir1/file1")
#>>> True
```

Some R/W operations:
```python
with stor_man['my_local_files'].open("file2", "w") as file:
    file.write("Hello local drive!")

# >>> 18
stor_man['my_local_files'].read_as_text("file2")
# >>> 'Hello local drive!'
```

Some advanced example:
```python
stor_man['my_local_files'].mkdirs("new/path/to")
stor_man['my_local_files'].list("new")
#>>> ['path']
stor_man['my_local_files'].list("new", depth=10)
#>>> ['path', 'path/to', 'path/to/file']
stor_man['my_local_files'].list("new", filter="file", depth=10)
#>>> ['path/to/file']
stor_man['my_local_files'].rmtree("new/path/to")
stor_man['my_local_files'].list("new", depth=10)
#>>> ['path']
stor_man['my_local_files'].write_as_text("new/file", "djhjhlv4")
with stor_man['my_local_files'].open("new/file", "r") as file:
    print(file.read())

#>>> djhjhlv4
stor_man['my_local_files'].read_as_bytes("new/file")
#>>> b'No, this is better!'
stor_man['my_local_files'].download_to_file("new/file", "/some/secret/path")
stor_man['my_local_files'].rmdir("new")
# Traceback (most recent call last):
#  ...
# OSError: Directory `new` is not empty.
stor_man['my_local_files'].rmtree("new")
```

To learn more, see documentation in code. For example:
```python
from bacx.storage.engines.local_drive import LocalDrive
help(LocalDrive)
help(LocalDrive.open)
```

### Aws storage engine:
Example configuration file:
```yaml
version: 1
settings:
  cache: null
storages:
  my_aws:
    type: aws
    link: bucket-name
    is_default: True
```
Amazon's boto3 library by default searches for credential in [this way](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials).
If you want to pass credentials through config, you can do it:
```yaml
... previous example ...
    is_default: True
    other:
      key_id: 'place_key_id_here'
      key: 'place_key_here'
```

Then use in code:
```python
from bacx.storage.manager import StorageManager
# use configuration yaml:
stor_man = StorageManager(path="/path/to/config.yml")
# or use dictionary directly:
stor_man = StorageManager(config={"place": {"here": "configuration"}})
```
Some aws examples:
```python
# download file:
stor_man['my_aws'].download_to_file('/cloud/path/file', '/local/path/file')
# or by default_storage, as my_aws is set to be default:
stor_man.default_storage().download_to_file('/cloud/path/file', '/local/path/file')
# upload file:
stor_man['my_aws'].upload_from_file('/cloud/path/file', '/local/path/file')
```

