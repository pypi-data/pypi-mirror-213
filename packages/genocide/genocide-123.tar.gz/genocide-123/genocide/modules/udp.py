# This file is placed in the Public Domain.
#
# pylint: disable=C0103,C0115,C0116,W0613,R0903


"udp to irc relay"


import select
import socket
import sys
import time


from ..listens import Listens
from ..objects import Object
from ..persist import Persist, last
from ..runtime import launch


def start():
    u = UDP()
    u.start()
    return u


class Cfg(Object):

    def __init__(self):
        super().__init__()
        self.host = "localhost"
        self.port = 5500


Persist.add(Cfg)


class UDP(Object):

    def __init__(self):
        super().__init__()
        self.stopped = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.setblocking(1)
        self._starttime = time.time()
        self.cfg = Cfg()

    def output(self, txt, addr):
        Listens.announce(txt.replace("\00", ""))

    def server(self):
        try:
            self._sock.bind((self.cfg.host, self.cfg.port))
        except socket.gaierror:
            return
        while not self.stopped:
            (txt, addr) = self._sock.recvfrom(64000)
            if self.stopped:
                break
            data = str(txt.rstrip(), "utf-8")
            if not data:
                break
            self.output(data, addr)

    def exit(self):
        self.stopped = True
        self._sock.settimeout(0.01)
        self._sock.sendto(bytes("exit", "utf-8"), (self.cfg.host, self.cfg.port))

    def start(self):
        last(self.cfg)
        launch(self.server)


def toudp(host, port, txt):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(txt.strip(), "utf-8"), (host, port))


def udp(event):
    cfg = Cfg()
    last(cfg)
    if len(sys.argv) > 2:
        txt = " ".join(sys.argv[2:])
        toudp(cfg.host, cfg.port, txt)
        return
    if not select.select([sys.stdin, ], [], [], 0.0)[0]:
        return
    while 1:
        try:
            (i, _o, e) = select.select([sys.stdin,], [], [sys.stderr,])
        except KeyboardInterrupt:
            return
        if e:
            break
        stop = False
        for sock in i:
            txt = sock.readline()
            if not txt:
                stop = True
                break
            toudp(cfg.host, cfg.port, txt)
        if stop:
            break
