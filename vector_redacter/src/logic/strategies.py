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
        pass

class JsonSaveStrategy(SaveStrategy):
    def save(self, filename: str, scene) -> None:
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
        items = scene.items()[::-1]
        for item in items:
            if hasattr(item, "to_dict"):
                data["shapes"].append(item.to_dict())
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

class ImageSaveStrategy(SaveStrategy):
    def __init__(self, format_name: str = "PNG", background_color: str = "transparent"):
        self.format_name = format_name
        self.bg_color = background_color

    def save(self, filename: str, scene) -> None:
        rect = scene.sceneRect()
        width = int(rect.width())
        height = int(rect.height())
        if width <= 0 or height <= 0:
            raise ValueError("Размер сцены должен быть больше 0")
        image = QImage(width, height, QImage.Format_ARGB32)
        if self.bg_color.lower() == "transparent":
            image.fill(QColor(0, 0, 0, 0))
        else:
            image.fill(QColor(self.bg_color))
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        scene.render(painter, QRectF(image.rect()), rect)
        painter.end()
        if not image.save(filename, self.format_name):
            raise IOError(f"Не удалось сохранить изображение: {filename}")

class FileManager:
    @staticmethod
    def save_project(filename: str, data: Dict[str, Any]) -> None:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except OSError as e:
            raise IOError(f"Не удалось записать файл: {e}")

    @staticmethod
    def load_project(filename: str) -> Dict[str, Any]:
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