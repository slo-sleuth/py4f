# Python for Forensics Framework

## Introduction
The goal of this project is to simplify the process of writing Python programs for the analysis of data, even for the beginner programmer.  Alternatively, the with the `py4f` module imported, the Python interpreter itself can be used as a data analysis tool.

With `py4f`, complex tasks are simplified.  The user need not know how to open files, import and use the hashlib module to calculate hash digests, or convert time stamps from integers or floats to human-readable dates.

## General usage

To import all the modules, simply import the library and use dot notation to access modules and/or methods.
```;python
>>> import py4f
>>> file_list = py4f.files.get_files('.', recursive=True)
>>> len(file_list)
5004
```

Access specific modules by importing them from `py4f`, e.g., the files module:

```;python
>>> from py4f import files
>>> file_list = files.get_files('.', recursive=True)
>>> len(file_list)
5004
```

Particular classes and/or methods can be imported from a module, thusly:

```;python
>>> from py4f.files import get_files
>>> file_list = get_files('.', True)
>>> len(file_list)
5004
```

## files.py

The `files.py` module is design to operate at the file level.  It contains a `File` base class that can be inherited into other classes to provide file operations common to all file types such as obtaining file status (size, links, time stamps, ownership, etc.), opening the file, calculating hash digests, and converting time stamps.

The module is structured as follows:

