from PyQt5.QtCore import (QEasingCurve, QFileInfo, QLineF, QMimeData,
                          QParallelAnimationGroup, QPoint, QPointF, QPropertyAnimation, qrand,
                          QRectF, qsrand, Qt, QTime, pyqtSignal)
from PyQt5.QtGui import (QBrush, QColor, QDrag, QImage, QPainter, QPen,
                         QPixmap, QTransform)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsObject, QWidget, QMessageBox, QLineEdit,
                             QPushButton, QDockWidget, QMainWindow, QListWidget, QListWidgetItem, QDialog,
                             QGraphicsScene, QGraphicsView, QTreeWidget, QTreeWidgetItem, QVBoxLayout)
import sys


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        dock = QDockWidget()
        dock.setWindowTitle('Corpus')
        dock.setAllowedAreas(Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)

        dockWrapper = QWidget()
        dockLayout = QVBoxLayout()
        dockWrapper.setLayout(dockLayout)
        self.corpusList = SignList(self)
        self.topLevelList = []
        self.corpusList.itemClicked.connect(self.loadHandShape)
        dockLayout.addWidget(self.corpusList)
        dock.setWidget(dockWrapper)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        centralWidget = QWidget()
        layout = QVBoxLayout()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.new = QLineEdit()
        layout.addWidget(self.new)

        add = QPushButton('Add')
        layout.addWidget(add)
        add.clicked.connect(self.addSign)

        addAsVariant = QPushButton('Add as a variant')
        layout.addWidget(addAsVariant)
        addAsVariant.clicked.connect(self.addAsSignVariant)

    def loadHandShape(self):
        pass

    def addAsSignVariant(self):
        sign = self.new.text()
        self.new.clear()
        if sign:
            existings = TopLevelList(self.topLevelList)
            existings.selected.connect(lambda s: self.top(s, sign))
            existings.exec_()

    def top(self, selected, sign):
        for i in range(self.corpusList.topLevelItemCount()):
            topLevel = self.corpusList.topLevelItem(i)
            gloss = topLevel.text(0)
            if gloss == selected:
                topLevel.addChild(QTreeWidgetItem([sign], type=1))
                break
        topLevel.sortChildren(0, Qt.AscendingOrder)

    def addSign(self):
        sign = self.new.text()
        self.new.clear()
        if sign:
            self.topLevelList.append(sign)
            newSign = QTreeWidgetItem([sign], type=0)
            self.corpusList.addTopLevelItem(newSign)
            self.corpusList.sortItems(0, Qt.AscendingOrder)


class TopLevelList(QDialog):
    selected = pyqtSignal(str)
    def __init__(self, topLevelItems):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.topLevelList = QListWidget()
        layout.addWidget(self.topLevelList)

        for item in topLevelItems:
            QListWidgetItem(item, self.topLevelList)

        Ok = QPushButton('Confirm')
        Ok.clicked.connect(self.accept)
        layout.addWidget(Ok)

    def accept(self):
        selected = self.topLevelList.selectedItems()[0].text()
        self.selected.emit(selected)
        super().accept()

