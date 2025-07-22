import os
import sys
import ctypes
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow

def get_resource_path(relative_path):
    """Получает абсолютный путь к ресурсу для работы в EXE и из исходников"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.join(os.path.abspath("."), "src")
    
    return os.path.join(base_path, relative_path)

def is_admin():
    """Проверяем, запущена ли программа с правами администратора"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Перезапускаем программу с правами администратора"""
    if sys.platform != 'win32':
        return False
        
    ctypes.windll.shell32.ShellExecuteW(
        None, 
        "runas", 
        sys.executable, 
        " ".join(sys.argv), 
        None, 
        1
    )
    sys.exit(0)

def handle_exception(exc_type, exc_value, exc_traceback):
    """Обработчик необработанных исключений"""
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Необработанное исключение:\n{error_msg}")
    
    # Запись ошибки в файл
    with open("error.log", "a", encoding="utf-8") as f:
        f.write(f"Ошибка приложения:\n{error_msg}\n\n")
    
    # Проверяем, существует ли экземпляр QApplication
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
    """Главная функция приложения"""
    # Установка обработчика исключений
    sys.excepthook = handle_exception
    
    # Проверка платформы (только для Windows)
    if sys.platform != 'win32':
        print("Данное приложение работает только в Windows")
        sys.exit(1)
    
    # Проверка прав администратора
    if not is_admin():
        # Автоматический перезапуск с правами администратора
        run_as_admin()
        sys.exit(0)
    
    try:
        # Создаем QApplication
        app = QApplication(sys.argv)
        
        # Устанавливаем иконку приложения
        icon_path = get_resource_path("resources/icons/app_icon.ico")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
            print(f"Иконка приложения установлена: {icon_path}")
        else:
            print(f"Иконка приложения не найдена: {icon_path}")
        
        # Запускаем главное окно
        window = MainWindow()
        if os.path.exists(icon_path):
            window.setWindowIcon(QIcon(icon_path))
        window.show()
        
        sys.exit(app.exec())
    
    except Exception as e:
        handle_exception(type(e), e, e.__traceback__)

if __name__ == "__main__":
    # Добавляем текущую директорию в путь поиска модулей
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    main()