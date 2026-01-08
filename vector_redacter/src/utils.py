# file: src/utils.py
"""
Утилиты для работы с ресурсами и путями.
"""
import sys
import os


def resource_path(relative_path: str) -> str:
    """
    Получает абсолютный путь к ресурсу.
    Работает и для dev-режима, и для PyInstaller.

    Args:
        relative_path: Относительный путь к ресурсу

    Returns:
        Абсолютный путь к ресурсу
    """
    try:
        # PyInstaller создает временную папку _MEIPASS при запуске
        base_path = sys._MEIPASS
    except Exception:
        # Если переменной нет, значит мы просто запускаем скрипт
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)