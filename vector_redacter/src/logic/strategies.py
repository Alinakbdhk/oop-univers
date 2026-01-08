# file: src/logic/strategies.py
"""
Стратегии сохранения данных (паттерн Strategy).
"""
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
from PySide6.QtGui import QImage, QPainter, QColor
from PySide6.QtCore import QRectF
from src.constants import PROJECT_VERSION, APP_NAME


class SaveStrategy(ABC):
    @abstractmethod
    def save(self, filename: str, scene) -> None:
        """
        Сохраняет данные в файл.

        Args:
            filename: Путь к файлу
            scene: Объект QGraphicsScene
        """
        pass


class JsonSaveStrategy(SaveStrategy):
    """Стратегия сохранения в JSON формат."""

    def save(self, filename: str, scene) -> None:
        # Подготовка структуры
        data: Dict[str, Any] = {
            "meta": {
                "version": PROJECT_VERSION,
                "app": APP_NAME,
                "created_at": datetime.now().isoformat()
            },
            "scene": {
                "width": scene.width(),
                "height": scene.height()
            },
            "shapes": []
        }

        # Сбор объектов в правильном порядке для Z-index
        items = scene.items()[::-1]  # Инвертируем порядок

        for item in items:
            if hasattr(item, "to_dict"):
                data["shapes"].append(item.to_dict())

        # Запись в файл
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


class ImageSaveStrategy(SaveStrategy):
    """Стратегия сохранения в изображение."""

    def __init__(self, format_name: str = "PNG", background_color: str = "transparent"):
        """
        Args:
            format_name: Формат изображения (PNG, JPG, BMP)
            background_color: Цвет фона или "transparent"
        """
        self.format_name = format_name
        self.bg_color = background_color

    def save(self, filename: str, scene) -> None:
        # Определяем размер картинки
        rect = scene.sceneRect()
        width = int(rect.width())
        height = int(rect.height())

        if width <= 0 or height <= 0:
            raise ValueError("Размер сцены должен быть больше 0")

        # Создаем буфер изображения
        image = QImage(width, height, QImage.Format_ARGB32)

        # Заливка фона
        if self.bg_color.lower() == "transparent":
            image.fill(QColor(0, 0, 0, 0))  # Прозрачный
        else:
            image.fill(QColor(self.bg_color))

        # Рендеринг
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Рендерим сцену
        scene.render(painter, QRectF(image.rect()), rect)

        painter.end()

        # Сохранение на диск
        if not image.save(filename, self.format_name):
            raise IOError(f"Не удалось сохранить изображение: {filename}")


class FileManager:
    """Менеджер файлов для работы с проектами."""

    @staticmethod
    def save_project(filename: str, data: Dict[str, Any]) -> None:
        """
        Сохраняет проект в файл.

        Args:
            filename: Полный путь к файлу
            data: Словарь с данными проекта

        Raises:
            IOError: Если не удалось записать файл
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except OSError as e:
            raise IOError(f"Не удалось записать файл: {e}")

    @staticmethod
    def load_project(filename: str) -> Dict[str, Any]:
        """
        Загружает проект из файла.

        Args:
            filename: Полный путь к файлу

        Returns:
            Словарь с данными проекта

        Raises:
            FileNotFoundError: Если файл не найден
            ValueError: Если файл поврежден
            IOError: Если ошибка чтения
        """
        import os

        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл не найден: {filename}")

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Файл поврежден или имеет неверный формат")
        except OSError as e:
            raise IOError(f"Ошибка чтения файла: {e}")