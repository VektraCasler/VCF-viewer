# vcf_data_viewer/application.py
''' An application to view a VCF data output file in a dashboard. '''

# IMPORTS ------------------------------------------------

import ttkbootstrap as tk 
from .global_variables import *
from .model import DataModel
from .mainmenu import MainMenu
from .view import RecordView

# VARIABLES ----------------------------------------------


# CLASSES ------------------------------------------------

class Application(tk.Window):

    def __init__(self) -> None:
        super().__init__()

        # Root Window
        self.title('VCF Data Viewer')
        self.resizable(True, True)
        self.change_theme('flatly')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.geometry('800x600')

        # Data Model
        self.model = DataModel()

        # Menu
        self.menu = MainMenu(self)
        self.config(menu=self.menu)

        # View
        self.view = RecordView(self)

        # Event binding
        event_callbacks={
            '<<FileLoad>>': self.load_file,
            '<<FileClear>>': self.clear_view,
            '<<FileSave>>': self.save_file,
            '<<FileQuit>>': lambda _: self.quit(),
            '<<DispoSave>>': self.update_disposition,
            '<space>': self.update_disposition,
            # '<<ExportTextFiles>>': self.export_text_files,
            '<<ThemeCosmo>>': lambda _: self.change_theme('cosmo'),
            '<<ThemeFlatly>>': lambda _: self.change_theme('flatly'),
            '<<ThemeJournal>>': lambda _: self.change_theme('journal'),
            '<<ThemeLitera>>': lambda _: self.change_theme('litera'),
            '<<ThemeLumen>>': lambda _: self.change_theme('lumen'),
            '<<ThemePulse>>': lambda _: self.change_theme('pulse'),
            '<<ThemeSandstone>>': lambda _: self.change_theme('sandstone'),
            '<<ThemeUnited>>': lambda _: self.change_theme('united'),
            '<<ThemeYeti>>': lambda _: self.change_theme('yeti'),
            '<<ThemeSuperhero>>': lambda _: self.change_theme('superhero'),
            '<<ThemeDarkly>>': lambda _: self.change_theme('darkly'),
            '<<ThemeCyborg>>': lambda _: self.change_theme('cyborg'),
            '<<TreeviewSelect>>': None,
        }
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        # Variables

        self.variables = dict()
        self.variables['filename'] = str()
        self.variables['status_text'] = str()
        self.variables['Disposition'] = dict()
        for x in DISPOSITIONS:
            self.variables['Disposition'][x] = int()

        self.validation = dict()
        self.validation['p-values'] = [
            "VCF: Binom P Value",
            "VCF: Fisher P Value",
            "Mpileup Qual: Filtered Variant Binomial P Value",
            "Mpileup Qual: Filtered Variant Fishers P Value",
            "Mpileup Qual: Unfiltered Variant Binomial P Value",
            "Mpileup Qual: Unfiltered Variant Fishers P Value",
            "VCF: STBP"
        ]

        return

    def change_theme(self, theme, *args):
        self.style.theme_use(theme)
        # self.style.configure('custom.TEntry', background='red', foreground='white', font=('Helvetica', 20))
        return

    def clear_view(self, *args):
        self.model = DataModel()
        self.view.clear_view()
        return

    def load_file(self, *args, **kwargs):
        self.view.load_file()
        self.model.variables['filename'] = self.view.variables['filename'].get()
        self.model.load_file()
        self.view.load_treeview(self.model.variables['variant_list'])
        self.transfer_disposition_counts()
        return

    def save_file(self, *args, **kwargs):
        self.model.save_file()
        return

    def update_disposition(self, *args, **kwargs):
        self.model.variables['selection_index'] = self.view.variables['selection_index'].get()
        self.model.variables['selection_disposition'] = self.view.variant['Disposition'].get()
        self.model.change_disposition()
        self.view.load_treeview(self.model.variables['variant_list'])
        self.transfer_disposition_counts()
        return
    
    def transfer_disposition_counts(self, *args, **kwargs):
        for x in DISPOSITIONS:
            self.view.variables['Disposition'][x].set(self.model.count_dispositions(x))
        return

# MAIN LOOP ----------------------------------------------

def main():

    # Mainloop
    root = Application()
    root.mainloop()    

    return

if __name__ == '__main__':
    main()
