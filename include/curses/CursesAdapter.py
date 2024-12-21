import curses
from abc import ABC, abstractmethod
from include.curses.IViewLib import IViewLib, IInputLib

class CursesAdapterView(IViewLib, IInputLib):
    def __init__(self):
        self.screen = curses.initscr()  # Инициализация curses и получение объекта экрана
        # curses.cbreak()  # Включение режима cbreak (немедленное получение ввода)
        curses.noecho()  # Отключение отображения вводимых символов на экране
        curses.curs_set(1)
        curses.start_color()  # Инициализация поддержки цветов
        self.screen.keypad(True)  # Включение поддержки специальных клавиш (стрелок и т.д.)
        # self.screen.nodelay(True)
        
    def get_max_y_x(self):
        return self.screen.getmaxyx()

    def clear_screen(self):
        self.screen.clear()  # Полная очистка экрана
        self.screen.refresh() # Обновление экрана, чтобы применить изменения

    def draw_text(self, y, x, text):
        try:
            self.screen.addstr(y, x, text)  # Печать строки в указанной позиции
        except curses.error:  # Координаты выходят за границы
            pass

    # Ожидание ввода одной клавиши
    def get_input_char(self):
        # print(curses.KEY_E)
        return self.screen.getch()
    
    def move_cursor(self, y, x):  # UP, DOWN, LEFT, RIGHT, ^ (0), $, w, b, gg, G, NG, PG_UP, PG_DOWN
        self.screen.move(y, x)  # Установка курсора по координатам (y, x)