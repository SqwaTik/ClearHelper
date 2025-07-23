import os
import sys
import json
import subprocess
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from widgets.gradient_bg import GradientBackground
from widgets.animated_button import AnimatedButton
from widgets.icon_button import IconButton
from dialogs.about_dialog import AboutDialog
from dialogs.help_dialog import HelpDialog
from dialogs.program_info_dialog import ProgramInfoDialog
from dialogs.settings_dialog import SettingsDialog
from core.program_manager import ProgramManager, get_resource_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clear Helper")
        self.setFixedSize(700, 450)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        
        # Устанавливаем иконку
        self.icon_path = get_resource_path("resources/icons/app_icon.ico")
        if os.path.exists(self.icon_path):
            self.setWindowIcon(QIcon(self.icon_path))
        
        self.programs = ProgramManager.get_programs()
        self.current_theme = "dark"
        self.hotkeys = self.load_hotkeys()
        self.running_processes = []
        self.force_quit = False
        self.init_ui()
        self.init_shortcuts()
        self.init_tray_icon()
    
    def init_ui(self):
        self.gradient_colors = self.load_gradient()
        self.central_widget = GradientBackground(self.gradient_colors)
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        header_layout = QHBoxLayout()
        title = QLabel("Clear Helper")
        title_font = QFont("Arial", 18, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #e0e0e0;")
        header_layout.addWidget(title, 0, Qt.AlignCenter)
        
        self.theme_btn = IconButton()
        icon_path = get_resource_path("resources/icons/theme.ico")
        if os.path.exists(icon_path):
            self.theme_btn.setIcon(QIcon(icon_path))
        self.theme_btn.setToolTip("Сменить тему (Ctrl+T)")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setProperty("light_theme", "false")
        header_layout.addWidget(self.theme_btn)
        
        self.settings_btn = IconButton()
        icon_path = get_resource_path("resources/icons/settings.ico")
        if os.path.exists(icon_path):
            self.settings_btn.setIcon(QIcon(icon_path))
        self.settings_btn.setToolTip("Настройки")
        self.settings_btn.clicked.connect(self.show_settings)
        self.settings_btn.setProperty("light_theme", "false")
        header_layout.addWidget(self.settings_btn)
        
        main_layout.addLayout(header_layout)
        
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
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        self.grid_layout = QGridLayout(container)
        self.grid_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.grid_layout.setHorizontalSpacing(12)
        self.grid_layout.setVerticalSpacing(10)
        self.grid_layout.setContentsMargins(15, 10, 15, 15)
        self.update_program_grid()
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area, 1)
        
        footer = QLabel("ПКМ на программе для дополнительных опций | Ctrl+T: сменить тему")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-size: 10px; color: #aaaaaa;")
        main_layout.addWidget(footer)
        
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Готов к работе")
        self.status_bar.setStyleSheet("""
            background: #1a1a1a;
            color: #aaaaaa;
            border-top: 1px solid #444444;
            font-size: 10px;
        """)
        self.apply_theme("dark")
    
    def update_program_grid(self):
        # Очищаем предыдущие элементы
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        row, col = 0, 0
        max_cols = 4  # Максимальное количество столбцов
        
        for app_name, app_data in self.programs.items():
            btn = AnimatedButton(app_data["name"])
            btn.setProperty("light_theme", "true" if self.current_theme == "light" else "false")
            btn.setToolTip(f"Запустить {app_data['name']}")
            btn.clicked.connect(lambda _, path=app_data["path"]: self.launch_app(path))
        
            icon_path = app_data["icon"]
            if icon_path and os.path.exists(icon_path):
                pixmap = QIcon(icon_path).pixmap(48, 48)
            else:
                pixmap = QIcon.fromTheme("application-x-executable").pixmap(48, 48)
            btn.setCustomIcon(pixmap)
        
            btn.setContextMenuPolicy(Qt.CustomContextMenu)
            btn.customContextMenuRequested.connect(
                lambda pos, data=app_data, button=btn: self.show_program_context_menu(pos, data, button))
        
            self.grid_layout.addWidget(btn, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def launch_app(self, path, admin=True):
        try:
            if admin:
                if ProgramManager.run_as_admin(path):
                    self.status_bar.showMessage("Запуск от администратора")
                else:
                    self.status_bar.showMessage("Запуск отменен")
                return
                
            if sys.platform == "win32":
                process = subprocess.Popen([path])
                self.running_processes.append(process)
            else:
                process = subprocess.Popen(path)
                self.running_processes.append(process)
                
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка запуска: {str(e)}")
        finally:
            QTimer.singleShot(3000, lambda: self.status_bar.showMessage("Готов к работе"))
    
    def show_program_context_menu(self, pos, program_data, button):
        menu = QMenu(self)
        
        info_action = menu.addAction("Информация")
        icon_path = get_resource_path("resources/icons/info.ico")
        if os.path.exists(icon_path):
            info_action.setIcon(QIcon(icon_path))
        info_action.triggered.connect(lambda: self.show_program_info(program_data))
        
        help_action = menu.addAction("Помощь")
        icon_path = get_resource_path("resources/icons/help.ico")
        if os.path.exists(icon_path):
            help_action.setIcon(QIcon(icon_path))
        help_action.triggered.connect(lambda: self.show_program_help(program_data))
        
        admin_action = menu.addAction("Запуск от администратора")
        icon_path = get_resource_path("resources/icons/admin.ico")
        if os.path.exists(icon_path):
            admin_action.setIcon(QIcon(icon_path))
        admin_action.triggered.connect(lambda: self.launch_app(program_data["path"], admin=True))
        
        menu.exec_(button.mapToGlobal(pos))
    
    def load_hotkeys(self):
        config_path = get_resource_path("config/hotkeys.json")
        default_hotkeys = {
            "theme_toggle": "Ctrl+T",
            "help": "F1",
            "about": "Ctrl+I",
            "exit": "Ctrl+Q",
            "settings": "Ctrl+S"
        }
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except:
            pass
        return default_hotkeys
    
    def load_gradient(self):
        config_path = get_resource_path("config/gradient.json")
        default_gradient = [
            {"r": 25, "g": 25, "b": 40},
            {"r": 30, "g": 30, "b": 50},
            {"r": 20, "g": 20, "b": 35}
        ]
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    colors = json.load(f)
                    return [QColor(c["r"], c["g"], c["b"]) for c in colors]
        except:
            pass
        return [QColor(c["r"], c["g"], c["b"]) for c in default_gradient]
    
    def save_gradient(self, colors):
        config_path = get_resource_path("config/gradient.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump([{"r": c.red(), "g": c.green(), "b": c.blue()} for c in colors], f)
        except:
            pass
    
    def init_shortcuts(self):
        QShortcut(QKeySequence(self.hotkeys["theme_toggle"]), self).activated.connect(self.toggle_theme)
        QShortcut(QKeySequence(self.hotkeys["help"]), self).activated.connect(self.show_help)
        QShortcut(QKeySequence(self.hotkeys["about"]), self).activated.connect(self.show_about)
        QShortcut(QKeySequence(self.hotkeys["exit"]), self).activated.connect(self.force_quit_and_close)
        QShortcut(QKeySequence(self.hotkeys["settings"]), self).activated.connect(self.show_settings)
    
    def init_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        if os.path.exists(self.icon_path):
            self.tray_icon.setIcon(QIcon(self.icon_path))
        else:
            self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        tray_menu = QMenu()
        restore_action = QAction("Восстановить", self)
        restore_action.triggered.connect(self.show_normal)
        theme_action = QAction("Сменить тему", self)
        theme_action.triggered.connect(self.toggle_theme)
        settings_action = QAction("Настройки", self)
        settings_action.triggered.connect(self.show_settings)
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.force_quit_and_close)
        tray_menu.addAction(restore_action)
        tray_menu.addAction(theme_action)
        tray_menu.addAction(settings_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
    
    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_normal()
    
    def show_normal(self):
        self.show()
        self.activateWindow()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    
    def show_program_info(self, program_data):
        dialog = ProgramInfoDialog(program_data, self)
        dialog.exec()
    
    def show_program_help(self, program_data):
        dialog = HelpDialog(program_data, self)
        dialog.exec()
    
    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            new_gradient = dialog.get_selected_gradient()
            if new_gradient != self.gradient_colors:
                self.gradient_colors = new_gradient
                self.central_widget.set_gradient(new_gradient)
                self.save_gradient(new_gradient)
    
    def toggle_theme(self):
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(new_theme)
        self.current_theme = new_theme
        self.status_bar.showMessage(f"Тема изменена: {new_theme}")
        QTimer.singleShot(3000, lambda: self.status_bar.showMessage("Готов к работе"))
        self.theme_btn.setProperty("light_theme", "true" if new_theme == "light" else "false")
        self.settings_btn.setProperty("light_theme", "true" if new_theme == "light" else "false")
        self.theme_btn.style().unpolish(self.theme_btn)
        self.theme_btn.style().polish(self.theme_btn)
        self.settings_btn.style().unpolish(self.settings_btn)
        self.settings_btn.style().polish(self.settings_btn)
        self.update_program_grid()
    
    def apply_theme(self, theme):
        palette = QPalette()
        if theme == "dark":
            palette.setColor(QPalette.Window, QColor(20, 20, 20))
            palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
            palette.setColor(QPalette.Base, QColor(30, 30, 30))
            palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
            palette.setColor(QPalette.ToolTipBase, QColor(220, 220, 220))
            palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
            palette.setColor(QPalette.Text, QColor(220, 220, 220))
            palette.setColor(QPalette.Button, QColor(50, 50, 50))
            palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
            palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
            palette.setColor(QPalette.Highlight, QColor(90, 135, 230))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        else:
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
            palette.setColor(QPalette.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Highlight, QColor(100, 150, 255))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        QApplication.instance().setPalette(palette)
    
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec()
    
    def show_help(self):
        dialog = HelpDialog(None, self)
        dialog.exec()
    
    def force_quit_and_close(self):
        self.force_quit = True
        self.close()
    
    def closeEvent(self, event):
        if self.force_quit:
            # Завершаем все запущенные процессы
            for process in self.running_processes:
                try:
                    if process.poll() is None:  # Проверяем, работает ли процесс
                        process.terminate()    # Пытаемся завершить корректно
                        process.wait(2)        # Ждем 2 секунды
                        if process.poll() is None:
                            process.kill()     # Принудительно завершаем
                except Exception as e:
                    print(f"Ошибка при завершении процесса: {e}")
            
            event.accept()
            QApplication.quit()
        else:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Clear Helper",
                "Программа свернута в трей",
                QSystemTrayIcon.Information,
                2000
            )