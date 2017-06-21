from imports import QHBoxLayout, QVBoxLayout, QPlainTextEdit, QDialog, QPushButton

class NotesDialog(QDialog):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.notepad = QPlainTextEdit()
        layout.addWidget(self.notepad)
        # buttonLayout = QHBoxLayout()
        # ok = QPushButton('OK')
        # ok.clicked.connect(self.accept)
        # cancel = QPushButton('Cancel')
        # cancel.clicked.connect(self.reject)
        # buttonLayout.addWidget(ok)
        # buttonLayout.addWidget(cancel)
        # layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def accept(self):
        self.hide()

    def reject(self):
        self.hide()

    def getText(self):
        return self.notepad.toPlainText()

    def setText(self, text):
        self.notepad.setPlainText(text)