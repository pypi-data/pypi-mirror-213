# This file is placed in the Public Domain.
#
# pylint: disable=C0114,C0115,C0116


"console print hook"


from .utility import doskip


def __dir__():
    return (
            'Logging',
           )


class Logging:

    skip = 'PING,PONG,PRIVMSG'
    verbose = False

    @staticmethod
    def debug(txt) -> None:
        if Logging.verbose and not doskip(txt, Logging.skip):
            Logging.raw(txt)

    @staticmethod
    def raw(txt) -> None:
        pass
