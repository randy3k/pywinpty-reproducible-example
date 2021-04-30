from __future__ import unicode_literals
import sys
import pyte
import operator
import threading
from contextlib import contextmanager
import six
import time
import os

if sys.platform.startswith("win"):
    import winpty
else:
    import ptyprocess


__all__ = ["PtyProcess", "Screen", "ByteStream", "Terminal"]


if sys.platform.startswith("win"):
    PtyProcess = winpty.PtyProcess
else:
    PtyProcess = ptyprocess.PtyProcess


class ByteStream(pyte.ByteStream):

    def start_feeding(self):
        screen = self.listener
        process = self.process

        def reader():
            while True:
                try:
                    data = process.read(1024)
                    if isinstance(data, bytes):
                        data = data.decode('utf-8')
                except EOFError:
                    break
                if data:
                    self.feed(data)
        t = threading.Thread(target=reader)
        t.start()


class Terminal(object):

    def __init__(self, process, screen, stream):
        self.process = process
        self.screen = screen
        self.stream = stream

    @classmethod
    @contextmanager
    def open(cls, cmd):
        env = os.environ.copy()
        process = PtyProcess.spawn(cmd, dimensions=(40, 80), env=env)
        screen = pyte.Screen(80, 40)
        stream = ByteStream(screen)
        stream.process = process
        stream.start_feeding()
        try:
            yield cls(process, screen, stream)
        finally:
            process.terminate(force=True)
