import os, sys
from imports import QLabel, Slot, QPixmap, Qt

class HandShapeImage(QLabel):

    def __init__(self, path, reversed=False, parent=None):
        super().__init__()
        self.image = QPixmap(path)
        self.isReversed = False
        self.setPixmap(self.image.scaled(self.width(), self.height(), Qt.KeepAspectRatio))
        self.mapping = {0: 'hand.png',
                        1: 'hand.png',
                        2: 'hand_thumb_selected.png',
                        3: 'hand_thumb_finger_contact.png',
                        4: 'hand_index_selected.png',
                        5: 'hand_middle_selected.png',
                        6: 'hand_ring_selected.png',
                        7: 'hand_pinky_selected.png'}
        self.reversed_mapping = {n: 'reversed_'+self.mapping[n] for n in self.mapping}
        self.mappingChoice = self.mapping

    @Slot(int)
    def transcriptionSlotChanged(self, e):
        file_name = 'hand_slot{}.JPG'.format(e)
        img = QPixmap(getMediaFilePath(file_name))
        self.setPixmap(img.scaled(self.width(), self.height(), Qt.KeepAspectRatio))
        #self.setPixmap(QPixmap(getMediaFilePath(file_name)))

    @Slot(int)
    def useReverseImage(self, e):
        self.mappingChoice = self.reversed_mapping

    @Slot(int)
    def useNormalImage(self, e):
        self.mappingChoice = self.mapping


def getMediaFilePath(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'media', filename)
    return os.path.join(os.path.abspath("."), 'media', filename)