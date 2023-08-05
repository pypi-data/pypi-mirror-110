from tkinter import *
import webbrowser as wb
import os

try:
    OF_locat = sys._MEIPASS
except:
    OF_locat = ''

class gui_window():

    def __init__(self,window_icon =False, procedure = False):
        super().__init__()

        # config view
        self.couleur = '#FFFFFF'
        # Window
        self.window = Tk()
        self.menubar = Menu(self.window)
        self.window.wm_attributes("-topmost", 2)
        self.window.resizable(0,0)
        if window_icon : 
            self.window.iconbitmap(os.path.join(OF_locat,window_icon))
        self.window.config(menu=self.menubar)
        self.procedure = procedure

    def help(self):
        wb.open_new(os.path.join(OF_locat, self.procedure))

    def show(self):
        self.window.mainloop()

    def close(self):
        self.window.destroy()

if __name__ == '__main__':
    gui = gui_window()
    gui.show()