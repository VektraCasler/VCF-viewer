# CSViewer.py
''' An application to view a csv file. '''

# IMPORTS ------------------------------------------------

import tkinter as tk 
from tkinter import filedialog as fd
import tkinter.ttk as ttk 
import os 
import csv
import json
from tkinter.messagebox import showinfo

# VARIABLES ----------------------------------------------

settings_filename = 'settings.json'
if os.path.exists(settings_filename):
    SETTINGS = json.load(settings_filename)
else:
    SETTINGS = {
    }

small_font = ('roboto',10)
large_font = ('roboto',24)

vcf_columns = [
"Original Input: Chrom",
"Original Input: Pos",
"Original Input: Reference allele",
"Original Input: Alternate allele",
"Variant Annotation: Gene",
"Variant Annotation: cDNA change",
"Variant Annotation: Protein Change",
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
"Mpileup Qual: Unfiltered Variant Forward Read Depth",
"Mpileup Qual: Unfiltered Variant Reverse Read Depth",
"Mpileup Qual: Unfiltered Variant Binomial Proportion",
"Mpileup Qual: Unfiltered Variant Binomial P Value",
"Mpileup Qual: Unfiltered Variant Fishers Odds Ratio",
"Mpileup Qual: Unfiltered Variant Fishers P Value",
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
]


