from imports import QVBoxLayout, QPlainTextEdit, QDialog, QHBoxLayout, QLineEdit, QLabel


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

        layout = QHBoxLayout()
        self.setLayout(layout)
        self.coderName = QLineEdit(coderName)

        layout.addWidget(QLabel('Default coder:'))
        layout.addWidget(self.coderName)

