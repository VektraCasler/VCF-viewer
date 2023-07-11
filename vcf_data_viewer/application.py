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
        self.style.theme_use('flatly')
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

        # Event binding, dictionary of event keywords and callbacks
        event_callbacks={
            '<<FileLoad>>': self.load_file,
            '<<FileClear>>': self.clear_view,
            '<<FileSave>>': self.save_file,
            '<<FileQuit>>': lambda _: self.quit(),

            '<<DispoSave>>': self.update_disposition,

            # '<space>': self.update_disposition,
            # '<Right>': self.treeview_next_focus,
            # '<Left>': self.treeview_prev_focus,
            # '<Up>': lambda _: self.view.treeviews['variant_list'].focus(),
            # '<Down>': lambda _: self.view.treeviews['variant_list'].focus(),

            '<<ExportTextFiles>>': self.model.output_text_files,

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

        # Binding all the callbacks and events
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        # Variable prep
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

        return None


    # Tried to get fancy by binding the keyboard for faster navigation.  Treeview caused problems.

    # def treeview_next_focus(self, *args):
    #     disposition = self.view.variant['Disposition'].get()
    #     print(disposition)
    #     index = DISPOSITIONS.index(disposition)
    #     print(index)
    #     index += 1
    #     print(index)
    #     if index > len(DISPOSITIONS) - 1:
    #         index = 0
    #     print(index)
    #     print(DISPOSITIONS[index])
    #     self.focus()
    #     self.view.radio_buttons[DISPOSITIONS[index]].focus()
    #     self.view.variant['Disposition'].set(DISPOSITIONS[index])
    #     focus = self.view.treeviews['variant_list'].focus()
    #     total_records = len(self.view.treeviews['variant_list'].get_children())
    #     focus = int(focus[1:], 16)
    #     focus += 1
    #     if focus > total_records:
    #         focus = total_records
    #     focus = "I" + str(hex(focus))[2:].upper().zfill(3)
    #     self.view.treeviews['variant_list'].focus(focus)
    #     pass
    #     return

    # def treeview_prev_focus(self, *args):
    #     focus = self.view.treeviews['variant_list'].focus()
    #     focus = int(focus[1:], 16)
    #     focus -= 1
    #     if focus < 1:
    #         focus = 1
    #     focus = "I" + str(hex(focus))[2:].upper().zfill(3)
    #     self.view.treeviews['variant_list'].focus(focus)
    # pass
    # return


    # def change_theme(self, theme, *args) -> None:
    #     """Method to update the color theme of the widgets."""

    #     self.style.theme_use(theme)

    #     return None


    def clear_view(self, *args) -> None:
        """ Method to clear the view and loaded data. """

        # nukes the data model and starts anew.
        self.model = DataModel()

        # clear the view widgets.
        self.view.clear_view()

        return None


    def load_file(self, *args, **kwargs) -> None:
        """ Method to transfer filenames between view and model, pull in data to model, and transfer data back to view. """

        # gets a file name from a dialog
        self.view.load_file()

        # transfer filename to model
        self.model.variables['filename'] = self.view.variables['filename'].get()

        # Loads data into model
        self.model.load_file()

        # transfers data from model to view
        self.view.load_treeview(self.model.variables['variant_list'])

        # updates disposition counters
        self.transfer_disposition_counts()

        return None


    def save_file(self, *args, **kwargs) -> None:
        """ Calls the model save method. """

        self.model.save_file()

        return None


    def update_disposition(self, *args, **kwargs) -> None:
        """ Returns the disposition from the view to the data model for saving. """

        # First, we'll tell the view to save any changes from the field widgets into the treeview data
        self.view.record_update()

        # now  ensures the model and the view are referencing the same variant
        selection = self.view.variables['selection_index'].get()

        # creating a dictionary of updated record field data
        update_dict = dict()
        for vcf_field in VCF_FIELDS:
            update_dict[vcf_field] = self.view.variant[vcf_field].get()

        # saving the disposition also
        disposition = self.view.variant['Disposition'].get()

        # Carry the change through the model's method, which also update dispo counts
        self.model.change_disposition(selection, disposition, update_dict)

        # Refresh the view
        self.view.load_treeview(self.model.variables['variant_list'])

        # update the disposition counters
        self.transfer_disposition_counts()

        return None


    def transfer_disposition_counts(self, *args, **kwargs) -> None:
        """ Method to move data between model and view for disposition counts. """

        for x in DISPOSITIONS:
            self.view.variables['Disposition'][x].set(self.model.count_dispositions(x))

        return None


# MAIN LOOP ----------------------------------------------

def main() -> None:

    # Mainloop
    root = Application()
    root.mainloop()    

    return None

if __name__ == '__main__':
    main()
