from model.cursorModel import CursorModel

import pytest
@pytest.fixture
def cursor():
    return CursorModel()

def test_initial_position(cursor):
    assert cursor.get_x() == 0, "Координа x при инициализации должна быть равна 0"
    assert cursor.get_y() == 0, "Координа y при инициализации должна быть равна 0"

def test_set_x(cursor):
    cursor.set_x(5)
    assert cursor.get_x() == 5, "Координа x должна быть равна 5"

def test_set_y(cursor):
    cursor.set_y(10)
    assert cursor.get_y() == 10, "Координа y должна быть равна 10"

def test_move_to(cursor):
    cursor.move_to(7, 3)
    assert cursor.get_y() == 7, "Координа y должна быть равна 7"
    assert cursor.get_x() == 3, "Координа x должна быть равна 3"

def test_move_up(cursor):
    cursor.move_to(5, 0)  # Начальная позиция
    cursor.move_up(0)
    assert cursor.get_y() == 4, "Курсор должен сместиться на одну позицию вверх (5->4)"
    for _ in range(15):
        cursor.move_up(0)
    assert cursor.get_y() == 0, "Не должно быть выхода за пределы верхней границы"

def test_move_down(cursor):
    cursor.move_to(0, 0)
    cursor.move_down(10, 0)
    assert cursor.get_y() == 1, "Курсор должен сместиться на одну позицию вниз (0->1)"
    for _ in range(15):
        cursor.move_down(10, 0)
    assert cursor.get_y() == 9, "Не должно быть выхода за пределы нижней границы"

def test_move_left(cursor):
    cursor.move_to(0, 5)  # Начальная позиция
    cursor.move_left()
    assert cursor.get_x() == 4, "Курсор должен сместиться на одну позицию влево (5->4)"
    for _ in range(15):
        cursor.move_left()  # Перемещение за пределы
    assert cursor.get_x() == 0, "Не должно быть выхода за пределы левой границы"

def test_move_right(cursor):
    cursor.move_to(0, 0)  # Начальная позиция
    cursor.move_right(10)
    assert cursor.get_x() == 1, "Курсор должен сместиться на одну позицию вправо (0->1)"
    for _ in range(15):
        cursor.move_right(10)  # Перемещение за пределы
    assert cursor.get_x() == 10, "Cursor should not move beyond the right boundary."

