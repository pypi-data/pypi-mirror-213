from __future__ import annotations

from dataclasses import dataclass, is_dataclass
import functools
from typing import get_type_hints


@functools.wraps(dataclass)
def nested_dataclass(*args, **kwargs):
  print('tässä ndc', repr(args), repr(kwargs))
  #raise RuntimeError
  def wrapper(cls):
    print('tässä wrapped', repr(cls))
    cls = nested_dataclass.__wrapped__(cls, **kwargs)
    @functools.wraps(cls.__init__)
    def __init__(self, *args, **kwargs):
      print('tässä ndc.init 0', repr(self.__annotations__))
      from aresti.rajapinta import Rajapinta
      tyypit = get_type_hints(self, {'Rajapinta': Rajapinta})
      print('tässä ndc.init 1', repr(args), repr(kwargs), repr(tyypit))
      for name, value in kwargs.items():
        field_type = tyypit.get(name, None)
        print('tässä ndc.init 2', repr(name), repr(value), repr(field_type))
        if is_dataclass(field_type) \
        and isinstance(value, dict):
          new_obj = field_type.saapuva(value)
          kwargs[name] = new_obj
      __init__.__wrapped__(self, *args, **kwargs)
    cls.__init__ = __init__
    return cls
    # def wrapper
  return wrapper(args[0]) if args else wrapper
