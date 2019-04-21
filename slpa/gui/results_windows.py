import csv
from imports import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFrame,
                     QFileDialog, QAbstractTableModel, QHeaderView, Qt, QModelIndex,
                     QTableView, QAbstractItemView, QSizePolicy, QApplication, QVariant,
                     QAbstractScrollArea)


class ResultsTableModel(QAbstractTableModel):
    def __init__(self, header, results):
        super().__init__()
        self.header = header
        self.results = results  # results is a list of dictionaries

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.results)

    def appendRows(self, entries):
        numOfRows = self.rowCount()
        self.beginInsertRows(QModelIndex(), numOfRows, numOfRows+len(entries)-1)
        for entry in entries:
            self.results.append(entry)
        self.endInsertRows()

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.header)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        column = index.column()
        if not index.isValid() or not (0 <= row < len(self.results)):
            return None

        entry = self.results[row]

        if role == Qt.DisplayRole:
            column_name = self.header[column]
            return entry[column_name]
        else:
            return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            header = self.header[section]
            return QVariant(header)
        return QVariant(int(section + 1))


class ResultsWindow(QDialog):
    def __init__(self, title, dialog, parent):
        super().__init__(parent=parent)
        self.setWindowTitle(title)
        self.dialog = dialog
        dataModel = ResultsTableModel(self.dialog.header, self.dialog.results)

        self.table = ResultsTableView()
        self.table.setModel(dataModel)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # The option buttons
        self.reopenButton = QPushButton('Reopen function dialog')
        self.reopenButton.clicked.connect(self.reopen)

        self.saveButton = QPushButton('Save to file')
        self.saveButton.clicked.connect(self.save)

        self.closeButton = QPushButton('Close window')
        self.closeButton.clicked.connect(self.reject)

        # Appearance
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        dialogWidth = self.table.horizontalHeader().length() + 25
        dialogHeight = self.table.verticalHeader().length() + 25
        self.resize(dialogWidth, dialogHeight)

        # Layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.reopenButton)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.closeButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.table)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

    # def sizeHint(self):
    #     sz = QDialog.sizeHint(self)
    #     minWidth = self.table.calcWidth()+41
    #     if sz.width() < minWidth:
    #
    #         sz.setWidth(minWidth)
    #     if sz.height() < 400:
    #         sz.setHeight(400)
    #     return sz

    def reopen(self):
        #TODO: maybe modify this so that function and result windows can appear together
        if self.dialog.exec_():
            if self.dialog.update:
                self.table.model().appendRows(self.dialog.results)
                self.table.resizeColumnsToContents()
                self.table.resizeRowsToContents()
            else:
                dataModel = ResultsTableModel(self.dialog.header, self.dialog.results)
                self.table.setModel(dataModel)
                self.table.resizeColumnsToContents()
                self.table.resizeRowsToContents()
        self.raise_()
        self.activateWindow()

    def save(self):
        fileDialog = QFileDialog(caption='Save results')
        fileDialog.setAcceptMode(QFileDialog.AcceptSave)
        fileDialog.setFileMode(QFileDialog.AnyFile)
        fileDialog.setNameFilter('Text files (*.txt *.csv)')
        fileDialog.selectFile('results')
        fileDialog.setDefaultSuffix('txt')

        if fileDialog.exec_():
            filename = fileDialog.selectedFiles()
            with open(filename[0], mode='w', encoding='utf-8-sig') as f:
                model = self.table.model()
                writer = csv.writer(f, delimiter='\t')
                writer.writerow(model.header)
                for row in range(model.rowCount()):
                    entry = list()
                    for column in range(model.columnCount()):
                        idx = model.index(row, column)
                        dataPoint = str(model.data(idx))
                        entry.append(dataPoint)
                    writer.writerow(entry)


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
    def __init__(self, header, results, settings):
        QAbstractTableModel.__init__(self)
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


class ResultsTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Appearance of the table
        self.verticalHeader().hide()
        self.horizontalHeader().setMinimumSectionSize(50)
        #self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Behavior of the table
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSortingEnabled(True)

        #self.clip = QApplication.clipboard()

    # def keyPressEvent(self, e):
    #     if (e.modifiers() & Qt.ControlModifier):
    #         try:
    #             selected = self.selectionModel().selectedRows()
    #         except AttributeError:
    #             super().keyPressEvent(e)
    #             return
    #         if e.key() == Qt.Key_C: #copy
    #             copyInfo = list()
    #             for row in selected:
    #                 copy = list()
    #                 for col in range(self.model().columnCount()):
    #                     ind = self.model().index(row.row(),col)
    #                     copy.append(self.model().data(ind, Qt.DisplayRole))
    #                 copy = '\t'.join(copy)
    #                 copyInfo.append(copy)
    #             copyInfo = '\n'.join(copyInfo)
    #             self.clip.setText(copyInfo)


    #def setModel(self, model):
    #    super().setModel(model)
    #    #super(TableWidget, self).setModel(model)
    #    self.resizeColumnsToContents()

    # def calcWidth(self):
    #     header = self.horizontalHeader()
    #     width = self.horizontalOffset()
    #     for i in range(header.count()):
    #         width += header.sectionSize(i)
    #     return width