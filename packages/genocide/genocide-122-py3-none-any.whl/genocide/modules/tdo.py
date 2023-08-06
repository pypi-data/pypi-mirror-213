# This file is placed in the Public Domain.
#
# pylint: disable=R,C0114,C0115,C0116


"maintain todo list"


import time


from ..objects import Object
from ..persist import Persist, write
from ..utility import elapsed, fntime


class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


Persist.add(Todo)


# COMMANDS


def dne(event):
    if not event.args:
        return
    selector = {'txt': event.args[0]}
    for obj in Persist.find('todo', selector):
        obj.__deleted__ = True
        write(obj)
        event.reply('ok')
        break


def tdo(event):
    if not event.rest:
        nmr = 0
        for obj in Persist.find('todo'):
            lap = elapsed(time.time()-fntime(obj.__oid__))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply("no todo")
        return
    obj = Todo()
    obj.txt = event.rest
    write(obj)
    event.reply('ok')
