# This file is placed in the Public Domain.
#
# pylint: disable=C0116


"list of available commands"


from ..command import Commands
from ..objects import keys


def cmd(event):
    event.reply(','.join(sorted(keys(Commands.cmds))))
