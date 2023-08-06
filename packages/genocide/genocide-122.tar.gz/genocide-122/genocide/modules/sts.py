# This file is placed in the Public Domain.
#
# pylint: disable=C0114,C0116


"show status of listeners"


from ..listens import Listens
from ..objfunc import prt


def sts(event):
    nmr = 0
    for bot in Listens.objs:
        if 'state' in dir(bot):
            event.reply(prt(bot.state, skip='lastline'))
            nmr += 1
    if nmr:
        event.reply("no status")
