from abc import ABC, abstractmethod

class IInputLib(ABC):
    @abstractmethod
    
    def get_input_char(self):
        pass

class IViewLib(ABC):
    @abstractmethod
    def clear_screen(self):
        pass
    
    @abstractmethod
    def draw_text(self, y, x, text):
        pass
    
    @abstractmethod
    def move_cursor(self, y, x):  # UP, DOWN, LEFT, RIGHT, ^ (0), $, w, b, gg, G, NG, PG_UP, PG_DOWN
        pass
