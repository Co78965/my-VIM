from abc import ABC, abstractmethod
from include.MyString import MyString
from include.curses.IViewLib import IViewLib
from model.mainModel import INotifyObserver


class View(INotifyObserver):
    def __init__(self, view : IViewLib):
        self.view = view
        self.buffer = []
        self.bar = [MyString()]
        self.coord = [0,0]
        self.dict_line = {0:0}
        self.save_y = 0
        self.sdvig = 0
        self.sdvig_buf = 0
    
    def parse_lines(self, lines): 
        try:
            index = self.dict_line.keys[-1]      
        except:
            index = 0

        if(self.buffer == []):
            start = 0
            stop = len(lines)

        elif(self.coord[1] < self.max_y):
            start = 0
            stop = min(self.max_y, len(lines))
            self.buffer = []

        elif(self.coord[1] >= self.max_y-1):
            start = self.coord[1] - self.max_y + 1
            stop = self.coord[1] + 1
            self.buffer = []

        self.sdvig = 0
        self.sdvig_buf = 0
        if(self.buffer == []):
            for i in range(start, stop):
                self.dict_line.setdefault(i+1, 0)
                if len(lines[i]) >= self.max_x:
                    cnt = len(lines[i])//self.max_x
                    self.dict_line[i+1] = self.dict_line[i]+1+cnt
                    for j in range(cnt+1):
                        if(len(self.buffer) > self.max_y-1):
                            self.sdvig+=1
                            del self.buffer[0]

                        self.buffer.append(lines[i].c_str()[0 + j*self.max_x : self.max_x*(j+1)])
                        # self.buffer.append(lines[i].c_str()[0 + j*self.max_x, self.max_x*(j+1)])
                    continue
                
                if(len(self.buffer) > self.max_y-1):
                    self.sdvig_buf+=1
                    del self.buffer[0]

                self.dict_line[i+1] = self.dict_line[i]+1
                self.buffer.append(lines[i].c_str())
    
    def update(self, data):
        self.max_y,  self.max_x = self.view.get_max_y_x()[0] - 1, self.view.get_max_y_x()[1]
        self.message = data['message']
        self.coord = [data['x'],data['y']]
        
        self.data = data['lines']

        self.parse_lines(data['lines'])
        
        self.bar = None if not data['command'].c_str() else data['command'].c_str()
        self.state = data['state'].c_str()
    
        self.show_screen()

    def show_screen(self):
        self.view.clear_screen()
        save_y = self.coord[1]
        self.coord[1] = self.dict_line[self.coord[1]] + self.coord[0]//self.max_x
        index = 0
        # print(self.dict_line)
        for i in range(len(self.buffer)):
            self.view.draw_text(index, 0, self.buffer[i])
            # print(index,  self.buffer[i])
            index += 1#массив добавить
        
        # print("sdwig 1", self.sdvig_buf, self.sdvig)
        
        self.sdvig = self.coord[0]//self.max_x - self.sdvig
    
        self.coord[0]%=self.max_x
        self.show_bar()
        
        coord_y = self.max_y + self.sdvig - self.sdvig_buf - 1 if self.max_y + self.sdvig - 1 < self.max_y - 1 else self.max_y - 1
        
        print("sdwig 2", coord_y, self.max_y, self.sdvig_buf, self.sdvig)
        
        if(self.state not in [":","?", "/"]):
            self.view.move_cursor(coord_y if self.max_y - 1 < self.coord[1] else self.coord[1], self.coord[0])
            self.save_y = self.coord[1]
    
    def show_bar(self):
        s = self.state
        
        if(s in [":","?", "/"]):
            if(self.bar):
                s+= self.bar
            start = 0
            stop = min(self.max_x - 10, len(s))

            if(len(s) >= self.max_x - 11):
                start = len(s) - self.max_x + 11
                stop += start

            self.view.draw_text(self.max_y, 0, f"{s[0]}{s[start+1:stop]}")
            self.view.draw_text(self.max_y, self.max_x - 5 - len(f"{self.coord[1], self.coord[0]}"), f"{self.max_y, self.coord[0]}")
            self.view.move_cursor(self.max_y, min(self.coord[0] + 1, self.max_x-11))
            return True
        
        self.view.draw_text(self.max_y, 0, s)
        # print(f"{self.coord[1], self.coord[0]}")
        self.view.draw_text(self.max_y, self.max_x - 5 - len(f"{self.coord[1], self.coord[0]}"), f"{self.coord[1], self.coord[0]}")
        return False
        