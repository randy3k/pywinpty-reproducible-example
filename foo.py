import time
import sys
from terminal import Terminal


command = [sys.executable, "--version"]
with Terminal.open(command) as terminal:
    time.sleep(1)
    print(terminal.screen.display[0].startswith("Python"))
