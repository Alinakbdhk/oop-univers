# file: main.py
"""
Главный файл для запуска приложения.
"""
import sys
from PySide6.QtWidgets import QApplication
from src.app import VectorEditorWindow
from src.constants import DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT


def main():
    """
    Главная функция приложения.
    """
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Vector Editor")
    app.setApplicationVersion("1.0")

    window = VectorEditorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()