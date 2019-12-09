from imports import QVBoxLayout, QPlainTextEdit, QDialog, QHBoxLayout, QLineEdit, QLabel, QPushButton


class NotesDialog(QDialog):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.notepad = QPlainTextEdit()
        layout.addWidget(self.notepad)
        self.setLayout(layout)

    def accept(self):
        self.hide()

    def reject(self):
        self.hide()

    def getText(self):
        return self.notepad.toPlainText()

    def setText(self, text):
        self.notepad.setPlainText(text)


class CoderDialog(QDialog):
    def __init__(self, coderName, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle('Edit default coder name')

        self._coderName = coderName

        layout = QVBoxLayout()
        self.setLayout(layout)

        inputLayout = QHBoxLayout()
        layout.addLayout(inputLayout)

        self.coderNameLineEdit = QLineEdit(self._coderName)
        inputLayout.addWidget(QLabel('Default coder:'))
        inputLayout.addWidget(self.coderNameLineEdit)

        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)

        okButton = QPushButton('Ok')
        buttonLayout.addWidget(okButton)
        okButton.clicked.connect(self.accept)

        cancelButton = QPushButton('Cancel')
        buttonLayout.addWidget(cancelButton)
        cancelButton.clicked.connect(self.reject)

    def accept(self):
        self._coderName = self.coderNameLineEdit.text()
        super().accept()

    @property
    def coderName(self):
        return self._coderName