```
NAME
    py4f.files
DESCRIPTION
    Module to obtain file metadata and perform basic operations on files such as
    opening, hashing, and typing.  File objects are enhanced Path objects.
CLASSES
    pathlib.Path(pathlib.PurePath)
        File
    
    class File(pathlib.Path)
     |  File(*args, **kwargs)
     |  
     |  Base class for file information and actions common to all file types.
     |  
     |  Method resolution order:
     |      File
     |      pathlib.Path
     |      pathlib.PurePath
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, follow_links: bool = False) -> None
     |      Initializes File() object from a string or a Path object
     |      with basic file information, e.g, name, size date stamps, etc.  Files
     |      are not automatically typed, or hashed as this can take substantial time
     |      and may not be needed in all circumstances.
     |  
     |  get_file_type(self) -> str
     |      Return and store the file type attribute as detected by
     |      python-magic.
     |  
     |  get_md5(self) -> str
     |      Returns and stores the hexadecimal MD5 hash digest attribute of the
     |      file.
     |  
     |  get_mime_type(self) -> str
     |      Return and store the mime type attribute as detected by
     |      python-magic.
     |  
     |  get_sha1(self) -> str
     |      Returns and stores the hexadecimal SHA1 hash digest attribute of the
     |      file.
     |  
     |  get_sha256(self) -> str
     |      Return and store the hexadecimal SHA256 hash digest attribute of the
     |      file.
     |  
     |  print_status(self) -> str
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from pathlib.Path:
     |  
     |  __enter__(self)
     |  
     |  __exit__(self, t, v, tb)
     |  
     |  absolute(self)
     |      Return an absolute version of this path.  This function works
     |      even if the path doesn't point to anything.
     |      
     |      No normalization is done, i.e. all '.' and '..' will be kept along.
     |      Use resolve() to get the canonical path to a file.
     |  
     |  chmod(self, mode)
     |      Change the permissions of the path, like os.chmod().
     |  
     |  exists(self)
     |      Whether this path exists.
     |  
     |  expanduser(self)
     |      Return a new path with expanded ~ and ~user constructs
     |      (as returned by os.path.expanduser)
     |  
     |  glob(self, pattern)
     |      Iterate over this subtree and yield all existing files (of any
     |      kind, including directories) matching the given relative pattern.
     |  
     |  group(self)
     |      Return the group name of the file gid.
     |  
     |  is_block_device(self)
     |      Whether this path is a block device.
     |  
     |  is_char_device(self)
     |      Whether this path is a character device.
     |  
     |  is_dir(self)
     |      Whether this path is a directory.
     |  
     |  is_fifo(self)
     |      Whether this path is a FIFO.
     |  
     |  is_file(self)
     |      Whether this path is a regular file (also True for symlinks pointing
     |      to regular files).
     |  
     |  is_mount(self)
     |      Check if this path is a POSIX mount point
     |  
     |  is_socket(self)
     |      Whether this path is a socket.
     |  
     |  is_symlink(self)
     |      Whether this path is a symbolic link.
     |  
     |  iterdir(self)
     |      Iterate over the files in this directory.  Does not yield any
     |      result for the special paths '.' and '..'.
     |  
     |  lchmod(self, mode)
     |      Like chmod(), except if the path points to a symlink, the symlink's
     |      permissions are changed, rather than its target's.
     |  
     |  link_to(self, target)
     |      Create a hard link pointing to a path named target.
     |  
     |  lstat(self)
     |      Like stat(), except if the path points to a symlink, the symlink's
     |      status information is returned, rather than its target's.
     |  
     |  mkdir(self, mode=511, parents=False, exist_ok=False)
     |      Create a new directory at this given path.
     |  
     |  open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None)
     |      Open the file pointed by this path and return a file object, as
     |      the built-in open() function does.
     |  
     |  owner(self)
     |      Return the login name of the file owner.
     |  
     |  read_bytes(self)
     |      Open the file in bytes mode, read it, and close the file.
     |  
     |  read_text(self, encoding=None, errors=None)
     |      Open the file in text mode, read it, and close the file.
     |  
     |  rename(self, target)
     |      Rename this path to the given path,
     |      and return a new Path instance pointing to the given path.
     |  
     |  replace(self, target)
     |      Rename this path to the given path, clobbering the existing
     |      destination if it exists, and return a new Path instance
     |      pointing to the given path.
     |  
     |  resolve(self, strict=False)
     |      Make the path absolute, resolving all symlinks on the way and also
     |      normalizing it (for example turning slashes into backslashes under
     |      Windows).
     |  
     |  rglob(self, pattern)
     |      Recursively yield all existing files (of any kind, including
     |      directories) matching the given relative pattern, anywhere in
     |      this subtree.
     |  
     |  rmdir(self)
     |      Remove this directory.  The directory must be empty.
     |  
     |  samefile(self, other_path)
     |      Return whether other_path is the same or not as this file
     |      (as returned by os.path.samefile()).
     |  
     |  stat(self)
     |      Return the result of the stat() system call on this path, like
     |      os.stat() does.
     |  
     |  symlink_to(self, target, target_is_directory=False)
     |      Make this path a symlink pointing to the given path.
     |      Note the order of arguments (self, target) is the reverse of os.symlink's.
     |  
     |  touch(self, mode=438, exist_ok=True)
     |      Create this file with the given access mode, if it doesn't exist.
     |  
     |  unlink(self, missing_ok=False)
     |      Remove this file or link.
     |      If the path is a directory, use rmdir() instead.
     |  
     |  write_bytes(self, data)
     |      Open the file in bytes mode, write to it, and close the file.
     |  
     |  write_text(self, data, encoding=None, errors=None)
     |      Open the file in text mode, write to it, and close the file.
     |  
     |  ----------------------------------------------------------------------
     |  Class methods inherited from pathlib.Path:
     |  
     |  cwd() from builtins.type
     |      Return a new path pointing to the current working directory
     |      (as returned by os.getcwd()).
     |  
     |  home() from builtins.type
     |      Return a new path pointing to the user's home directory (as
     |      returned by os.path.expanduser('~')).
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from pathlib.Path:
     |  
     |  __new__(cls, *args, **kwargs)
     |      Construct a PurePath from one or several strings and or existing
     |      PurePath objects.  The strings and path objects are combined so as
     |      to yield a canonicalized path, which is incorporated into the
     |      new PurePath object.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from pathlib.PurePath:
     |  
     |  __bytes__(self)
     |      Return the bytes representation of the path.  This is only
     |      recommended to use under Unix.
     |  
     |  __eq__(self, other)
     |      Return self==value.
     |  
     |  __fspath__(self)
     |  
     |  __ge__(self, other)
     |      Return self>=value.
     |  
     |  __gt__(self, other)
     |      Return self>value.
     |  
     |  __hash__(self)
     |      Return hash(self).
     |  
     |  __le__(self, other)
     |      Return self<=value.
     |  
     |  __lt__(self, other)
     |      Return self<value.
     |  
     |  __reduce__(self)
     |      Helper for pickle.
     |  
     |  __repr__(self)
     |      Return repr(self).
     |  
     |  __rtruediv__(self, key)
     |  
     |  __str__(self)
     |      Return the string representation of the path, suitable for
     |      passing to system calls.
     |  
     |  __truediv__(self, key)
     |  
     |  as_posix(self)
     |      Return the string representation of the path with forward (/)
     |      slashes.
     |  
     |  as_uri(self)
     |      Return the path as a 'file' URI.
     |  
     |  is_absolute(self)
     |      True if the path is absolute (has both a root and, if applicable,
     |      a drive).
     |  
     |  is_reserved(self)
     |      Return True if the path contains one of the special names reserved
     |      by the system, if any.
     |  
     |  joinpath(self, *args)
     |      Combine this path with one or several arguments, and return a
     |      new path representing either a subpath (if all arguments are relative
     |      paths) or a totally different path (if one of the arguments is
     |      anchored).
     |  
     |  match(self, path_pattern)
     |      Return True if this path matches the given pattern.
     |  
     |  relative_to(self, *other)
     |      Return the relative path to another path identified by the passed
     |      arguments.  If the operation is not possible (because this is not
     |      a subpath of the other path), raise ValueError.
     |  
     |  with_name(self, name)
     |      Return a new path with the file name changed.
     |  
     |  with_suffix(self, suffix)
     |      Return a new path with the file suffix changed.  If the path
     |      has no suffix, add given suffix.  If the given suffix is an empty
     |      string, remove the suffix from the path.
     |  
     |  ----------------------------------------------------------------------
     |  Readonly properties inherited from pathlib.PurePath:
     |  
     |  anchor
     |      The concatenation of the drive and root, or ''.
     |  
     |  drive
     |      The drive prefix (letter or UNC path), if any.
     |  
     |  name
     |      The final path component, if any.
     |  
     |  parent
     |      The logical parent of the path.
     |  
     |  parents
     |      A sequence of this path's logical parents.
     |  
     |  parts
     |      An object providing sequence-like access to the
     |      components in the filesystem path.
     |  
     |  root
     |      The root of the path, if any.
     |  
     |  stem
     |      The final path component, minus its last suffix.
     |  
     |  suffix
     |      The final component's last suffix, if any.
     |      
     |      This includes the leading period. For example: '.txt'
     |  
     |  suffixes
     |      A list of the final component's suffixes, if any.
     |      
     |      These include the leading periods. For example: ['.tar', '.gz']
FUNCTIONS
    get_files(path: str, recursive: bool = False) -> list
        Return list of File objects from path.  If path is a directory, all files
        from the directory are returned and optionally recurses into subdirectory.
```
