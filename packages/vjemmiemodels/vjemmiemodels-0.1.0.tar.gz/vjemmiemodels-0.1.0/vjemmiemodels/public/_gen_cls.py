"""Contains public definitions for the Pydantic models used to verify and generate JSON bodies in HTTP replies.
"""
from pydantic import BaseModel
from ..internal import *

# TODO: delete!

# Dynamically generates classes from the Pydantic models containing the word 'Out'.
classes = {}
for clsname, cls in dict(globals()).items():
    if isinstance(cls, type) and issubclass(cls, BaseModel) and "Out" in clsname:
        name, *_ = clsname.split("Out")
        public_cls = type(name, (cls,), {})
        public_cls.__name__ = name
        public_cls.__qualname__ == name
        classes[name] = public_cls

globals().update(classes)
__all__ = [clsname for clsname in classes]
