class CursorModel:
    __y = 0
    __x = 0
    
    def set_x(self, coord_x):
        self.__x = coord_x
    
    def set_y(self, coord_y):
        self.__y = coord_y

    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def move_to(self, y, x):
        self.__y = y
        self.__x = x

    def move_up(self, x_prev):
        self.__y = max(0, self.__y - 1)
        self.__x = min(x_prev, self.__x)

    def move_down(self, max_y, x_next):
        self.__y = min(max_y - 1, self.__y + 1)
        self.__x = min(x_next, self.__x)

    def move_left(self):
        self.__x = max(0, self.__x - 1)
 
    def move_right(self, max_x):
        self.__x = min(max_x, self.__x + 1)