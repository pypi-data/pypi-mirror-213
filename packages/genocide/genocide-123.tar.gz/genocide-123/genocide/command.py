# This file is placed in the Public Domain.
#
# pylint: disable=C0114,C0115,C0116,W0703


"commands and their handling"


import inspect


from .errored import Errors
from .evented import Event
from .logging import Logging
from .objects import Object, copy


def __dir__():
    return (
            'Commands',
           )


MODNAMES = {
           }


class Commands(Object):

    cmds = Object()
    modnames = copy(Object(), MODNAMES)
    modules = None
    ondemand = True

    @staticmethod
    def add(func) -> None:
        cmd = func.__name__
        setattr(Commands.cmds, cmd, func)
        setattr(Commands.modnames, cmd, func.__module__)

    @staticmethod
    def handle(evt) -> Event:
        evt.parse(evt.txt)
        func = getattr(Commands.cmds, evt.cmd, None)
        if Commands.ondemand and not func:
            modname = getattr(Commands.modnames, evt.cmd, None)
            mod = None
            if modname:
                Logging.debug(f"load {modname}")
                mod = getattr(
                              Commands.modules,
                              modname.split(".")[-1],
                              None
                             )
                func = getattr(mod, evt.cmd, None)
        if func:
            try:
                func(evt)
                evt.show()
            except Exception as ex:
                Errors.handle(ex)
        evt.ready()
        return evt

    @staticmethod
    def scan(mod) -> None:
        for _key, cmd in inspect.getmembers(mod, inspect.isfunction):
            if 'event' in cmd.__code__.co_varnames:
                Commands.add(cmd)
