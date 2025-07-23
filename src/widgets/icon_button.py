from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class IconButton(QPushButton):
    def __init__(self, icon_path=None, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)
        
        self._icon_size = QSize(24, 24)
        self._default_size = QSize(36, 36)
        self._hover_size = QSize(40, 40)
        self._glow_enabled = True
        
        if icon_path:
            self.setIcon(QIcon(icon_path))
        
        self.setIconSize(self._icon_size)
        self.setFixedSize(self._default_size)
        
        # Animation for icon size
        self.icon_anim = QPropertyAnimation(self, b"iconSize")
        self.icon_anim.setDuration(300)
        self.icon_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        # Animation for button size
        self.size_anim = QPropertyAnimation(self, b"size")
        self.size_anim.setDuration(300)
        self.size_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        self.setStyleSheet("""
            QPushButton {
                background: #2a2a2a;
                border-radius: 18px;
                border: 1px solid #444444;
            }
            QPushButton:hover {
                background: #3a3a3a;
            }
        """)
    
    def enterEvent(self, event):
        self.icon_anim.stop()
        self.icon_anim.setStartValue(self.iconSize())
        self.icon_anim.setEndValue(QSize(28, 28))
        self.icon_anim.start()
        
        self.size_anim.stop()
        self.size_anim.setStartValue(self.size())
        self.size_anim.setEndValue(self._hover_size)
        self.size_anim.start()
    
    def leaveEvent(self, event):
        self.icon_anim.stop()
        self.icon_anim.setStartValue(self.iconSize())
        self.icon_anim.setEndValue(self._icon_size)
        self.icon_anim.start()
        
        self.size_anim.stop()
        self.size_anim.setStartValue(self.size())
        self.size_anim.setEndValue(self._default_size)
        self.size_anim.start()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        
        # Draw glow effect
        if self._glow_enabled and self.underMouse():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Create radial gradient for glow
            center = self.rect().center()
            radius = min(self.width(), self.height()) * 0.6
            gradient = QRadialGradient(center, radius)
            
            # Theme-based glow color
            glow_color = QColor(90, 135, 230, 120)  # Blue for dark theme
            if self.property("light_theme") == "true":
                glow_color = QColor(100, 150, 255, 150)  # Brighter blue for light theme
            
            gradient.setColorAt(0.0, glow_color)
            gradient.setColorAt(1.0, QColor(0, 0, 0, 0))
            
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect(), 18, 18)