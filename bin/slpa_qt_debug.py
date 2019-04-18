import os
import sys
base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0,base)

if __name__ == '__main__':
    app = main.QApplicationMessaging(sys.argv)
    if app.isRunning():
        if len(sys.argv) > 1:
            app.sendMessage(sys.argv[1])
        else:
            app.sendMessage('ARISE')
    else:
        main = main.MainWindow(app)

        app.aboutToQuit.connect(main.cleanUp)
        app.setActiveWindow(main)
        main.show()
        sys.exit(app.exec_())