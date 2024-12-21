import sys
import os

from include.MyString import MyString

class MyStringDecorator(MyString):
    def __init__(self, text):
        super().__init__(text)
        self.text = text

    def rfind(self, substring, index=None):
        if index is None:
            index = self.size() - 1 
        
        count = len(substring)
        

        for i in range(index, -1, -1):  # Идем по строке в обратном порядке

            if self.substr(i-1, count) == substring:
                return i-1
        return -1

class TextModel:
    def __init__(self):
        self.lines = [MyString("")]  # Начинаем с одной пустой строки
        self.command_line = MyString("")
    
    def insert_to_command(self, x, char):
        s = MyString(self.command_line)
        s.insert(x, char)
        print("insert_char: ", s)
        self.command_line = s

    def get_line_from_file(self,file):
        arr = []
        for line in file.readlines():
            arr.append(MyString(line.rstrip('\n')))
        print(arr)
        return arr

    def insert_char(self, line_idx, char_idx, char):
        """Вставить символ в заданную строку на указанную позицию."""
        if 0 <= line_idx < len(self.lines):
            s = MyString(self.lines[line_idx])
            s.insert(char_idx, char)
            # print("insert_char: ", s)
            self.lines[line_idx] = s
        else:
            raise IndexError("Line index out of range")

    def delete_char_command(self, char_idx, lenght = 1):
        s = MyString(self.command_line)
        s.erase(char_idx, lenght)
        self.command_line = s
        
    def delete_char(self, line_idx, char_idx, lenght = 1):
        if 0 <= line_idx < len(self.lines):
            s = MyString(self.lines[line_idx])
            s.erase(char_idx, lenght)
            self.lines[line_idx] = s
        else:
            raise IndexError("Line index out of range")

    def add_line(self, index, x):
        """Добавить новую строку."""
        temp = self.lines[index-1]
        new = MyString("")
        for i in range(x, len(temp)):
            new += temp[i]
        
        print(self.lines[index-1], x, len(temp)-x)
        self.lines[index-1].erase(x, len(temp)-x)
        
        print(self.lines[index-1])

        self.lines.insert(index, new)

    def delete_command(self):
        self.command_line.clear()

    def delete_line(self, index):
        print("delete_line: ", self.lines[index].c_str())
        del self.lines[index]

    def _delete_line(self, index):
        """Удалить строку."""
        if 0 <= index < len(self.lines):
            self.lines.pop(index)
        else:
            raise IndexError("Line index out of range")

    def replace(self, line_idx, char_idx, length, new_text):
        """Заменить часть строки."""
        if 0 <= line_idx < len(self.lines):
            self.lines[line_idx].replace(char_idx, length, new_text)
        else:
            raise IndexError("Line index out of range")

    def find_string(self, substring, start_line=0, start_pos=0, direction='forward'):
        """Найти подстроку в тексте начиная с указанной строки и позиции."""
        if direction == 'forward':
            
            # Поиск вперед, начиная с start_line и start_pos
            for line_idx in range(start_line, len(self.lines)):

                if(line_idx != start_line):
                    start_pos = 0
                
                # start_pos += 1
                
                line = self.lines[line_idx]
                pos = line.find(substring, start_pos+1)  # Ищем начиная с позиции start_pos
                
                print(line_idx, pos)
                
                if pos != -1:
                    return line_idx, pos  # Вернуть индекс строки и позицию подстроки
        
        elif direction == 'backward':
            # Поиск назад, начиная с start_line и start_pos
            
            for line_idx in range(start_line, -1, -1):
                # print(line_idx)
                line = MyStringDecorator(self.lines[line_idx])
                # print(line, substring, start_pos)

                if(line_idx != start_line):
                    start_pos=None
                
                pos = line.rfind(MyString(substring), start_pos)  # Ищем до позиции start_pos
                
                if pos != -1:
                    return line_idx, pos  # Вернуть индекс строки и позицию подстроки
        
        return -1, -1  # Не найдено
    
    def get_mystring(self, text):
        return MyString(text)
