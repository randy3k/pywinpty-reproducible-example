from winpty import PtyProcess


def test_foo():
    proc = PtyProcess.spawn('python')
    proc.write('print("hello world!")\r\n')
