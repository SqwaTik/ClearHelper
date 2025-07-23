import os
import sys
import ctypes
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
from core.installer import is_installed, run_installer_gui, is_admin, run_as_admin

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    return os.path.join(base_path, relative_path)

def handle_exception(exc_type, exc_value, exc_traceback):
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Необработанное исключение:\n{error_msg}")
    
    with open("error.log", "a", encoding="utf-8") as f:
        f.write(f"Ошибка приложения:\n{error_msg}\n\n")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    QMessageBox.critical(
        None,
        "Критическая ошибка",
        f"Произошла критическая ошибка:\n\n{error_msg}\n\nПодробности в error.log"
    )
    sys.exit(1)

def main():
    sys.excepthook = handle_exception
    
    if sys.platform != 'win32':
        print("Данное приложение работает только в Windows")
        sys.exit(1)
    
    # Проверяем, установлено ли приложение
    if not is_installed():
        # Запускаем установщик
        run_installer_gui()
        sys.exit(0)
    
    # Проверка прав администратора
    if not is_admin():
        run_as_admin()
        sys.exit(0)
    
    try:
        app = QApplication(sys.argv)
        
        icon_path = get_resource_path("resources/icons/app_icon.ico")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
        
        window = MainWindow()
        if os.path.exists(icon_path):
            window.setWindowIcon(QIcon(icon_path))
        window.show()
        
        sys.exit(app.exec())
    
    except Exception as e:
        handle_exception(type(e), e, e.__traceback__)

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()