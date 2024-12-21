import pytest
from model.mainModel import MainModel
import os

@pytest.fixture
def main_model():
    """Создает экземпляр MainModel для тестов."""
    return MainModel()

def test_open_file(main_model):
    f = open("model/tests/test_files/test_not_empty.txt", "w+")
    f.write("Line 1\nLine 2\nLine 3")
    f.close()

    main_model.text_model.command_line = main_model.text_model.get_mystring("model/tests/test_files/test_not_empty.txt")

    # Базовый сценарий
    main_model.open_file()
    # os.remove("test_not_empty.txt")
    assert len(main_model.text_model.lines) == 3
    assert main_model.text_model.lines[0].c_str() == "Line 1"
    assert main_model.text_model.lines[1].c_str() == "Line 2"
    assert main_model.text_model.lines[2].c_str() == "Line 3"
    
    f = open("model/tests/test_files/test_empty.txt", "w+")
    f.close()

    main_model.text_model.command_line = main_model.text_model.get_mystring("model/tests/test_files/test_empty.txt")
    main_model.open_file()
    assert len(main_model.text_model.lines) == 0

    # f = open("model/tests/test_files/random_file", "r")
    # f.close()
    main_model.text_model.command_line = main_model.text_model.get_mystring("model/tests/test_files/random_file")
    main_model.open_file()
    assert len(main_model.text_model.lines) == 0

def test_write_file(main_model):
    # Запись в текущий файл
    main_model.filename = main_model.text_model.get_mystring("model/tests/test_files/test_empty_write.txt")

    main_model.text_model.lines = [main_model.text_model.get_mystring("Write to current file: Line 1"), main_model.text_model.get_mystring("Write to current file: Line 2")]
    main_model.write_file()
    assert os.path.exists("model/tests/test_files/test_empty_write.txt")
    f = open("model/tests/test_files/test_empty_write.txt")
    assert all(line.c_str() == f.readline().rstrip('\n') for line in main_model.text_model.lines)
    f.close()

    # Запись в переданный файл через команду
    main_model.filename = main_model.text_model.get_mystring("model/tests/test_files/test_empty_write.txt")
    main_model.text_model.command_line = main_model.text_model.get_mystring("model/tests/test_files/test_empty_write_new_file.txt")

    main_model.text_model.lines = [main_model.text_model.get_mystring("Write to new file:  Line 1"), main_model.text_model.get_mystring("Write to new file: Line 2")]
    main_model.write_file()

    assert main_model.filename.c_str() != "model/tests/test_files/test_empty_write_new_file.txt"
    assert os.path.exists("model/tests/test_files/test_empty_write_new_file.txt")
    f = open("model/tests/test_files/test_empty_write_new_file.txt")
    assert all(line.c_str() == f.readline().rstrip('\n') for line in main_model.text_model.lines)
    f.close()


def test_move_to_line(main_model):
    """Тест перемещения на строку: существующая строка, несуществующая строка."""
    main_model.text_model.lines = [main_model.text_model.get_mystring(f"Line {i}") for i in range(5)]
    
    # Существующая строка
    main_model.move_to_line(3)
    assert main_model.cursor_model.get_y() == 3

    # Несуществующая строка
    main_model.move_to_line(10)
    assert main_model.cursor_model.get_y() != 10  # Положение курсора не меняется

def test_input_char(main_model):
    """Тест ввода символов: в текст, в командную строку."""
    # Ввод в текст
    main_model.input_char("A")
    assert main_model.text_model.lines[0].c_str() == "A"

    # Ввод в командную строку
    main_model.change_display("bar")
    main_model.input_char("B", bar=True)
    assert main_model.text_model.command_line.c_str() == "B"

def test_search(main_model):
    """Тест поиска текста: вперед и назад, строка найдена, строка не найдена."""
    main_model.text_model.lines = [
        main_model.text_model.get_mystring("Hello world"),
        main_model.text_model.get_mystring("Another line"),
    ]

    # Поиск вперед
    assert main_model.search("world", "forward")
    assert (main_model.cursor_model.get_y(), main_model.cursor_model.get_x()) == (0, 6)

    # Поиск назад
    main_model.cursor_model.move_to(1, 11)
    assert main_model.search("Another", "backward")
    assert (main_model.cursor_model.get_y(), main_model.cursor_model.get_x()) == (1, 0)

    # Поиск несуществующей строки
    assert not main_model.search("notfound", "forward")

def test_repeat_search(main_model):
    """Тест повторного поиска: направление вперед, назад."""
    main_model.text_model.lines = [main_model.text_model.get_mystring("Hello world"), main_model.text_model.get_mystring("Another line")]
    main_model.search("world", "forward")

    # Повторный поиск вперед
    main_model.repeat_search()
    assert main_model.cursor_model.get_y() == 0
    assert main_model.cursor_model.get_x() == 6

    # Повторный поиск назад
    main_model.repeat_search(reverse=True)
    assert main_model.cursor_model.get_y() == 0
    assert main_model.cursor_model.get_x() == 6

