from PyQt5.QtWidgets import QFormLayout, QDialog, QRadioButton, QPushButton, QLineEdit, QHBoxLayout, QLabel


class LocationEntry(QDialog):
    def __init__(self, parent=None):
        super(LocationEntry, self).__init__(parent)

        self.setup_ui()

    def setup_ui(self):
        form = QFormLayout()

        address_label = QLabel('Address:')
        address_entry = QLineEdit()
        address_layout = QHBoxLayout()
        address_layout.addWidget(address_label)
        address_layout.addWidget(address_entry)

        city_label = QLabel('City:')
        city_entry = QLineEdit()
        city_layout = QHBoxLayout()
        city_layout.addWidget(city_label)
        city_layout.addWidget(city_entry)

        state_label = QLabel('State:')
        state_entry = QLineEdit()
        state_layout = QHBoxLayout()
        state_layout.addWidget(state_label)
        state_layout.addWidget(state_entry)

        country_label = QLabel('Country:')
        country_entry = QLineEdit()
        country_layout = QHBoxLayout()
        country_layout.addWidget(country_label)
        country_layout.addWidget(country_entry)

        c_s_c_layout = QHBoxLayout()
        c_s_c_layout.addLayout(city_layout)
        c_s_c_layout.addLayout(state_layout)
        c_s_c_layout.addLayout(country_layout)

        lived_button = QRadioButton('Lived')
        visited_button = QRadioButton('Visited')
        wish_button = QRadioButton('Wish List')
        category_layout = QHBoxLayout()
        category_layout.addWidget(lived_button)
        category_layout.addWidget(visited_button)
        category_layout.addWidget(wish_button)

        submit_button = QPushButton('Submit')

        form.addRow(address_layout)
        form.addRow(c_s_c_layout)
        form.addRow(category_layout)
        form.addRow(submit_button)

        self.setLayout(form)

        self.show()


