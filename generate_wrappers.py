import os
from comtypes.client import GetModule
from traceback import print_exc

print("Генерация Python-оберток для системных библиотек...")

try:
    # Главный источник PKEY констант
    print("Обработка propsys.dll...")
    # GetModule(os.path.join(os.environ["SystemRoot"], "System32", "MMDeviceAPI.dll"))
    GetModule(os.path.join(os.environ["SystemRoot"], "System32", "propsys.dll"))
    # GetModule(r"C:\Windows\System32\propsys.dll")
    print(" -> Успешно.")

    # Источник специфичных для аудио интерфейсов и констант
    print("Обработка MMDeviceAPI.dll...")
    # Этот вызов может быть не нужен, если propsys уже все сгенерировал,
    # но для полноты картины он важен.
    GetModule(os.path.join(os.environ["SystemRoot"], "System32", "MMDeviceAPI.dll"))
    print(" -> Успешно.")

    print("\nГенерация завершена!")
    print("Проверьте папку 'comtypes/gen' в вашей среде Python.")
    print("Она может находиться, например, тут: C:\\Python39\\Lib\\site-packages\\comtypes\\gen")

except Exception as e:
    print(f"\nПроизошла ошибка: {e}")
    print("Возможно, вам нужно запустить этот скрипт с правами администратора.")
    print_exc()