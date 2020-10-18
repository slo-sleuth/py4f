# Python for Forensics Framework

## Introduction
The goal of this project is to simplify the process of writing Python programs 
for the analysis of data, even for the beginner programmer.  Alternatively, the 
with the `py4f` module imported, the Python interpreter itself can be used as a 
data analysis tool.

With `py4f`, complex tasks are simplified.  The user need not know how to open 
files, import and use the hashlib module to calculate hash digests, or convert 
time stamps from integers or floats to human-readable dates.

## General usage

To import all the modules, simply import the library and use dot notation to 
access modules and/or methods.
```python
>>> import py4f
>>> files = py4f.files.get_files('.')
>>> file_list = [f for f in files]
>>> len(file_list)
5004
```

Access specific modules by importing them from `py4f`, e.g., the files module:

```python
>>> from py4f import files
>>> file_list = files.get_files('.')
>>> file_list = [f for f in files]
>>> len(file_list)
5004
```

Particular classes and/or methods can be imported from a module, thusly:

```python
>>> from py4f.files import get_files
>>> file_list = get_files('.', True)
>>> file_list = [f for f in files]
>>> len(file_list)
5004
```

## files.py

The `files.py` module is design to operate at the file level.  It contains a 
`File` class that can be inherited by other classes to provide file 
operations common to all file types such as obtaining file status (size, links, 
time stamps, ownership, etc.), opening the file, calculating hash digests, and 
converting time stamps.

A list of file objects can be generated using the module function `get_files` 
which takes a path argument and can optionally recurse subdirectories and 
filter by globbing.  The function returns a generator rather than a list to 
save system memory and improve scripting performance (it can take a long time 
to generate a full file list).
 
Example demonstrating size difference between generator and list of File
objects:

```python
>>> from py4f.files import get_files
>>> files = get_files('/usr')
>>> files.__sizeof__()  # check in-memory size of generator
96
>>> file_list = [f for f in files if f]
>>> file_list.__sizeof__()  # check in-memory size of list
578912

```

File objects have attributes (e.g. size, time stamps, hash values, etc.) and 
methods (is_file(), get_md5(), open(), etc.).  The results of the methods are
returned as well as stored as attributes.

Example:
  
```python
>>> from py4f.files import File
>>> f = File('/usr')
>>> f.is_file()
False
>>> f.is_dir()
True
>>> f.modified  # returns datetime object
datetime.datetime(2020, 1, 1, 8, 0, tzinfo=datetime.timezone.utc)
>>> print(f.modified)
2020-01-01 08:00:00+00:00
>>> f.print_status()
  File: /usr/bin
  Size: 33696	Blocks: 0	Block Sz: 4096
Device: 16777221	Inode: 1152921500312765116	Links: 1053
  Mode: 16877	UID: 0	GID: 0
Access: 2020-01-01 08:00:00+00:00
Modify: 2020-01-01 08:00:00+00:00
Change: 2020-01-01 08:00:00+00:00
Create: 2020-01-01 08:00:00+00:00
```

The `get_files` function supports globbing through the `pattern` parameter
(default is '*') and returns matching File objects.  It seeks matches
recursively (unless the path parameter is a file) listing, but this behavior 
can be altered through the `recursive` parameter.

**Examples:**

Search all files from the root of the file system:
```python
>>> for f in get_files('/'):
...     # do something here
```

This is equivalent to:

```python
>>> for f in get_files('/', pattern='*', recursive='True')
...     # do something here
```

Return file objects from only the supplied directory:

```python
>>> files = get_files('/', recursive=False)
```