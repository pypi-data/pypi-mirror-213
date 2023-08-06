# This file is placed in the Public Domain.
#
# pylint: disable=C0114,C0116


"show listeners"


from ..listens import Listens
from ..objects import kind
from ..objfunc import prt


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(prt(Listens.objs[index]))
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(' | '.join([kind(obj) for obj in Listens.objs]))
