from PyQt6.QtWidgets import QMainWindow, QTabWidget, QTableView, QWidget, QVBoxLayout, QHBoxLayout, \
                            QPushButton, QFileDialog, QErrorMessage, QMenuBar, QLabel, QMessageBox, QAbstractItemView, QMenu
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QKeySequence, QFont, QAction
from MapWidget import TravelMap
from LocationData import LocationHandler
from FormWidgets import LocationEntry
import platform
from os import path

# TODO:  Add support for logging full trips (might require tree widget rather than table to display data)
# TODO:  Add support for UnTappd data
# TODO:  Auto-adjust width of columns to fit data (at least for most important columns)
# TODO:  Hide/show less used columns?
# TODO:  Add multi user/config support
# TODO:  Save/restore settings between sessions?
# TODO:  Add key shortcuts and Menu shortcuts?
# TODO:  Modify table to use graphical check marks and x's instead of True/False, stars for Favorites
# TODO:  Get QTableView clickable sorting to work?
# TODO:  Encrypt saved geodata?
# TODO:  Look into iCloud backup for user data
# TODO:  Further graphical improvements, make prettier
# TODO:  Data analysis graphical objects (progress bars, pie charts, plots)?


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.statusBar().showMessage('Loading Data...')

        # Prepare data model
        self.model = LocationHandler()
        self.model.data_changed.connect(self.on_data_change)
        self.model.new_save_state.connect(self.check_save_state)
        self.model.exception.connect(self.error_dialog)

        # Prepare main widgets
        self.mapWidget = TravelMap(self.model.data, self)
        self.tableWidget = QTableView()
        self.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.customContextMenuRequested.connect(self.on_context_menu_req)
        self.tableWidget.doubleClicked.connect(self.on_cell_doubleclick)
        # self.tableWidget.clicked.connect(self.on_cell_click)

        # Create/show remaining ui
        self.init_ui()

        # Populate model and display results
        dirname = path.dirname(__file__)
        self.csvfile = path.join(dirname, 'data/user_sca_geodata.csv')
        self.model.read_csv(self.csvfile)
        self.mapWidget.update_data(self.model.data)
        self.display_data()

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

        newAction.setShortcut(QKeySequence.StandardKey.New)
        newAction.setToolTip(self.tr('File:New tooltip', 'Create a new, empty document'))
        # newAction.triggered.connect(self.load_file())

        # layout = QHBoxLayout()
        tabWidget = QTabWidget()
        dataWidget = QWidget()

        self.country_stats = QLabel('Countries visited:  / ')
        self.country_stats.setFont(label_font)
        self.country_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state_stats = QLabel('States visited:  / ')
        self.state_stats.setFont(label_font)
        self.state_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wish_stats = QLabel('Wish list: ')
        self.wish_stats.setFont(label_font)
        self.wish_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        button_layout.addWidget(add_location_button, Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(self.save_data_button, Qt.AlignmentFlag.AlignRight)

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
        self.update_stats()

    def check_save_state(self):
        if self.model.saved:
            self.save_data_button.setVisible(False)
        else:
            self.save_data_button.setVisible(True)

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

    def on_context_menu_req(self, point):
        row = self.tableWidget.indexAt(point).row()
        index = self.tableWidget.model().model_index(row)

        menu = QMenu(self)
        edit = menu.addAction('Edit Selected')
        remove = menu.addAction('Remove Selected')
        add = menu.addAction('Add New')
        action = menu.exec(self.mapToGlobal(point))
        if action == edit:
            self.edit_location(index)
        elif action == add:
            self.add_location()
        elif action == remove:
            self.remove_location(index)

    def on_cell_doubleclick(self, cell):
        # print(cell.data(), self.model.data.at[cell.row(), 'Country'])
        index = self.tableWidget.model().model_index(cell.row())
        self.edit_location(index)

    def add_location(self):
        form = LocationEntry(None, self)
        form.submitted.connect(self.push_data)
        form.exec()

    def edit_location(self, index):
        data = self.model.data.loc[index]
        form = LocationEntry(data.to_dict(), self)
        form.submitted.connect(self.push_data)
        form.exception.connect(self.error_dialog)
        form.exec()

    def error_dialog(self, e):
        QMessageBox().warning(self, 'Error Encountered!', str(e))

    def remove_location(self, index):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Are you sure you wish to remove " + self.model.data.loc[index]['City'] + "?")
        msg.setWindowTitle("Remove Location")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        result = msg.exec()
        if result == QMessageBox.StandardButton.Ok:
            self.statusBar().showMessage('Removing location...')
            self.model.remove_location(index)
            self.mapWidget.update_data(self.model.data)
            self.display_data()
            self.statusBar().showMessage('Location Removed!', 2000)

    def save_data(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Are you sure you wish to save your changes?")
        msg.setWindowTitle("Save Data")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        result = msg.exec()
        if result == QMessageBox.StandardButton.Ok:
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

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                return str(self._data.values[index.row()][index.column()]).strip()
        return None

    def model_index(self, row):
        return self._data.index[row]

    def setData(self, index, value, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return False
        if role == Qt.ItemDataRole.DisplayRole and index.column() == 0:
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

    def headerData(self, col, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]
        return None

