from imports import (QThread, Signal, QDialog, QVBoxLayout, QPushButton,
                     QHBoxLayout, Slot)


class FunctionWorker(QThread):
    dataReady = Signal(object)

    def __init__(self):
        super().__init__()
        #self.stopped = False

    def run(self):
        pass  #implement in subclass

    def setParams(self, kwargs):
        self.kwargs = kwargs
        #self.kwargs['call_back'] = self.emitProgress
        #self.kwargs['stop_check'] = self.stopCheck
        #self.stopped = False
        #self.total = None

#    def closeEvent(self, event):
#        self.stop()

#    def stop(self):
#        self.stopped = True

#    def stopCheck(self):
#        return self.stopped

#    def emitProgress(self,*args):
#        if isinstance(args[0],str):
#            self.updateProgressText.emit(args[0])
#            return
#        elif isinstance(args[0],dict):
#            self.updateProgressText.emit(args[0]['status'])
#            return
#        else:
#            progress = args[0]
#            if len(args) > 1:
#                self.total = args[1]
#        if self.total:
#            self.updateProgress.emit((progress/self.total))


class FunctionDialog(QDialog):
    header = None
    about = None
    name = ''

    def __init__(self, parent, settings, worker):
        super().__init__(parent)

        self.settings = settings

        self.setWindowTitle(self.name.title())

        self.newTableButton = QPushButton('Run/Restart')
        self.newTableButton.setDefault(True)
        self.newTableButton.clicked.connect(self.newTable)

        self.oldTableButton = QPushButton('Append to current results table')
        self.oldTableButton.clicked.connect(self.oldTable)

        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.reject)

        self.aboutButton = QPushButton('About {}...'.format(self.name))
        self.aboutButton.clicked.connect(self.open_about)

        acLayout = QHBoxLayout()
        acLayout.addWidget(self.newTableButton)
        acLayout.addWidget(self.oldTableButton)
        acLayout.addWidget(self.cancelButton)
        acLayout.addWidget(self.aboutButton)

        self.thread = worker
        self.thread.dataReady.connect(self.setResults)

        #if self.settings['tooltips']:
        #    self.aboutButton.setToolTip(('<FONT COLOR=black>'
        #                                 '{}'
        #                                 '</FONT>'.format('\n'.join(self.about)))
        #                                )

        majorLayout = QVBoxLayout()
        majorLayout.addLayout(acLayout)

        self.setLayout(majorLayout)
        self.resize(1000, 500)

    @Slot(object)
    def setResults(self, results):
        pass  # Implemented in subclasses

    def generateKwargs(self):
        pass  # Implemented in subclasses

    def calc(self):
        kwargs = self.generateKwargs()
        #if kwargs is None:
        #    return
        self.thread.setParams(kwargs)
        self.thread.start()

        #result = self.progressDialog.exec_()

        #self.progressDialog.reset()
        #if result:
        #self.accept()

    def newTable(self):
        self.update = False
        self.calc()

    def oldTable(self):
        self.update = True
        self.calc()

    def open_about(self):
        #TODO: implement this
        pass
        #self.aboutWindow = HelpDialog(self, self.name)
        #self.aboutWindow.exec_()