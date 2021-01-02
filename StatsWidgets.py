from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QRectF, QPointF, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter


class BarChart(QWidget):
    def __init__(self, bars):
        super(BarChart, self).__init__()

        layout = QVBoxLayout()

        self.bars = {}
        for bar in bars:
            self.bars[bar['name']] = BarWidget(bar['value'], bar['max'], bar['color'])
            layout.addWidget(self.bars[bar['name']])

        self.setLayout(layout)


class BarWidget(QWidget):
    length_changed = pyqtSignal(float)

    def __init__(self, name='', current=0.0, maximum=100.0, color=QColor()):
        super(BarWidget, self).__init__()

        self._value = current
        self._max_length = maximum
        self.color = color
        self.bar = Bar()
        self.name_label = QLabel(name)

        layout = QHBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.bar)
        self.setLayout(layout)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val):
        self._value = min(new_val, self.max_length)
        self.length_changed.emit(self.value)

    @property
    def max_length(self):
        return self._max_length

    @max_length.setter
    def max_length(self, new_max):
        self._max_length = new_max


class Bar(QWidget):
    def __init__(self, foreground=QColor(), background=QColor()):
        super(Bar, self).__init__()

        self.fg_color = foreground
        self.bg_color = background

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin()

        painter.end()
