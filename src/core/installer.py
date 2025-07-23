# src/core/installer.py
import os
import sys
import json
import shutil
import ctypes
import subprocess
import traceback
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog, 
                             QMessageBox, QProgressBar, QFrame, QSizePolicy)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QLinearGradient, QColor, QFont, QBrush
from PySide6.QtCore import Qt, QThread, Signal, QSettings, QPoint, QRect

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
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QLinearGradient(0, 0, 0, self.height())
        
        step = 1.0 / (len(self.colors) - 1) if len(self.colors) > 1 else 1.0
        for i, color in enumerate(self.colors):
            gradient.setColorAt(i * step, color)
        
        painter.fillRect(event.rect(), gradient)

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    return os.path.join(base_path, relative_path)

def is_installed():
    return os.path.exists(os.path.join(os.getcwd(), "install_config.json"))

def get_default_install_path():
    """Получает путь установки по умолчанию с запоминанием последнего выбора"""
    settings = QSettings("ClearHelper", "Installer")
    last_path = settings.value("last_install_path", "")
    
    if last_path and os.path.exists(last_path):
        return last_path
    
    return str(Path("C:/ClearHelper"))

def run_installer_gui():
    app = QApplication(sys.argv)
    window = InstallerWindow()
    window.show()
    sys.exit(app.exec())

