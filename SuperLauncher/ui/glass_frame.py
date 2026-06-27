from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QRectF

class GlassFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._tint = QColor(25, 25, 35, 220)
        self._border_color = QColor(255, 255, 255, 25)
        self._radius = 16

    def set_tint(self, r, g, b, a=220):
        self._tint = QColor(r, g, b, a)
        self.update()

    def paintEvent(self, event):
        rect = self.rect()
        if rect.width() < 4 or rect.height() < 4:
            return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(rect).adjusted(2, 2, -2, -2)
        p.setBrush(QBrush(self._tint))
        p.setPen(QPen(self._border_color, 1))
        p.drawRoundedRect(r, self._radius, self._radius)
