from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextBrowser, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
import os

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")
        self.setFixedSize(480, 380)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        title = QLabel("Clear Helper")
        title.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 18, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        version = QLabel("Версия 1.0.0")
        version.setAlignment(Qt.AlignCenter)
        version.setFont(QFont("Arial", 12))
        layout.addWidget(version)
        
        icon = QLabel()
        icon.setAlignment(Qt.AlignCenter)
        icon_path = os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "app_icon.ico")
        if os.path.exists(icon_path):
            icon.setPixmap(QIcon(icon_path).pixmap(56, 56))
        else:
            icon.setPixmap(QIcon.fromTheme("application-x-executable").pixmap(56, 56))
        layout.addWidget(icon)
        
        info = QTextBrowser()
        info.setHtml("""
            <p>Удобный лаунчер для системных утилит</p>
            <p><b>Основные возможности:</b></p>
            <ul>
                <li>Запуск программ с правами администратора</li>
                <li>Контекстное меню для каждой программы</li>
                <li>Подробная информация и справка</li>
                <li>Смена тем оформления</li>
                <li>Настраиваемые градиенты фона</li>
                <li>Работа из системного трея</li>
                <li>Горячие клавиши для управления</li>
            </ul>
            <p>© 2025 Clear Helper Team. Все права защищены.</p>
        """)
        info.setStyleSheet("""
            background: #1e1e1e;
            color: #e0e0e0;
            border-radius: 8px;
            border: 1px solid #444444;
            padding: 12px;
        """)
        layout.addWidget(info, 1)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #3a3a3a;
                color: #e0e0e0;
                border: 1px solid #444444;
                border-radius: 6px;
                padding: 8px 18px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #4a3a3a;
            }
        """)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)