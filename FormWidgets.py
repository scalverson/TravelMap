from PyQt5.QtWidgets import QFormLayout, QDialog, QRadioButton, QPushButton, QLineEdit, QHBoxLayout, QLabel # , QButtonGroup
from PyQt5.QtCore import pyqtSignal
# from pandas import DataFrame as df


class LocationEntry(QDialog):
    submitted = pyqtSignal(dict)

    def __init__(self, data=None):
        super(LocationEntry, self).__init__() # parent)

        self.setWindowTitle('Add/Edit Location')

        self.setup_ui()

        if data:
            if 'Address' in data.keys():
                self.address_entry.setText(data['Address'])
            if 'City' in data.keys():
                self.city_entry.setText(data['City'])
            if 'State' in data.keys():
                self.state_entry.setText(data['State'])
            if 'Country' in data.keys():
                self.country_entry.setText(data['Country'])

            if 'Lived' in data.keys():
                self.lived_button.setChecked(data['Lived'])
            if 'Visited' in data.keys():
                self.visited_button.setChecked(data['Visited'])
            if 'Wish' in data.keys():
                self.wish_button.setChecked(data['Wish'])

            if 'Favorite' in data.keys():
                self.favorite_button.setChecked(data['Favorite'])

    def setup_ui(self):
        form = QFormLayout()

        address_label = QLabel('Address:')
        self.address_entry = QLineEdit()
        address_layout = QHBoxLayout()
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_entry)

        city_label = QLabel('City:')
        self.city_entry = QLineEdit()
        city_layout = QHBoxLayout()
        city_layout.addWidget(city_label)
        city_layout.addWidget(self.city_entry)

        state_label = QLabel('State:')
        self.state_entry = QLineEdit()
        state_layout = QHBoxLayout()
        state_layout.addWidget(state_label)
        state_layout.addWidget(self.state_entry)

        country_label = QLabel('Country:')
        self.country_entry = QLineEdit()
        country_layout = QHBoxLayout()
        country_layout.addWidget(country_label)
        country_layout.addWidget(self.country_entry)

        c_s_c_layout = QHBoxLayout()
        c_s_c_layout.addLayout(city_layout)
        c_s_c_layout.addLayout(state_layout)
        c_s_c_layout.addLayout(country_layout)

        self.lived_button = QRadioButton('Lived')
        self.visited_button = QRadioButton('Visited')
        self.visited_button.toggled.connect(self.on_visited_selection)
        self.wish_button = QRadioButton('Wish List')
        # category_group = QButtonGroup()
        # category_group.addButton(self.lived_button)
        # category_group.addButton(self.visited_button)
        # category_group.addButton(self.wish_button)

        self.favorite_button = QRadioButton('Favorite')
        self.favorite_button.setAutoExclusive(False)
        self.favorite_button.setEnabled(False)
        # other_group = QButtonGroup()
        # other_group.addButton(self.favorite_button)

        category_layout = QHBoxLayout()
        category_layout.addWidget(self.lived_button)
        category_layout.addWidget(self.visited_button)
        category_layout.addWidget(self.wish_button)
        category_layout.addWidget(self.favorite_button)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.submit_entry)

        form.addRow(address_layout)
        form.addRow(c_s_c_layout)
        form.addRow(category_layout)
        form.addRow(submit_button)

        self.setLayout(form)

        self.show()

    def on_visited_selection(self):
        if self.visited_button.isChecked():
            self.favorite_button.setEnabled(True)
        else:
            self.favorite_button.setEnabled(False)
            self.favorite_button.setChecked(False)

    def submit_entry(self):
        data = {'Address':   str(self.address_entry.text()),
                'City':      str(self.city_entry.text()),
                'State':     str(self.state_entry.text()),
                'Country':   str(self.country_entry.text()),
                'Lived':     self.lived_button.isChecked(),
                'Visited':   self.visited_button.isChecked(),
                'Wish':      self.wish_button.isChecked(),
                'Favorite':  self.favorite_button.isChecked()}
        self.submitted.emit(data)
        self.accepted.emit()
        self.close()