# CLASSES ------------------------------------------------

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(
            tw, 
            text=self.text, 
            justify=tk.LEFT,
            background="#ffffe0", 
            relief=tk.SOLID, 
            borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class App(tk.Tk):

    def __init__(self) -> None:
        super().__init__()

        # Root Window
        self.title('VCF Result Viewer')
        self.resizable(True, True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.geometry('600x400')

        # Variables
        self.filename = tk.StringVar()
        self.filename.set('No CSV File Loaded')
        self.status_text = tk.StringVar()
        self.disposition = tk.StringVar()
        self.dispo_none_count = tk.IntVar()
        self.dispo_unknown_count = tk.IntVar()
        self.dispo_VUS_count = tk.IntVar()
        self.dispo_mutation_count = tk.IntVar()

        self.variant_info = dict()
        for x in vcf_columns:
            self.variant_info[x] = tk.StringVar()
        
        # Base Frame
        self.base_frame = tk.Frame(self)
        self.base_frame.columnconfigure(0, weight=1)
        self.base_frame.columnconfigure(1, weight=99)
        self.base_frame.rowconfigure(0, weight=1)
        self.base_frame.grid(column=0,row=0, sticky='nsew')
        
        # Left Frame
        self.frame_left = tk.LabelFrame(self.base_frame, text="VCF File Info")
        self.frame_left.grid(column=0, row=0, sticky='wens', ipadx=5, ipady=5, padx=10, pady=10)
        self.frame_left.columnconfigure(0, weight=5)
        self.frame_left.columnconfigure(1, weight=1)
        self.frame_left.rowconfigure(0, weight=1)
        self.frame_left.rowconfigure(1, weight=1)
        self.frame_left.rowconfigure(2, weight=99)

        # Left Frame widgets
        tk.Button(self.frame_left, text="Load a CSV File", command=self.loadCSV).grid(column=0, row=0, columnspan=2, sticky='news', padx=5, pady=5)
        self.filenamelabel = tk.Label(self.frame_left, textvariable=self.filename, relief='sunken', bg='#FFFFFF')
        self.filenamelabel.grid(column=0, row=1, columnspan=2, sticky='news', padx=5, pady=5, ipady=10)
        CreateToolTip(self.filenamelabel, text = 'VCF processing output file currently loaded for viewing.')

        # Treeview
        self.variant_tree = ttk.Treeview(self.frame_left, columns=vcf_columns, displaycolumns=[4], selectmode='browse', show='headings')
        for x in vcf_columns:
            self.variant_tree.heading(x, text=x, anchor='center')
        self.variant_tree.heading(4, text='Variant')
        self.variant_tree.grid(column=0, row=2, columnspan=1, sticky='nsew', padx=(5,0), pady=5)
        self.variant_tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Treeview Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_left, orient=tk.VERTICAL, command=self.variant_tree.yview)
        self.variant_tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=1, sticky='nse', padx=(0,5), pady=5)

        # Disposition Frame
        # tk.Button(self.frame_left, text="Load a CSV File", command=self.loadCSV).grid(column=0, row=9, columnspan=2, sticky='news', padx=5, pady=5)
        self.disposition_frame = tk.LabelFrame(self.frame_left, text="Disposition")
        self.disposition_frame.grid(column=0, columnspan=2, row=9, sticky='news', padx=10, pady=10)
        self.disposition_frame.rowconfigure(0, weight=1)
        for x in range(4):
            self.disposition_frame.columnconfigure(x, weight=1)
        tk.Label(self.disposition_frame, text='NA').grid(row=0, column=0)
        tk.Label(self.disposition_frame, text='???').grid(row=0, column=1)
        tk.Label(self.disposition_frame, text='VUS').grid(row=0, column=2)
        tk.Label(self.disposition_frame, text='Mut').grid(row=0, column=3)
        
        self.radio_none = tk.Radiobutton(self.disposition_frame, text="1", variable=self.disposition, anchor='center')
        self.radio_none.grid(row=1, column=0, sticky='news')
        self.radio_unknown = tk.Radiobutton(self.disposition_frame, text="2", variable=self.disposition, anchor='center')
        self.radio_unknown.grid(row=1, column=1, sticky='news')
        self.radio_VUS = tk.Radiobutton(self.disposition_frame, text="3", variable=self.disposition, anchor='center')
        self.radio_VUS.grid(row=1, column=2, sticky='news')
        self.radio_mutation = tk.Radiobutton(self.disposition_frame, text="4", variable=self.disposition, anchor='center')
        self.radio_mutation.grid(row=1, column=3, sticky='news')
        
        tk.Label(self.disposition_frame, textvariable=self.dispo_none_count).grid(row=2, column=0, sticky='ns', padx=5)
        tk.Label(self.disposition_frame, textvariable=self.dispo_unknown_count).grid(row=2, column=1, sticky='ns', padx=5)
        tk.Label(self.disposition_frame, textvariable=self.dispo_VUS_count).grid(row=2, column=2, sticky='ns', padx=5)
        tk.Label(self.disposition_frame, textvariable=self.dispo_mutation_count).grid(row=2, column=3, sticky='ns', padx=5)
        
        tk.Button(self.frame_left, text="Load a CSV File", command=self.loadCSV).grid(column=0, row=99, columnspan=4, sticky='news', padx=5, pady=5)


        # Right Frame------------------------------------------------
        self.frame_right = tk.Frame(self.base_frame)
        self.frame_right.columnconfigure(0, weight=1)
        self.frame_right.columnconfigure(1, weight=1)
        self.frame_right.rowconfigure(0,weight=0)
        self.frame_right.rowconfigure(1,weight=1)
        self.frame_right.rowconfigure(2,weight=1)

        self.frame_right.grid(column=1, row=0, sticky='nsew', ipadx=5, ipady=5)

        # Basic Info Frame-------------------------------------------
        self.BI_frame = tk.LabelFrame(self.frame_right, text='Locus Info')
        self.BI_frame.columnconfigure(0, weight=1)
        self.BI_frame.columnconfigure(1, weight=1)
        self.BI_frame.columnconfigure(2, weight=3)
        self.BI_frame.columnconfigure(3, weight=0)
        self.BI_frame.columnconfigure(4, weight=3)
        self.BI_frame.rowconfigure(0, weight=1)
        self.BI_frame.rowconfigure(1, weight=1)
        self.BI_frame.rowconfigure(2, weight=1)
        self.BI_frame.rowconfigure(3, weight=1)
        self.BI_frame.grid(column=0, row=0, columnspan=2, sticky='news', padx=10, pady=10)

        tk.Label(self.BI_frame, text="Gene").grid(column=0, row=0, rowspan=1,sticky='news')
        self.genelabel = tk.Label(self.BI_frame, width=6, textvariable=self.variant_info["Variant Annotation: Gene"], relief='sunken', bg='#FFFFFF', font=('bold', 24, 'bold'))
        self.genelabel.grid(column=0, row=1, rowspan=3,sticky='news', padx=10, pady=10)
        CreateToolTip(self.genelabel, text = 'Gene currently selected from the variant list.')
        tk.Label(self.BI_frame, text="Chromosome").grid(column=1, row=0, sticky='news')
        self.chromelabel = tk.Label(self.BI_frame, textvariable=self.variant_info["Original Input: Chrom"], relief='sunken', bg='#FFFFFF')
        self.chromelabel.grid(column=1, row=1, sticky='news', pady=5, padx=10, ipady=5)
        CreateToolTip(self.chromelabel, text = 'Chromosome on which this gene is located.')
        tk.Label(self.BI_frame, text="Base Pair").grid(column=1, row=2, sticky='news')
        self.bplabel = tk.Label(self.BI_frame, textvariable=self.variant_info["Original Input: Pos"], relief='sunken', bg='#FFFFFF')
        self.bplabel.grid(column=1, row=3, sticky='news', pady=5, padx=10, ipady=5)
        CreateToolTip(self.bplabel, text = 'Base pair location for gene on this chromosome.')
        tk.Label(self.BI_frame, text="Ref Allele").grid(column=2, row=2, sticky='news')
        self.refallelelabel = tk.Label(self.BI_frame, textvariable=self.variant_info["Original Input: Reference allele"], relief='sunken', bg='#FFFFFF')
        self.refallelelabel.grid(column=2, row=3, sticky='news', pady=5, padx=10, ipady=5)
        CreateToolTip(self.refallelelabel, text = 'Reference allele found at this location.')
        tk.Label(self.BI_frame, text="-->", fg='red').grid(column=3, row=3, sticky='news')
        tk.Label(self.BI_frame, text="Variant Allele").grid(column=4, row=2, sticky='news')
        self.altallelelabel = tk.Label(self.BI_frame, textvariable=self.variant_info["Original Input: Alternate allele"], relief='sunken', bg='#FFFFFF')
        self.altallelelabel.grid(column=4, row=3, sticky='news', pady=5, padx=10, ipady=5)
        CreateToolTip(self.altallelelabel, text = 'Variant allele encountered in sequencing.')
        tk.Label(self.BI_frame, text="DNA Change (c-dot)").grid(column=2, row=0, sticky='news')
        self.cdotlabel = tk.Label(self.BI_frame, text="C-dot", textvariable=self.variant_info["Variant Annotation: cDNA change"], relief='sunken', bg='#FFFFFF')
        self.cdotlabel.grid(column=2, row=1, sticky='news', pady=5, padx=10, ipady=5)
        CreateToolTip(self.cdotlabel, text = 'DNA change nomenclature.')
        tk.Label(self.BI_frame, text="Protein Change (p-dot)").grid(column=4, row=0, sticky='news')
        self.pdotlabel = tk.Label(self.BI_frame, text="P-dot", textvariable=self.variant_info["Variant Annotation: Protein Change"], relief='sunken', bg='#FFFFFF')
        self.pdotlabel.grid(column=4, row=1, sticky='news', pady=5, padx=10, ipady=5)
        CreateToolTip(self.pdotlabel, text = 'Protein change nomenclature.')


        # Genexys Info Frame------------------------------------------------
        self.GX_frame = tk.LabelFrame(self.frame_right, text='Genexys Data')
        self.GX_frame.grid(column=0, row=1, padx=(10,10), pady=(0,10), sticky='news')
        self.GX_frame.columnconfigure(0, weight=2)
        self.GX_frame.columnconfigure(1, weight=3)
        self.GX_frame.columnconfigure(2, weight=1)
        self.GX_frame.columnconfigure(3, weight=1)

        # Genexys Region
        self.MPL_GX_frame = tk.Frame(self.GX_frame, relief='raised', border=5)
        self.MPL_GX_frame.grid(column=0, columnspan=4, row=20, padx=5, pady=5, sticky='news')
        self.MPL_GX_frame.columnconfigure(0, weight=2)
        self.MPL_GX_frame.columnconfigure(1, weight=1)
        self.MPL_GX_frame.columnconfigure(2, weight=2)
        self.MPL_GX_frame.columnconfigure(3, weight=2)
        tk.Label(self.MPL_GX_frame, text='Genexys', font=('bold', 20, 'bold')).grid(column=0, row=0, rowspan=2, sticky='news', padx=10, pady=(10,0))
        tk.Label(self.MPL_GX_frame, text='Read Counts').grid(column=0, row=2, rowspan=1, sticky='news')
        tk.Label(self.MPL_GX_frame, text='Forward').grid(column=2, row=0, sticky='news', ipady=5, pady=(5,0), padx=5)
        tk.Label(self.MPL_GX_frame, text='Reverse').grid(column=3, row=0, sticky='news', ipady=5, pady=(5,0), padx=5)
        tk.Label(self.MPL_GX_frame, text='Reference').grid(column=1, row=1, sticky='news', ipady=5, pady=5, padx=5)
        tk.Label(self.MPL_GX_frame, text='Variant').grid(column=1, row=2, sticky='news', ipady=5, pady=5, padx=5)
        self.GXFSRFlabel = tk.Label(self.MPL_GX_frame, textvariable=self.variant_info["VCF: FSRF"], relief='sunken', bg='#FFFFFF')
        self.GXFSRFlabel.grid(column=2, row=1, sticky='news', pady=5, padx=5)
        CreateToolTip(self.GXFSRFlabel, text = 'Genexys count of REFERENCE allele FORWARD reads at this location.')
        self.GXFSRRlabel = tk.Label(self.MPL_GX_frame, textvariable=self.variant_info["VCF: FSRR"], relief='sunken', bg='#FFFFFF')
        self.GXFSRRlabel.grid(column=3, row=1, sticky='news', pady=5, padx=5)
        CreateToolTip(self.GXFSRRlabel, text = 'Genexys count of REFERENCE allele REVERSE reads at this location.')
        self.GXFSAFlabel = tk.Label(self.MPL_GX_frame, textvariable=self.variant_info["VCF: FSAF"], relief='sunken', bg='#FFFFFF')
        self.GXFSAFlabel.grid(column=2, row=2, sticky='news', pady=5, padx=5)
        CreateToolTip(self.GXFSAFlabel, text = 'Genexys count of VARIANT allele FORWARD reads at this location.')
        self.GXFSARlabel = tk.Label(self.MPL_GX_frame, textvariable=self.variant_info["VCF: FSAR"], relief='sunken', bg='#FFFFFF')
        self.GXFSARlabel.grid(column=3, row=2, sticky='news', pady=5, padx=5)
        CreateToolTip(self.GXFSARlabel, text = 'Genexys count of VARIANT allele REVERSE reads at this location.')

        tk.Label(self.GX_frame, text="Variant Binomial Proportion").grid(column=0, row=24, sticky='news', pady=5, padx=5)
        tk.Label(self.GX_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Binomial Proportion"], relief='sunken', bg='#FFFFFF').grid(column=1, row=24, sticky='news', pady=5, padx=10, ipady=5)
        tk.Label(self.GX_frame, text="P-value").grid(column=2, row=24, sticky='news', pady=5, padx=5)
        tk.Label(self.GX_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Binomial P Value"], relief='sunken', bg='#FFFFFF').grid(column=3, row=24, sticky='news', pady=5, padx=10, ipady=5)

        tk.Label(self.GX_frame, text="Variant Fishers Odds Ratio").grid(column=0, row=25, sticky='news', pady=5, padx=5)
        tk.Label(self.GX_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Fishers Odds Ratio"], relief='sunken', bg='#FFFFFF').grid(column=1, row=25, sticky='news', pady=5, padx=10, ipady=5)
        tk.Label(self.GX_frame, text="P-value").grid(column=2, row=25, sticky='news', pady=5, padx=5)
        tk.Label(self.GX_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Fishers P Value"], relief='sunken', bg='#FFFFFF').grid(column=3, row=25, sticky='news', pady=5, padx=10, ipady=5)

        tk.Label(self.GX_frame, text="Allele Fraction").grid(column=0, row=0, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: AF"]).grid(column=1, row=0, sticky='news')
        tk.Label(self.GX_frame, text="FAO").grid(column=0, row=1, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: FAO"]).grid(column=1, row=1, sticky='news')
        tk.Label(self.GX_frame, text="FDP").grid(column=0, row=2, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: FDP"]).grid(column=1, row=2, sticky='news')
        tk.Label(self.GX_frame, text="HRUN").grid(column=0, row=3, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: HRUN"]).grid(column=1, row=3, sticky='news')
        tk.Label(self.GX_frame, text="Filter").grid(column=0, row=4, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: Filter"]).grid(column=1, row=4, sticky='news')
        tk.Label(self.GX_frame, text="Genotype").grid(column=0, row=5, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: Genotype"]).grid(column=1, row=5, sticky='news')
        tk.Label(self.GX_frame, text="Length of Variant (BP)").grid(column=0, row=14, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: LEN"]).grid(column=1, row=14, sticky='news')
        tk.Label(self.GX_frame, text="QD").grid(column=0, row=15, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: QD"]).grid(column=1, row=15, sticky='news')
        tk.Label(self.GX_frame, text="Strand Bias Calculation").grid(column=0, row=16, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: STB"]).grid(column=1, row=16, sticky='news')
        tk.Label(self.GX_frame, text="P-Value").grid(column=2, row=16, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: STBP"]).grid(column=3, row=16, sticky='news')
        tk.Label(self.GX_frame, text="SVTYPE").grid(column=0, row=18, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: SVTYPE"]).grid(column=1, row=18, sticky='news')
        tk.Label(self.GX_frame, text="TYPE").grid(column=0, row=19, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: TYPE"]).grid(column=1, row=19, sticky='news')
        tk.Label(self.GX_frame, text="QUAL").grid(column=0, row=30, sticky='news')
        tk.Label(self.GX_frame, textvariable=self.variant_info["VCF: QUAL"]).grid(column=1, row=30, sticky='news')

        # MPL Info Frame------------------------------------------------
        self.MPL_frame = tk.LabelFrame(self.frame_right, text='M-Pileup Data')
        self.MPL_frame.grid(column=1, row=1, padx=(10,10), pady=(0,10), sticky='news')
        self.MPL_frame.columnconfigure(0, weight=2)
        self.MPL_frame.columnconfigure(1, weight=3)
        self.MPL_frame.columnconfigure(2, weight=1)
        self.MPL_frame.columnconfigure(3, weight=1)

        # Q20 Region
        self.MPL_Q20_frame = tk.Frame(self.MPL_frame, relief='raised', border=5)
        self.MPL_Q20_frame.grid(column=0, columnspan=4, row=3, padx=5, pady=5, sticky='news')
        self.MPL_Q20_frame.columnconfigure(0, weight=2)
        self.MPL_Q20_frame.columnconfigure(1, weight=1)
        self.MPL_Q20_frame.columnconfigure(2, weight=2)
        self.MPL_Q20_frame.columnconfigure(3, weight=2)
        tk.Label(self.MPL_Q20_frame, text='Q20', font=('bold', 20, 'bold')).grid(column=0, row=0, rowspan=2, sticky='news', padx=10, pady=(10,0))
        tk.Label(self.MPL_Q20_frame, text='Read Counts').grid(column=0, row=2, rowspan=1, sticky='news')
        tk.Label(self.MPL_Q20_frame, text='Forward').grid(column=2, row=0, sticky='news', ipady=5, pady=(5,0), padx=5)
        tk.Label(self.MPL_Q20_frame, text='Reverse').grid(column=3, row=0, sticky='news', ipady=5, pady=(5,0), padx=5)
        tk.Label(self.MPL_Q20_frame, text='Reference').grid(column=1, row=1, sticky='news', ipady=5, pady=5, padx=5)
        tk.Label(self.MPL_Q20_frame, text='Variant').grid(column=1, row=2, sticky='news', ipady=5, pady=5, padx=5)
        tk.Label(self.MPL_Q20_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Forward Read Depth"], relief='sunken', bg='#FFFFFF').grid(column=2, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.MPL_Q20_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Reverse Read Depth"], relief='sunken', bg='#FFFFFF').grid(column=3, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.MPL_Q20_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Reference Forward Read Depth"], relief='sunken', bg='#FFFFFF').grid(column=2, row=2, sticky='news', pady=5, padx=5)
        tk.Label(self.MPL_Q20_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Reference Reverse Read Depth"], relief='sunken', bg='#FFFFFF').grid(column=3, row=2, sticky='news', pady=5, padx=5)

        tk.Label(self.MPL_frame, text="Variant Binomial Proportion").grid(column=0, row=4, sticky='news', pady=5, padx=5)
        tk.Label(self.MPL_frame, textvariable=self.variant_info["VCF: Binom Proportion"], relief='sunken', bg='#FFFFFF').grid(column=1, row=4, sticky='news', pady=5, padx=10, ipady=5)
        tk.Label(self.MPL_frame, text="P-value").grid(column=2, row=4, sticky='news', pady=5, padx=5)
        tk.Label(self.MPL_frame, textvariable=self.variant_info["VCF: Binom P Value"], relief='sunken', bg='#FFFFFF').grid(column=3, row=4, sticky='news', pady=5, padx=10, ipady=5)

        tk.Label(self.MPL_frame, text="Variant Fishers Odds Ratio").grid(column=0, row=5, sticky='news', pady=5, padx=5)
        tk.Label(self.MPL_frame, textvariable=self.variant_info["VCF: Fisher Odds Ratio"], relief='sunken', bg='#FFFFFF').grid(column=1, row=5, sticky='news', pady=5, padx=10, ipady=5)
        tk.Label(self.MPL_frame, text="P-value").grid(column=2, row=5, sticky='news', pady=5, padx=5)
        tk.Label(self.MPL_frame, textvariable=self.variant_info["VCF: Fisher P Value"], relief='sunken', bg='#FFFFFF').grid(column=3, row=5, sticky='news', pady=5, padx=10, ipady=5)

        # Q1 Region
        self.MPL_Q1_frame = tk.Frame(self.MPL_frame, relief='raised', border=5)
        self.MPL_Q1_frame.grid(column=0, columnspan=4, row=6, padx=5, pady=5, sticky='news')
        self.MPL_Q1_frame.columnconfigure(0, weight=2)
        self.MPL_Q1_frame.columnconfigure(1, weight=1)
        self.MPL_Q1_frame.columnconfigure(2, weight=2)
        self.MPL_Q1_frame.columnconfigure(3, weight=2)
        tk.Label(self.MPL_Q1_frame, text='Q1', font=('bold', 20, 'bold')).grid(column=0, row=0, rowspan=2, sticky='news', padx=10, pady=10)
        tk.Label(self.MPL_Q1_frame, text='Read Counts').grid(column=0, row=2, rowspan=1, sticky='news')
        tk.Label(self.MPL_Q1_frame, text='Forward').grid(column=2, row=0, sticky='news', ipady=5, pady=(5,0), padx=5)
        tk.Label(self.MPL_Q1_frame, text='Reverse').grid(column=3, row=0, sticky='news', ipady=5, pady=(5,0), padx=5)
        tk.Label(self.MPL_Q1_frame, text='Reference').grid(column=1, row=1, sticky='news', ipady=5, pady=5, padx=5)
        tk.Label(self.MPL_Q1_frame, text='Variant').grid(column=1, row=2, sticky='news', ipady=5, pady=5, padx=5)
        tk.Label(self.MPL_Q1_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Reference Forward Read Depth"], relief='sunken', bg='#FFFFFF').grid(column=2, row=2, sticky='news', pady=5, padx=10)
        tk.Label(self.MPL_Q1_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Reference Reverse Read Depth"], relief='sunken', bg='#FFFFFF').grid(column=3, row=2, sticky='news', pady=5, padx=10)
        tk.Label(self.MPL_Q1_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Forward Read Depth"], relief='sunken', bg='#FFFFFF').grid(column=2, row=1, sticky='news', pady=5, padx=10)
        tk.Label(self.MPL_Q1_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Reverse Read Depth"], relief='sunken', bg='#FFFFFF').grid(column=3, row=1, sticky='news', pady=5, padx=10)

        # Q1 Stats Area
        tk.Label(self.MPL_frame, text="Variant Binomial Proportion").grid(column=0, row=7, sticky='news', pady=5, padx=5)
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Binomial Proportion"], relief='sunken', bg='#FFFFFF').grid(column=1, row=7, sticky='news', pady=5, padx=10, ipady=5)
        tk.Label(self.MPL_frame, text="P-value").grid(column=2, row=7, sticky='news', pady=5, padx=5)
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Binomial P Value"], relief='sunken', bg='#FFFFFF').grid(column=3, row=7, sticky='news', pady=5, padx=10, ipady=5)
        tk.Label(self.MPL_frame, text="Variant Fishers Odds Ratio").grid(column=0, row=8, sticky='news', pady=5, padx=5)
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"], relief='sunken', bg='#FFFFFF').grid(column=1, row=8, sticky='news', pady=5, padx=10, ipady=5)
        tk.Label(self.MPL_frame, text="P-value").grid(column=2, row=8, sticky='news', pady=5, padx=5)
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Fishers P Value"], relief='sunken', bg='#FFFFFF').grid(column=3, row=8, sticky='news', pady=5, padx=10, ipady=5)

        # MPL Listed Stats
        tk.Label(self.MPL_frame, text="Total Read Depth").grid(column=0, row=0, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Read Depth"], relief='sunken', bg='#FFFFFF').grid(column=1, row=0, sticky='news', pady=5, padx=10, ipady=5)
        tk.Label(self.MPL_frame, text="Read Start-Point Count").grid(column=0, row=1, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Start Reads"], relief='sunken', bg='#FFFFFF').grid(column=1, row=1, sticky='news', pady=5, padx=10, ipady=5)
        tk.Label(self.MPL_frame, text="Read End-Point Count").grid(column=0, row=2, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Stop Reads"], relief='sunken', bg='#FFFFFF').grid(column=1, row=2, sticky='news', pady=5, padx=10, ipady=5)


        return
    
    def loadCSV(self):

        csv_dict = dict()
        self.filename.set(str(fd.askopenfilename(filetypes=[('CSV','*.csv')])))
        with open(self.filename.get(), 'r') as csv_file:
            counter = 0
            for row in csv.DictReader(csv_file, fieldnames=vcf_columns, delimiter='\t'):
                if counter != 0:
                    csv_dict[counter] = row
                    values_list = list()
                    for key, value in csv_dict[counter].items():
                        values_list.append(value)
                    self.variant_tree.insert('', tk.END, values=values_list)
                counter += 1

        return
    
    def item_selected(self, event):

        for selected_item in self.variant_tree.selection():
            item = self.variant_tree.item(selected_item)
            record = item['values']

            for x in range(len(vcf_columns)):
                self.variant_info[vcf_columns[x]].set(record[x])

        return

# FUNCTIONS ----------------------------------------------

def CreateToolTip(widget: tk.Widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# MAIN LOOP ----------------------------------------------

def main():

    # Mainloop
    root = App()
    root.mainloop()    

    return

if __name__ == '__main__':
    main()
