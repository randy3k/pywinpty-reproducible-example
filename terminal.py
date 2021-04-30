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
    ParentPtyProcess = winpty.PtyProcess
else:
    ParentPtyProcess = ptyprocess.PtyProcess


class PtyProcess(ParentPtyProcess):

    def read(self, nbytes):
        if sys.platform.startswith("win"):
            return super(PtyProcess, self).read(nbytes).encode("utf-8")
        else:
            return super(PtyProcess, self).read(nbytes)

    def write(self, data):
        if sys.platform.startswith("win"):
            super(PtyProcess, self).write(data.decode("utf-8"))
        else:
            super(PtyProcess, self).write(data)


class Screen(pyte.Screen):

    def __init__(self, process, *args, **kwargs):
        self._process = process
        super(Screen, self).__init__(*args, **kwargs)

    def write_process_input(self, data):
        self._process.write(data.encode("utf-8"))


class ByteStream(pyte.ByteStream):

    def start_feeding(self):
        screen = self.listener
        process = screen._process

        def reader():
            while True:
                try:
                    data = process.read(1024)
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
        screen = Screen(process, 80, 40)
        stream = ByteStream(screen)
        stream.start_feeding()
        try:
            yield cls(process, screen, stream)
        finally:
            process.terminate(force=True)
