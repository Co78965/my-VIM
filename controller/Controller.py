from controller.state import SearchState, NavEditState, InputTextState, InputCommandState
from include.curses.IViewLib import IInputLib
from model.mainModel import INotifyObserver

class Controller():
    def __init__(self, obs : INotifyObserver, curses : IInputLib, model):
        self.curses = curses
        self.model = model
        self.nav_edit = NavEditState(self) #base
        self.search = SearchState(self)
        self.text = InputTextState(self)
        self.command = InputCommandState(self)
        self.o = False
        self.help = False
        self.model.add_observer(obs)

        self.state = self.nav_edit

        self.modes = {
            self.nav_edit: "",
            self.command: ":",
            self.text: "INSERT",
            self.search: ["?","/"]
        }

        self.complex_command = ""
        self.num = ""
        self.type_search = ""

    def wait_input(self):
        x = self.curses.get_input_char()
        self.parse_command((x))
        
    def parse_command(self, command):
        self.state.parse_command(command)
    
    def set_state(self, state):
        if(state == self.search):
            self.model.set_mode(self.type_search)
        else:
            self.model.set_mode(self.modes[state])   
        print(self.modes[state])
        self.state = state