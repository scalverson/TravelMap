from PyQt5.QtWidgets import QMainWindow, QAction, QTabWidget, QTableWidget
from PyQt5.QtWebKit import
from MapWidget import TravelMap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        newAct = QAction('New Profile', self)
        loadAct = QAction('Load Profile', self)

        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAct)
        fileMenu.addAction(loadAct)

        self.tabWidget = QTabWidget()
        self.mapWidget = TravelMap()
        self.tableWidget = QTableWidget()

        self.tabWidget.addTab(self.mapWidget, 'Map')
        self.tabWidget.addTab(self.tableWidget, 'Data')

        self.statusBar().showMessage('Ready')

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('MyTravel')
        self.show()