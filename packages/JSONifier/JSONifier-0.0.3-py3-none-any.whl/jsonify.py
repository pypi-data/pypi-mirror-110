from typing import Any
import json

class JSONifier:
  """
    Build a JSONifier object from a dict or a readable file. 

    ...

    Params
    ----------
    *These params are used in the initialization of an instance of this class.*    

    mode : str
        Define the mode in which to read and parse the given `data`.

    data : Any
        The data for the JSONifier object.

    Attributes
    ----------
    mode : str
        *Set when a new instance of the class is made.*

    data : Any
        *Set when a new instance of the class is made.*

    valid_modes : list
        *List of valid modes for instantiating a new JSONifier object.*

    call_methods : list
        *List of valid methods for the call function.*

    call_return_methods : list
        *List of valid methods for specifying how to get the instance data back from the call method.*

    write_methods : list
        *List of valid methods for writing to a json file.*

    Methods
    -------
    call(self, ret) - _builtin_
        The call function (calling an instance as a function).  `ret` is the return method.

    init(self, mode: str = None, data: Any = None) - _builtin_
        *Make a new instance.  Refer to `params` for information on the parameters.*

    @classmethod
    create(cls, mode, data)
        *Alternative constructor for the class.*

    @classmethod
    fromFile(cls, file)
        *Alternative constructor from a file path.*

    @classmethod
    fromDict(cls, file)
        *Alternative constructor from a supplied dictionary.*

    get_data(self)
        *Return the instance's data.*

    replace(self, key=None, value=None)
        *Replace the specified key with the specified value.*

    @staticmethod
    write(method="json", file=None, data=None)
        *Write to a specific file the data supplied.
  """

  valid_modes = [
    "dict", "dictionary", "file", "from"
  ]
  call_methods = [
    "get", "list", "data", "replace", "add"
  ]
  call_return_methods = [
    "get", "var", "to_variable", "variable", "set", "print"
  ]
  write_methods = [
    "normal", "default", "json"
  ]

  def __call__(self, ret):
    if ret.lower() not in JSONifier.call_return_methods:
      raise ValueError("Provide a valid return mode!")
      return
    if ret.lower() == "get" or ret.lower() == "var" or ret.lower() == "to_variable" or ret.lower() == "variable" or ret.lower() == "set":
      return self.data
    elif ret.lower() == "print":
      print(self.data)
    
  def __init__(self, mode: str = None, data: Any = None):
    if mode.lower() not in JSONifier.valid_modes:
      raise TypeError("Not a valid mode!")
    else:
      if mode.lower() == "dict" or mode.lower() == "dictionary":
        try:
          self.data = dict(data)
        except:
          raise TypeError("You used mode dict, and supported invalid data for type dict.")
      elif mode.lower() == "file" or mode.lower() == "from":
        try:
          with open(data, "r") as f:
            self.data = json.load(f)
        except:
          raise TypeError("You used mode file, the file path you supplied is invalid.")

  def __enter__(self):
    return self
        
  def __exit__(self, exc_type, exc_value, exc_traceback):
    pass

  @classmethod
  def create(cls, mode, data):
    if mode is None or data is None:
      raise ValueError("Must provide both a mode and data!")
      return
    return cls(mode, data)

  @classmethod
  def fromFile(cls, file):
    if file is None:
      raise ValueError("Must provide a file path!")
      return
    return cls("file", file)

  @classmethod
  def fromDict(cls, dictionary):
    if dictionary is None:
      raise ValueError("Must provide a valid dict!")
      return
    return cls("dict", dictionary)

  def get_data(self):
    return self.data

  def replace(self, key = None, value=None):
    if key is None or value is None:
      raise ValueError("Supply a key and a new value to update the key with!")
      return
    self.data[key] = value

  @staticmethod
  def write(method="json", file = None, data=None):
    if method.lower() not in JSONifier.write_methods:
      raise ValueError("Provide a valid write method!")
      return
    if file is None:
      return ValueError("Provide a file to write data to!")
      return
    if method.lower() == "normal" or method.lower() == "default":
      with open(file, "w") as f:
        f.write(str(data))
    elif method.lower() == "json":
      with open(file, "w") as f:
        json.dump(data, f)