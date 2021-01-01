from PyQt5.QtWidgets import QMainWindow, QAction, QTabWidget, QTableView, QWidget, QVBoxLayout, QHBoxLayout, \
                            QPushButton, QFileDialog, QMenuBar, QLabel, QMessageBox, QAbstractItemView
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence, QFont
from MapWidget import TravelMap
from LocationData import LocationHandler
from FormWidgets import LocationEntry
import platform
from os import path
import operator


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.statusBar().showMessage('Loading Data...')

        self.model = LocationHandler()
        dirname = path.dirname(__file__)
        self.csvfile = path.join(dirname, 'data/user_sca_geodata.csv')
        self.model.read_csv(self.csvfile)

        # print(self.model.country_cnt, self.model.state_cnt)

        self.mapWidget = TravelMap(self.model.data)
        self.tableWidget = QTableView()
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.doubleClicked.connect(self.on_cell_click)

        self.init_ui()
        self.display_data()

        self.model.data_changed.connect(self.on_data_change)

        self.on_data_change()
        self.statusBar().showMessage('Ready', 2000)

    def init_ui(self):
        label_font = QFont()
        label_font.setPointSize(20)
        label_font.setBold(True)

        self.statusBar().showMessage('Generating Display...')

        if platform.uname().system.startswith('Darw'):
            self._menu_bar = QMenuBar()  # parentless menu bar for Mac OS
        else:
            self._menu_bar = self.menuBar()  # refer to the default one

        # newAct = QAction('New Profile', self)
        # newAct.triggered.connect(self.new_config())
        # loadAct = QAction('Load Profile', self)
        # loadAct.triggered.connect(self.load_file())

        fileMenu = self._menu_bar.addMenu(self.tr('Menu name', '&File'))
        newAction = fileMenu.addAction(self.tr('Fine Menu Command', '&New'))
        # fileMenu.addAction(loadAct)

        newAction.setShortcut(QKeySequence.New)
        newAction.setToolTip(self.tr('File:New tooltip', 'Create a new, empty document'))
        # newAction.triggered.connect(self.load_file())

        # layout = QHBoxLayout()
        tabWidget = QTabWidget()
        dataWidget = QWidget()

        self.country_stats = QLabel('Countries visited:  / ')
        self.country_stats.setFont(label_font)
        self.country_stats.setAlignment(Qt.AlignCenter)
        self.state_stats = QLabel('States visited:  / ')
        self.state_stats.setFont(label_font)
        self.state_stats.setAlignment(Qt.AlignCenter)
        self.wish_stats = QLabel('Wish list: ')
        self.wish_stats.setFont(label_font)
        self.wish_stats.setAlignment(Qt.AlignCenter)
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(self.state_stats)
        stats_layout.addWidget(self.country_stats)
        stats_layout.addWidget(self.wish_stats)

        add_location_button = QPushButton('Add Location')
        add_location_button.setFixedWidth(150)
        add_location_button.clicked.connect(self.add_location)
        self.save_data_button = QPushButton('Save Data')
        self.save_data_button.setFixedWidth(150)
        self.save_data_button.setVisible(False)
        self.save_data_button.clicked.connect(self.save_data)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_location_button, Qt.AlignLeft)
        button_layout.addWidget(self.save_data_button, Qt.AlignRight)

        data_layout = QVBoxLayout()
        data_layout.addLayout(stats_layout)
        data_layout.addWidget(self.tableWidget)
        data_layout.addLayout(button_layout)

        # data_layout.setAlignment(add_location_button)
        dataWidget.setLayout(data_layout)

        tabWidget.addTab(self.mapWidget, 'Map')
        tabWidget.addTab(dataWidget, 'Data')

        # layout.addWidget(tabWidget)
        self.setCentralWidget(tabWidget)

        self.setGeometry(600, 600, 900, 600)
        self.setWindowTitle('MyTravel')
        self.show()

    def on_data_change(self):
        if self.model.saved:
            self.save_data_button.setVisible(False)
        else:
            self.save_data_button.setVisible(True)
        self.update_stats()

    def update_stats(self):
        self.country_stats.setText('Countries visited: ' + str(self.model.country_cnt) + '/' + str(self.model.total_countries))
        self.state_stats.setText('States visited: ' + str(self.model.state_cnt) + '/' + str(self.model.total_states))

        wish_cnt = len(self.model.data[self.model.data['Wish'] == 1])
        self.wish_stats.setText('Wish list: ' + str(wish_cnt))

    def load_file(self):
        file = QFileDialog().getOpenFileName(self, "Load Data", '', "Comma Separated Value Files (*.csv)")
        # print(file)
        self.model.read_csv(file[0])
        self.display_data()

    def display_data(self):
        self.tableWidget.setModel(PandasModel(self.model.data))
        # self.tableWidget.setSortingEnabled(True)
        self.tableWidget.repaint()

    def on_cell_click(self, cell):
        # print(cell.data(), self.model.data.at[cell.row(), 'Country'])
        data = self.model.data.loc[cell.row()]
        form = LocationEntry(data.to_dict())
        form.submitted.connect(self.push_data)
        form.exec_()

    def add_location(self):
        form = LocationEntry()
        form.submitted.connect(self.push_data)
        form.exec_()

    def save_data(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Are you sure you wish to save your changes?")
        msg.setWindowTitle("Save Data")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        result = msg.exec()
        if result == QMessageBox.Ok:
            self.statusBar().showMessage('Saving...')
            self.model.write_csv(self.csvfile)
            self.statusBar().showMessage('Saving...', 2000)

    def push_data(self, entry=None):
        # print(entry)
        if type(entry) == dict:
            self.model.new_location(entry)  # entry['Address'], entry['City'], entry['State'], entry['Country'])
            self.mapWidget.update_data(self.model.data)
            self.display_data()


class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def setData(self, index, value, role=Qt.DisplayRole):
        if not index.isValid():
            return False
        if role == Qt.DisplayRole and index.column() == 0:
            # do stuff
            pass
        else:
            pass
        # self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
        # print(">>> setData() index.row = ", index.row())
        # print(">>> setData() index.column = ", index.column())
        self.dataChanged.emit(index, index)
        return True

    def insertRows(self, position, rows=1, index=QModelIndex()):
        """ Insert a row into the model. """
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)

        # for row in range(rows):
        #    self._data.insert(position + row, {"name": "", "address": ""})

        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        """ Remove a row from the model. """
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)

        del self._data[position:position + rows]

        self.endRemoveRows()
        return True

    # def sort(self, col, order=None):
        # """sort table by given column number col"""
        # print(">>> sort() col = ", col)
        # if col != 0:
        #    self.layoutAboutToBeChanged.emit()
        #    self._data = sorted(self._data, key=operator.itemgetter(col))
        #   if order == Qt.DescendingOrder:
        #        self._data.reverse()
        #    self.layoutChanged.emit()

    def headerData(self, col, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

