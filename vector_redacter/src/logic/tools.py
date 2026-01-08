# file: src/logic/tools.py
from abc import ABC, abstractmethod
from src.logic.factory import ShapeFactory
from src.logic.commands import AddShapeCommand, MoveCommand
from PySide6.QtCore import Qt, QPointF
from PySide6.QtWidgets import QGraphicsView


class Tool(ABC):
    def __init__(self, view, undo_stack):
        self.view = view
        self.scene = view.scene
        self.undo_stack = undo_stack

    @abstractmethod
    def mouse_press(self, event):
        pass

    @abstractmethod
    def mouse_move(self, event):
        pass

    @abstractmethod
    def mouse_release(self, event):
        pass


class CreationTool(Tool):
    def __init__(self, view, shape_type: str, undo_stack, color: str = "black"):
        super().__init__(view, undo_stack)
        self.shape_type = shape_type
        self.color = color
        self.start_pos = None
        self.temp_shape = None

    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = self.view.mapToScene(event.pos())

            try:
                self.temp_shape = ShapeFactory.create_shape(
                    self.shape_type,
                    self.start_pos,
                    self.start_pos,
                    self.color
                )
                self.scene.addItem(self.temp_shape)
            except ValueError:
                pass

    def mouse_move(self, event):
        if self.temp_shape and self.start_pos:
            current_pos = self.view.mapToScene(event.pos())
            self.temp_shape.set_geometry(self.start_pos, current_pos)

    def mouse_release(self, event):
        if event.button() == Qt.LeftButton and self.temp_shape:
            end_pos = self.view.mapToScene(event.pos())

            self.scene.removeItem(self.temp_shape)
            self.temp_shape = None

            try:
                final_shape = ShapeFactory.create_shape(
                    self.shape_type,
                    self.start_pos,
                    end_pos,
                    self.color
                )

                command = AddShapeCommand(self.scene, final_shape)
                self.undo_stack.push(command)

                print(f"Command pushed: {command.text()}")

            except ValueError:
                pass

            self.start_pos = None

        QGraphicsView.mouseReleaseEvent(self.view, event)


class SelectionTool(Tool):
    def __init__(self, view, undo_stack):
        super().__init__(view, undo_stack)
        self.item_positions = {}

    def mouse_press(self, event):
        QGraphicsView.mousePressEvent(self.view, event)

        self.item_positions.clear()
        for item in self.scene.selectedItems():
            self.item_positions[item] = item.pos()

    def mouse_move(self, event):
        QGraphicsView.mouseMoveEvent(self.view, event)

    def mouse_release(self, event):
        QGraphicsView.mouseReleaseEvent(self.view, event)

        moved_items = []
        for item, old_pos in self.item_positions.items():
            new_pos = item.pos()
            if new_pos != old_pos:
                moved_items.append((item, old_pos, new_pos))

        if moved_items:
            self.undo_stack.beginMacro("Move Items")

            for item, old_pos, new_pos in moved_items:
                cmd = MoveCommand(item, old_pos, new_pos)
                self.undo_stack.push(cmd)

            self.undo_stack.endMacro()

        self.item_positions.clear()