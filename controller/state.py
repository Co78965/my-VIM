from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def parse_command(self, command):
        pass

class SearchState(State):
    def __init__(self, mode):
        self.mode = mode
    
    def parse_command(self, command):
        self.mode.complex_command = self.mode.model.text_model.command_line.c_str()
        print("self.mode.complex_line: ", self.mode.complex_command)
        
        if(command == 27):
            print("Exit")
            self.mode.set_state(self.mode.nav_edit)
            self.mode.model.change_display('main')
            return
        
        elif(command == 10): #accept command
            if(self.mode.type_search == '/'):
                self.mode.model.search(self.mode.complex_command, "forward")

            elif(self.mode.type_search == '?'):
                self.mode.model.search(self.mode.complex_command, "backward")
            
            self.mode.set_state(self.mode.nav_edit)
            self.mode.complex_command = ''
            return
        
        elif command == 546:
            self.mode.model.resize() 
            return
        
        elif(command in (8, 0xc5)):
            self.mode.model.delete_char(True)
            return

        try:
            # print(chr(command))
            self.mode.model.input_char(chr(command), True)
        except:
            print("err: ",command)

class NavEditState(State):
    def __init__(self, mode):
        self.mode = mode
        self.buffer = ""  # Буфер для копирования и вставки
        # self.mode.complex_command = ""

    def parse_command(self, command):
        self.mode.o = False
        # print(command)
        if(command == 27 and self.mode.help):
            self.mode.help = False
            self.mode.model.change_display('help')
            return
        elif(command == 8):
            self.mode.complex_command = ''
        elif command == 546:
            self.mode.model.resize() 
            return
        elif command == 261:  # RIGHT
            self.mode.model.move_cursor('right')
            return
        elif command == 260:  # LEFT
            self.mode.model.move_cursor('left')
            return
        elif command == 259:  # UP
            # print("Курсор вверх")
            self.mode.model.move_cursor('up')
            return
        elif command == 258:  # DOWN
            self.mode.model.move_cursor('down')
            return
        elif command == 339:  # PG_UP
            self.mode.model.move_cursor('page_up')
            return
        elif command == 338:  # PG_DOWN
            self.mode.model.move_cursor('page_down')
            return
        elif(command in (8, 0xc5)):
            self.mode.model.delete_char()
            return
        elif command == 0:
            return
        elif(command == 10):
            self.mode.model.add_line()
            return
        elif command != -1:
            self.mode.complex_command += chr(command)
        
        # print("command: ", self.mode.complex_command, " ", len(self.mode.complex_command))
        
        if self.mode.complex_command == ':':
            self.mode.complex_command = ''
            self.mode.set_state(self.mode.command)
            self.mode.model.change_display('bar')
        
        elif self.mode.complex_command == 'N':
            self.mode.complex_command = ''
            self.mode.model.repeat_search(True)
        elif self.mode.complex_command == 'n':
            self.mode.complex_command = ''
            self.mode.model.repeat_search(False)
       
        elif self.mode.complex_command in ['/', '?']:
            self.mode.type_search = self.mode.complex_command
            self.mode.model.change_display(self.mode.complex_command)
            self.mode.complex_command = ''
            self.mode.set_state(self.mode.search)
            
        # Переход в начало и конец строки
        elif self.mode.complex_command in ['^', '0']:  # начало строки
            self.mode.complex_command = ''
            self.mode.model.move_cursor('start_string')
        
        # Ввод символов
        elif self.mode.complex_command == 'i':  # Ввод перед курсором
            self.mode.complex_command = ''
            self.mode.set_state(self.mode.text)
        
        elif self.mode.complex_command == 'o':  # Ввод перед курсором
            self.mode.complex_command = ''
            self.mode.o = True
            self.mode.set_state(self.mode.text)

        elif self.mode.complex_command == 'I':  # Ввод в начало строки
            self.mode.complex_command = ''
            self.mode.set_state(self.mode.text)
            self.mode.model.move_cursor('start_string')
        elif self.mode.complex_command == 'A':  # Ввод в конец строки
            self.mode.complex_command = ''
            self.mode.model.move_cursor('end_string')
            self.mode.set_state(self.mode.text)
        elif self.mode.complex_command == 'S':  # Удалить строку и начать ввод        
            self.mode.complex_command = ''
            self.mode.model.delete_line(True)  # Удаляем строку перед вводом
            self.mode.model.move_cursor('start_string')
            self.mode.set_state(self.mode.text)
           
        elif self.mode.complex_command == '$':  # конец строки
            self.mode.model.move_cursor('end_string')
            self.mode.complex_command = ''

        # Перемещение по словам
        elif self.mode.complex_command == 'w':  # следующее слово
            self.mode.model.move_cursor('end_word')
            self.mode.complex_command = ''
        
        elif self.mode.complex_command == 'b':  # предыдущее слово
            self.mode.model.move_cursor('start_word')
            self.mode.complex_command = ''

        elif self.mode.complex_command == 'G':  # конец файла
            self.mode.model.move_cursor('end_file')
            self.mode.complex_command = ''
        
        # Удаление
        elif self.mode.complex_command == 'x':  # удалить символ
            self.mode.model.delete_char()
            self.mode.complex_command = ''
                
        elif self.mode.complex_command == 'p':  # вставить
            self.mode.model.paste_after_cursor()
            self.mode.complex_command = ''

        elif self.mode.complex_command == 'r':  # Заменить символ
            c = self.mode.curses.get_input_char()
            self.mode.model.move_cursor("right")
            self.mode.model.delete_char(command=False)  # Удаляем символ под курсором
            #self.mode.model.move_cursor("right")
            self.mode.model.input_char(chr(c))
            self.mode.model.move_cursor("left")
            self.mode.complex_command = ''
        
        elif len(self.mode.complex_command) and self.mode.complex_command[-1] == ('G'):  # переход на строку
            try:
                
                line_num = int(self.mode.complex_command[:-1])
                self.mode.complex_command = ''
                self.mode.model.move_cursor('num_string', line_num)

            except:
                return 

        elif self.mode.complex_command == 'gg':  # начало файла
            self.mode.complex_command = ''
            self.mode.model.move_cursor('start_file')
            
        elif self.mode.complex_command == 'diw':  # удалить слово
            self.mode.complex_command = ''
            self.mode.model.delete_string()
            self.mode.model.move_cursor('start_string')
            
        elif self.mode.complex_command == 'dd':  # вырезать строку
            self.mode.complex_command = ''
            self.mode.model.cut_current_line()
            
        elif self.mode.complex_command == 'yy':  # копировать строку
            self.mode.complex_command = ''
            self.mode.model.copy_current_line()
            
        elif self.mode.complex_command == 'yw':  # копировать слово
            self.mode.complex_command = ''
            self.mode.model.copy_word_under_cursor()

            

