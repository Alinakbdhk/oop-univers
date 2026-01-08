# file: src/logic/shapes.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItemGroup
from PySide6.QtGui import QPen, QColor, QPainterPath
from PySide6.QtCore import QPointF
from src.constants import DEFAULT_STROKE_WIDTH, DEFAULT_COLOR


class ShapeMeta(type(QGraphicsPathItem), type(ABC)):
    pass


class Shape(QGraphicsPathItem, ABC, metaclass=ShapeMeta):
    def __init__(self, color: str = DEFAULT_COLOR, stroke_width: int = DEFAULT_STROKE_WIDTH):
        super().__init__()
        pen = QPen(QColor(color))
        pen.setWidth(stroke_width)
        self.setPen(pen)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable)

    def set_active_color(self, color: str) -> None:
        """Базовая реализация для Листьев (Line, Rect)"""
        pen = self.pen()
        pen.setColor(QColor(color))
        self.setPen(pen)

    def set_stroke_width(self, width: int) -> None:
        """Устанавливает толщину линии для фигуры"""
        pen = self.pen()
        pen.setWidth(width)
        self.setPen(pen)

    @property
    @abstractmethod
    def type_name(self) -> str:
        """Возвращает строковый идентификатор типа фигуры ('rect', 'line')"""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Сериализация данных фигуры для сохранения в JSON"""
        pass

    @abstractmethod
    def set_geometry(self, start_point: QPointF, end_point: QPointF) -> None:
        """
        Метод для динамического обновления формы фигуры.
        Принимает две точки (старт рисования и текущее положение мыши).
        """
        pass


class Rectangle(Shape):
    def __init__(self, x: float, y: float, w: float, h: float,
                 color: str = DEFAULT_COLOR, stroke_width: int = DEFAULT_STROKE_WIDTH):
        super().__init__(color, stroke_width)
        self._x = x  # Изменили с x на _x
        self._y = y  # Изменили с y на _y
        self._w = w  # Изменили с w на _w
        self._h = h  # Изменили с h на _h
        self._create_geometry()

    def _create_geometry(self) -> None:
        path = QPainterPath()
        path.addRect(self._x, self._y, self._w, self._h)
        self.setPath(path)

    def set_geometry(self, start_point: QPointF, end_point: QPointF) -> None:
        self._x = min(start_point.x(), end_point.x())
        self._y = min(start_point.y(), end_point.y())
        self._w = abs(end_point.x() - start_point.x())
        self._h = abs(end_point.y() - start_point.y())

        path = QPainterPath()
        path.addRect(self._x, self._y, self._w, self._h)
        self.setPath(path)

    @property
    def x(self) -> float:  # Добавляем свойство для доступа
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def w(self) -> float:
        return self._w

    @property
    def h(self) -> float:
        return self._h

    @property
    def type_name(self) -> str:
        return "rect"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],
            "props": {
                "x": self._x,  # Используем _x
                "y": self._y,
                "w": self._w,
                "h": self._h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }


class Line(Shape):
    def __init__(self, x1: float, y1: float, x2: float, y2: float,
                 color: str = DEFAULT_COLOR, stroke_width: int = DEFAULT_STROKE_WIDTH):
        super().__init__(color, stroke_width)
        self._x1 = x1  # Изменили
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._create_geometry()

    def _create_geometry(self) -> None:
        path = QPainterPath()
        path.moveTo(self._x1, self._y1)
        path.lineTo(self._x2, self._y2)
        self.setPath(path)

    def set_geometry(self, start_point: QPointF, end_point: QPointF) -> None:
        self._x1 = start_point.x()
        self._y1 = start_point.y()
        self._x2 = end_point.x()
        self._y2 = end_point.y()

        path = QPainterPath()
        path.moveTo(self._x1, self._y1)
        path.lineTo(self._x2, self._y2)
        self.setPath(path)

    @property
    def x1(self) -> float:
        return self._x1

    @property
    def y1(self) -> float:
        return self._y1

    @property
    def x2(self) -> float:
        return self._x2

    @property
    def y2(self) -> float:
        return self._y2

    @property
    def type_name(self) -> str:
        return "line"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],
            "props": {
                "x1": self._x1, "y1": self._y1,
                "x2": self._x2, "y2": self._y2,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }


class Ellipse(Shape):
    def __init__(self, x: float, y: float, w: float, h: float,
                 color: str = DEFAULT_COLOR, stroke_width: int = DEFAULT_STROKE_WIDTH):
        super().__init__(color, stroke_width)
        self._x = x  # Изменили
        self._y = y
        self._w = w
        self._h = h
        self._create_geometry()

    def _create_geometry(self) -> None:
        path = QPainterPath()
        path.addEllipse(self._x, self._y, self._w, self._h)
        self.setPath(path)

    def set_geometry(self, start_point: QPointF, end_point: QPointF) -> None:
        self._x = min(start_point.x(), end_point.x())
        self._y = min(start_point.y(), end_point.y())
        self._w = abs(end_point.x() - start_point.x())
        self._h = abs(end_point.y() - start_point.y())

        path = QPainterPath()
        path.addEllipse(self._x, self._y, self._w, self._h)
        self.setPath(path)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def w(self) -> float:
        return self._w

    @property
    def h(self) -> float:
        return self._h

    @property
    def type_name(self) -> str:
        return "ellipse"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],
            "props": {
                "x": self._x, "y": self._y,
                "w": self._w, "h": self._h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }


class Group(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable, True)
        self.setHandlesChildEvents(True)

    @property
    def type_name(self) -> str:
        return "group"

    def set_geometry(self, start: QPointF, end: QPointF) -> None:
        pass

    def set_active_color(self, color: str) -> None:
        """Рекурсивно меняет цвет всех детей."""
        for child in self.childItems():
            if hasattr(child, 'set_active_color'):
                child.set_active_color(color)

    def set_stroke_width(self, width: int) -> None:
        """Рекурсивно меняет толщину всех детей."""
        for child in self.childItems():
            if hasattr(child, 'set_stroke_width'):
                child.set_stroke_width(width)

    def to_dict(self) -> Dict[str, Any]:
        children_data: List[Dict[str, Any]] = []
        for child in self.childItems():
            if hasattr(child, 'to_dict'):
                children_data.append(child.to_dict())

        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],  # Используем pos()
            "children": children_data
        }