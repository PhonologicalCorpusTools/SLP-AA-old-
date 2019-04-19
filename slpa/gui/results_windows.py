import csv
from imports import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFrame,
                     QFileDialog, QAbstractTableModel, QHeaderView, Qt,
                     QModelIndex, QTableView, QAbstractItemView, QSizePolicy, QApplication)

class ResultsWindow(QDialog):
    def __init__(self, title, dialog, parent):
        QDialog.__init__(self, parent=parent)
        self.dialog = dialog
        dataModel = ResultsModel(self.dialog.header, self.dialog.results, self._parent.settings)
        layout = QVBoxLayout()
        self.table = TableWidget()
        self.table.setModel(dataModel)
        try:
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        except AttributeError:
            self.table.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.table)
        self.aclayout = QHBoxLayout()

        self.redoButton = QPushButton('Reopen function dialog')
        self.redoButton.clicked.connect(self.redo)

        self.saveButton = QPushButton('Save to file')
        self.saveButton.clicked.connect(self.save)

        self.closeButton = QPushButton('Close window')
        self.closeButton.clicked.connect(self.reject)

        self.aclayout.addWidget(self.redoButton)
        self.aclayout.addWidget(self.saveButton)
        self.aclayout.addWidget(self.closeButton)

        #acframe = QFrame()
        #acframe.setLayout(self.aclayout)

        layout.addLayout(self.aclayout)
        self.setLayout(layout)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.setWindowTitle(title)
        dialogWidth = self.table.horizontalHeader().length() + 50
        dialogHeight = self.table.verticalHeader().length() + 50
        self.resize(dialogWidth, dialogHeight)

    def sizeHint(self):
        sz = QDialog.sizeHint(self)
        minWidth = self.table.calcWidth()+41
        if sz.width() < minWidth:

            sz.setWidth(minWidth)
        if sz.height() < 400:
            sz.setHeight(400)
        return sz

    def redo(self):
        print(self.dialog.exec_())
        print(self.dialog.update)
        if self.dialog.exec_():
            if self.dialog.update:
                self.table.model().addRows(self.dialog.results)
            else:
                dataModel = ResultsModel(self.dialog.header,self.dialog.results, self._parent.settings)
                self.table.setModel(dataModel)
        self.raise_()
        self.activateWindow()

    def save(self):
        filename = QFileDialog.getSaveFileName(self,'Choose save file',
                        filter = 'Text files (*.txt *.csv)')

        if filename and filename[0]:
            with open(filename[0], mode='w', encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter='\t')
                writer.writerow(self.table.model().columns)
                for row in self.table.model().rows:
                    writer.writerow(row)


class BaseTableModel(QAbstractTableModel):

    def __init__(self, settings, parent = None):
        self.columns = []
        self.rows = []
        self.allData = []
        QAbstractTableModel.__init__(self, parent)
        self.settings = settings

    def rowCount(self, parent = None):
        return len(self.rows)

    def columnCount(self, parent = None):
        return len(self.columns)

    def sort(self, col, order):
        """sort table by given column number col"""
        self.layoutAboutToBeChanged.emit()
        self.rows = sorted(self.rows,
                key=lambda x: x[col])
        if order == Qt.DescendingOrder:
            self.rows.reverse()
        self.layoutChanged.emit()

    def data(self, index, role = None):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        row = index.row()
        col = index.column()
        try:
            data = self.rows[row][col]
            if isinstance(data,float):
                data = str(round(data,self.settings['sigfigs']))
            elif isinstance(data,bool):
                if data:
                    data = 'Yes'
                else:
                    data = 'No'
            elif isinstance(data,(list, tuple)):
                data = ', '.join(data)
            else:
                data = str(data)
        except IndexError:
            data = ''

        return data

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[col]
        return None

    def addRow(self,row):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        if isinstance(row[0], dict):
            self.rows.append([row[header] for header in self.columns])
        else:
            self.rows.append(row)
        self.endInsertRows()

    def addRows(self,rows):
        self.beginInsertRows(QModelIndex(),self.rowCount(),self.rowCount() + len(rows)-1)
        for row in rows:
            if isinstance(row, dict):
                self.rows.append([row[header] for header in self.columns])
            else:
                self.rows.append(row)
        self.endInsertRows()

    def removeRow(self,ind):
        self.beginRemoveRows(QModelIndex(),ind,ind)
        del self.rows[ind]
        self.endRemoveRows()

    def removeRows(self, inds):
        inds = sorted(inds, reverse=True)
        for i in inds:
            self.beginRemoveRows(QModelIndex(),i,i)
            del self.rows[i]
            self.endRemoveRows()

class ResultsModel(BaseTableModel):
    def __init__(self, header, results, settings, parent=None):
        QAbstractTableModel.__init__(self,parent)
        self.settings = settings
        headerDynamic = []
        headerStatic = []
        headerIdx = -1
        for currHeader in header:
            headerIdx += 1
            currRow = 0
            stop = 0
            while stop is not 1 and currRow+1 < len(results):
                cv = results[currRow][currHeader]
                nv = results[currRow+1][currHeader]
                if cv != nv:
                    stop = 1
                currRow +=1
            if stop == 0:
                headerStatic.append(headerIdx)
            else:
                headerDynamic.append(headerIdx)

        newHeader = []
        for headerIdx in (headerDynamic + headerStatic):
            newHeader.append(header[headerIdx])

        orderResults = settings.__getitem__('resultsDisplay')
        if orderResults['unique_first']:
            self.columns = newHeader
        else:
            self.columns = header
        currRows = []
        for row in results:
            currRow = []
            for currHeader in self.columns:
                currRow.append(row[currHeader])
            currRows.append(currRow)
        self.rows = currRows


class TableWidget(QTableView):
    def __init__(self,parent=None):
        super(TableWidget, self).__init__(parent=parent)

        self.verticalHeader().hide()

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.horizontalHeader().setMinimumSectionSize(70)

        self.setSortingEnabled(True)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        self.clip = QApplication.clipboard()

    def keyPressEvent(self, e):
        if (e.modifiers() & Qt.ControlModifier):
            try:
                selected = self.selectionModel().selectedRows()
            except AttributeError:
                super().keyPressEvent(e)
                return
            if e.key() == Qt.Key_C: #copy
                copyInfo = list()
                for row in selected:
                    copy = list()
                    for col in range(self.model().columnCount()):
                        ind = self.model().index(row.row(),col)
                        copy.append(self.model().data(ind, Qt.DisplayRole))
                    copy = '\t'.join(copy)
                    copyInfo.append(copy)
                copyInfo = '\n'.join(copyInfo)
                self.clip.setText(copyInfo)


    def setModel(self,model):
        super(TableWidget, self).setModel(model)
        self.resizeColumnsToContents()

    def calcWidth(self):
        header = self.horizontalHeader()
        width = self.horizontalOffset()
        for i in range(header.count()):
            width += header.sectionSize(i)
        return width