import time
import sys
from .terminal import Terminal


def test_foo():
    command = [sys.executable, "--version"]
    with Terminal.open(command) as terminal:
        time.sleep(1)
        assert terminal.screen.display[0].startswith("Python")
