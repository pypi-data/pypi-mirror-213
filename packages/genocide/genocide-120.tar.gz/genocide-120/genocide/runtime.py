# This file is placed in the Pubic Domain.
#
# pylint: disable=C0114,C0115,C0116,W0613,W0212


"runtime"


import functools
import io
import time
import traceback


from .evented import Event
from .objects import update
from .logging import Logging
from .command import Commands
from .configs import Cfg
from .errored import Errors
from .threads import Thread
from .utility import spl


def __dir__():
    return (
            'DATE',
            'STARTTIME',
            'Config',
            'Cfg',
            'command',
            'launch',
            'parse_cli',
            'threaded'
           )


DATE = time.ctime(time.time()).replace("  ", " ")
NAME = __name__.split('.', maxsplit=1)[0]
STARTTIME = time.time()


Cfg.debug = False
Cfg.mod = "cmd,err,flt,irc,mdl,mod,rss,sts,thr,upt,ver"
Cfg.skip = "PING,PONG,PRIVMSG"
Cfg.threaded = False
Cfg.version = "101"


# FUNCTIONS


def command(cli, txt) -> Event:
    evt = cli.event(txt)
    Commands.handle(evt)
    evt.ready()
    return evt


def scanstr(pkg, mods, init=None, doall=False, wait=False) -> None:
    res = []
    if doall:
        mods = ",".join(pkg.__all__)
    for modname in spl(mods):
        mod = getattr(pkg, modname, None)
        if not mod:
            continue
        if not init:
            Commands.scan(mod)
        if init and "start" in dir(mod):
            mod._thr = launch(mod.start)
        res.append(mod)
    if wait:
        for module in res:
            if "_thr" in dir(module):
                module._thr.join()
    return res


def launch(func, *args, **kwargs) -> Thread:
    thrname = kwargs.get('name', '')
    thr = Thread(func, thrname, *args)
    thr.start()
    return thr


def parse_cli(txt) -> Cfg:
    evt = Event()
    evt.parse(txt)
    update(Cfg, evt, False)
    Cfg.mod += evt.mods
    return Cfg


def threaded(func, *args, **kwargs) -> None:

    @functools.wraps(func)
    def threadedfunc(*args, **kwargs):
        thr = launch(func, *args, **kwargs)
        if args:
            args[0]._thr = thr
        return thr

    return threadedfunc


def waiter(clear=True):
    got = []
    for ex in Errors.errors:
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(ex),
                                                       ex,
                                                       ex.__traceback__
                                                      )
                            )
        for line in stream.readlines():
            Logging.debug(line)
        got.append(ex)
    if clear:
        for exc in got:
            Errors.errors.remove(exc)
