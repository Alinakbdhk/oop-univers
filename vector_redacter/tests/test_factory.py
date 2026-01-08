# file: tests/test_factory.py
"""
Тесты для фабрики фигур.
"""
import pytest
from PySide6.QtCore import QPointF
from src.logic.factory import ShapeFactory
from src.logic.shapes import Rectangle, Line, Ellipse


def test_rectangle_normalization():
    """Проверяем нормализацию координат прямоугольника."""
    start = QPointF(100, 100)
    end = QPointF(10, 10)  # Тянем влево-вверх

    shape = ShapeFactory.create_shape("rect", start, end, "red")

    assert isinstance(shape, Rectangle)
    assert shape.x == 10
    assert shape.y == 10
    assert shape.w == 90
    assert shape.h == 90
    assert shape.pen().color().name().upper() == "#FF0000"


def test_line_creation():
    """Проверяем создание линии."""
    start = QPointF(0, 0)
    end = QPointF(100, 100)

    shape = ShapeFactory.create_shape("line", start, end, "blue")

    assert isinstance(shape, Line)
    assert shape.x1 == 0
    assert shape.y1 == 0
    assert shape.x2 == 100
    assert shape.y2 == 100


def test_ellipse_creation():
    """Проверяем создание эллипса."""
    start = QPointF(50, 50)
    end = QPointF(150, 150)

    shape = ShapeFactory.create_shape("ellipse", start, end, "green")

    assert isinstance(shape, Ellipse)
    assert shape.x == 50
    assert shape.y == 50
    assert shape.w == 100
    assert shape.h == 100


def test_unknown_shape():
    """Проверяем обработку неизвестного типа фигуры."""
    start = QPointF(0, 0)
    end = QPointF(10, 10)

    with pytest.raises(ValueError):
        ShapeFactory.create_shape("unknown", start, end, "black")