# file: src/app.py
"""
Главное окно приложения.
"""
import json
from typing import Optional
from PySide6.QtGui import QCloseEvent, QAction
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QWidget,
                               QHBoxLayout, QFrame, QVBoxLayout, QPushButton,
                               QColorDialog, QFileDialog)
from PySide6.QtGui import QColor, QKeySequence, QIcon
from src.constants import (DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT,
                           TYPE_SELECT, TYPE_LINE, TYPE_RECT, TYPE_ELLIPSE)
from src.widgets.canvas import EditorCanvas
from src.widgets.properties import PropertiesPanel
from src.logic.strategies import JsonSaveStrategy, ImageSaveStrategy, FileManager
from src.logic.factory import ShapeFactory


class VectorEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Window Created: Конструктор отработал")

        self.setWindowTitle("Vector Editor")
        self.resize(1200, 600)

        # Создание виджетов
        self._create_tool_buttons()
        self._create_canvas()
        self._init_ui()

    def _create_tool_buttons(self):
        """Создает кнопки инструментов."""
        self.btn_select = QPushButton("Select")
        self.btn_line = QPushButton("Line")
        self.btn_rect = QPushButton("Rect")
        self.btn_ellipse = QPushButton("Ellipse")
        self.btn_color = QPushButton("Выбрать цвет")

        self.current_color = QColor("black")
        self._update_color_button()

        # Делаем кнопки переключаемыми
        for btn in [self.btn_select, self.btn_line, self.btn_rect, self.btn_ellipse]:
            btn.setCheckable(True)

        self.btn_select.setChecked(True)

        # Подключаем сигналы
        self.btn_select.clicked.connect(lambda: self.on_change_tool(TYPE_SELECT))
        self.btn_line.clicked.connect(lambda: self.on_change_tool(TYPE_LINE))
        self.btn_rect.clicked.connect(lambda: self.on_change_tool(TYPE_RECT))
        self.btn_ellipse.clicked.connect(lambda: self.on_change_tool(TYPE_ELLIPSE))
        self.btn_color.clicked.connect(self.on_select_color)

    def _create_canvas(self):
        """Создает холст."""
        self.current_tool = TYPE_SELECT
        self.canvas = EditorCanvas()
        self.canvas.scene.setSceneRect(0, 0, DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT)
        self.canvas.set_color(self.current_color.name())
        self.canvas.set_tool(self.current_tool)

    def _init_ui(self):
        """Инициализирует пользовательский интерфейс."""
        self.statusBar().showMessage("Готов к работе")
        self._create_menus()
        self._create_toolbar()
        self._setup_layout()

    def _create_menus(self):
        """Создает меню."""
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("&File")

        # Open Action
        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.on_open_clicked)
        file_menu.addAction(open_action)

        # Save Actions
        save_action = QAction("&Save Project...", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.on_save_project_clicked)
        file_menu.addAction(save_action)

        export_png_action = QAction("&Export as PNG...", self)
        export_png_action.triggered.connect(lambda: self.on_export_image_clicked("PNG"))
        file_menu.addAction(export_png_action)

        export_jpg_action = QAction("&Export as JPG...", self)
        export_jpg_action.triggered.connect(lambda: self.on_export_image_clicked("JPG"))
        file_menu.addAction(export_jpg_action)

        file_menu.addSeparator()

        # Exit Action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Close the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")

        # Undo/Redo Actions
        stack = self.canvas.undo_stack
        undo_action = stack.createUndoAction(self, "&Undo")
        undo_action.setShortcut(QKeySequence.Undo)

        redo_action = stack.createRedoAction(self, "&Redo")
        redo_action.setShortcut(QKeySequence.Redo)

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()

        # Group/Ungroup Actions
        group_action = QAction("&Group", self)
        group_action.setShortcut(QKeySequence("Ctrl+G"))
        group_action.triggered.connect(self.canvas.group_selection)

        ungroup_action = QAction("&Ungroup", self)
        ungroup_action.setShortcut(QKeySequence("Ctrl+U"))
        ungroup_action.triggered.connect(self.canvas.ungroup_selection)

        edit_menu.addAction(group_action)
        edit_menu.addAction(ungroup_action)
        edit_menu.addSeparator()

        # Delete Action
        delete_action = QAction("&Delete", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.canvas.delete_selected)
        self.addAction(delete_action)
        edit_menu.addAction(delete_action)

    def _create_toolbar(self):
        """Создает панель инструментов."""
        toolbar = self.addToolBar("Main Toolbar")

        # Получаем действия из стека отмены
        stack = self.canvas.undo_stack
        undo_action = stack.createUndoAction(self, "Undo")
        redo_action = stack.createRedoAction(self, "Redo")

        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)
        toolbar.addSeparator()

        # Группировка
        group_action = QAction("Group", self)
        group_action.triggered.connect(self.canvas.group_selection)
        toolbar.addAction(group_action)

        ungroup_action = QAction("Ungroup", self)
        ungroup_action.triggered.connect(self.canvas.ungroup_selection)
        toolbar.addAction(ungroup_action)

        toolbar.addSeparator()

        # Удаление
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.canvas.delete_selected)
        toolbar.addAction(delete_action)

    def _setup_layout(self):
        """Настраивает компоновку окна."""
        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Левая панель инструментов
        tools_panel = QFrame()
        tools_panel.setFixedWidth(150)
        tools_panel.setStyleSheet("background-color: #f0f0f0;")

        tools_layout = QVBoxLayout(tools_panel)
        tools_layout.addWidget(self.btn_select)
        tools_layout.addWidget(self.btn_line)
        tools_layout.addWidget(self.btn_rect)
        tools_layout.addWidget(self.btn_ellipse)
        tools_layout.addWidget(self.btn_color)
        tools_layout.addStretch()

        # Панель свойств
        self.props_panel = PropertiesPanel(self.canvas.scene, self.canvas.undo_stack)

        # Добавляем все панели в основной layout
        main_layout.addWidget(tools_panel)
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(self.props_panel)

    def on_change_tool(self, tool_name: str):
        """Обработчик смены инструмента."""
        self.current_tool = tool_name
        print(f"Выбран инструмент: {tool_name}")

        # Сбрасываем все кнопки
        for btn in [self.btn_select, self.btn_line, self.btn_rect, self.btn_ellipse]:
            btn.setChecked(False)

        # Устанавливаем активную кнопку
        if tool_name == TYPE_SELECT:
            self.btn_select.setChecked(True)
        elif tool_name == TYPE_LINE:
            self.btn_line.setChecked(True)
        elif tool_name == TYPE_RECT:
            self.btn_rect.setChecked(True)
        elif tool_name == TYPE_ELLIPSE:
            self.btn_ellipse.setChecked(True)

        self.canvas.set_tool(tool_name)

    def on_select_color(self):
        """Обработчик выбора цвета."""
        color = QColorDialog.getColor(self.current_color, self, "Выберите цвет")

        if color.isValid():
            self.current_color = color
            self._update_color_button()
            self.canvas.set_color(color.name())
            print(f"Выбран цвет: {color.name()}")

    def _update_color_button(self):
        """Обновляет внешний вид кнопки цвета."""
        self.btn_color.setText(f"Цвет: {self.current_color.name()}")
        self.btn_color.setStyleSheet(f"color: {self.current_color.name()};")

    def on_save_project_clicked(self):
        """Обработчик сохранения проекта."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Сохранить проект", "",
            "Vector Project (*.json *.vec);;All Files (*)"
        )

        if not filename:
            return

        # Добавляем расширение .vec если его нет
        if not filename.lower().endswith(('.json', '.vec')):
            filename += '.vec'

        try:
            strategy = JsonSaveStrategy()
            strategy.save(filename, self.canvas.scene)
            self.statusBar().showMessage(f"Проект сохранен: {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка сохранения",
                                 f"Не удалось сохранить проект:\n{str(e)}")

    def on_export_image_clicked(self, format_name: str = "PNG"):
        """Обработчик экспорта в изображение."""
        filters = {
            "PNG": "PNG Image (*.png)",
            "JPG": "JPEG Image (*.jpg)"
        }

        filename, _ = QFileDialog.getSaveFileName(
            self, f"Экспорт в {format_name}", "",
            filters.get(format_name, "All Files (*)")
        )

        if not filename:
            return

        # Добавляем расширение если его нет
        if format_name == "PNG" and not filename.lower().endswith('.png'):
            filename += '.png'
        elif format_name == "JPG" and not filename.lower().endswith(('.jpg', '.jpeg')):
            filename += '.jpg'

        try:
            bg_color = "white" if format_name == "JPG" else "transparent"
            strategy = ImageSaveStrategy(format_name, bg_color)
            strategy.save(filename, self.canvas.scene)
            self.statusBar().showMessage(f"Изображение сохранено: {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка экспорта",
                                 f"Не удалось экспортировать изображение:\n{str(e)}")

    def on_open_clicked(self):
        """Обработчик открытия проекта."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Открыть проект", "",
            "Vector Project (*.json *.vec);;All Files (*)"
        )

        if not filename:
            return

        try:
            # Загружаем данные из файла
            data = FileManager.load_project(filename)

            # Проверяем структуру файла
            if "shapes" not in data:
                raise ValueError("Некорректный формат файла")

            # Очищаем сцену и историю
            self.canvas.scene.clear()
            self.canvas.undo_stack.clear()

            # Восстанавливаем размер сцены
            scene_info = data.get("scene", {})
            width = scene_info.get("width", DEFAULT_SCENE_WIDTH)
            height = scene_info.get("height", DEFAULT_SCENE_HEIGHT)
            self.canvas.scene.setSceneRect(0, 0, width, height)

            # Восстанавливаем фигуры
            shapes_data = data.get("shapes", [])
            errors_count = 0

            for shape_dict in shapes_data:
                try:
                    shape_obj = ShapeFactory.from_dict(shape_dict)
                    self.canvas.scene.addItem(shape_obj)
                except Exception as e:
                    print(f"Ошибка загрузки фигуры: {e}")
                    errors_count += 1

            # Обновляем статус
            if errors_count > 0:
                self.statusBar().showMessage(
                    f"Загружено с ошибками ({errors_count} фигур пропущено)")
            else:
                self.statusBar().showMessage(f"Проект загружен: {filename}")

        except FileNotFoundError as e:
            QMessageBox.critical(self, "Ошибка", f"Файл не найден:\n{str(e)}")
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка",
                                 f"Некорректный формат файла:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки",
                                 f"Не удалось загрузить проект:\n{str(e)}")

    def closeEvent(self, event: QCloseEvent):
        """Обработчик закрытия окна."""
        print("Попытка закрыть окно...")

        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите выйти?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            print("Window Closed: Разрешаем закрытие")
            event.accept()
        else:
            print("Отмена закрытия")
            event.ignore()