import os
from imports import QMessageBox, QFileDialog
from lexicon import Corpus

def checkForCorpus(function):
    def ask(*args, **kwargs):
        self = args[0]
        if self.corpus is None:
            alert = QMessageBox()
            alert.setWindowTitle('No corpus loaded')
            alert.setText('You must have a corpus loaded before you can save words. What would you like to do?')
            alert.addButton('Create a new corpus', QMessageBox.AcceptRole)
            alert.addButton('Add this word to an existing corpus', QMessageBox.NoRole)

            alert.exec_()
            role = alert.buttonRole(alert.clickedButton())
            if role == QMessageBox.AcceptRole:# create new corpus
                savename = QFileDialog.getSaveFileName(self, 'Save Corpus File', os.getcwd(), '*.corpus')
                path = savename[0]
                if not path:
                    return
                if not path.endswith('.corpus'):
                    path = path + '.corpus'
                kwargs['file_mode'] = 'w'
                kwargs['path'] = path
                kwargs['name'] = os.path.split(path)[1].split('.')[0]
                self.corpus = Corpus(kwargs)

            elif role == QMessageBox.NoRole: # load existing corpus and add to it
                self.loadCorpus()
                if self.corpus is None:
                    # corpus will be None if the user opened a file dialog, then changed their mind and cancelled
                    return
        function(*args, **kwargs)
    return ask

def checkForGloss(function):
    def ask(*args, **kwargs):
        if not args[0].currentGloss():
            alert = QMessageBox()
            alert.setWindowTitle('Missing gloss')
            alert.setText('Please enter a gloss before saving')
            alert.exec_()
            return
        function(*args, **kwargs)
    return ask

def checkForUnsavedChanges(function):
    def ask(*args, **kwargs):
        if args[0].askSaveChanges and not args[0].autoSave:
            alert = QMessageBox()
            alert.setWindowTitle('Warning')
            alert.setText('The current gloss has unsaved changes.\n What would you like to do?')
            alert.addButton('Continue without saving', QMessageBox.AcceptRole)
            alert.addButton('Go back', QMessageBox.RejectRole)
            alert.exec_()
            role = alert.buttonRole(alert.clickedButton())
            if role == QMessageBox.RejectRole:
                return
        function(*args, **kwargs)
    return ask