class InputTextState(State):
    def __init__(self, mode):
        self.mode = mode
        self.replace_mode = False  # Флаг режима замены символа

    def parse_command(self, command):
        # print(command)
        if command == 27:  # ESC для выхода из режима ввода
            print("Выход из режима ввода текста")
            self.mode.set_state(self.mode.nav_edit)
            return
        elif(command == 10):
            self.mode.model.add_line()
        elif (command) == 261:  # вправо
            self.mode.model.move_cursor('right')
        
        elif (command) ==260:  # влево
            self.mode.model.move_cursor('left')
        
        elif (command) == 259:  # вверх
            self.mode.model.move_cursor('up')
        
        elif (command) == 258:  # вниз
            self.mode.model.move_cursor('down')
        
        elif(command in (8, 0xc5)):
            self.mode.model.delete_char()
        elif command == 546:
            self.mode.model.resize() 
            return
        else:   
            # print("state: ",self.mode.o)
            self.mode.model.input_char(chr(command), o=self.mode.o)

class InputCommandState(State):
    def __init__(self, mode):
        self.mode = mode
        self.press_w = False
        self.press_o = False
        self.press_x = False
        self.press_q = False
        self.press_q1 = False
        self.press_h = False
    
    def parse_command(self, command):
        # Сделать ввод в self.mode.complex_command, после нажатия на enter парсить строку уже по питону
        self.mode.complex_command = self.mode.model.text_model.command_line.c_str()
        print("self.mode.complex_line: ", self.mode.complex_command)
        if(command == 27):
            print("Exit")
            self.mode.set_state(self.mode.nav_edit)
            self.mode.model.change_display('main')
            return
        # дописать про номер с переходом на строку

        elif(command == 10): #accept command
            print("command: ",self.mode.complex_command)
            if(self.mode.complex_command[0] == "w"):
                print("write_file w")
                try:
                    command, filename = self.mode.complex_command.split()
                    self.mode.model.write_file(filename)
                except:
                    self.mode.model.write_file()
                self.mode.complex_command = ""

            elif(self.mode.complex_command[0] == "x"):
                print("exit with save")
                try:
                    command, filename = self.mode.complex_command.split()
                    self.mode.model.write_file(filename)
                except:
                    self.mode.model.write_file()

                self.mode.complex_command = ""
                self.mode.model.exit()
            
            elif(self.mode.complex_command == "wq!"):
                print("exit with save")
                self.mode.model.write_file()
                self.mode.model.exit()
            elif(self.mode.complex_command == "q!"):
                self.mode.model.exit()
            elif(self.mode.complex_command == "q"): 
                self.mode.model.exit("q") #добавить проверку на изменение файла

            elif(self.mode.complex_command[0] == "o"):
                print("open_file")
                try:
                    command, filename = self.mode.complex_command.split()
                    self.mode.model.open_file(filename)
                    self.mode.complex_command = ''
                except:
                    self.mode.complex_command = ''
                    return
            
            elif(self.mode.complex_command == 'h'):
                self.mode.help = True
                self.mode.complex_command == ''
                self.mode.model.help()

            else: #ни одного совпадения с коммандами
                self.mode.complex_command = ""
                print("//ни одна команда не подошла//")
            self.mode.set_state(self.mode.nav_edit)
            return
        
        elif(command in (8, 0xc5)):
            self.mode.model.delete_char(True)
            return

        try:
            print(chr(command))
            self.mode.model.input_char(chr(command), True)
        except:
            print("err: ",command)
        