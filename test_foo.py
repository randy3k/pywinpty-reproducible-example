from winpty import PtyProcess
import sys


def test_foo():
    proc = PtyProcess.spawn([sys.executable])
    while not proc.isalive():
        pass
