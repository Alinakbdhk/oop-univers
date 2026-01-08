from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt
from PySide6.QtGui import QUndoStack
from src.logic.tools import SelectionTool, CreationTool
from src.logic.shapes import Group
from src.logic.commands import DeleteCommand
from src.constants import (TYPE_SELECT, TYPE_LINE, TYPE_RECT, TYPE_ELLIPSE,
                          DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT)

class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT)
        self.undo_stack = QUndoStack(self)
        self.undo_stack.setUndoLimit(50)
        self.current_color = "black"
        self.tools = {
            TYPE_SELECT: SelectionTool(self, self.undo_stack),
            TYPE_RECT: CreationTool(self, TYPE_RECT, self.undo_stack, self.current_color),
            TYPE_LINE: CreationTool(self, TYPE_LINE, self.undo_stack, self.current_color),
            TYPE_ELLIPSE: CreationTool(self, TYPE_ELLIPSE, self.undo_stack, self.current_color)
        }
        self.current_tool = self.tools[TYPE_SELECT]
        self.setMouseTracking(True)

    def group_selection(self):
        selected_items = self.scene.selectedItems()
        if len(selected_items) < 2:
            return
        group = Group()
        self.scene.addItem(group)
        for item in selected_items:
            item.setSelected(False)
            group.addToGroup(item)
        group.setSelected(True)
        print("Группа создана")

    def ungroup_selection(self):
        selected_items = self.scene.selectedItems()
        for item in selected_items:
            if isinstance(item, Group):
                self.scene.destroyItemGroup(item)
                print("Группа расформирована")

    def delete_selected(self):
        selected = self.scene.selectedItems()
        if not selected:
            return
        self.undo_stack.beginMacro("Delete Selection")
        for item in selected:
            cmd = DeleteCommand(self.scene, item)
            self.undo_stack.push(cmd)
        self.undo_stack.endMacro()

    def set_tool(self, tool_name: str):
        if tool_name in self.tools:
            self.current_tool = self.tools[tool_name]
            if tool_name == TYPE_SELECT:
                self.setCursor(Qt.CursorShape.ArrowCursor)
            else:
                self.setCursor(Qt.CursorShape.CrossCursor)

    def set_color(self, color_name: str):
        self.current_color = color_name
        print(f"Canvas: установлен цвет {color_name}")
        for tool_name, tool in self.tools.items():
            if isinstance(tool, CreationTool):
                tool.color = color_name

    def mousePressEvent(self, event):
        if self.current_tool == self.tools[TYPE_SELECT]:
            item = self.itemAt(event.pos())
            if not item:
                self.scene.clearSelection()
        self.current_tool.mouse_press(event)

    def mouseMoveEvent(self, event):
        self.current_tool.mouse_move(event)

    def mouseReleaseEvent(self, event):
        self.current_tool.mouse_release(event)