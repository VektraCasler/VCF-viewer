# variant_data_viewer/application.py
''' An application to view a variant data output file in a dashboard. '''

# IMPORTS ------------------------------------------------

import sys
import ttkbootstrap as tk 

from .global_variables import *
from .infotrack_db import *
from .bed_db import *
from .model import DataModel
from .mainmenu import MainMenu
from .view import RecordView

# VARIABLES ----------------------------------------------

DATA_FIELDS = [
    "Original Input: Chrom",
    "Original Input: Pos",
    "Original Input: Reference allele",
    "Original Input: Alternate allele",
    "Variant Annotation: Gene",
    "Variant Annotation: cDNA change",
    "Variant Annotation: Protein Change",
    "Variant Annotation: RefSeq",
    "VCF: AF",
    "VCF: FAO",
    "VCF: FDP",
    "VCF: HRUN",
    "VCF: Filter",
    "VCF: Genotype",
    "COSMIC: ID",
    "COSMIC: Variant Count",
    "COSMIC: Variant Count (Tissue)",
    "ClinVar: ClinVar ID",
    "ClinVar: Clinical Significance",
    "gnomAD3: Global AF",
    "PhyloP: Vert Score",
    "CADD: Phred",
    "PolyPhen-2: HDIV Prediction",
    "SIFT: Prediction",
    "VCF: FSAF",
    "VCF: FSAR",
    "VCF: FSRF",
    "VCF: FSRR",
    "VCF: Fisher Odds Ratio",
    "VCF: Fisher P Value",
    "VCF: Binom Proportion",
    "VCF: Binom P Value",
    "Mpileup Qual: Read Depth",
    "Mpileup Qual: Start Reads",
    "Mpileup Qual: Stop Reads",
    "Mpileup Qual: Filtered Reference Forward Read Depth",
    "Mpileup Qual: Filtered Reference Reverse Read Depth",
    "Mpileup Qual: Unfiltered Reference Forward Read Depth",
    "Mpileup Qual: Unfiltered Reference Reverse Read Depth",
    "Mpileup Qual: Filtered Variant Forward Read Depth",
    "Mpileup Qual: Filtered Variant Reverse Read Depth",
    "Mpileup Qual: Filtered Variant Binomial Proportion",
    "Mpileup Qual: Filtered Variant Binomial P Value",
    "Mpileup Qual: Filtered Variant Fishers Odds Ratio",
    "Mpileup Qual: Filtered Variant Fishers P Value",
    "Mpileup Qual: Filtered VAF",
    "Mpileup Qual: Unfiltered Variant Forward Read Depth",
    "Mpileup Qual: Unfiltered Variant Reverse Read Depth",
    "Mpileup Qual: Unfiltered Variant Binomial Proportion",
    "Mpileup Qual: Unfiltered Variant Binomial P Value",
    "Mpileup Qual: Unfiltered Variant Fishers Odds Ratio",
    "Mpileup Qual: Unfiltered Variant Fishers P Value",
    "Mpileup Qual: Unfiltered VAF",
    "VCF: LEN",
    "VCF: QD",
    "VCF: STB",
    "VCF: STBP",
    "VCF: SVTYPE",
    "VCF: TYPE",
    "VCF: QUAL",
    "Variant Annotation: Coding",
    "Variant Annotation: Sequence Ontology",
    "Variant Annotation: Transcript",
    "Variant Annotation: All Mappings",
    "UniProt (GENE): Accession Number",
    "dbSNP: rsID",
    "MDL: Sample Count",
    "MDL: Variant Frequency",
    "MDL: Sample List",
    'amp_ID',
    'Cytoband',
    'MANE_transcript (GRCh38)',
    'Genexus_transcript (GRCh37)',
    'Genexus_Exon(s)',
    'Genexus_codons',
    'tier',
    'test_tissue',
    "Disposition",
]

# CLASSES ------------------------------------------------

class Application(tk.Window):

    def __init__(self) -> None:

        super().__init__()

        # Root Window
        self.title('Variant Data Viewer')
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
            '<<FileQuit>>': lambda _: sys.exit(),

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
        self.filename = str()
        self.status_text = str()
        self.disposition = dict()
        for x in DISPOSITIONS:
            self.disposition[x] = int()

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

    def clear_view(self, *args) -> None:
        """ Method to clear the view and loaded data. """

        # nukes the data model and starts anew.
        self.model = DataModel()

        # clear the view widgets.
        self.view.clear_view()

        return None

    def load_file(self, *args, **kwargs) -> None:
        """ Method to transfer filenames between view and model, pull in data \
            to model, and transfer data back to view. """

        # gets a file name from a dialog
        self.view.load_file()

        # transfer filename to model
        self.model.filename = self.view.filename.get()

        # Loads data into model
        self.model.load_file()

        # transfers data from model to view
        self.view.load_treeview(self.model.variant_list)

        # updates disposition counters
        self.transfer_disposition_counts()

        return None

    def save_file(self, *args, **kwargs) -> None:
        """ Calls the model save method. """

        self.model.save_file()

        return None

    def update_disposition(self, *args, **kwargs) -> None:
        """ Returns the disposition from the view to the data model for \
            saving. """

        # First, we'll tell the view to save any changes from the field \
        # widgets into the treeview data
        updated_record = self.view.record_update()

        # now  ensures the model and the view are referencing the same variant.
        selection = self.view.selection_index.get()

        # saving the disposition also
        disposition = self.view.variant['Disposition'].get()

        # Carry the change through the model's method, which also update \
        # dispo counts.
        self.model.change_disposition(selection, disposition, updated_record)

        # Refresh the view
        self.view.load_treeview(self.model.variant_list)

        # update the disposition counters
        self.transfer_disposition_counts()

        return None

    def transfer_disposition_counts(self, *args, **kwargs) -> None:
        """ Method to move data between model and view for disposition \
            counts. """

        for x in DISPOSITIONS:
            self.view.disposition[x].set(self.model.count_dispositions(x))

        return None

# MAIN LOOP ----------------------------------------------

def main() -> None:

    # Mainloop
    root = Application()
    root.mainloop()    

    return None

if __name__ == '__main__':
    main()
