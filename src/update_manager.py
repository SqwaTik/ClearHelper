from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton
from PySide6.QtCore import QThread, Signal, QTimer
import requests

class UpdateChecker(QThread):
    update_found = Signal(str, str)
    no_update = Signal()
    error = Signal(str)

    def __init__(self, current_version):
        super().__init__()
        self.current_version = current_version

    def run(self):
        try:
            response = requests.get(
                "https://api.github.com/repos/SqwaTik/ClearHelper/releases/latest",
                timeout=10
            )
            
            if response.status_code != 200:
                self.error.emit(f"Ошибка сервера: {response.status_code}")
                return
                
            release_data = response.json()
            latest_version = release_data['tag_name'].lstrip('v')

            if self.compare_versions(latest_version, self.current_version) > 0:
                for asset in release_data['assets']:
                    if asset['name'].endswith('.zip'):
                        download_url = asset['browser_download_url']
                        self.update_found.emit(latest_version, download_url)
                        return
                self.error.emit("Архив не найден в релизе")
            else:
                self.no_update.emit()
                
        except Exception as e:
            self.error.emit(f"Ошибка: {str(e)}")

    def compare_versions(self, v1, v2):
        """Сравнивает версии в формате X.Y.Z"""
        v1_parts = list(map(int, v1.split('.')))
        v2_parts = list(map(int, v2.split('.')))
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_val = v1_parts[i] if i < len(v1_parts) else 0
            v2_val = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1_val > v2_val:
                return 1
            elif v1_val < v2_val:
                return -1
        return 0

class UpdateDialog(QDialog):
    def __init__(self, current_version, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Обновление Clear Helper")
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.status_label = QLabel("Проверка обновлений...")
        layout.addWidget(self.status_label)
        
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        self.checker = UpdateChecker(current_version)
        self.checker.update_found.connect(self.on_update_found)
        self.checker.no_update.connect(self.on_no_update)
        self.checker.error.connect(self.on_error)
        self.checker.start()
        
        # Автоматическое закрытие через 3 секунды, если нет обновлений
        QTimer.singleShot(3000, self.accept_if_no_update)
    
    def accept_if_no_update(self):
        if not self.checker.isRunning():
            self.accept()
    
    def on_update_found(self, version, url):
        self.status_label.setText(f"Доступна новая версия: {version}")
        self.accept()
    
    def on_no_update(self):
        self.status_label.setText("У вас установлена последняя версия")
        self.accept()
    
    def on_error(self, error):
        self.status_label.setText(f"Ошибка: {error}")
        self.accept()