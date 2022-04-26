from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QRectF, QPointF, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter


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
        background = QColor('darkGrey')
        self.name_label = QLabel(name)
        self.bar = Bar(color, background)
        self.value_label = QLabel()

        layout = QHBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.bar)
        layout.addWidget(self.value_label)
        self.setLayout(layout)

        self.length_changed.connect(self.bar.percent)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val):
        self._value = min(new_val, self.max_length)
        percent = self._value / self.max_length
        self.length_changed.emit(percent)

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
        self._percent = 0.0

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, p=0.5):
        if (p >= 0.0) and (p <= 1.0):
            self._percent = p
            self.update()

    def paintEvent(self, event):
        bg_rect = self.rect()
        bg_width = bg_rect.width()
        fg_width = bg_width * self.percent
        fg_rect = bg_rect.setWidth(fg_width)

        painter = QPainter()
        painter.begin()
        painter.setBrush(self.bg_color)
        painter.drawRect(bg_rect)
        painter.setBrush(self.fg_color)
        painter.drawRect(fg_rect)
        painter.end()
