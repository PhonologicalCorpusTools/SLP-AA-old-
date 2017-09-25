import os, sys
from imports import QLabel, Slot, QPixmap

class HandShapeImage(QLabel):

    def __init__(self, path, reversed=False, parent=None):
        super().__init__()
        self.image = QPixmap(path)
        self.isReversed = False
        self.setPixmap(self.image)
        self.mapping = {0: 'hand.png',
                        1: 'hand.png',
                        2: 'hand_thumb_selected.png',
                        3: 'hand_thumb_finger_contact.png',
                        4: 'hand_index_selected.png',
                        5: 'hand_middle_selected.png',
                        6: 'hand_ring_selected.png',
                        7: 'hand_pinky_selected.png'}
        self.reversed_mapping = {n:'reversed_'+self.mapping[n] for n in self.mapping}
        self.mappingChoice = self.mapping

    @Slot(int)
    def transcriptionSlotChanged(self, e):
        file_name = 'hand_slot{}.png'.format(e)
        self.setPixmap(QPixmap(getMediaFilePath(file_name)))

    @Slot(int)
    def useReverseImage(self, e):
        self.mappingChoice = self.reversed_mapping

    @Slot(int)
    def useNormalImage(self, e):
        self.mappingChoice = self.mapping\


def getMediaFilePath(filename):
    if hasattr(sys, 'frozen'):
        dir = os.path.dirname(sys.executable)
        path = os.path.join(dir, 'media', filename)
    else:
        path = os.path.join(os.getcwd(), 'media', filename)
    return path