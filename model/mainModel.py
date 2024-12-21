import sys
from abc import abstractmethod, ABC

from model.textModel import TextModel
from model.cursorModel import CursorModel

class INotifyObserver(ABC):
    @abstractmethod
    def update():
        pass

class MainModel:
    def __init__(self):
        self.text_model = TextModel()
        self.cursor_model = CursorModel()
        self.observer = None
        self.last_search_text = None  # Последняя строка поиска
        self.last_search_direction = None # Последнее направление поиска ('forward' или 'backward')
        self.direction = ["forward", "backward"]
        self.file_name = None
        self.old_version = None
        self.old_version_help = None
        self.__clipboard = ""
        self.save_x, self.save_y = 0, 0
        self.mode = self.text_model.get_mystring("")
        
    def add_line(self):
        y, x = self.cursor_model.get_y(), self.cursor_model.get_x()                
        # print("x: ", x)
        self.text_model.add_line(y+1, x)
        if(x == len(self.text_model.lines[y])):
            x = 0
        self.cursor_model.move_to(y+1, x)
        self.notify_observers("add_new_line")
        
    # from interface IInputCommandModel
    def open_file(self, filename): 
        #o filename
        try: 
            self.file_name = filename
            # print(self.file_name)
            with open(self.file_name, 'r',  encoding="utf_8_sig") as file:
                self.text_model.lines = self.text_model.get_line_from_file((file))
                print(self.text_model.lines)
                self.old_version = self.text_model.lines
                print("file: ", self.text_model.lines)
            self.text_model.command_line.erase(0, len(self.text_model.command_line))
            self.cursor_model.move_to(len(self.text_model.lines)-1, len(self.text_model.lines[len(self.text_model.lines)-1]))
            self.notify_observers('open_file')
        
        except Exception as e:
            self.text_model.command_line.erase(0, len(self.text_model.command_line))
            self.cursor_model.move_to(self.save_y, self.save_x)
            print(e)

    def write_file(self, filenName = None): 
        #(x and exit)
        #(w + in current file)
        #(w + filename)
        filename = self.file_name
        if(filenName != None and self.file_name != filenName):
            filename = filenName

        with open(filename, 'w+') as file:
            for line in self.text_model.lines:
                file.write(line.c_str() + '\n')

        self.text_model.command_line.erase(0, len(self.text_model.command_line))
        self.old_version = self.text_model.lines
        self.notify_observers('write_file')

    def exit(self, type = None):
        #q exit without changes (only q! if change excist)
        #q! exit without save 
        #wq! writefile and exit
        print(type, self.old_version != self.text_model.lines)
        if type == "q" and self.old_version != self.text_model.lines:
            return
        
        self.file_name = None
        self.old_version = None
        self.notify_observers('exit')
        sys.exit()

    def move_to_line(self, line_number):
        # some 'number' (int) move to line with thos number
        if 0 <= line_number < len(self.text_model.lines):
            self.cursor_model.move_to(line_number, 0)
            self.notify_observers('move_to_line')
        else:
            # print(f"Ошибка: Строка с номером {line_number} не существует!")
            self.notify_observers('line isn\'t exists')

    def help(self):
        self.old_version_help = self.text_model.lines
        self.text_model.command_line.erase(0, len(self.text_model.command_line))
        self.open_file("model\help.txt")
        self.cursor_model.set_x(0)
        self.notify_observers('help')

    # from interface ITextInputModel  
    # При вводе команды, с контроллера вызывается команда
    # перемещения курсора на нужную позицию
    # - i остаться на месте + ввод перед курсором
    # - I перейти в начало строки + ввод текста 
    # - A перейти в конец строки + ввод текста
    # - S удалить всю строку + ввод текста
    # - r перейти на строку ниже + заменить один символ

    def replace_char(self, char):
        y, x = self.cursor_model.get_y(), self.cursor_model.get_x()
        self.text_model.lines[y][x+1] = char

    def input_char(self, char, bar = False, o = False): #ok
        if(bar):
            x = self.cursor_model.get_x()
            self.text_model.insert_to_command(x, char)
            self.cursor_model.move_right(len(self.text_model.command_line)+1)
            # print("coord: ", x)
        else:
            y, x = self.cursor_model.get_y(), self.cursor_model.get_x()
            # print(y, x)
            self.text_model.insert_char(y, x, char)
            if(not(o)):
                self.cursor_model.move_right(len(self.text_model.lines[y])+1)
        
        # print(o)
        # self.old_version = self.text_model.lines
        self.notify_observers('input_char')

    def change_display(self, display):
        if(display == 'bar'):
            self.save_y, self.save_x = self.cursor_model.get_y(), self.cursor_model.get_x()
            self.cursor_model.set_x(0)
            # self.notify_observers("Начать отображение на командной строке --> переход на ожидание ввода")
            self.notify_observers('display_change_bar')    
        elif(display == 'main'):
            self.cursor_model.move_to(self.save_y, self.save_x)
            # print(self.save_x, self.save_y)
            # self.notify_observers("Начать отображение на основном экране --> переход на ожидание ввода")
            self.text_model.delete_command()
            self.notify_observers('display_change_main')  
        elif(display in ['?','/']):
            self.save_y, self.save_x = self.cursor_model.get_y(), self.cursor_model.get_x()
            self.cursor_model.move_to(self.save_y, self.save_x)
            # self.notify_observers("Начать отображение на основном экране --> переход на ожидание ввода")
            self.cursor_model.set_x(0)
            self.notify_observers(display)  
        elif(display == "help"):
            self.text_model.lines = []
            if(self.old_version_help):
                self.text_model.lines = self.old_version_help
            self.change_display("main")

    # from INavEditModel 
    def move_cursor(self, direction, number = ''): #ok
        """Переместить курсор в заданном направлении."""
        if direction == 'up':
            y = self.cursor_model.get_y()
            if(not y):
                # self.notify_observers(direction)  
                return
            len_prev_line = len(self.text_model.lines[y-1])
            self.cursor_model.move_up(len_prev_line)
        elif direction == 'down':
            y = self.cursor_model.get_y()
            if(y+1 >= len(self.text_model.lines)):
                return
            len_next_line = len(self.text_model.lines[y+1])
            self.cursor_model.move_down(len(self.text_model.lines), len_next_line)
        elif direction == 'left':
            self.cursor_model.move_left()
        elif direction == 'right':
            y = self.cursor_model.get_y()
            current_line = self.text_model.lines[y]
            self.cursor_model.move_right(len(current_line))
        
        elif direction == 'start_string': #^ or 0
            self.cursor_model.set_x(0)
            y, x = self.cursor_model.get_y(), self.cursor_model.get_x()
            # print("start: ", y, x)
        elif direction == 'end_string':#$
            cur_y = self.cursor_model.get_y()  # Текущая строка
            end_x = len(self.text_model.lines[cur_y])  # Длина строки (количество символов)
            self.cursor_model.set_x(end_x)
        
        elif direction == 'start_word': #b
            x = self.cursor_model.get_x()
            if(x-1 <= -1):
                return
            self.cursor_model.set_x(x-1)
            start_x, _ = self.get_word_boundaries()
            self.cursor_model.set_x(start_x)
        elif direction == 'end_word':  #w
            x = self.cursor_model.get_x()
            
            if(x+1 >= len(self.text_model.lines[self.cursor_model.get_y()])):
                return
            
            self.cursor_model.set_x(x+1)
            _, end_x = self.get_word_boundaries()
            self.cursor_model.set_x(end_x)
        
        elif direction == 'start_file': #gg  
            self.cursor_model.move_to(0,0)
        elif direction == 'end_file': #G 
            y = len(self.text_model.lines) - 1
            x = len((self.text_model.lines)[y])
            self.cursor_model.move_to(y, x)
        
        elif direction == 'num_string': #NG (N - number string)
            self.cursor_model.set_x(0)
            self.cursor_model.set_y(min(int(number)-1, len(self.text_model.lines)))
            
        self.notify_observers(direction, False)  
        
    def delete_line(self , S = False):
        y = self.cursor_model.get_y()
        if(S):
            y = self.cursor_model.get_y()
            self.text_model.lines[y] = self.text_model.get_mystring("")
            return

        self.text_model.delete_line(y)
        # self.old_version = self.text_model.lines
        self.notify_observers('delete_line')  

    def delete_string(self): #diw #ok
        y, x = self.cursor_model.get_y(), self.cursor_model.get_x()
        start, end = self.get_word_boundaries()
        self.text_model.delete_char(y, start, end - start)
        # self.old_version = self.text_model.lines
        self.notify_observers('delete_string')  

    def delete_char(self, command = False): #x delete char right cursor #ok
        y, x = self.cursor_model.get_y(), self.cursor_model.get_x() - 1
        if(command):
            if(x == -1):
                return
            self.text_model.delete_char_command(x)
            # print("del: ", x)
            self.cursor_model.move_left()
            self.notify_observers('delete_char_bar')  

        else:
            # print("del: ", x," ", y)
            if(y != 0 and x == -1):
                self.text_model.delete_line(y)
                self.cursor_model.move_to(y-1, len(self.text_model.lines[y-1]))
                self.notify_observers('delete_char_bar')  
                # self.old_version = self.text_model.lines
                return
            elif(x == -1):
                return
            
            self.text_model.delete_char(y,x)
            self.cursor_model.move_left()
            # self.old_version = self.text_model.lines
            self.notify_observers('delete_char_bar')  
             
    def cut_current_line(self): #dd #ok
        y = self.cursor_model.get_y()
        if 0 <= y < len(self.text_model.lines):
            self.__clipboard = ()
            
            tmp_clipboard = ''
            
            for i in range(len(self.text_model.lines[y].c_str())):
                # print((self.text_model.lines[y].c_str()[i]))
                tmp_clipboard += self.text_model.lines[y].c_str()[i]
                # print(typed(self.__clipboard))
            
            self.__clipboard = self.text_model.get_mystring(tmp_clipboard)
            
            self.text_model.delete_line(y)  # Удалить строку
            self.cursor_model.set_y(max(0, y - 1))  # Переместить курсор на строку выше
            # self.old_version = self.text_model.lines
            self.notify_observers('cut_word')  
    
    def copy_current_line(self): #yy #ok
        y = self.cursor_model.get_y()
        if 0 <= y < len(self.text_model.lines):
            self.__clipboard = self.text_model.lines[y]  # Сохранить строку в буфер обмена
            self.notify_observers('copy_line')  

    def copy_word_under_cursor(self): #yw #ok
        y, x = self.cursor_model.get_y(), self.cursor_model.get_x()
        if 0 <= y < len(self.text_model.lines):
            current_line = self.text_model.lines[y].c_str()
            start, end = self.get_word_boundaries()
            self.__clipboard = self.text_model.get_mystring(current_line[start:end])
            self.notify_observers('copy_word')  

    def paste_after_cursor(self): #p #ok
        if self.__clipboard:  # Проверить, есть ли данные в буфере обмена
            y, x = self.cursor_model.get_y(), self.cursor_model.get_x()
            self.text_model.insert_char(y, x, self.__clipboard.c_str())  # Вставить после курсора
            self.cursor_model.set_x(x + len(self.__clipboard))  # Переместить курсор после вставленного текста
            # self.old_version = self.text_model.lines
            self.notify_observers('past_word/line')  


    #from interface ISearchModel - full
    def search(self, text, direction, repeat = False):#/text <CR> #ok
        self.text_model.command_line.erase(0, len(self.text_model.command_line))
        # print(direction)
        y, x = self.save_y, self.save_x-1
        
        if not repeat:
            self.last_search_text = text
            self.last_search_direction = self.direction.index(direction)
        
        # Поиск с текущей строки и текущей позиции
        y_find, x_find = self.text_model.find_string(text, y, x+1, direction)
        
        if y_find != -1 and x_find != -1:
            # Найдена строка, переместить курсор
            self.cursor_model.move_to(y_find, x_find)
            # self.last_search_text = text
            # self.last_search_direction = self.direction.index(direction)
            self.notify_observers('search')  
            return True
        
        self.cursor_model.move_to(self.save_y, self.save_x)
        # print(y, x, y_find, x_find)
        return False


    def repeat_search(self, reverse=False):#?text <CR> #n reverse = False, N reverse = True #ok
        try:
            self.save_y, self.save_x = self.cursor_model.get_y(), self.cursor_model.get_x()
        
            if(reverse):
                self.search(self.last_search_text, self.direction[1 - self.last_search_direction], True)
                print("repeat_search reverse N", self.direction[1 - self.last_search_direction])
                return
            
            self.search(self.last_search_text, self.direction[self.last_search_direction])
        except:
            pass
    # Вне интерфейсов, общие методы
    def get_word_boundaries(self):  #ok
        y, x = self.cursor_model.get_y(), self.cursor_model.get_x()
        if 0 <= y < len(self.text_model.lines):
            current_line = self.text_model.lines[y]

            # Определяем начало слова
            start = x
            while start > 0 and current_line[start - 1] != " ":
                start -= 1

            # Определяем конец слова
            end = x
            while end < len(current_line) and current_line[end] != " ":
                end += 1

            return start, end
        return None, None

    def add_observer(self, observer):
        self.observer = observer

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message, change = True):
        data = {
            "x":self.cursor_model.get_x(),
            "y": self.cursor_model.get_y(),
            "lines": self.text_model.lines,
            "command": self.text_model.command_line,
            "message": message, 
            "state": self.mode,
            "change": change
        }
        self.observer.update(data)

    def get_clipboard(self):
        return self.__clipboard

    def set_mode(self, cur_mode):
        self.mode = self.text_model.get_mystring(cur_mode)
        self.notify_observers("set_state")
    
    def resize(self):
        self.notify_observers("resize")