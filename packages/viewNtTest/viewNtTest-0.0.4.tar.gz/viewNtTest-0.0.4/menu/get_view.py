from menu.menu.view import gui_window
from menu.menu.menu_widget import FrameMenu

def show():
    gui = gui_window()
    frame_menu = FrameMenu(gui.window)
    frame_menu.frame_menu.grid()
    gui.show()


if __name__ == '__main__':
    show()
