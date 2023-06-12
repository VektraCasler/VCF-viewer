# vcf_data_viewer/application.py
""" Main application root window. """

# IMPORTS ------------------------------------------------

import ttkbootstrap as tk
from tkinter import messagebox
from tkinter import filedialog

from . import views as v 
from . import models as m
from . import images
from .mainmenu import MainMenu

import os 
import json
import webbrowser

# CLASSES ------------------------------------------------

class Application(tk.Window):
    """ Application root window. """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.model = m.DataModel

        self.title("VCF Data Viewer")
        self.columnconfigure(0, weight=1)
        self.taskbar_icon = tk.PhotoImage(file=images.URMC_LOGO_16)
        self.iconphoto(True, self.taskbar_icon)

        self.settings_model = m.SettingsModel()
        self._load_settings()

        menu = MainMenu(self, self.settings)
        self.config(menu=menu)

        event_callbacks={
            '<<FileSelect>>': self._on_file_select,
            '<<FileClear>>': self._on_file_select,
            '<<FileSave>>': self._on_file_select,
            '<<FileQuit>>': lambda _: self.quit(),
            '<<ExportTextFiles>>': self._export_text_files,
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
            '<<NewRecord>>': self._new_record
        }
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        # tk.Label(
        #     self,
        #     text="VCF Data Viewer Application",
        #     font=("TkDefaultFont", 16)
        # ).grid(row=0)

        self.recordform = v.ViewerWindow(
            self, 
            self.model,
            self.settings
        )

        # self.recordform.grid(row=1, padx=10, sticky=(tk.W + tk.E))
        self.recordform.bind('<<SaveRecord>>', self._on_save)
        self.notebook.add(self.recordform, text='Entry Form')
        self.recordlist = v.RecordList(self)
        self.notebook.insert(0, self.recordlist, text='Records')
        self._populate_recordlist()
        self.recordlist.bind('<<OpenRecord>>', self._open_record)

        # status bar
        self.status = tk.StringVar()
        self.statusbar = tk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)
        tk.Label(self, textvariable=self.status).grid(sticky=(tk.W + tk.E), row=3, padx=10)

        self._records_saved = 0
        self._show_recordlist()

        return

    def _on_save(self, *_):
        """Handles save button clicks"""
        
        # First, check for errors
        errors = self.recordform.get_errors()
        if errors:
            self.status.set(
                "Cannot save, error in fields: {}"
                .format(', '.join(errors.keys()))
            )
            message = "Cannot save record"
            detail = (
                "The following fields have errors: "
                "\n * {}".format(
                    '\n *'.join(errors.keys())
            ))
            print(message)
            messagebox.showerror(
                title = "Error",
                message=message,
                detail=detail
            )
            return False

        data = self.recordform.get()
        rownum = self.recordform.current_record
        self.model.save_record(data, rownum)
        self._records_saved += 1
        self.status.set(
            f"{self._records_saved} records saved this session"
        )
        self.recordform.reset()
        self._populate_recordlist()

    def _on_file_select(self, *_):
        """ Handle the file->select action. """
        
        filename = filedialog.asksaveasfilename(
            title="Select the target file for saving records",
            defaultextension='.csv',
            filetypes=[('CSV', '*.csv *.CSV')]
        )

        if filename:
            self.model = m.VariantListModel(filename=filename)
            self._populate_recordlist()

        return

    def _load_settings(self):
        '''Load settings into our self.settings dict.'''
        
        vartypes = {
            'bool': tk.BooleanVar,
            'str': tk.StringVar,
            'int': tk.IntVar,
            'float':tk.DoubleVar
        }
        self.settings = dict()
        for key, data in self.settings_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.settings[key] = vartype(value=data['value'])
            
        for var in self.settings.values():
            var.trace_add('write', self._save_settings)
        
        return
            
    def _save_settings(self, *_):
        for key, variable in self.settings.items():
            self.settings_model.set(key, variable.get())
        self.settings_model.save()

        return

    def _show_recordlist(self, *_):
        self.notebook.select(self.recordlist)

    def _populate_recordlist(self):
        try:
            rows = self.model.get_all_records()
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem reading file',
                detail=str(e)
            )
        else:
            self.recordlist.populate(rows)

    def _new_record(self, *_):
        self.recordform.load_record(None)
        # self.notebook.select(self.recordform)

    def _open_record(self, *_):
        '''Open the selected id from recordlist in the recordform'''
        rowkey=self.treeview_variant_list.selected_id
        try:
            record = self.model.get_record(rowkey)
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem reading file',
                detail=str(e)
            )
        else:
            self.recordform.load_record(rowkey, record)
            self.notebook.select(self.recordform)
    
        return
    
    def _export_text_files(self, *_):
        pass
        return

# MAIN LOOP ----------------------------------------------

def main():
    pass
    return

if __name__ == '__main__':
    main()