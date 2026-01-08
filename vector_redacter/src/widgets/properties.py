# file: src/widgets/properties.py
# file: src/widgets/properties.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                               QSpinBox, QPushButton, QColorDialog, QFrame,
                               QDoubleSpinBox, QHBoxLayout)
from PySide6.QtCore import Qt
from src.logic.commands import ChangeColorCommand, ChangeWidthCommand


class PropertiesPanel(QWidget):
    def __init__(self, scene, undo_stack):
        super().__init__()
        self.scene = scene
        self.undo_stack = undo_stack
        self._is_cleanup = False

        self._init_ui()

        if self.scene:
            self.scene.selectionChanged.connect(self.on_selection_changed)

    def _init_ui(self):
        self.setFixedWidth(250)
        self.setStyleSheet("background-color: #f0f0f0; border-left: 1px solid #ccc;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Свойства")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        self.lbl_type = QLabel("Тип: Не выбрано")
        layout.addWidget(self.lbl_type)

        # Поля X и Y
        layout.addWidget(QLabel("Позиция:"))
        geo_layout = QHBoxLayout()

        self.spin_x = QDoubleSpinBox()
        self.spin_x.setRange(-10000, 10000)
        self.spin_x.setPrefix("X: ")
        self.spin_x.valueChanged.connect(self.on_geo_changed)

        self.spin_y = QDoubleSpinBox()
        self.spin_y.setRange(-10000, 10000)
        self.spin_y.setPrefix("Y: ")
        self.spin_y.valueChanged.connect(self.on_geo_changed)

        geo_layout.addWidget(self.spin_x)
        geo_layout.addWidget(self.spin_y)
        layout.addLayout(geo_layout)

        layout.addWidget(QLabel("Толщина обводки:"))
        self.spin_width = QSpinBox()
        self.spin_width.setRange(1, 50)
        self.spin_width.valueChanged.connect(self.on_width_changed)
        layout.addWidget(self.spin_width)

        layout.addWidget(QLabel("Цвет линии:"))
        self.btn_color = QPushButton()
        self.btn_color.setFixedHeight(30)
        self.btn_color.clicked.connect(self.on_color_clicked)
        layout.addWidget(self.btn_color)

        layout.addStretch()
        self.setEnabled(False)

    def on_selection_changed(self):
        if self._is_cleanup or self.scene is None:
            self.setEnabled(False)
            return

        try:
            selected_items = self.scene.selectedItems()
        except (RuntimeError, AttributeError):
            self.setEnabled(False)
            return

        if not selected_items:
            self.setEnabled(False)
            self.lbl_type.setText("Тип: Не выбрано")
            self.spin_x.setValue(0)
            self.spin_y.setValue(0)
            self.spin_width.setValue(1)
            self.btn_color.setStyleSheet("background-color: transparent")
            return

        self.setEnabled(True)
        item = selected_items[0]

        # Определяем тип объекта
        type_text = "Объект"
        if hasattr(item, "type_name"):
            type_text = item.type_name.capitalize()
        else:
            type_text = type(item).__name__

        if len(selected_items) > 1:
            type_text += f" (+{len(selected_items) - 1})"

        self.lbl_type.setText(f"Тип: {type_text}")

        # Обновляем X и Y - используем pos() для получения позиции
        self.spin_x.blockSignals(True)
        self.spin_y.blockSignals(True)
        self.spin_x.setValue(item.pos().x())
        self.spin_y.setValue(item.pos().y())
        self.spin_x.blockSignals(False)
        self.spin_y.blockSignals(False)

        # Обновляем ширину с проверкой на смешанные значения
        self.update_width_ui(selected_items)

        # Обновляем цвет
        current_color = "#000000"
        if hasattr(item, "pen") and item.pen() is not None:
            current_color = item.pen().color().name()

        self.btn_color.setStyleSheet(
            f"background-color: {current_color}; border: 1px solid gray;")

    def update_width_ui(self, selected_items):
        self.spin_width.blockSignals(True)

        first_width = -1
        is_mixed = False

        for i, item in enumerate(selected_items):
            if not hasattr(item, "pen"):
                continue

            w = item.pen().width()

            if i == 0:
                first_width = w
            else:
                if w != first_width:
                    is_mixed = True
                    break

        if is_mixed:
            self.spin_width.setValue(first_width)
            self.spin_width.setStyleSheet("background-color: #fffacd;")
            self.spin_width.setToolTip("Выбраны объекты с разной толщиной")
        else:
            self.spin_width.setValue(first_width)
            self.spin_width.setStyleSheet("")
            self.spin_width.setToolTip("")

        self.spin_width.blockSignals(False)

    def on_width_changed(self, value):
        if self._is_cleanup or self.scene is None:
            return

        try:
            selected_items = self.scene.selectedItems()
        except (RuntimeError, AttributeError):
            return

        if not selected_items:
            return

        self.undo_stack.beginMacro("Change Width All")

        for item in selected_items:
            cmd = ChangeWidthCommand(item, value)
            self.undo_stack.push(cmd)

        self.undo_stack.endMacro()

        if self.scene:
            try:
                self.scene.update()
            except:
                pass

    def on_geo_changed(self, value):
        if self._is_cleanup or self.scene is None:
            return

        try:
            selected_items = self.scene.selectedItems()
        except (RuntimeError, AttributeError):
            return

        if not selected_items:
            return

        new_x = self.spin_x.value()
        new_y = self.spin_y.value()

        # Используем setPos() для установки позиции
        for item in selected_items:
            item.setPos(new_x, new_y)

        if self.scene:
            try:
                self.scene.update()
            except:
                pass

    def on_color_clicked(self):
        if self._is_cleanup or self.scene is None:
            return

        try:
            selected_items = self.scene.selectedItems()
        except (RuntimeError, AttributeError):
            return

        if not selected_items:
            return

        color = QColorDialog.getColor(title="Выберите цвет линии")

        if color.isValid():
            hex_color = color.name()

            self.btn_color.setStyleSheet(
                f"background-color: {hex_color}; border: 1px solid gray;")

            self.undo_stack.beginMacro("Change Color All")

            for item in selected_items:
                cmd = ChangeColorCommand(item, hex_color)
                self.undo_stack.push(cmd)

            self.undo_stack.endMacro()

            if self.scene:
                try:
                    self.scene.update()
                except:
                    pass

    def cleanup(self):
        self._is_cleanup = True
        self.scene = None
        self.setEnabled(False)

        try:
            self.spin_x.valueChanged.disconnect()
            self.spin_y.valueChanged.disconnect()
            self.spin_width.valueChanged.disconnect()
            self.btn_color.clicked.disconnect()
        except:
            pass