def test_delete_char(main_model):
    """Тест удаления символа: в тексте, в командной строке."""
    # main_model.text_model.lines = [main_model.text_model.get_mystring("Hello")]
    main_model.input_char('H', False)
    main_model.input_char('e', False)
    main_model.input_char('l', False)
    main_model.input_char('l', False)
    main_model.input_char('o', False)
    
    # Удаление символа в тексте
    main_model.delete_char()
    assert main_model.text_model.lines[0].c_str() == "Hell"

    # Удаление символа в командной строке
    main_model.change_display("bar")
    # main_model.text_model.command_line = main_model.text_model.get_mystring("Hello")
    main_model.input_char('H', True)
    main_model.input_char('e', True)
    main_model.input_char('l', True)
    main_model.input_char('l', True)
    main_model.input_char('o', True)
    
    main_model.delete_char(command=True)
    
    assert main_model.text_model.command_line.c_str() == "Hell"

def test_cut_current_line(main_model):
    """Тест вырезания строки: существующая строка, последняя строка."""
    main_model.text_model.lines = [
        main_model.text_model.get_mystring("Line 1"),
        main_model.text_model.get_mystring("Line 2"),
    ]

    # Вырезание существующей строки
    main_model.cut_current_line()
    assert main_model.text_model.lines[0].c_str() == "Line 2"
    assert main_model.get_clipboard().c_str() == "Line 1"

    # Вырезание последней строки
    main_model.cursor_model.set_y(0)

    main_model.cut_current_line()
    assert len(main_model.text_model.lines) == 0
    assert main_model.get_clipboard().c_str() == "Line 2"

def test_copy_current_line(main_model):
    """Тест копирования строки: копирование первой и последней строк."""
    main_model.text_model.lines = [main_model.text_model.get_mystring("Line 1")]

    # Копирование строки
    main_model.copy_current_line()
    assert main_model.get_clipboard().c_str() == "Line 1"

def test_paste_after_cursor(main_model):
    """Тест вставки текста: после курсора, в конец строки."""
    main_model.input_char('H', False)
    main_model.input_char('e', False)
    main_model.input_char('l', False)
    main_model.input_char('l', False)
    main_model.input_char('o', False)
    
    main_model.copy_current_line()
    # Вставка после курсора
    main_model.paste_after_cursor()
    assert main_model.text_model.lines[0].c_str() == "HelloHello"

def test_move_cursor(main_model):
    """Тестирование перемещения курсора во всех направлениях."""
    # Устанавливаем начальное состояние текста
    main_model.text_model.lines = [
        main_model.text_model.get_mystring("Line 1"),
        main_model.text_model.get_mystring("Line 2"),
        main_model.text_model.get_mystring("Line 3"),
    ]
    main_model.cursor_model.move_to(1, 3)  # Начальная позиция курсора: строка 1, символ 3

    # Тестируем движение вверх
    main_model.move_cursor('up')
    assert main_model.cursor_model.get_y() == 0  # Переместился на строку выше
    assert main_model.cursor_model.get_x() == 3  # Координата X сохранилась

    # Тестируем движение вниз
    main_model.move_cursor('down')
    assert main_model.cursor_model.get_y() == 1  # Вернулся на строку 1
    assert main_model.cursor_model.get_x() == 3  # Координата X сохранилась

    # Тестируем движение влево
    main_model.move_cursor('left')
    assert main_model.cursor_model.get_y() == 1
    assert main_model.cursor_model.get_x() == 2  # Переместился на символ левее

    # Тестируем движение вправо
    main_model.move_cursor('right')
    assert main_model.cursor_model.get_y() == 1
    assert main_model.cursor_model.get_x() == 3  # Вернулся на символ 3

    # Тестируем переход в начало строки
    main_model.move_cursor('start_string')
    assert main_model.cursor_model.get_x() == 0  # Курсор в начале строки

    # Тестируем переход в конец строки
    main_model.move_cursor('end_string')
    assert main_model.cursor_model.get_x() == len(main_model.text_model.lines[1].c_str())  # В конец строки 1

    # Тестируем переход к началу файла
    main_model.move_cursor('start_file')
    assert main_model.cursor_model.get_y() == 0  # В начало текста
    assert main_model.cursor_model.get_x() == 0  # В начало строки

    # Тестируем переход к концу файла
    main_model.move_cursor('end_file')
    assert main_model.cursor_model.get_y() == len(main_model.text_model.lines) - 1  # На последнюю строку
    assert main_model.cursor_model.get_x() == len(main_model.text_model.lines[-1].c_str())  # В конец строки

    # Тестируем переход к номеру строки
    main_model.move_cursor('num_string', '2')
    assert main_model.cursor_model.get_y() == 1  # Переместился на строку 2 (индекс 1)
    assert main_model.cursor_model.get_x() == 0  # В начало строки

    # Тестируем переход к началу слова
    main_model.cursor_model.move_to(0, 4)  # Позиция курсора на строке 0, после слова
    main_model.move_cursor('start_word')
    assert main_model.cursor_model.get_x() == 0  # К началу слова "Line"

    # Тестируем переход к концу слова
    main_model.move_cursor('end_word')
    assert main_model.cursor_model.get_x() == 4  # К концу слова "Line"