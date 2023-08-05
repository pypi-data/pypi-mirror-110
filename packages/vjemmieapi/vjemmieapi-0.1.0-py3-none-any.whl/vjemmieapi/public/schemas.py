"""Contains public definitions for the Pydantic models used to verify and generate JSON bodies in HTTP replies.
"""

from pydantic import BaseModel
from ..schemas import *


__all__ = []


def make_public_schemas():
    """Dynamically generates classes from the Pydantic models
    containing the word 'Out'."""
    global __all__
    classes = {}
    for clsname, cls in globals().items():
        if isinstance(cls, type) and issubclass(cls, BaseModel) and "Out" in clsname:
            name, *_ = clsname.split("Out")
            public_cls = type(name, (cls,), {})
            public_cls.__name__ = name
            public_cls.__qualname__ == name
            classes[name] = public_cls
    globals().update(classes)
    __all__ = [clsname for clsname in classes]


make_public_schemas()
