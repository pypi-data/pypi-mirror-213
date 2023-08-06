# This file is placed in the Public Domain.
#
# pylint: disable=C0114,C0115,C0116,W0613


"user interfacing handlers"


from .command import Commands
from .handler import Handler
from .listens import Listens


def __dir__():
    return (
            'Client',
           )


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        Listens.add(self)
        self.register('command', Commands.handle)

    def announce(self, txt) -> None:
        self.raw(txt)

    def raw(self, txt) -> None:
        pass

    def say(self, channel, txt) -> None:
        self.raw(txt)
