from imports import QMessageBox

class WarningBox(QMessageBox):

    def __init__(self):
        super().__init__()

    def closeEvent(self, e):
        return

def checkForGloss(function):
    def ask(*args, **kwargs):
        if not args[0].gloss.glossEdit.text():
            alert = WarningBox()
            alert.setWindowTitle('Missing gloss')
            alert.setText('Please enter a gloss before saving')
            alert.exec_()
            return
        function(*args, **kwargs)
    return ask

def checkForUnsavedChanges(function):
    def ask(*args, **kwargs):
        if args[0].askSaveChanges:
            alert = WarningBox()
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