# This file is placed in the Public Domain.
#
# pylint: disable=C0114,C0116


"list of loadable modules"


from ..command import Commands


def mod(event):
    event.reply(",".join(Commands.modules.__all__))
