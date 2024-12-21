from model.textModel import TextModel

import pytest

@pytest.fixture
def text_model():
    """Создает экземпляр TextModel для тестирования."""
    return TextModel()

def test_insert_char(text_model):
    """Тест вставки символа в строку."""
    text_model.insert_char(0, 0, 'A')
    assert text_model.lines[0].c_str() == 'A'
    
    text_model.insert_char(0, 1, 'B')
    assert text_model.lines[0].c_str() == 'AB'
    
    text_model.insert_char(0, 1, 'C')
    assert text_model.lines[0].c_str() == 'ACB'


def test_delete_char(text_model):
    """Тест удаления символов."""
    text_model.insert_char(0, 0, 'Hello')
    text_model.delete_char(0, 1, 3)
    assert text_model.lines[0].c_str() == 'Ho'
    
    text_model.delete_char(0, 0)
    assert text_model.lines[0].c_str() == 'o'


def test_add_and_delete_line(text_model):
    """Тест добавления и удаления строк."""
    text_model.add_line(1, 0)
    assert len(text_model.lines) == 2

    text_model._delete_line(1)
    assert len(text_model.lines) == 1


def test_replace(text_model):
    """Тест замены части строки."""
    text_model.insert_char(0, 0, 'Hello')
    text_model.replace(0, 1, 3, 'i')
    assert text_model.lines[0].c_str() == 'Hio'


def test_find_string_forward(text_model):
    """Тест поиска строки вперед."""
    text_model.insert_char(0, 0, 'Hello world')
    text_model.add_line(1,0)
    
    text_model.insert_char(1, 0, 'Another line')
    
    print(text_model.lines[1].c_str())
    
    result = text_model.find_string('world')
    # assert result == (0, 6)

    result = text_model.find_string('Another')
    # assert result == (1, 0)

    # result = text_model.find_string('Not found')
    # assert result == (-1, -1)


def test_find_string_backward(text_model):
    """Тест поиска строки назад."""
    text_model.insert_char(0, 0, 'Hello world')
    text_model.add_line(1,0)
    text_model.insert_char(1, 0, 'Another line')
    
    # result = text_model.find_string('world', 2-1, 11, direction='backward')
    # assert result == (0, 6)

    result = text_model.find_string('Another', 2-1, 11, direction='backward')
    assert result == (1, 0)

    result = text_model.find_string('Not found', 2-1, 11, direction='backward')
    assert result == (-1, -1)


def test_insert_to_command(text_model):
    """Тест вставки символа в командную строку."""
    text_model.insert_to_command(0, 'A')
    assert text_model.command_line.c_str() == 'A'
    
    text_model.insert_to_command(1, 'B')
    assert text_model.command_line.c_str() == 'AB'


def test_delete_command(text_model):
    """Тест очистки командной строки."""
    text_model.insert_to_command(0, 'Hello')
    text_model.delete_command()
    assert text_model.command_line.c_str() == ''