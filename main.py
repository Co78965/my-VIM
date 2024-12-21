from include.curses.CursesAdapter import CursesAdapterView
from model.mainModel import MainModel
from view.view import View
from controller.Controller import Controller

curses = CursesAdapterView()
view = View(curses)
model = MainModel()

c = Controller(view, curses, model)

while(1):
    c.wait_input()