# This file is placed in the Public Domain.
#
# pylint: disable=E0012,R,C0114,C0115,C0116,C0209,W0613,E1101


"clean namespace"


import datetime
import os
import uuid


def __dir__():
    return (
            'Object',
            'copy',
            'dumprec',
            'ident',
            'items',
            'keys',
            'kind',
            'update',
            'values'
           )


class Object:

    __slots__ = ('__dict__', '__oid__')

    def __init__(self):
        self.__oid__ = ident(self)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return dumprec(self)


def copy(obj, val) -> None:
    if isinstance(val, list):
        update(obj, dict(val))
    elif isinstance(val, zip):
        update(obj, dict(val))
    elif isinstance(val, dict):
        update(obj, val)
    elif isinstance(val, Object):
        update(obj, vars(val))
    return obj


def dumprec(obj, ooo="{"):
    for key, value in items(obj):
        if issubclass(type(value), Object):
            ooo += "'%s': %s" % (str(key), dumprec(value, ooo))
            continue
        else:
            ooo += "'%s': '%s'" % (str(key), str(value))
    ooo += "}"
    return ooo


def ident(obj) -> str:
    return os.path.join(
                        kind(obj),
                        str(uuid.uuid4().hex),
                        os.sep.join(str(datetime.datetime.now()).split())
                       )


def items(obj) -> []:
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj) -> []:
    return obj.__dict__.keys()


def kind(obj) -> str:
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def update(obj, data, empty=True) -> None:
    for key, value in items(data):
        if not empty and not value:
            continue
        setattr(obj, key, value)


def values(obj) -> []:
    return obj.__dict__.values()
