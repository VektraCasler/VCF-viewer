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
        self.title('VCF Result Viewer')
        self.resizable(True, True)
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
            '<<FileSelect>>': self.load_file,
            '<<FileClear>>': self.clear_view,
            '<<FileSave>>': self.save_file,
            '<<FileQuit>>': lambda _: self.quit(),
            # '<<ExportTextFiles>>': self._export_text_files,
            '<<ThemeCosmo>>': lambda _: self.style.theme_use('cosmo'),
            '<<ThemeFlatly>>': lambda _: self.style.theme_use('flatly'),
            '<<ThemeJournal>>': lambda _: self.style.theme_use('journal'),
            '<<ThemeLitera>>': lambda _: self.style.theme_use('litera'),
            '<<ThemeLumen>>': lambda _: self.style.theme_use('lumen'),
            '<<ThemePulse>>': lambda _: self.style.theme_use('pulse'),
            '<<ThemeSandstone>>': lambda _: self.style.theme_use('sandstone'),
            '<<ThemeUnited>>': lambda _: self.style.theme_use('united'),
            '<<ThemeYeti>>': lambda _: self.style.theme_use('yeti'),
            '<<ThemeSuperhero>>': lambda _: self.style.theme_use('superhero'),
            '<<ThemeDarkly>>': lambda _: self.style.theme_use('darkly'),
            '<<ThemeCyborg>>': lambda _: self.style.theme_use('cyborg'),
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

    def clear_view(self, *args):
        self.view.clear_view()
        return

    def load_file(self, *args, **kwargs):
        self.model.variables['filename'] = self.view.variables['filename'].get()
        self.model.load_file()
        # for x in VCF_FIELDS:
        #     self.view.variant[x].set(self.model.variables['selected_variant'][x])
        self.view.load_treeview(self.model.variables['variant_list'])
        return

    def save_file(self, *args, **kwargs):
        self.model.save_file()
        return

# MAIN LOOP ----------------------------------------------

def main():

    # Mainloop
    root = Application()
    root.mainloop()    

    return

if __name__ == '__main__':
    main()
