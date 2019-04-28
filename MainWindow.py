from PyQt5.QtWidgets import QMainWindow, QAction, QTabWidget, QTableView, QWidget, QVBoxLayout, \
                            QPushButton, QFileDialog, QMenuBar
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
from MapWidget import TravelMap
from LocationData import LocationHandler
import platform
from os import path


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.statusBar().showMessage('Loading Data...')

        self.model = LocationHandler()
        dirname = path.dirname(__file__)
        csvfile = path.join(dirname, 'data/user_sca_geodata.csv')
        self.model.read_csv(csvfile)
        self.data = self.model.data

        self.mapWidget = TravelMap(self.data)
        self.tableWidget = QTableView()

        self.init_ui()
        self.display_data()

        self.statusBar().showMessage('Ready')

    def init_ui(self):
        self.statusBar().showMessage('Generating Display...')

        if platform.uname().system.startswith('Darw'):
            self._menu_bar = QMenuBar()  # parentless menu bar for Mac OS
        else:
            self._menu_bar = self.menuBar()  # refer to the default one

        #newAct = QAction('New Profile', self)
        #newAct.triggered.connect(self.new_config())
        #loadAct = QAction('Load Profile', self)
        #loadAct.triggered.connect(self.load_file())

        fileMenu = self._menu_bar.addMenu(self.tr('Menu name', '&File'))
        newAction = fileMenu.addAction(self.tr('Fine Menu Command', '&New'))
        #fileMenu.addAction(loadAct)

        newAction.setShortcut(QKeySequence.New)
        newAction.setToolTip(self.tr('File:New tooltip', 'Create a new, empty document'))
        # newAction.triggered.connect(self.load_file())

        #layout = QHBoxLayout()
        tabWidget = QTabWidget()
        dataWidget = QWidget()
        addLocationButton = QPushButton('Add Location')

        data_layout = QVBoxLayout()
        data_layout.addWidget(self.tableWidget)
        data_layout.addWidget(addLocationButton)
        data_layout.setAlignment(addLocationButton, Qt.AlignLeft)
        dataWidget.setLayout(data_layout)

        tabWidget.addTab(self.mapWidget, 'Map')
        tabWidget.addTab(dataWidget, 'Data')

        #layout.addWidget(tabWidget)
        self.setCentralWidget(tabWidget)

        self.setGeometry(600, 600, 900, 600)
        self.setWindowTitle('MyTravel')
        self.show()

    def load_file(self):
        file = QFileDialog().getOpenFileName(self, "Load Data", '', "Comma Separated Value Files (*.csv)")
        # print(file)
        self.model.read_csv(file[0])
        self.display_data()

    def display_data(self):
        self.tableWidget.setModel(PandasModel(self.data))
        self.tableWidget.update()


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

    def headerData(self, col, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

