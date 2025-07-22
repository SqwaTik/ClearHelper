from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class GradientButton(QPushButton):
    def __init__(self, colors, parent=None):
        super().__init__(parent)
        self.colors = colors
        self.setFixedSize(80, 80)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw gradient background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        step = 1.0 / (len(self.colors) - 1) if len(self.colors) > 1 else 1.0
        for i, color in enumerate(self.colors):
            gradient.setColorAt(i * step, color)
        
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 8, 8)
        
        # Draw border if selected
        if self.isChecked():
            painter.setPen(QColor(100, 180, 255))
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки Clear Helper")
        self.setMinimumSize(700, 500)
        
        self.selected_gradient = None
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                padding: 8px 15px;
            }
        """)
        
        # Theme tab
        theme_tab = QWidget()
        theme_layout = QVBoxLayout(theme_tab)
        
        # Gradient selection
        gradients_group = QGroupBox("Градиенты фона")
        gradients_layout = QGridLayout()
        
        # Predefined gradients
        self.gradients = [
            [QColor(25, 25, 40), QColor(30, 30, 50), QColor(20, 20, 35)],  # Deep Blue
            [QColor(50, 15, 35), QColor(70, 20, 45), QColor(40, 10, 25)],  # Dark Purple
            [QColor(15, 35, 25), QColor(20, 45, 30), QColor(10, 25, 15)],  # Forest Green
            [QColor(40, 20, 15), QColor(50, 25, 20), QColor(30, 15, 10)],  # Earth Brown
            [QColor(20, 20, 30), QColor(30, 30, 45), QColor(15, 15, 25)],  # Midnight Blue
            [QColor(35, 15, 25), QColor(45, 20, 35), QColor(25, 10, 20)],  # Berry Red
            [QColor(15, 30, 35), QColor(20, 40, 45), QColor(10, 25, 30)],  # Ocean Teal
            [QColor(30, 20, 35), QColor(40, 25, 45), QColor(25, 15, 30)],  # Royal Purple
            [QColor(35, 25, 15), QColor(45, 35, 20), QColor(25, 15, 10)],  # Amber Gold
            [QColor(20, 30, 40), QColor(25, 40, 50), QColor(15, 20, 30)]   # Steel Blue
        ]
        
        self.gradient_buttons = []
        row, col = 0, 0
        max_cols = 5
        
        for i, gradient in enumerate(self.gradients):
            btn = GradientButton(gradient)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=i: self.select_gradient(idx))
            gradients_layout.addWidget(btn, row, col)
            self.gradient_buttons.append(btn)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        gradients_group.setLayout(gradients_layout)
        theme_layout.addWidget(gradients_group)
        
        # Hotkeys tab
        hotkeys_tab = QWidget()
        hotkeys_layout = QVBoxLayout(hotkeys_tab)
        
        hotkeys_group = QGroupBox("Горячие клавиши")
        hotkeys_list = QListWidget()
        hotkeys_list.setSelectionMode(QAbstractItemView.NoSelection)
        
        hotkeys = [
            ("Смена темы", "Ctrl+T"),
            ("Открыть справку", "F1"),
            ("Информация о программе", "Ctrl+I"),
            ("Открыть настройки", "Ctrl+S"),
            ("Выход", "Ctrl+Q")
        ]
        
        for name, key in hotkeys:
            item = QListWidgetItem(f"{name}: {key}")
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            hotkeys_list.addItem(item)
        
        hotkeys_group_layout = QVBoxLayout()
        hotkeys_group_layout.addWidget(hotkeys_list)
        hotkeys_group.setLayout(hotkeys_group_layout)
        hotkeys_layout.addWidget(hotkeys_group)
        
        # Add tabs
        self.tabs.addTab(theme_tab, "Темы")
        self.tabs.addTab(hotkeys_tab, "Горячие клавиши")
        
        main_layout.addWidget(self.tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setMinimumWidth(100)
        self.ok_btn.clicked.connect(self.accept)
        
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setMinimumWidth(100)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.ok_btn)
        
        main_layout.addLayout(button_layout)
        
        # Apply styles
        self.apply_styles()
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background: #2a2a2a;
                color: #e0e0e0;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #444444;
                border-radius: 8px;
                margin-top: 20px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                left: 10px;
            }
            QListWidget {
                background: #1e1e1e;
                border: 1px solid #444444;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton {
                background: #3a3a3a;
                color: #e0e0e0;
                border: 1px solid #444444;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #4a3a3a;
            }
            QPushButton:pressed {
                background: #151515;
            }
        """)
    
    def select_gradient(self, idx):
        # Deselect all other buttons
        for i, btn in enumerate(self.gradient_buttons):
            btn.setChecked(i == idx)
        
        self.selected_gradient = self.gradients[idx]
    
    def get_selected_gradient(self):
        return self.selected_gradient