class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Установка Clear Helper")
        self.setFixedSize(700, 600)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.old_pos = None
        
        # Центральный виджет с градиентом
        self.central_widget = GradientBackground()
        self.setCentralWidget(self.central_widget)
        
        # Основной лейаут
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(40, 40, 40, 30)
        main_layout.setSpacing(20)
        
        # Заголовок с кнопкой закрытия
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Установка Clear Helper")
        title_font = QFont("Arial", 20, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #e0e0e0;")
        header_layout.addWidget(title)
        
        # Кнопка закрытия
        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: #3a3a3a;
                color: #e0e0e0;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #ff5555;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        header_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(header_layout)
        
        # Иконка
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)
        icon_path = get_resource_path("resources/icons/app_icon.ico")
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
        else:
            icon_label.setText("Clear Helper")
            icon_label.setStyleSheet("font-size: 24px; color: #e0e0e0;")
        
        main_layout.addWidget(icon_label)
        
        # Контейнер для настроек
        settings_frame = QFrame()
        settings_frame.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 45, 180);
                border-radius: 15px;
                border: 1px solid #444466;
            }
        """)
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setContentsMargins(25, 25, 25, 25)
        settings_layout.setSpacing(20)
        
        # Поле для пути установки
        path_layout = QHBoxLayout()
        path_label = QLabel("Путь установки:")
        path_label.setStyleSheet("font-size: 14px; color: #e0e0e0;")
        self.path_edit = QLineEdit(get_default_install_path())
        self.path_edit.setStyleSheet("""
            QLineEdit {
                background: #2a2a3a;
                color: #e0e0e0;
                border: 1px solid #555577;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
        """)
        path_button = QPushButton("Обзор...")
        path_button.setStyleSheet("""
            QPushButton {
                background: #4a86e8;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #3a76d8;
            }
        """)
        path_button.clicked.connect(self.select_install_path)
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_edit, 1)
        path_layout.addWidget(path_button)
        settings_layout.addLayout(path_layout)
        
        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background: #555577;")
        settings_layout.addWidget(separator)
        
        # Опции
        options_layout = QVBoxLayout()
        options_layout.setSpacing(15)
        
        self.desktop_shortcut = self.create_option_checkbox("Создать ярлык на рабочем столе")
        self.start_menu_shortcut = self.create_option_checkbox("Добавить в меню Пуск")
        self.autostart = self.create_option_checkbox("Запускать при входе в систему")
        self.taskbar_pin = self.create_option_checkbox("Закрепить на панели задач")
        self.launch_after = self.create_option_checkbox("Запустить Clear Helper после установки")
        
        options_layout.addWidget(self.desktop_shortcut)
        options_layout.addWidget(self.start_menu_shortcut)
        options_layout.addWidget(self.autostart)
        options_layout.addWidget(self.taskbar_pin)
        options_layout.addWidget(self.launch_after)
        settings_layout.addLayout(options_layout)
        
        main_layout.addWidget(settings_frame)
        
        # Прогресс бар
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                background: #2a2a3a;
                border: 1px solid #555577;
                border-radius: 8px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background: #4a86e8;
                border-radius: 8px;
            }
        """)
        self.progress.setVisible(False)
        self.progress.setFixedHeight(0)  # Начальная высота 0
        main_layout.addWidget(self.progress)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background: #5a5a7a;
                color: #e0e0e0;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #6a6a8a;
            }
        """)
        self.cancel_button.clicked.connect(self.close)
        
        self.install_button = QPushButton("Установить")
        self.install_button.setStyleSheet("""
            QPushButton {
                background: #4a86e8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #3a76d8;
            }
            QPushButton:pressed {
                background: #2a66c8;
            }
        """)
        self.install_button.clicked.connect(self.start_installation)
        
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.install_button)
        main_layout.addLayout(buttons_layout)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None
    
    def create_option_checkbox(self, text):
        checkbox = QCheckBox(text)
        checkbox.setStyleSheet("""
            QCheckBox {
                color: #e0e0e0;
                font-size: 14px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 5px;
                border: 2px solid #555577;
                background: #2a2a3a;
            }
            QCheckBox::indicator:checked {
                background: #4a86e8;
                image: url(none);
            }
        """)
        checkbox.setChecked(True)
        return checkbox
    
    def select_install_path(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для установки",
            get_default_install_path()
        )
        if path:
            self.path_edit.setText(path)
    
    def start_installation(self):
        install_path = self.path_edit.text()
        if not install_path:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите путь установки")
            return
        
        # Сохраняем выбранный путь
        settings = QSettings("ClearHelper", "Installer")
        settings.setValue("last_install_path", install_path)
        
        # Создаем поток установки
        self.install_thread = InstallThread(
            install_path,
            self.desktop_shortcut.isChecked(),
            self.start_menu_shortcut.isChecked(),
            self.autostart.isChecked(),
            self.taskbar_pin.isChecked(),
            self.launch_after.isChecked()
        )
        
        # Подключаем сигналы
        self.install_thread.progress_changed.connect(self.update_progress)
        self.install_thread.finished.connect(self.installation_finished)
        self.install_thread.error_occurred.connect(self.show_error)
        
        # Показываем прогресс
        self.progress.setFixedHeight(20)  # Восстанавливаем высоту
        self.progress.setVisible(True)
        self.install_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        
        # Запускаем установку
        self.install_thread.start()
    
    def update_progress(self, value):
        self.progress.setValue(value)
    
    def installation_finished(self):
        self.progress.setVisible(False)
        self.progress.setFixedHeight(0)  # Сбрасываем высоту
        
        QMessageBox.information(
            self,
            "Установка завершена",
            "Clear Helper успешно установлен!"
        )
        
        self.close()
    
    def show_error(self, message):
        self.progress.setVisible(False)
        self.progress.setFixedHeight(0)  # Сбрасываем высоту
        self.install_button.setEnabled(True)
        self.cancel_button.setEnabled(True)
        QMessageBox.critical(self, "Ошибка установки", message)

class InstallThread(QThread):
    progress_changed = Signal(int)
    finished = Signal()
    error_occurred = Signal(str)
    
    def __init__(self, install_path, create_desktop_shortcut, create_start_menu_shortcut, 
                 enable_autostart, pin_to_taskbar, launch_after):
        super().__init__()
        self.install_path = install_path
        self.create_desktop_shortcut = create_desktop_shortcut
        self.create_start_menu_shortcut = create_start_menu_shortcut
        self.enable_autostart = enable_autostart
        self.pin_to_taskbar = pin_to_taskbar
        self.launch_after = launch_after
    
    def run(self):
        try:
            # Создаем папку для установки
            os.makedirs(self.install_path, exist_ok=True)
            
            # Определяем путь к исходным файлам
            if getattr(sys, 'frozen', False):
                source_dir = os.path.dirname(sys.executable)
            else:
                source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
            
            # Критически важные папки для копирования
            critical_folders = ["programs", "resources", "config"]
            
            # Подсчет общего количества файлов
            total_files = 0
            for folder in critical_folders:
                src_folder = os.path.join(source_dir, folder)
                if os.path.exists(src_folder):
                    for root, dirs, files in os.walk(src_folder):
                        total_files += len(files)
            
            # Добавляем основные файлы
            main_files = ["ClearHelper.exe", "version.txt"]
            for file in main_files:
                if os.path.exists(os.path.join(source_dir, file)):
                    total_files += 1
            
            if total_files == 0:
                self.error_occurred.emit("Не найдены файлы для установки")
                return
            
            copied_files = 0
            
            # Копируем основные папки
            for folder in critical_folders:
                src = os.path.join(source_dir, folder)
                dst = os.path.join(self.install_path, folder)
                
                if os.path.exists(src):
                    # Удаляем целевую папку, если она существует
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    
                    # Копируем папку
                    shutil.copytree(src, dst)
                    
                    # Обновляем прогресс
                    for root, dirs, files in os.walk(src):
                        copied_files += len(files)
                        progress = int((copied_files / total_files) * 100)
                        self.progress_changed.emit(progress)
                else:
                    self.error_occurred.emit(f"Критическая папка не найдена: {folder}")
                    return
            
            # Копируем основные файлы
            for file in main_files:
                src = os.path.join(source_dir, file)
                dst = os.path.join(self.install_path, file)
                
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    copied_files += 1
                    progress = int((copied_files / total_files) * 100)
                    self.progress_changed.emit(progress)
            
            # Создаем ярлыки
            app_exe = os.path.join(self.install_path, "ClearHelper.exe")
            
            if self.create_desktop_shortcut:
                self.create_shortcut(
                    app_exe,
                    os.path.join(os.path.expanduser("~"), "Desktop", "Clear Helper.lnk"),
                    "Clear Helper"
                )
            
            if self.create_start_menu_shortcut:
                start_menu_path = os.path.join(
                    os.getenv("APPDATA"),
                    "Microsoft", "Windows", "Start Menu", "Programs",
                    "Clear Helper.lnk"
                )
                self.create_shortcut(
                    app_exe,
                    start_menu_path,
                    "Clear Helper"
                )
            
            # Автозапуск
            if self.enable_autostart:
                autostart_path = os.path.join(
                    os.getenv("APPDATA"),
                    "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
                    "Clear Helper.lnk"
                )
                self.create_shortcut(
                    app_exe,
                    autostart_path,
                    "Clear Helper"
                )
            
            # Закрепление на панели задач
            if self.pin_to_taskbar:
                self.pin_to_taskbar_fn(app_exe)
            
            # Создаем конфиг для приложения
            config = {
                "installed": True,
                "install_path": self.install_path
            }
            with open(os.path.join(self.install_path, "install_config.json"), "w") as f:
                json.dump(config, f)
            
            # Запуск после установки
            if self.launch_after:
                self.launch_application(app_exe)
            
            self.progress_changed.emit(100)
            self.finished.emit()
            
        except Exception as e:
            error_msg = f"Ошибка установки: {str(e)}\n\n{traceback.format_exc()}"
            self.error_occurred.emit(error_msg)
    
    def create_shortcut(self, target, shortcut_path, description):
        try:
            # Создаем папки для ярлыка
            os.makedirs(os.path.dirname(shortcut_path), exist_ok=True)
            
            from win32com.client import Dispatch
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.IconLocation = target
            shortcut.Description = description
            shortcut.save()
        except ImportError:
            # Создаем .bat файл как fallback
            with open(shortcut_path.replace(".lnk", ".bat"), "w") as f:
                f.write(f'@"{target}"')
        except Exception as e:
            print(f"Ошибка создания ярлыка: {str(e)}")
    
    def pin_to_taskbar_fn(self, app_path):
        """Закрепление приложения на панели задач"""
        try:
            # Создаем временный ярлык
            temp_dir = os.path.join(os.getenv("APPDATA"), "Microsoft", "Internet Explorer", "Quick Launch", "User Pinned", "TaskBar")
            os.makedirs(temp_dir, exist_ok=True)
            temp_shortcut = os.path.join(temp_dir, "ClearHelper.lnk")
            
            # Создаем ярлык
            self.create_shortcut(app_path, temp_shortcut, "Clear Helper")
            
            # Закрепляем с помощью PowerShell
            powershell_cmd = f'''
            $shell = New-Object -ComObject Shell.Application
            $folder = $shell.Namespace('{temp_dir}')
            $item = $folder.ParseName('ClearHelper.lnk')
            $verb = $item.Verbs() | Where-Object {{$_.Name -match 'Закрепить на панели задач'}}
            if ($verb) {{ $verb.DoIt() }}
            Start-Sleep -Seconds 2
            Remove-Item -Path '{temp_shortcut}' -Force
            '''
            
            # Выполняем PowerShell команду
            subprocess.run(["powershell", "-Command", powershell_cmd], shell=True)
                
        except Exception as e:
            print(f"Ошибка закрепления на панели задач: {str(e)}")
    
    def launch_application(self, app_path):
        """Запуск приложения после установки"""
        try:
            if os.path.exists(app_path):
                # Запускаем приложение от имени администратора
                ctypes.windll.shell32.ShellExecuteW(
                    None, 
                    "runas", 
                    app_path, 
                    None, 
                    None, 
                    1
                )
                return True
            return False
        except Exception as e:
            print(f"Ошибка запуска приложения: {str(e)}")
            return False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, 
        "runas", 
        sys.executable, 
        " ".join(sys.argv), 
        None, 
        1
    )
    sys.exit(0)