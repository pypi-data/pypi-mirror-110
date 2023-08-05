from tkinter import *

try:
    OF_locat = sys._MEIPASS
except:
    OF_locat = ''

class FrameMenu():

    def __init__(self, window, frame_bg='#FFFFFF', label_bg = '#FFFFFF', list_bg_select = '#0099ff'):

        self.frame_menu = Frame(window, background = frame_bg)
        self.var_dossiers = StringVar()
        self.var_dossiers.set("")
        self.var_lab_dossiers = StringVar()
        self.var_lab_dossiers.set("")
        self.var_client = StringVar()
        self.var_base = StringVar()
        
        # label
        self.lab_dossier = Label(self.frame_menu ,  text="Dossiers \ud83d\udd0e",font=('Helvetica', 14, 'bold') , foreground='orange', background=label_bg)
        self.label_select_client = Label(self.frame_menu, textvariable = self.var_lab_dossiers, width = 20, height = 3, wraplength = 160, font=('Helvetica', 10), background=label_bg, anchor="center")

        # Saisie
        self.saisie_dossier = Entry(self.frame_menu ,  width=40, textvariable=self.var_dossiers, cursor='question_arrow')
        self.saisie_dossier.focus_set()

        # # liste 
        self.liste_dossiers = Listbox(self.frame_menu , width=40,  height=10, selectbackground=list_bg_select, cursor="hand2")

        # boutons
        self.generate = Button(self.frame_menu, text = "Sélectionner", width=10)

        # placement 
        self.lab_dossier.grid(row=0,  padx=10, pady=3,sticky='n', columnspan = 2)
        self.saisie_dossier.grid(row=1,  padx=15, pady=5, columnspan = 2)
        self.liste_dossiers.grid(row=2,  padx=15, pady=5, columnspan = 2)
        self.label_select_client.grid(row=8, column=0,  padx=(15,5), pady= 15, sticky='w')
        self.generate.grid(row=8, column=1, padx=(5,15), pady= 15, sticky='e')


if __name__=='__main__':

    from view import gui_window
    gui = gui_window()
    frame_menu = FrameMenu(gui.window)
    frame_menu.frame_menu.grid()
    gui.show()