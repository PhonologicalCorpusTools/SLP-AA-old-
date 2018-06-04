from imports import QColorDialog, QColor


class ColourPickerDialog(QColorDialog):

    def __init__(self):
        super().__init__()
        self.setCustomColor(0, QColor(255,214,197,255))
        self.setCustomColor(2, QColor(231,193,178,255))
        self.setCustomColor(4, QColor(255,226,201,255))
        self.setCustomColor(8, QColor(231,203,181,255))
        self.setCustomColor(10, QColor(230,200,176,255))
        self.setCustomColor(12, QColor(255,203,163,255))
        self.setCustomColor(14, QColor(232,184,148,255))
        self.setCustomColor(1, QColor(231,179,141,255))
        self.setCustomColor(3, QColor(216,144,95,255))
        self.setCustomColor(5, QColor(194,129,85,255))
        self.setCustomColor(7, QColor(190,121,74,255))
        self.setCustomColor(9, QColor(136,81,58,255))
        self.setCustomColor(11, QColor(123,73,52,255))
        self.setCustomColor(13, QColor(115,62,38,255))
        self.setCustomColor(15, QColor(18,0,0,255))