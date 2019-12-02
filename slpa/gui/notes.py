from imports import QVBoxLayout, QPlainTextEdit, QDialog


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
