# mainmenu.py
''' The menu file for the VCF Data Viewer application.  Part of view, but enough to be it's own module. '''

# IMPORTS ------------------------------------------------

import ttkbootstrap as tk 
from tkinter import messagebox

# VARIABLES ----------------------------------------------

# CLASSES ------------------------------------------------

class MainMenu(tk.Menu):
    '''The Application's main menu.'''

    def _event(self, sequence):
        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback

    def __init__(self, parent, settings, **kwargs):
        super().__init__(parent, **kwargs)
        self.settings = settings
        
        # File Menu --------------------------------
        menu_file = tk.Menu(self, tearoff=False)
        menu_file.add_command(
            label="Open", 
            command=self._event('<<FileSelect>>')
        )
        menu_file.add_command(
            label="Clear", 
            command=self._event('<<FileClear>>')
        )
        menu_file.add_command(
            label="Save", 
            command=self._event('<<FileSave>>')
        )
        menu_file.add_separator()
        menu_file.add_command(
            label="Quit",
            command=self._event('<<FileQuit>>')
        )
        
        # Go Menu ----------------------------------
        menu_go = tk.Menu(self, tearoff=False)
        menu_go.add_command(
            label = "Export Text Files",
            command=self._event('<<ExportTextFiles>>')
        )

        # Themes Menu -------------------------------
        menu_theme = tk.Menu(self, tearoff=0)
        menu_theme.add_command(
            label='Cosmo', 
            command=self._event('<<ThemeCosmo>>')
        )
        menu_theme.add_command(
            label='Flatly', 
            command=self._event('<<ThemeFlatly>>')
        )
        menu_theme.add_command(
            label='Journal', 
            command=self._event('<<ThemeJournal>>')
        )
        menu_theme.add_command(
            label='Litera', 
            command=self._event('<<ThemeLitera>>')
        )
        menu_theme.add_command(
            label='Lumen', 
            command=self._event('<<ThemeLumen>>')
        )
        menu_theme.add_command(
            label='Pulse', 
            command=self._event('<<ThemePulse>>')
        )
        menu_theme.add_command(
            label='Sandstone', 
            command=self._event('<<ThemeSandstone>>')
        )
        menu_theme.add_command(
            label='United', 
            command=self._event('<<ThemeUnited>>')
        )
        menu_theme.add_command(
            label='Yeti', 
            command=self._event('<<ThemeYeti>>')
        )
        menu_theme.add_separator()
        menu_theme.add_command(
            label='Superhero', 
            command=self._event('<<ThemeSuperhero>>')
        )
        menu_theme.add_command(
            label='Darkly', 
            command=self._event('<<ThemeDarkly>>')
        )
        menu_theme.add_command(
            label='Cyborg', 
            command=self._event('<<ThemeCyborg>>')
        )

        # Help Menu ----------------------------
        menu_help = tk.Menu(self, tearoff=False)
        menu_help.add_command(
            label='About...',
            command=self.show_about
        )

        # Add menus in the right order...
        self.add_cascade(label='File', menu=menu_file)
        self.add_cascade(label='Go', menu=menu_go)
        self.add_cascade(label='Theme', menu=menu_theme)
        self.add_cascade(label='Help', menu=menu_help)

        return

    def show_about(self):
        '''Show the about dialog'''
        
        about_message = 'VCF Data Viewer'
        about_detail = (
            'Written by Vektra Casler MD \n'
            '\n'
            'For assistance, please contact \n'
            'vektra_casler@urmc.rochester.edu'
        )
        messagebox.showinfo(
            title='About',
            message=about_message,
            detail=about_detail
        )

# MAIN LOOP ----------------------------------------------

def main():

    pass

    return

if __name__ == '__main__':
    main()