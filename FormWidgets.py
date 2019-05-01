from PyQt5.QtWidgets import QFormLayout, QDialog, QRadioButton, QPushButton, QLineEdit, QHBoxLayout, QLabel, \
                            QButtonGroup
#from PyQt5.QtCore import Qt
from pandas import DataFrame as df


class LocationEntry(QDialog):
    def __init__(self, parent=None):
        super(LocationEntry, self).__init__(parent)

        self.setup_ui()

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
        self.wish_button = QRadioButton('Wish List')
        #category_group = QButtonGroup()
        #category_group.addButton(self.lived_button)
        #category_group.addButton(self.visited_button)
        #category_group.addButton(self.wish_button)

        self.favorite_button = QRadioButton('Favorite')
        self.favorite_button.setAutoExclusive(False)
        #other_group = QButtonGroup()
        #other_group.addButton(self.favorite_button)

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

    def submit_entry(self):
        #self.emit(accepted())
        data = {'Address':   self.state_entry.Text(),
                'City':      self.city_entry.Text(),
                'State':     self.state_entry.Text(),
                'Country':   self.country_entry.Text(),
                'Lived':     self.lived_button.isChecked(),
                'Visited':   self.visited_button.isChecked(),
                'Wish':      self.wish_button.isChecked(),
                'Favorite':  self.favorite_button.isChecked()}

