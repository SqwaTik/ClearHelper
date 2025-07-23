import os
import sys
import ctypes
import subprocess

def get_resource_path(relative_path):
    """Получает абсолютный путь к ресурсу для работы в EXE и из исходников"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.join(os.path.abspath("."), "src")
    
    full_path = os.path.join(base_path, relative_path)
    print(f"Ресурсный путь: {relative_path} -> {full_path}")
    return full_path

class ProgramManager:
    @staticmethod
    def get_programs():
        try:
            base_path = get_resource_path("programs")
            print(f"Поиск программ в: {base_path}")
            
            if not os.path.exists(base_path):
                print(f"Папка с программами не найдена: {base_path}")
                return {}
            
            programs = {}
            default_icon = get_resource_path("resources/icons/default_app.ico")
            
            for app_dir in os.listdir(base_path):
                app_path = os.path.join(base_path, app_dir)
                if not os.path.isdir(app_path):
                    continue
                    
                exe_found = False
                icon_path = default_icon
                exe_path = None

                for file in os.listdir(app_path):
                    file_path = os.path.join(app_path, file)
                    if file.lower().endswith(".exe"):
                        exe_path = file_path
                        exe_found = True
                    elif file.lower().endswith(".ico"):
                        icon_path = file_path
                
                if exe_found and exe_path:
                    # Информация о программах (сокращенный вариант)
                    info = f"{app_dir} - системная утилита"
                    help_text = "Для получения справки по программе обратитесь к документации"
                    
                    if "Everything" in app_dir:
                        info = "Everything - утилита для мгновенного поиска файлов и папок"
                        
                        cheat_clients = sorted([
                            "impact", "wurst", "bleachhack", "aristois", "huzuni", "skillclient", 
                            "nodus", "inertia", "ares", "sigma", "meteor", "atomic", "zamorozka", 
                            "liquidbounce", "nurik", "nursultan", "celestial", "calestial", "celka", 
                            "expensive", "neverhook", "excellent", "wexside", "wildclient", "minced", 
                            "deadcode", "akrien", "jigsaw", "future", "jessica", "dreampool", "vape", 
                            "infinity", "flux", "squad", "norules", "konas", "zeusclient", "richclient", 
                            "ghost_client", "rusherhack", "thunderhack", "moonhack", "winner", "nova", 
                            "exire", "doomsday", "nightware", "ricardo", "extazyy", "troxill", "antileak", 
                            "arbuz", ".akr", ".wex", "dauntiblyat", "rename_me_please", "editme", "takker", 
                            "fuzeclient", "wisefolder", "netlimiter", "flauncher", "clean-main", "vec.dll", 
                            "USBOblivion.exe", "Feather", "delta", "eclipse", "venus", "jex", "hakari", 
                            "hush", "hach", "Amethyst", "haruka", "pyrix", "unleashed", "paradox", 
                            "illustrative", "exclight", "neverlose", "neverdeath", "nitex", "dettex", 
                            "neris", "aqua", "eclipse", "dabber", "felon", "swag", "mentality", "astra", 
                            "rocksolona", "relative", "shipuchka", "miraculos", "churka", "neverbels", 
                            "deluxe", "valhalla", "deadly", "miraculis", "private", "vesence"
                        ])
                        
                        cheat_mods = sorted([
                            "bariton", "xray", "x-ray", "spambot", "CleanCut", "spam_bot", 
                            "inventory_walk", "player_highlighter", "aimbot", "freecam", 
                            "bedrock_breaker_mode", "viaversion", "double_hotbar", "elytra_swap", 
                            "armor_hotswap", "smart_moving", "chest", "savesearcher", "worlddownloader", 
                            "topkautobuy", "topkaautobuy", "gumballoff", "tweakeroo", "mob_hitbox", 
                            "librarian_trade_finder", "sacurachorusfind", "autoattack", "entity_outliner", 
                            "clickcrystals", "entity_xray", 
                            "invmove", "viabackwards", "viarewind", "viafabric", "viaforge", "viaproxy", 
                            "vialoader", "viamcp", "hitbox", "chunkcopy", "elytrahack", "SeedCracker", 
                            "DiamondSim", "ForgeHax", "StepUp", "clientcommands", "xaero", "worldmap", 
                            "InventoryProfiles", "auto-clicker", "autoclick", "Control-Tweaks", 
                            "SwingThroughGrass", "through", "camerautils", "mobhealthbar"
                        ])
                        
                        cheat_sizes = [
                            "size:7204864 (dll с весом 7036 кб) – автобай",
                            "size:9332326 (расширение dll) – старый автобай",
                            "size:9400174 (любое расширение, 9180 кб) – мп3 хитбоксы",
                            "size:1613824 | size:1499136 | size:1488896 (расширение .dll/.jar) – хитбоксы",
                            "size:10071288 (расширение .exe) – WiseFolderHider"
                        ]
                        
                        clients_formatted = " | ".join(cheat_clients)
                        mods_formatted = " | ".join(cheat_mods)
                        sizes_formatted = "\n".join(cheat_sizes)
                        
                        help_text = f"""
                        <h2>Руководство по использованию Everything</h2>
                        <p>Everything - мощный инструмент для мгновенного поиска файлов и папок на вашем компьютере.</p>
                        
                        <h3>Основные возможности:</h3>
                        <ul>
                            <li>Мгновенный поиск по всему компьютеру</li>
                            <li>Поддержка сложных поисковых запросов</li>
                            <li>Интеграция с проводником Windows</li>
                            <li>Поддержка регулярных выражений</li>
                            <li>Поиск по содержимому файлов</li>
                        </ul>
                        
                        <h3>Чит клиенты:</h3>
                        <div style="background: #2a2a2a; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                            <p style="font-size: 14px; line-height: 1.6;">{clients_formatted}</p>
                        </div>
                        
                        <h3>Читерские моды:</h3>
                        <div style="background: #2a2a2a; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                            <p style="font-size: 14px; line-height: 1.6;">{mods_formatted}</p>
                        </div>
                        
                        <h3>Читерские веса:</h3>
                        <div style="background: #2a2a2a; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                            <pre style="font-size: 14px; line-height: 1.6;">{sizes_formatted}</pre>
                            <p>Исключения .dll файлы по путям С:\\Windows\\WinSxS и С:\\Windows\\System32 с весом 1464 и 1576 кб.</p>
                        </div>
                        
                        <h3>Советы по поиску:</h3>
                        <ul>
                            <li>Используйте <code>*.jar</code> для поиска всех jar файлов</li>
                            <li><code>!C:\\Windows</code> - исключить папку Windows из поиска</li>
                            <li><code>size:>100MB</code> - файлы больше 100 МБ</li>
                            <li><code>modified:today</code> - файлы измененные сегодня</li>
                        </ul>
                        """
                    elif "RegScanner" in app_dir:
                        info = "RegScanner - инструмент для сканирования реестра Windows"
                        help_text = """
                        <h2>Руководство по использованию RegScanner</h2>
                        <p>RegScanner позволяет быстро находить ключи и значения в реестре Windows.</p>
                        
                        <h3>Основные возможности:</h3>
                        <ul>
                            <li>Быстрый поиск по всему реестру</li>
                            <li>Фильтрация результатов</li>
                            <li>Экспорт найденных ключей</li>
                            <li>Поиск по шаблонам</li>
                            <li>Поиск в бинарных данных</li>
                        </ul>
                        
                        <h3>Примеры использования:</h3>
                        <ul>
                            <li>Поиск следов вредоносных программ</li>
                            <li>Настройка системных параметров</li>
                            <li>Устранение ошибок реестра</li>
                            <li>Анализ установленных программ</li>
                        </ul>
                        
                        <h3>Текст</h3>
                        <div style="background: #2a2a2a; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                            <p style="font-size: 14px; line-height: 1.6;">
                                Celestial, Nursultan, Expensive, nova-dev, Akrien, WexSide, DeadCode, 
                                Wild, Avalon, Troxill, calestial, DreamPool, Excellent, inegay, 
                                Wissend, Elysium, Aurora, Verist, NewCode, VenusWare, Catlavan, 
                                DeltaLoader, Delta, Wenose, Monoton, DarkSide, haruka
                            </p>
                        </div>
                        <h3>Comma-delemited list</h3>
                        <div style="background: #2a2a2a; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                            <p style="font-size: 14px; line-height: 1.6;">
                                HKLM\SOFTWARE\Microsoft\FuzzyDS, HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\
                            </p>
                        </div>
                        <h3>Как должно выглядеть</h3>
                        <div style="background: #2a2a2a; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                            <p style="font-size: 14px; line-height: 1.6;">
                                <a href="https://fastpic.org/view/125/2025/0718/_f3f5d88498bfee7d7a0d3d8d1200d5e9.png.html">Пример изображения</a>
                            </p>
                        </div>
                        """
                    elif "LastActivityView" in app_dir:
                        info = "LastActivityView - показывает историю активности на компьютере"
                        help_text = """
                        <h2>Руководство по использованию LastActivityView</h2>
                        <p>LastActivityView предоставляет детальную информацию о последних действиях на компьютере.</p>
                        
                        <h3>Основные возможности:</h3>
                        <ul>
                            <li>Показывает запущенные приложения</li>
                            <li>Отображает открытые файлы</li>
                            <li>Фиксирует посещенные веб-страницы</li>
                            <li>Показывает включение/выключение компьютера</li>
                            <li>Отображает подключения USB устройств</li>
                        </ul>
                        
                        <h3>Как использовать:</h3>
                        <ol>
                            <li>Запустите программу</li>
                            <li>Дождитесь загрузки данных</li>
                            <li>Используйте фильтры для поиска нужных событий</li>
                            <li>Экспортируйте результаты при необходимости</li>
                        </ol>
                        """
                    elif "BrowserDownloadsView" in app_dir:
                        info = "BrowserDownloadsView - просмотр истории загрузок браузеров"
                        help_text = """
                        <h2>Руководство по использованию BrowserDownloadsView</h2>
                        <p>Просматривайте историю загрузок из различных браузеров.</p>
                        """
                    elif "ProcessHacker" in app_dir:
                        info = "ProcessHacker - продвинутый диспетчер задач"
                        help_text = """
                        <h2>Руководство по использованию ProcessHacker</h2>
                        <p>Мониторинг процессов, служб, сетевых соединений и дисковых операций.</p>
                        """
                    elif "UsbDriveLog" in app_dir:
                        info = "UsbDriveLog - история подключений USB устройств"
                        help_text = """
                        <h2>Руководство по использованию UsbDriveLog</h2>
                        <p>Просмотр истории подключения USB накопителей к компьютеру.</p>
                        """
                    elif "CachedProgramsList" in app_dir:
                        info = "CachedProgramsList - список кэшированных программ"
                        help_text = """
                        <h2>Руководство по использованию CachedProgramsList</h2>
                        <p>Отображение программ, сохраненных в кэше Windows.</p>
                        """
                    elif "JournalTrace" in app_dir:
                        info = "JournalTrace - анализ журнальных событий"
                        help_text = """
                        <h2>Руководство по использованию JournalTrace</h2>
                        <p>Анализ журнальных событий Windows для диагностики системы.</p>
                        """
                    elif "ShellBag" in app_dir:
                        info = "ShellBag - история просмотров папок"
                        help_text = """
                        <h2>Руководство по использованию ShellBag</h2>
                        <p>Просмотр истории открытых папок и их настроек в Windows.</p>
                        """
                    elif "ProcessActivityView" in app_dir:
                        info = "ProcessActivityView - активность процессов"
                        help_text = """
                        <h2>Руководство по использованию ProcessActivityView</h2>
                        <p>Мониторинг активности запущенных процессов в системе.</p>
                        """
                    elif "OpenSaveFilesView" in app_dir:
                        info = "OpenSaveFilesView - история открытия/сохранения файлов"
                        help_text = """
                        <h2>Руководство по использованию OpenSaveFilesView</h2>
                        <p>Просмотр истории открытия и сохранения файлов в системе.</p>
                        """
                    elif "WinPrefetchView" in app_dir:
                        info = "WinPrefetchView - анализ Prefetch файлов"
                        help_text = """
                        <h2>Руководство по использованию WinPrefetchView</h2>
                        <p>Анализ Prefetch файлов для определения запущенных программ.</p>
                        """
                    elif "PreviousFilesRecovery" in app_dir:
                        info = "PreviousFilesRecovery - восстановление предыдущих версий"
                        help_text = """
                        <h2>Руководство по использованию PreviousFilesRecovery</h2>
                        <p>Восстановление предыдущих версий файлов и теневых копий.</p>
                        """
                    elif "ExecutedProgramsList" in app_dir:
                        info = "ExecutedProgramsList - список запущенных программ"
                        help_text = """
                        <h2>Руководство по использованию ExecutedProgramsList</h2>
                        <p>Просмотр истории запуска программ на компьютере.</p>
                        """
                    else:
                        info = f"{app_dir} - системная утилита"
                        help_text = "Для получения справки по программе обратитесь к документации"
                    
                    programs[app_dir] = {
                        "name": app_dir,
                        "path": exe_path,
                        "icon": icon_path,
                        "info": info,
                        "help": help_text,
                        "admin_required": True
                    }
                    print(f"Найдена программа: {app_dir} -> {exe_path}")
            return programs
        except Exception as e:
            print(f"Ошибка загрузки программ: {str(e)}")
            return {}
    
    @staticmethod
    def run_as_admin(path):
        if sys.platform != "win32":
            return False
            
        try:
            result = ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                path, 
                None, 
                None, 
                1
            )
            
            if result <= 32:
                return result == 1223  # 1223 - пользователь отменил
            return True
        except Exception as e:
            print(f"Admin run error: {e}")
            return False