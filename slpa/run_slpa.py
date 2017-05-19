#!/usr/bin/env python
import sys
import os
from main import MainWindow, QApplicationMessaging

if sys.platform.startswith('win'):
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.expanduser('~/Documents'))
        # Implementing dummy stdout and stderr for frozen Windows release
        class FakeSTD(object):
            def write(self, string):
                pass
            def flush(self):
                pass
        #This should fix stdout flush errors, but doesn't always
        #Also needs a small tweak to multiprocessing.process._bootstrap
        sys.stdout = FakeSTD()
        sys.stderr = FakeSTD()

def run_slpa():

    app = QApplicationMessaging(sys.argv)
    if app.isRunning():
        if len(sys.argv) > 1:
            app.sendMessage(sys.argv[1])
        else:
            app.sendMessage('ARISE')
    else:
        slpaGUI = MainWindow(app)
        app.aboutToQuit.connect(slpaGUI.cleanUp)

        app.setActiveWindow(slpaGUI)
        slpaGUI.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    run_slpa()

