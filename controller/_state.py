from abc import ABC, abstractmethod

# Базовый класс команды
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Конкретные команды
class MoveCursorCommand(Command):
    def __init__(self, model, direction):
        self.model = model
        self.direction = direction

    def execute(self):
        self.model.move_cursor(self.direction)

class DeleteCharCommand(Command):
    def __init__(self, model):
        self.model = model

    def execute(self, flag = False):
        self.model.delete_char(flag)

class AddLineCommand(Command):
    def __init__(self, model):
        self.model = model

    def execute(self):
        self.model.add_line()

class SearchCommand(Command):
    def __init__(self, model, search_type, query):
        self.model = model
        self.search_type = search_type
        self.query = query

    def execute(self):
        self.model.search(self.query, self.search_type)

# Абстрактное состояние
class State(ABC):
    @abstractmethod
    def parse_command(self, command):
        pass

# Состояние поиска
class SearchState(State):
    def __init__(self, mode):
        self.mode = mode

    def parse_command(self, command):
        self.mode.complex_command = self.mode.model.text_model.command_line.c_str()
        print("self.mode.complex_command: ", self.mode.complex_command)

        if command == 27:  # ESC
            print("Exit Search")
            self.mode.set_state(self.mode.nav_edit)
            self.mode.model.change_display('main')
            return

        elif command == 10:  # Enter
            if self.mode.type_search in ('/', '?'):
                search_type = "forward" if self.mode.type_search == '/' else "backward"
                SearchCommand(self.mode.model, search_type, self.mode.complex_command).execute()

            self.mode.set_state(self.mode.nav_edit)
            self.mode.complex_command = ''
            return

        elif command in (8, 0xc5):  # Backspace
            DeleteCharCommand(self.mode.model).execute()
            return

        elif command == 546:  # Resize
            self.mode.model.resize()
            return

        try:
            self.mode.model.input_char(chr(command), True)
        except:
            print("err: ", command)

# Состояние редактирования и навигации
class NavEditState(State):
    def __init__(self, mode):
        self.mode = mode
        self.commands = {
            'right': MoveCursorCommand(self.mode.model, 'right'),
            'left': MoveCursorCommand(self.mode.model, 'left'),
            'up': MoveCursorCommand(self.mode.model, 'up'),
            'down': MoveCursorCommand(self.mode.model, 'down'),
            'delete_char': DeleteCharCommand(self.mode.model),
            'add_line': AddLineCommand(self.mode.model),
        }

    def parse_command(self, command):
        if command == 27 and self.mode.help:  # Exit help
            self.mode.help = False
            self.mode.model.change_display('help')
            return

        elif command == 261:  # RIGHT
            self.commands['right'].execute()
            return

        elif command == 260:  # LEFT
            self.commands['left'].execute()
            return

        elif command == 259:  # UP
            self.commands['up'].execute()
            return

        elif command == 258:  # DOWN
            self.commands['down'].execute()
            return

        elif command in (8, 0xc5):  # DELETE CHAR
            self.commands['delete_char'].execute()
            return

        elif command == 10:  # ADD LINE
            self.commands['add_line'].execute()
            return

        # Аналогичная обработка complex_command для других команд
        if chr(command) in ":/":
            self.mode.complex_command = chr(command)
            if self.mode.complex_command == ':':
                self.mode.set_state(self.mode.command)
                self.mode.model.change_display('bar')
            elif self.mode.complex_command in ['/', '?']:
                self.mode.type_search = self.mode.complex_command
                self.mode.set_state(self.mode.search)

# Состояние ввода текста
class InputTextState(State):
    def __init__(self, mode):
        self.mode = mode

    def parse_command(self, command):
        if command == 27:  # ESC
            print("Выход из режима ввода текста")
            self.mode.set_state(self.mode.nav_edit)
            return
        elif command == 10:  # Enter
            AddLineCommand(self.mode.model).execute()
        elif command in (8, 0xc5):  # Backspace
            DeleteCharCommand(self.mode.model).execute()
        elif command == 546:  # Resize
            self.mode.model.resize()
        else:
            self.mode.model.input_char(chr(command), o=self.mode.o)

# Состояние ввода команд
class InputCommandState(State):
    def __init__(self, mode):
        self.mode = mode

    def parse_command(self, command):
        self.mode.complex_command = self.mode.model.text_model.command_line.c_str()
        print("self.mode.complex_command: ", self.mode.complex_command)

        if command == 27:  # ESC
            print("Exit Command")
            self.mode.set_state(self.mode.nav_edit)
            self.mode.model.change_display('main')
            return
        
        elif command == 546:  # Resize
            self.mode.model.resize()
            return
        
        elif command in (8, 0xc5):  # Backspace
            DeleteCharCommand(self.mode.model).execute(True)
            return
        
        elif command == 10:  # Enter
            print("command: ", self.mode.complex_command)
            if self.mode.complex_command.startswith("w"):
                self.mode.model.write_file()
            elif self.mode.complex_command == "q!":
                self.mode.model.exit()
            elif self.mode.complex_command.startswith("o"):
                filename = self.mode.complex_command[1:].strip()
                self.mode.model.open_file(filename)
            self.mode.set_state(self.mode.nav_edit)
        try:
            # print(chr(command))
            self.mode.model.input_char(chr(command), True)
        except:
            print("err: ",command)
