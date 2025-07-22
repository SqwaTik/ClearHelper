from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextBrowser, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPixmap
import os

class ProgramInfoDialog(QDialog):
    def __init__(self, program_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Информация: {program_data['name']}")
        self.setFixedSize(480, 380)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        title = QLabel(program_data["name"])
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 16, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)
        icon_path = program_data["icon"]
        if icon_path and os.path.exists(icon_path):
            icon_pixmap = QIcon(icon_path).pixmap(56, 56)
        else:
            icon_pixmap = QIcon.fromTheme("application-x-executable").pixmap(56, 56)
        icon_label.setPixmap(icon_pixmap)
        layout.addWidget(icon_label)
        
        info_label = QLabel("Описание:")
        info_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(info_label)
        
        info_text = QTextBrowser()
        info_text.setPlainText(program_data["info"] or "Описание отсутствует")
        info_text.setStyleSheet("""
            background: #1e1e1e;
            color: #e0e0e0;
            border: 1px solid #444444;
            border-radius: 8px;
            padding: 12px;
        """)
        layout.addWidget(info_text, 1)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #3a3a3a;
                color: #e0e0e0;
                border: 1px solid #444444;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #4a3a3a;
            }
        """)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)