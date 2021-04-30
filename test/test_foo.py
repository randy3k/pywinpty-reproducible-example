import sys
from .terminal import Terminal


def test_foo():
    command = [sys.executable, "--version"]
    with Terminal.open(command) as terminal:
        terminal.line(0).assert_startswith("Python")
