# This file is placed in the Public Domain.
#
# pylint: disable=R,C0114,C0115,C0116,W0613,E1101


"store to disk"


import os
import _thread


from .decoder import load
from .default import Default
from .encoder import dump
from .objects import Object, ident, items, kind, update
from .objfunc import search
from .utility import cdir, fnclass, fntime, strip


def __dir__():
    return (
            'Persist',
            'last',
            'read',
            'write',
            'writerec'
           )


disklock = _thread.allocate_lock()


class Persist(Object):

    cls = Default()
    workdir = ""

    @staticmethod
    def add(clz) -> str:
        setattr(Persist.cls, f"{clz.__module__}.{clz.__name__}", clz)

    @staticmethod
    def clz(mtc) -> type:
        mtc = mtc.lower()
        for clzz in Persist.cls:
            if mtc == clzz.split(".")[-1].lower():
                yield clzz

    @staticmethod
    def files() -> []:
        return os.listdir(os.path.join(Persist.workdir, "store"))

    @staticmethod
    def find(mtc, selector=None) -> []:
        if selector is None:
            selector = {}
        for fnm in Persist.fns(mtc):
            obj = Persist.hook(fnm)
            if '__deleted__' in obj:
                continue
            if selector and not search(obj, selector):
                continue
            yield obj

    @staticmethod
    def fns(mtc) -> []:
        assert Persist.workdir
        dname = ''
        lst = mtc.lower().split(".")[-1]
        for rootdir, dirs, _files in os.walk(Persist.workdir, topdown=False):
            if dirs:
                dname = sorted(dirs)[-1]
                if dname.count('-') == 2:
                    ddd = os.path.join(rootdir, dname)
                    fls = sorted(os.listdir(ddd))
                    if fls:
                        path2 = os.path.join(ddd, fls[-1])
                        spl = strip(path2).split(os.sep, maxsplit=1)[0]
                        if lst in spl.lower().split(".")[-1]:
                            yield strip(path2)

    @staticmethod
    def get(cmd) -> type:
        return getattr(Persist.cls, cmd, None)

    @staticmethod
    def hook(otp) -> type:
        clz = fnclass(otp)
        cls = Persist.get(clz)
        if cls:
            obj = cls()
            read(obj, otp)
            return obj
        obj = Object()
        read(obj, otp)
        return obj

    @staticmethod
    def logdir() -> str:
        return os.path.join(Persist.workdir, "logs")

    @staticmethod
    def match(mtc, selector=None) -> []:
        if selector is None:
            selector = {}
        for tpe in Persist.clz(mtc):
            for fnm in Persist.fns(tpe):
                obj = Persist.hook(fnm)
                if '__deleted__' in obj:
                    continue
                if selector and not search(obj, selector):
                    continue
                yield obj

    @staticmethod
    def path(pth) -> str:
        return os.path.join(Persist.workdir, 'store', pth)

    @staticmethod
    def remove(clz) -> None:
        delattr(Persist.cls, f"{clz.__module__}.{clz.__name__}")

    @staticmethod
    def storedir() -> str:
        return os.path.join(Persist.workdir, "store")


# FUNCTIONS


def last(obj, selector=None) -> None:
    if selector is None:
        selector = {}
    result = sorted(
                    Persist.find(kind(obj), selector),
                    key=lambda x: fntime(x.__oid__)
                   )
    if result:
        inp = result[-1]
        update(obj, inp)
        obj.__oid__ = inp.__oid__
    return obj.__oid__


def read(obj, pth) -> str:
    pth = Persist.path(pth)
    with disklock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            data = load(ofile)
            update(obj, data)
    obj.__oid__ = strip(pth)
    return obj.__oid__


def readrec(obj, pth=None) -> type:
    ooo = type(obj)()
    if pth:
        read(ooo, pth)
    else:
        update(ooo, obj)
    oooo = type(obj)()
    for key, value in items(ooo):
        if issubclass(type(value), Object):
            setattr(oooo, key, readrec(value))
            continue
        else:
            setattr(oooo, key, value)
    return oooo


def write(obj) -> str:
    try:
        pth = Persist.path(obj.__oid__)
    except TypeError:
        pth = Persist.path(ident(obj))
    cdir(pth)
    with disklock:
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile)
    return strip(pth)


def writerec(obj):
    ooo = type(obj)()
    for key, value in items(obj):
        if issubclass(type(value), Object):
            setattr(ooo, key, writerec(value))
        else:
            setattr(ooo, key, str(value))
    return write(ooo)
