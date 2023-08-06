# This file is placed in the Public Domain.
#
# pylint: disable=C0116


"basic configuration"


from ..objects import keys
from ..objfunc import edit, prt
from ..persist import last, write
from ..runtime import Cfg


def __dir__():
    return (
            "kcfg",
           )


__all__ = __dir__()


def kcfg(event):
    last(Cfg)
    if not event.sets:
        event.reply(
                    prt(
                        Cfg,
                        keys(Cfg)
                       )
                   )
    else:
        edit(Cfg, event.sets)
        write(Cfg)
        event.reply('ok')
