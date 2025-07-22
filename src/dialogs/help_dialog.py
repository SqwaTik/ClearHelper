from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import os
import re

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scale = 1.0
        self._max_scale = 3.0
        self._min_scale = 0.5
        self._base_pixmap = None
        
    def setPixmap(self, pixmap):
        self._base_pixmap = pixmap
        self._update_pixmap()
        
    def _update_pixmap(self):
        if self._base_pixmap:
            scaled = self._base_pixmap.scaled(
                self._base_pixmap.width() * self._scale,
                self._base_pixmap.height() * self._scale,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            super().setPixmap(scaled)
    
    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self._scale = min(self._scale * 1.1, self._max_scale)
            else:
                self._scale = max(self._scale * 0.9, self._min_scale)
            self._update_pixmap()
            event.accept()
        else:
            super().wheelEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._scale = 1.0
            self._update_pixmap()
            event.accept()
        else:
            super().mousePressEvent(event)

class HelpDialog(QDialog):
    def __init__(self, program_data, parent=None):
        super().__init__(parent)
        self.program_data = program_data
        self.image_labels = []
        
        if program_data:
            self.setWindowTitle(f"Помощь: {program_data['name']}")
        else:
            self.setWindowTitle("Справка по Clear Helper")
            
        self.setFixedSize(700, 600)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # Добавляем верхнюю панель с заголовком и датой
        header_layout = QHBoxLayout()
        
        if program_data:
            title = QLabel(f"Помощь по {program_data['name']}")
        else:
            title = QLabel("Справка по Clear Helper")
        
        title_font = QFont("Arial", 16, QFont.Bold)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        # Добавляем дату в правый верхний угол
        date_text = "Обновлено: 18.07.2025"
        if program_data:
            # Пытаемся извлечь дату из текста справки
            match = re.search(r'Обновлено: (\d{2}\.\d{2}\.\d{4})', program_data["help"])
            if match:
                date_text = f"Обновлено: {match.group(1)}"
        
        date_label = QLabel(date_text)
        date_label.setFont(QFont("Arial", 10))
        date_label.setStyleSheet("color: #aaaaaa;")
        header_layout.addStretch()
        header_layout.addWidget(date_label)
        
        layout.addLayout(header_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background: transparent;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #5B86E5;
                min-height: 16px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(15)
        
        if program_data:
            content = program_data["help"] or "Информация о помощи отсутствует"
        else:
            content = """
            <h3>Использование лаунчера</h3>
            <p><b>Запуск программ:</b> Щелкните по иконке программы для запуска</p>
            <p><b>Дополнительные опции:</b> Правый клик по иконке программы открывает контекстное меню</p>
            
            <h3>Горячие клавиши</h3>
            <ul>
                <li><b>Ctrl+T:</b> Сменить тему оформления</li>
                <li><b>F1:</b> Открыть справку</li>
                <li><b>Ctrl+I:</b> Открыть информацию о программе</li>
                <li><b>Ctrl+Q:</b> Выйти из приложения</li>
                <li><b>Ctrl+S:</b> Открыть настройки</li>
            </ul>
            
            <h3>Системный трей</h3>
            <p>При закрытии приложение сворачивается в системный трей. Для восстановления окна дважды кликните по иконке в трее.</p>
            """
        
        help_text = QTextBrowser()
        help_text.setHtml(content)
        help_text.setOpenExternalLinks(True)
        help_text.setStyleSheet("""
            background: #1e1e1e;
            color: #e0e0e0;
            border-radius: 8px;
            border: 1px solid #444444;
            padding: 12px;
        """)
        container_layout.addWidget(help_text)
        
        if program_data and program_data["name"] == "RegScanner":
            images_dir = os.path.join(os.path.dirname(__file__), "..", "resources", "images", "regscanner")
            if os.path.exists(images_dir):
                for img_file in os.listdir(images_dir):
                    if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        img_path = os.path.join(images_dir, img_file)
                        
                        caption = QLabel(img_file.split('.')[0].replace('_', ' ').title())
                        caption.setStyleSheet("font-size: 12px; font-weight: bold; color: #e0e0e0;")
                        caption.setAlignment(Qt.AlignCenter)
                        container_layout.addWidget(caption)
                        
                        img_label = ImageLabel()
                        img_label.setAlignment(Qt.AlignCenter)
                        pixmap = QPixmap(img_path)
                        img_label.setPixmap(pixmap)
                        img_label.setStyleSheet("background: #2a2a2a; border-radius: 8px; padding: 5px;")
                        img_label.setToolTip("Ctrl+колесико мыши для масштабирования\nЛКМ для сброса масштаба")
                        container_layout.addWidget(img_label)
                        self.image_labels.append(img_label)
        
        scroll_area.setWidget(container)
        layout.addWidget(scroll_area, 1)
        
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