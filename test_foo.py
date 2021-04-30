from winpty import PtyProcess


def test_foo():
    proc = PtyProcess.spawn('python')
    while not proc.isalive():
        pass