class SignList(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(500, 200)
        self.setColumnCount(1)
        self.setHeaderLabels(['Signs'])


if __name__ == '__main__':

    def printItem(item):
        if item.childCount() != 0 and item.type() == 0:
            alert = QMessageBox()
            alert.setWindowTitle('Warning')
            alert.setText('Please select one of the variants')
            #alert.addButton('Continue and save', QMessageBox.YesRole)
            #alert.addButton('Continue but don\'t save', QMessageBox.NoRole)
            #alert.addButton('Go back', QMessageBox.RejectRole)
            alert.exec_()

    app = QApplication(sys.argv)

    # l1 = QTreeWidgetItem(['Sign1'], type=0)
    # l2 = QTreeWidgetItem(['Sign2'], type=0)
    # l3 = QTreeWidgetItem(['Sign3'], type=0)
    # #l2 = QTreeWidgetItem(['AA', 'BB', 'CC'])
    #
    # for i in range(3):
    #     l1_child = QTreeWidgetItem(["Variant" + str(i+1)], type=1)
    #     l1.addChild(l1_child)
    #
    # for j in range(2):
    #     l2_child = QTreeWidgetItem(["Variant" + str(j+1)], type=1)
    #     l2.addChild(l2_child)

    w = MyWidget()
    app.setActiveWindow(w)
    w.show()

    #tw = SignList(w)

    #tw.addTopLevelItem(l1)
    #tw.addTopLevelItem(l2)
    #tw.addTopLevelItem(l3)

    #tw.itemClicked.connect(printItem)

    #top_1 = tw.topLevelItem(1)

    #print(tw.topLevelItemCount())
    #print(top_1.text(0))
    #print(l1.childCount())
    sys.exit(app.exec_())

# class ColorItem(QGraphicsItem):
#     n = 0
#
#     def __init__(self):
#         super(ColorItem, self).__init__()
#
#         self.color = QColor(qrand() % 256, qrand() % 256, qrand() % 256)
#
#         self.setToolTip(
#             "QColor(%d, %d, %d)\nClick and drag this color onto the robot!" %
#             (self.color.red(), self.color.green(), self.color.blue())
#         )
#         self.setCursor(Qt.OpenHandCursor)
#         self.setAcceptedMouseButtons(Qt.LeftButton)
#
#     def boundingRect(self):
#         return QRectF(-15.5, -15.5, 34, 34)
#
#     def paint(self, painter, option, widget):
#         painter.setPen(Qt.NoPen)
#         painter.setBrush(Qt.darkGray)
#         painter.drawEllipse(-12, -12, 30, 30)
#         painter.setPen(QPen(Qt.black, 1))
#         painter.setBrush(QBrush(self.color))
#         painter.drawEllipse(-15, -15, 30, 30)
#
#     def mousePressEvent(self, event):
#         self.setCursor(Qt.ClosedHandCursor)
#
#     def mouseMoveEvent(self, event):
#         if QLineF(QPointF(event.screenPos()),
#                   QPointF(event.buttonDownScreenPos(Qt.LeftButton))).length() < QApplication.startDragDistance():
#             return
#
#         drag = QDrag(event.widget())
#         mime = QMimeData()
#         drag.setMimeData(mime)
#
#         ColorItem.n += 1
#         if ColorItem.n > 2 and qrand() % 3 == 0:
#             root = QFileInfo(__file__).absolutePath()
#
#             image = QImage(root + '/images/head.png')
#             mime.setImageData(image)
#             drag.setPixmap(QPixmap.fromImage(image).scaled(30, 40))
#             drag.setHotSpot(QPoint(15, 30))
#         else:
#             mime.setColorData(self.color)
#             mime.setText("#%02x%02x%02x" % (self.color.red(), self.color.green(), self.color.blue()))
#
#             pixmap = QPixmap(34, 34)
#             pixmap.fill(Qt.white)
#
#             painter = QPainter(pixmap)
#             painter.translate(15, 15)
#             painter.setRenderHint(QPainter.Antialiasing)
#             self.paint(painter, None, None)
#             painter.end()
#
#             pixmap.setMask(pixmap.createHeuristicMask())
#
#             drag.setPixmap(pixmap)
#             drag.setHotSpot(QPoint(15, 20))
#
#         drag.exec_()
#         self.setCursor(Qt.OpenHandCursor)
#
#     def mouseReleaseEvent(self, event):
#         self.setCursor(Qt.OpenHandCursor)
#
#
# class RobotPart(QGraphicsObject):
#     def __init__(self, parent=None):
#         super(RobotPart, self).__init__(parent)
#
#         self.color = QColor(Qt.lightGray)
#         self.dragOver = False
#
#         self.setAcceptDrops(True)
#
#     def dragEnterEvent(self, event):
#         if event.mimeData().hasColor():
#             event.setAccepted(True)
#             self.dragOver = True
#             self.update()
#         else:
#             event.setAccepted(False)
#
#     def dragLeaveEvent(self, event):
#         self.dragOver = False
#         self.update()
#
#     def dropEvent(self, event):
#         self.dragOver = False
#         if event.mimeData().hasColor():
#             self.color = QColor(event.mimeData().colorData())
#
#         self.update()
#
#
# class RobotHead(RobotPart):
#     def __init__(self, parent=None):
#         super(RobotHead, self).__init__(parent)
#
#         self.pixmap = QPixmap()
#
#     def boundingRect(self):
#         return QRectF(-15, -50, 30, 50)
#
#     def paint(self, painter, option, widget=None):
#         if self.pixmap.isNull():
#             painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
#             painter.drawRoundedRect(-10, -30, 20, 30, 25, 25, Qt.RelativeSize)
#             painter.setBrush(Qt.white)
#             painter.drawEllipse(-7, -3 - 20, 7, 7)
#             painter.drawEllipse(0, -3 - 20, 7, 7)
#             painter.setBrush(Qt.black)
#             painter.drawEllipse(-5, -1 - 20, 2, 2)
#             painter.drawEllipse(2, -1 - 20, 2, 2)
#             painter.setPen(QPen(Qt.black, 2))
#             painter.setBrush(Qt.NoBrush)
#             painter.drawArc(-6, -2 - 20, 12, 15, 190 * 16, 160 * 16)
#         else:
#             painter.scale(.2272, .2824)
#             painter.drawPixmap(QPointF(-15 * 4.4, -50 * 3.54), self.pixmap)
#
#     def dragEnterEvent(self, event):
#         if event.mimeData().hasImage():
#             event.setAccepted(True)
#             self.dragOver = True
#             self.update()
#         else:
#             super(RobotHead, self).dragEnterEvent(event)
#
#     def dropEvent(self, event):
#         if event.mimeData().hasImage():
#             self.dragOver = False
#             self.pixmap = QPixmap(event.mimeData().imageData())
#             self.update()
#         else:
#             super(RobotHead, self).dropEvent(event)
#
#
# class RobotTorso(RobotPart):
#     def boundingRect(self):
#         return QRectF(-30, -20, 60, 60)
#
#     def paint(self, painter, option, widget=None):
#         painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
#         painter.drawRoundedRect(-20, -20, 40, 60, 25, 25, Qt.RelativeSize)
#         painter.drawEllipse(-25, -20, 20, 20)
#         painter.drawEllipse(5, -20, 20, 20)
#         painter.drawEllipse(-20, 22, 20, 20)
#         painter.drawEllipse(0, 22, 20, 20)
#
#
# class RobotLimb(RobotPart):
#     def boundingRect(self):
#         return QRectF(-5, -5, 40, 10)
#
#     def paint(self, painter, option, widget=None):
#         painter.setBrush(self.color.lighter(130) if self.dragOver else self.color)
#         painter.drawRoundedRect(self.boundingRect(), 50, 50, Qt.RelativeSize)
#         painter.drawEllipse(-5, -5, 10, 10)
#
#
# class Robot(RobotPart):
#     def __init__(self):
#         super(Robot, self).__init__()
#
#         self.setFlag(self.ItemHasNoContents)
#
#         self.torsoItem = RobotTorso(self)
#         self.headItem = RobotHead(self.torsoItem)
#         self.upperLeftArmItem = RobotLimb(self.torsoItem)
#         self.lowerLeftArmItem = RobotLimb(self.upperLeftArmItem)
#         self.upperRightArmItem = RobotLimb(self.torsoItem)
#         self.lowerRightArmItem = RobotLimb(self.upperRightArmItem)
#         self.upperRightLegItem = RobotLimb(self.torsoItem)
#         self.lowerRightLegItem = RobotLimb(self.upperRightLegItem)
#         self.upperLeftLegItem = RobotLimb(self.torsoItem)
#         self.lowerLeftLegItem = RobotLimb(self.upperLeftLegItem)
#
#         settings = (
#             #    Item                       Position        Rotation  Scale
#             #                                x     y    start    end
#             (self.headItem, 0, -18, 20, -20, 1.1),
#             (self.upperLeftArmItem, -15, -10, 190, 180, 0),
#             (self.lowerLeftArmItem, 30, 0, 50, 10, 0),
#             (self.upperRightArmItem, 15, -10, 300, 310, 0),
#             (self.lowerRightArmItem, 30, 0, 0, -70, 0),
#             (self.upperRightLegItem, 10, 32, 40, 120, 0),
#             (self.lowerRightLegItem, 30, 0, 10, 50, 0),
#             (self.upperLeftLegItem, -10, 32, 150, 80, 0),
#             (self.lowerLeftLegItem, 30, 0, 70, 10, 0),
#             (self.torsoItem, 0, 0, 5, -20, 0),
#         )
#
#         animation = QParallelAnimationGroup(self)
#         for item, pos_x, pos_y, start_rot, end_rot, scale in settings:
#             item.setPos(pos_x, pos_y)
#
#             rot_animation = QPropertyAnimation(item, b'rotation')
#             rot_animation.setStartValue(start_rot)
#             rot_animation.setEndValue(end_rot)
#             rot_animation.setEasingCurve(QEasingCurve.SineCurve)
#             rot_animation.setDuration(2000)
#             animation.addAnimation(rot_animation)
#
#             if scale > 0:
#                 scale_animation = QPropertyAnimation(item, b'scale')
#                 scale_animation.setEndValue(scale)
#                 scale_animation.setEasingCurve(QEasingCurve.SineCurve)
#                 scale_animation.setDuration(2000)
#                 animation.addAnimation(scale_animation)
#
#         animation.setLoopCount(-1)
#         animation.start()
#
#     def boundingRect(self):
#         return QRectF()
#
#     def paint(self, painter, option, widget=None):
#         pass
#
#
# class GraphicsView(QGraphicsView):
#
#     def resizeEvent(self, e):
#         pass
#
#
# if __name__ == '__main__':
#
#     import sys
#     import math
#
#     app = QApplication(sys.argv)
#
#     qsrand(QTime(0, 0, 0).secsTo(QTime.currentTime()))
#
#     scene = QGraphicsScene(-200, -200, 400, 400)
#
#     for i in range(10):
#         item = ColorItem()
#         angle = i * 6.28 / 10.0
#         item.setPos(math.sin(angle) * 150, math.cos(angle) * 150)
#         scene.addItem(item)
#
#     robot = Robot()
#     robot.setTransform(QTransform.fromScale(1.2, 1.2), True)
#     robot.setPos(0, -20)
#     scene.addItem(robot)
#
#     view = GraphicsView(scene)
#     view.setRenderHint(QPainter.Antialiasing)
#     view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
#     view.setBackgroundBrush(QColor(230, 200, 167))
#     view.setWindowTitle("Drag and Drop Robot")
#     view.show()
#
# sys.exit(app.exec_())