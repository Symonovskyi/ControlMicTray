# ![Presentation ControlMicTray](https://controlmictray.pp.ua/src/img/logo/Microphone.svg) ControlMicTray

[![Release (latest by date)](https://img.shields.io/github/v/release/Symonovskyi/ControlMicTray?style=for-the-badge)](https://github.com/Symonovskyi/ControlMicTray/releases) ![Release Date](https://img.shields.io/github/release-date/Symonovskyi/ControlMicTray?style=for-the-badge) [![All releases](https://img.shields.io/github/downloads/Symonovskyi/ControlMicTray/total?style=for-the-badge)](https://github.com/Symonovskyi/ControlMicTray/releases) [![License](https://img.shields.io/github/license/Symonovskyi/ControlMicTray?style=for-the-badge)](https://github.com/Symonovskyi/ControlMicTray/blob/main/LICENSE)  
![Commits since latest release](https://img.shields.io/github/commits-since/Symonovskyi/ControlMicTray/latest?style=for-the-badge) ![Code size in bytes](https://img.shields.io/github/languages/code-size/Symonovskyi/ControlMicTray?style=for-the-badge) ![Lines of code](https://aschey.tech/tokei/github/Symonovskyi/ControlMicTray?style=for-the-badge)  
![Locked Python version](https://img.shields.io/github/pipenv/locked/python-version/Symonovskyi/ControlMicTray?style=for-the-badge) ![Locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/Symonovskyi/ControlMicTray/pyqt6?style=for-the-badge) ![Locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/Symonovskyi/ControlMicTray/keyboard?style=for-the-badge) ![Locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/Symonovskyi/ControlMicTray/pycaw?style=for-the-badge)

## Language

* [Go to English](#en)
* [Go to Ukrainian​ ​​💙💛​](#uk)

---

### EN

#### Control your microphone comfortably with ControlMicTray🎙️

<img src="https://controlmictray.pp.ua/src/img/presentation/presentation_01.gif" alt="Demo ControlMicTray" align="left" style="padding-right:20px;"/>

An application **for Windows** that allows you to monitor and control your microphone without unnecessary movements: an icon in the system tray will show its current status, and a personal customizable hotkey will allow you to quickly control it.<br clear="left"/>

### Installing

1. 👩🏻‍💻Download the latest version of the application from [releases page](https://github.com/Symonovskyi/ControlMicTray/releases);
2. 📂Open the downloaded file;
3. 🏆Profit!

#### *TODO*: Realized stuff as of 04.04.2024

* [x] Dark theme
* [x] Walkie-talkie mode
* [x] Microphone mute/unmute with a customizable shortcut key
* [x] Microphone mute/unmute in the application's menu
* [x] Automatic application startup at system boot
* [x] Microphone mute on application startup
* [ ] Support for multiple languages
* [ ] Automatic updates support
* [ ] Notifications from the application
* [ ] Select which microphone to use
* [x] Fully functional portable version

---

### UK

#### Пануйте над своїм мікрофоном з комфортом, використовуючи ControlMicTray🎙️

<img src="https://controlmictray.pp.ua/src/img/presentation/presentation_01.gif" alt="Demo ControlMicTray" align="left" style="padding-right:20px;"/>

Додаток **для Windows**, який дозволяє моніторити та керувати Вашим мікрофоном без зайвих рухів: іконка в системному треї покаже його поточний стан, а персональна настроювана гаряча клавіша дозволить швидко керувати ним.<br clear="left"/>

#### Встановлення

1. 👩🏻‍💻Завантажити останню версію додатку з [сторінки релізів](https://github.com/Symonovskyi/ControlMicTray/releases);
2. 📂Відкрити завантажений файл;
3. 🏆Профіт!

#### *TODO*: Реалізовано станом на 04.04.2024

* [x] Темна тема;
* [x] Режим "Рації";
* [x] Вимкнення та увімкнення мікрофона за допомогою настроюваної гарячої клавіші;
* [x] Вимкнення та увімкнення мікрофона в меню додатку;
* [x] Автоматичний запуск додатку при старті системи;
* [x] Вимкнення мікрофона при запуску додатку;
* [x] Повноцінна портативна версія.

#### База Данных

* [ ] 🔥 Проверить наличие всех необходимых таблиц. Если хотя бы одной нет — создать все заново.🤷‍♀️
* [ ] 🔥 Если дата релиза не соответствует актуальной версии — обновить данные в таблицах.🤷‍♀️
* [ ] 🔥 В случае возникновения исключения вывести сообщение в консоль, записать в лог и пересоздать базу данных.
* [ ] 🔥 Инициализация базы данных должна происходить в `TrayIcon`.👀

#### Управление Микрофонами

* [ ] 🔥 Получение списка доступных микрофонов.👀
* [ ] 🔥 Определение устройства по умолчанию.👀
* [ ] 🔥 Определение устройства связи по умолчанию.👀
* [ ] 🔥 Выставление микрофона по умолчанию.👀
* [ ] 🔥 Выставление устройства связи по умолчанию.👀
* [ ] 🔥 Мутирование микрофона.👀
* [ ] 🔥 Настроить программу на распознавание изменений микрофонов в системе с использованием примера из GitHub `pycaw`.👀
* [ ] 🔥 Ввести новую иконку для отображения состояния активного микрофона в подменю "Микрофоны".👀
* [ ] 🔥 Возможность выбора конкретного микрофона для работы.👀

#### Горячие Клавиши

* [ ] 🔥 При нажатии `Esc` — возвращаемся без изменений.👀
* [ ] 🔥 При нажатии `Delete` — очищаем поле `hotkey`.👀
* [ ] 🔥 Если поле `hotkey` пустое — выводим плейсхолдер `Нажмите для установки`.👀

* [ ] 💡 Реализовать возможность регулировки громкости активного микрофона с помощью колесика мыши, когда курсор находится на значке микрофона.
* [ ] 💡 Добавить кнопку для открытия свойств микрофона (включая усилитель и основную громкость).
* [ ] 💡 Хранить уровни громкости только для активного микрофона в базе данных.

#### Интерфейс и Локализация

* [ ] 💡 Разработать интерфейс с учетом системной темы.🤷‍♀️
* [ ] 💡 Добавить возможность изменения горячих клавиш вне зависимости от выбранного режима.
* [ ] 💡 Поддержка разных языков с определением локали системы и использованием соответствующего языка по умолчанию.🤷‍♀️
* [ ] 💡 Добавить систему уведомлений от приложения.👀

#### Автоматические Обновления и Структура Проекта

* [ ] 💡 Поддержка автоматических обновлений (с возможностью пропустить обновление).👀
* [ ] 💡 Реализовать микросервисную архитектуру с соответствующей структурой проекта: controllers, controllers/api, ui, database.
* [ ] 💡 Разделить функционал в `settingsWindow.py` на отдельные сервисы.👀
* [ ] 🔥 Добавить логирование (режимы dev/prod).🤷‍♀️

### Дополнительные Рекомендации

* [ ] ❄️ Использовать `keyboard.kb_parse_hotkey` вместо передачи текста напрямую.👀
* [ ] ❄️ Использовать qt атрибут `parent` для окон вместо прямых ссылок на инстансы.👀
* [ ] ❄️ Изменить логику для режима рации: избавиться от двух qt сигналов, оставить один для обоих режимов программы.👀
* [ ] ❄️ Перейти на использование `QSQLDatabase`.
* [ ] ❄️ Перенести кастомные классы для `QKeySequence`, `QMenu` и `KeyboardManager`, а также методы в `absolutePath.py` в `miscellaneous.py`.
* [ ] ❄️ Везде, где это возможно, использовать систему сигнал/слот для обработки событий.👀
* [ ] ❄️ Добавить поддержку мыши и протестировать функционал хоткеев после рефакторинга.
* [ ] ❄️ Если в системе нет микрофонов — вывести уведомление об отсутствии микрофонов и продолжить работу.👀








### Структура Проекта

├── .gitignore
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
├── resources/
├── icons/
│   ├── ControlMicTray.ico
│   └── Microphone.svg
├── src/
│   ├── __init__.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── database_adapter.py  # Адаптер для работы с БД
│   │   ├── microphone_adapter.py  # Адаптер для работы с микрофонами
│   │   └── system_adapter.py  # Адаптер для работы с системными настройками
│   ├── application/
│   │   ├── __init__.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── microphone_service.py  # Логика управления микрофонами
│   │   │   ├── hotkey_service.py  # Логика горячих клавиш
│   │   │   └── settings_service.py  # Логика настроек приложения
│   │   └── use_cases/
│   │       ├── __init__.py
│   │       ├── mute_microphone.py  # Use case для отключения микрофона
│   │       ├── toggle_walkie_talkie_mode.py  # Use case для режима "Рации"
│   │       └── update_settings.py  # Use case для обновления настроек
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── microphone.py  # Сущность микрофона
│   │   │   └── settings.py  # Сущность настроек
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── microphone_repository.py  # Интерфейс для репозитория микрофонов
│   │       └── settings_repository.py  # Интерфейс для репозитория настроек
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── models.py  # Модели данных для БД
│   │   │   └── repository.py  # Реализация репозиториев для БД
│   │   └── interfaces/
│   │       ├── __init__.py
│   │       ├── microphone_interace.py  # Управление микрофонами через pycaw
│   │       └── hotkey_interface.py  # Управление горячими клавишами через keyboard
│   ├── presentation/
│   │   ├── __init__.py
│   │   ├── tray_service.py  # Логика системного трея (вынесена из UI)
│   │   ├── ui/
│   │   │   ├── __init__.py
│   │   │   ├── about_window.py  # Окно "О программе"
│   │   │   ├── settings_window.py  # Окно настроек
│   │   │   └── views/
│   │   │       ├── __init__.py
│   │   │       ├── about_view.ui  # UI файл для окна "О программе"
│   │   │       └── settings_view.ui  # UI файл для окна настроек
│   │   └── styles/
│   │       ├── __init__.py
│   │       └── style_manager.py  # Управление стилями приложения
│   └── utils/
│       ├── __init__.py
│       └── event_bus.py  # Централизованная шина событий










### Пример использования

Для поддержки работы с разными операционными системами (Windows и macOS), нужно добавить механизм выбора реализации в зависимости от текущей ОС. Это можно сделать через **фабричный паттерн** или **стратегию**, чтобы динамически выбирать нужный менеджер микрофона.

---

### Обновленная структура:

```
├── src/
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── microphone_adapter.py  # Адаптер для работы с микрофонами
│   │   └── system_adapter.py  # Адаптер для работы с системными настройками
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── microphone_managers/
│   │   │   ├── __init__.py
│   │   │   ├── windows_microphone_manager.py  # Реализация для Windows
│   │   │   └── macos_microphone_manager.py    # Реализация для macOS
│   │   └── microphone_factory.py              # Фабрика для выбора менеджера
│   ├── application/
│   │   ├── services/
│   │   │   ├── microphone_service.py          # Сервис микрофона
│   │   └── use_cases/
│   │       ├── mute_microphone.py             # Use case для отключения микрофона
│   ├── domain/
│   │   ├── interfaces/
│   │   │   ├── i_microphone_repository.py     # Интерфейс для репозитория микрофонов
```

---

### Как это работает?

1. **`i_microphone_repository.py`**: Определяет общий интерфейс для работы с микрофоном.
2. **`windows_microphone_manager.py` и `macos_microphone_manager.py`**: Реализуют работу с микрофоном для каждой ОС.
3. **`microphone_factory.py`**: Выбирает нужную реализацию в зависимости от ОС.
4. **`microphone_adapter.py`**: Использует фабрику для получения нужного менеджера.
5. **`microphone_service.py`**: Работает через адаптер, не зная о конкретной реализации.

---

### Пример кода:

#### 1. **`i_microphone_repository.py`**
```python
# i_microphone_repository.py
from abc import ABC, abstractmethod

class IMicrophoneRepository(ABC):
    @abstractmethod
    def mute(self):
        """Отключает микрофон."""
        pass

    @abstractmethod
    def unmute(self):
        """Включает микрофон."""
        pass

    @abstractmethod
    def is_muted(self) -> bool:
        """Проверяет, выключен ли микрофон."""
        pass
```

---

#### 2. **`windows_microphone_manager.py`**
```python
# windows_microphone_manager.py
from .interfaces.i_microphone_repository import IMicrophoneRepository
from pycaw.pycaw import AudioUtilities

class WindowsMicrophoneManager(IMicrophoneRepository):
    def __init__(self):
        self.devices = AudioUtilities.GetMicrophone()

    def mute(self):
        self.devices.SetMute(True)

    def unmute(self):
        self.devices.SetMute(False)

    def is_muted(self) -> bool:
        return self.devices.GetMute()
```

---

#### 3. **`macos_microphone_manager.py`**
```python
# macos_microphone_manager.py
from .interfaces.i_microphone_repository import IMicrophoneRepository
import osascript  # Библиотека для выполнения AppleScript

class MacOSMicrophoneManager(IMicrophoneRepository):
    def mute(self):
        osascript.run("set volume input volume 0")

    def unmute(self):
        osascript.run("set volume input volume 50")  # Восстанавливаем громкость

    def is_muted(self) -> bool:
        result = osascript.run("input volume of (get volume settings)")
        return int(result) == 0
```

---

#### 4. **`microphone_factory.py`**
```python
# microphone_factory.py
import platform
from .microphone_managers.windows_microphone_manager import WindowsMicrophoneManager
from .microphone_managers.macos_microphone_manager import MacOSMicrophoneManager

def get_microphone_manager():
    system = platform.system()
    if system == "Windows":
        return WindowsMicrophoneManager()
    elif system == "Darwin":  # macOS
        return MacOSMicrophoneManager()
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")
```

---

#### 5. **`microphone_adapter.py`**
```python
# microphone_adapter.py
from .microphone_factory import get_microphone_manager

class MicrophoneAdapter:
    def __init__(self):
        self.manager = get_microphone_manager()  # Динамический выбор менеджера

    def toggle_mute(self):
        if self.manager.is_muted():
            self.manager.unmute()
        else:
            self.manager.mute()

    def get_status(self) -> str:
        return "Muted" if self.manager.is_muted() else "Unmuted"
```

---

#### 6. **`microphone_service.py`**
```python
# microphone_service.py
from .microphone_adapter import MicrophoneAdapter

class MicrophoneService:
    def __init__(self):
        self.adapter = MicrophoneAdapter()

    def toggle_microphone(self):
        """Переключает состояние микрофона."""
        self.adapter.toggle_mute()

    def get_microphone_status(self) -> str:
        """Возвращает текущее состояние микрофона."""
        return self.adapter.get_status()
```

---

### Как это всё работает вместе?

1. **Presentation Layer** вызывает методы сервиса:
   ```python
   # tray_service.py
   from src.application.services.microphone_service import MicrophoneService

   class TrayService:
       def __init__(self):
           self.microphone_service = MicrophoneService()

       def on_tray_icon_click(self):
           self.microphone_service.toggle_microphone()
           status = self.microphone_service.get_microphone_status()
           print(f"Microphone status: {status}")
   ```

2. **MicrophoneService** использует адаптер:
   ```python
   # microphone_service.py
   self.adapter.toggle_mute()
   ```

3. **MicrophoneAdapter** выбирает менеджер через фабрику:
   ```python
   # microphone_adapter.py
   self.manager = get_microphone_manager()
   ```

4. **Фабрика выбирает реализацию в зависимости от ОС**:
   ```python
   # microphone_factory.py
   if system == "Windows":
       return WindowsMicrophoneManager()
   elif system == "Darwin":
       return MacOSMicrophoneManager()
   ```

5. **Конкретный менеджер выполняет операции**:
   - Для Windows используется `pycaw`.
   - Для macOS используется `osascript`.

---

### Преимущества:

1. **Модульность**: Каждая ОС имеет свою реализацию, что упрощает поддержку и расширение.
2. **Гибкость**: Легко добавить поддержку новой ОС (например, Linux).
3. **Тестируемость**: Можно тестировать каждый компонент независимо.
4. **Чистота кода**: Бизнес-логика не зависит от конкретной реализации работы с микрофоном.

---

### Пример вывода:
```plaintext
Microphone status: Muted
Microphone status: Unmuted
```

Такая структура позволяет легко поддерживать разные ОС, сохраняя чистоту и модульность кода.