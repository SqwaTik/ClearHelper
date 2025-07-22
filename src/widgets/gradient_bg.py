from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QLinearGradient, QColor
from PySide6.QtCore import Qt, QPoint

class GradientBackground(QWidget):
    def __init__(self, colors=None, parent=None):
        super().__init__(parent)
        self.colors = colors or [
            QColor(25, 25, 40),
            QColor(30, 30, 50),
            QColor(20, 20, 35)
        ]
    
    def set_gradient(self, colors):
        self.colors = colors
        self.update()
    
    def paintEvent(self, event):
        if not self.colors or len(self.colors) == 0:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))
        
        step = 1.0 / (len(self.colors) - 1) if len(self.colors) > 1 else 1.0
        for i, color in enumerate(self.colors):
            gradient.setColorAt(i * step, color)
        
        painter.fillRect(self.rect(), gradient)