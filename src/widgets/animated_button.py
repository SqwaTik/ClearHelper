from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)
        
        self._default_size = QSize(150, 85)
        self._hover_size = QSize(155, 90)
        self._glow_enabled = True
        
        self.setMinimumSize(self._default_size)
        self.setMaximumSize(self._hover_size)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Внутренний layout для иконки и текста
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)
        
        # Label для иконки
        self.icon_label = QLabel(self)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.icon_label)
        
        # Label для текста
        self.text_label = QLabel(text, self)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #e0e0e0;")
        self.layout.addWidget(self.text_label)
        
        # Анимации
        self.icon_anim = QPropertyAnimation(self, b"iconSize")
        self.icon_anim.setDuration(300)
        self.icon_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self.size_anim = QPropertyAnimation(self, b"minimumSize")
        self.size_anim.setDuration(300)
        self.size_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self.setStyleSheet("""
            QPushButton {
                background: #1e1e1e;
                border-radius: 8px;
                border: 1px solid #3a3a3a;
            }
            QPushButton:hover {
                background: #2a2a2a;
            }
            QPushButton:pressed {
                background: #151515;
            }
        """)
    
    def setCustomIcon(self, pixmap):
        self.icon_label.setPixmap(pixmap)
    
    def enterEvent(self, event):
        self.icon_anim.stop()
        self.icon_anim.setStartValue(self.iconSize())
        self.icon_anim.setEndValue(QSize(54, 54))
        self.icon_anim.start()
        
        self.size_anim.stop()
        self.size_anim.setStartValue(self.minimumSize())
        self.size_anim.setEndValue(self._hover_size)
        self.size_anim.start()
    
    def leaveEvent(self, event):
        self.icon_anim.stop()
        self.icon_anim.setStartValue(self.iconSize())
        self.icon_anim.setEndValue(QSize(48, 48))
        self.icon_anim.start()
        
        self.size_anim.stop()
        self.size_anim.setStartValue(self.minimumSize())
        self.size_anim.setEndValue(self._default_size)
        self.size_anim.start()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        
        if self._glow_enabled and self.underMouse():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            center = self.rect().center()
            radius = min(self.width(), self.height()) * 0.6
            gradient = QRadialGradient(center, radius)
            glow_color = QColor(90, 135, 230, 120)
            if self.property("light_theme") == "true":
                glow_color = QColor(100, 150, 255, 150)
            gradient.setColorAt(0.0, glow_color)
            gradient.setColorAt(1.0, QColor(0, 0, 0, 0))
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect(), 8, 8)