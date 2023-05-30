# CSViewer.py
''' An application to view a csv file. '''

# IMPORTS ------------------------------------------------

import tkinter as tk 
from tkinter import filedialog as fd
# import tkinter.ttk as ttk 
import ttkbootstrap as ttk 
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
    "Disposition",
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
    "COSMIC: Variant Count (Tissue)", # Very long text, needs wordwrap
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
    "Variant Annotation: All Mappings", # Very long text, needs wordwrap
    "UniProt (GENE): Accession Number",
    "dbSNP: rsID",
    "MDL: Sample Count",
    "MDL: Variant Frequency",
    "MDL: Sample List", # Very long text, needs wordwrap
]

tooltips = {
    "Disposition":'What to call this variant.',
    "Original Input: Chrom":'Chromosome on which this gene is found.',
    "Original Input: Pos":'Base pair position of the gene on the chromosome.',
    "Original Input: Reference allele":'Expected finding at this base pair location.',
    "Original Input: Alternate allele":'Specimen finding at this base pair location.',
    "Variant Annotation: Gene":'Gene currently selected from the variant list.',
    "Variant Annotation: cDNA change":'Alteration in the DNA at this location.',
    "Variant Annotation: Protein Change":'Resultant alteration in the protein at this location.',
    "VCF: AF":'Allele fraction of reads with this variant.',
    "VCF: FAO":"tooltip needed",
    "VCF: FDP":"tooltip needed",
    "VCF: HRUN":"tooltip needed",
    "VCF: Filter":"tooltip needed",
    "VCF: Genotype":"tooltip needed",
    "COSMIC: ID":"tooltip needed",
    "COSMIC: Variant Count":"tooltip needed",
    "COSMIC: Variant Count (Tissue)":"tooltip needed", # Very long text, needs wordwrap
    "ClinVar: ClinVar ID":"tooltip needed",
    "ClinVar: Clinical Significance":"tooltip needed",
    "gnomAD3: Global AF":"tooltip needed",
    "PhyloP: Vert Score":"tooltip needed",
    "CADD: Phred":"tooltip needed",
    "PolyPhen-2: HDIV Prediction":"tooltip needed",
    "SIFT: Prediction":"tooltip needed",
    "VCF: FSAF":"tooltip needed",
    "VCF: FSAR":"tooltip needed",
    "VCF: FSRF":"tooltip needed",
    "VCF: FSRR":"tooltip needed",
    "VCF: Fisher Odds Ratio":"tooltip needed",
    "VCF: Fisher P Value":"tooltip needed",
    "VCF: Binom Proportion":"tooltip needed",
    "VCF: Binom P Value":"tooltip needed",
    "Mpileup Qual: Read Depth":"tooltip needed",
    "Mpileup Qual: Start Reads":"tooltip needed",
    "Mpileup Qual: Stop Reads":"tooltip needed",
    "Mpileup Qual: Filtered Reference Forward Read Depth":"tooltip needed",
    "Mpileup Qual: Filtered Reference Reverse Read Depth":"tooltip needed",
    "Mpileup Qual: Unfiltered Reference Forward Read Depth":"tooltip needed",
    "Mpileup Qual: Unfiltered Reference Reverse Read Depth":"tooltip needed",
    "Mpileup Qual: Filtered Variant Forward Read Depth":"tooltip needed",
    "Mpileup Qual: Filtered Variant Reverse Read Depth":"tooltip needed",
    "Mpileup Qual: Filtered Variant Binomial Proportion":"tooltip needed",
    "Mpileup Qual: Filtered Variant Binomial P Value":"tooltip needed",
    "Mpileup Qual: Filtered Variant Fishers Odds Ratio":"tooltip needed",
    "Mpileup Qual: Filtered Variant Fishers P Value":"tooltip needed",
    "Mpileup Qual: Unfiltered Variant Forward Read Depth":"tooltip needed",
    "Mpileup Qual: Unfiltered Variant Reverse Read Depth":"tooltip needed",
    "Mpileup Qual: Unfiltered Variant Binomial Proportion":"tooltip needed",
    "Mpileup Qual: Unfiltered Variant Binomial P Value":"tooltip needed",
    "Mpileup Qual: Unfiltered Variant Fishers Odds Ratio":"tooltip needed",
    "Mpileup Qual: Unfiltered Variant Fishers P Value":"tooltip needed",
    "VCF: LEN":"tooltip needed",
    "VCF: QD":"tooltip needed",
    "VCF: STB":"tooltip needed",
    "VCF: STBP":"tooltip needed",
    "VCF: SVTYPE":"tooltip needed",
    "VCF: TYPE":"tooltip needed",
    "VCF: QUAL":"tooltip needed",
    "Variant Annotation: Coding":"tooltip needed",
    "Variant Annotation: Sequence Ontology":"tooltip needed",
    "Variant Annotation: Transcript":"tooltip needed",
    "Variant Annotation: All Mappings":"tooltip needed", # Very long text, needs wordwrap
    "UniProt (GENE): Accession Number":"tooltip needed",
    "dbSNP: rsID":"tooltip needed",
    "MDL: Sample Count":"tooltip needed",
    "MDL: Variant Frequency":"tooltip needed",
    "MDL: Sample List":"tooltip needed", # Very long text, needs wordwrap
}

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
        self.geometry('800x600')
        self.color_warning = '#CC0000'
        self.color_normal = '#000000'
        self.color_enabled = '#ffffff'
        self.color_disabled = '#cccccc'


        # Variables
        self.vars = dict()
        self.vars['filename'] = tk.StringVar()
        self.vars['filename'].set('No CSV File Loaded')
        self.vars['status_text'] = tk.StringVar()
        self.vars['disposition'] = tk.StringVar()
        self.vars['dispo_none_count'] = tk.IntVar()
        self.vars['dispo_unknown_count'] = tk.IntVar()
        self.vars['dispo_VUS_count'] = tk.IntVar()
        self.vars['dispo_mutation_count'] = tk.IntVar()

        self.variant = dict()
        for x in vcf_columns:
            self.variant[x] = tk.StringVar()

        self.labels = dict()
        for x in vcf_columns:
            self.labels[x] = tk.Label()

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
        
        # FRAMES ------------------------------------------------------------------------

        # Base Frame
        self.frame_base = tk.Frame(self)
        self.frame_base.pack(expand=True, fill='both',ipadx=10, ipady=10)
        # Left Frame
        self.frame_left = tk.LabelFrame(self.frame_base, text="VCF File Info", relief='groove')
        self.frame_left.pack(side='left', expand=False, fill='y',ipadx=10, ipady=10, padx=5, pady=5)
        #File load button
        self.labels['filename'] = tk.Label(self.frame_left, textvariable=self.vars['filename'], relief='groove')
        self.labels['filename'].pack(side='top', expand=False, fill='x',ipady=5, padx=5, pady=5)
        tk.Button(self.frame_left, text="Load a CSV File", command=self.loadCSV).pack(side='top', expand=False, fill='x', ipady=5, padx=5, pady=5)
        # Treeview Frame
        self.frame_treeview = tk.Frame(self.frame_left)
        self.frame_treeview.pack(side='top',expand=True,fill='both', padx=5)
        # Treeview list
        self.treeview_variant_list = ttk.Treeview(self.frame_treeview, columns=vcf_columns, displaycolumns=[5,0], selectmode='browse', show='headings')
        for x in vcf_columns:
            self.treeview_variant_list.heading(x, text=x, anchor='center')
        self.treeview_variant_list.heading(5, text='Variant')
        self.treeview_variant_list.heading(0, text='Disposition')
        self.treeview_variant_list.column(column=0, width=100, anchor='center')
        self.treeview_variant_list.column(column=5, width=100, anchor='center')
        self.treeview_variant_list.pack(side='left', expand=True, fill='both')
        self.treeview_variant_list.bind('<<TreeviewSelect>>', self.item_selected)
        # Treeview Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_treeview, orient=tk.VERTICAL, command=self.treeview_variant_list.yview)
        self.treeview_variant_list.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side='left', expand=False, fill='y')
        # Disposition Frame
        self.frame_disposition = tk.LabelFrame(self.frame_left, text="Variant Disposition", relief='groove')
        self.frame_disposition.pack(side='top', expand=False, fill='x', padx=5)
        self.frame_dispo_1 = tk.Frame(self.frame_disposition)
        self.frame_dispo_1.pack(side='top', expand=False, fill='x')
        self.frame_dispo_2 = tk.Frame(self.frame_disposition)
        self.frame_dispo_2.pack(side='top', expand=False, fill='x')
        self.frame_dispo_3 = tk.Frame(self.frame_disposition)
        self.frame_dispo_3.pack(side='top', expand=False, fill='x')
        self.frame_dispo_4 = tk.Frame(self.frame_disposition)
        self.frame_dispo_4.pack(side='top', expand=False, fill='x')
        # Disposition labels
        self.labels['none_count'] = tk.Label(self.frame_dispo_1, textvariable=self.vars['dispo_none_count'], width=5)
        self.labels['none_count'].pack(side='left', expand=False, fill='y')
        self.labels['low_vaf_count'] = tk.Label(self.frame_dispo_2, textvariable=self.vars['dispo_unknown_count'], width=5)
        self.labels['low_vaf_count'].pack(side='left', expand=False, fill='y')
        self.labels['vus_count'] = tk.Label(self.frame_dispo_3, textvariable=self.vars['dispo_VUS_count'], width=5)
        self.labels['vus_count'].pack(side='left', expand=False, fill='y')
        self.labels['mutation_count'] = tk.Label(self.frame_dispo_4, textvariable=self.vars['dispo_mutation_count'], width=5)
        self.labels['mutation_count'].pack(side='left', expand=False, fill='y')
        # Radio buttons for disposition
        self.radio_none = tk.Radiobutton(self.frame_dispo_1, text="Unassigned", variable=self.vars['disposition'], anchor='w')
        self.radio_none.pack(side='left', expand=False, fill='both')
        self.radio_unknown = tk.Radiobutton(self.frame_dispo_2, text="Low VAF", variable=self.vars['disposition'], anchor='w')
        self.radio_unknown.pack(side='left', expand=False, fill='both')
        self.radio_VUS = tk.Radiobutton(self.frame_dispo_3, text="VUS", variable=self.vars['disposition'], anchor='w')
        self.radio_VUS.pack(side='left', expand=False, fill='both')
        self.radio_mutation = tk.Radiobutton(self.frame_dispo_4, text="Harmful", variable=self.vars['disposition'], anchor='w')
        self.radio_mutation.pack(side='left', expand=False, fill='both')
        # Process output files button
        tk.Button(self.frame_left, text="Create Disposition Lists").pack(side='top', expand=False, fill='x', padx=5, pady=5, ipady=5)
        # Right Frame
        self.frame_right = tk.Frame(self.frame_base)
        self.frame_right.pack(side='left', expand=True, fill='both',ipadx=10, ipady=10)
        # Basic Info Frame
        self.frame_basic_info = tk.LabelFrame(self.frame_right, text='Locus Info')
        self.frame_basic_info.pack(side='top', expand=False, fill='x', padx=5, pady=5)
        self.frame_basic_info_gene = tk.Frame(self.frame_basic_info)
        self.frame_basic_info_gene.pack(side='left',expand=False, fill='both', padx=5, pady=5)
        self.frame_basic_info_chrom = tk.Frame(self.frame_basic_info)
        self.frame_basic_info_chrom.pack(side='left',expand=False,fill='both', padx=5, pady=5)
        self.frame_basic_info_changes = tk.Frame(self.frame_basic_info)
        self.frame_basic_info_changes.pack(side='left',expand=False,fill='both', padx=5, pady=5)
        self.frame_basic_info_alleles = tk.Frame(self.frame_basic_info)
        self.frame_basic_info_alleles.pack(side='left',expand=True,fill='both', padx=5, pady=5)
        tk.Label(self.frame_basic_info_gene, text="Gene").pack(side='top',expand=False,fill='x')
        self.labels["Variant Annotation: Gene"] = tk.Label(self.frame_basic_info_gene, width=8, textvariable=self.variant["Variant Annotation: Gene"], relief='groove', font=('bold', 24, 'bold'))
        self.labels["Variant Annotation: Gene"].pack(side='top',expand=True,fill='both')
        tk.Label(self.frame_basic_info_chrom, text="Chromosome").pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Chrom"] = tk.Label(self.frame_basic_info_chrom, width=6, textvariable=self.variant["Original Input: Chrom"], relief='groove')
        self.labels["Original Input: Chrom"].pack(side='top',expand=False, fill='x')
        tk.Label(self.frame_basic_info_chrom, text="Base Pair").pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Pos"] = tk.Label(self.frame_basic_info_chrom, width=12, textvariable=self.variant["Original Input: Pos"], relief='groove')
        self.labels["Original Input: Pos"].pack(side='top',expand=False, fill='x')
        tk.Label(self.frame_basic_info_alleles, text="Ref Allele", anchor='nw').pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Reference allele"] = tk.Label(self.frame_basic_info_alleles, anchor='w', textvariable=self.variant["Original Input: Reference allele"], relief='groove')
        self.labels["Original Input: Reference allele"].pack(side='top',expand=False, fill='x')
        tk.Label(self.frame_basic_info_alleles, text="Variant Allele", anchor='w').pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Alternate allele"] = tk.Label(self.frame_basic_info_alleles, anchor='w', textvariable=self.variant["Original Input: Alternate allele"], relief='groove')
        self.labels["Original Input: Alternate allele"].pack(side='top',expand=False, fill='x')
        tk.Label(self.frame_basic_info_changes, text="DNA Change (c-dot)").pack(side='top',expand=False, fill='x')
        self.labels["Variant Annotation: cDNA change"] = tk.Label(self.frame_basic_info_changes, text="C-dot", textvariable=self.variant["Variant Annotation: cDNA change"], relief='groove')
        self.labels["Variant Annotation: cDNA change"].pack(side='top',expand=False, fill='x')
        tk.Label(self.frame_basic_info_changes, text="Protein Change (p-dot)").pack(side='top',expand=False, fill='x')
        self.labels["Variant Annotation: Protein Change"] = tk.Label(self.frame_basic_info_changes, text="P-dot", width=24, textvariable=self.variant["Variant Annotation: Protein Change"], relief='groove')
        self.labels["Variant Annotation: Protein Change"].pack(side='top',expand=False, fill='x')

        # middle frame
        self.frame_middle = tk.Frame(self.frame_right)
        self.frame_middle.pack(side='top',expand=True,fill='both', padx=5, pady=5)
        # Genexys Info Frame------------------------------------------------
        self.frame_genexys = tk.LabelFrame(self.frame_middle, text='Strand Bias Data', relief='groove')
        self.frame_genexys.pack(side='left', expand=False, fill='both', padx=(0,10))
        # Genexys Read Bias Area
        self.frame_sb_GX = tk.LabelFrame(self.frame_genexys, text="Genexys")
        self.frame_sb_GX.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frame_sb_GX.rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frame_sb_GX.columnconfigure(x, weight=1)
        tk.Label(self.frame_sb_GX, text='Genexys', width=8, font=('bold', 20, 'bold')).grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        tk.Label(self.frame_sb_GX, text='Forward').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frame_sb_GX, text='Reverse').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frame_sb_GX, text='Reference', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_GX, text='Variant', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSRF'] = tk.Label(self.frame_sb_GX, textvariable=self.variant["VCF: FSRF"], relief='groove')
        self.labels['VCF: FSRF'].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSRR'] = tk.Label(self.frame_sb_GX, textvariable=self.variant["VCF: FSRR"], relief='groove')
        self.labels['VCF: FSRR'].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSAF'] = tk.Label(self.frame_sb_GX, textvariable=self.variant["VCF: FSAF"], relief='groove')
        self.labels['VCF: FSAF'].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSAR'] = tk.Label(self.frame_sb_GX, textvariable=self.variant["VCF: FSAR"], relief='groove')
        self.labels['VCF: FSAR'].grid(column=3, row=2, sticky='news', pady=5, padx=5)
        # Separator
        ttk.Separator(self.frame_sb_GX, orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frame_sb_GX_results = tk.Frame(self.frame_sb_GX)
        self.frame_sb_GX_results.grid(column=0, row=5, columnspan=4, sticky='news')
        self.frame_sb_GX_results.rowconfigure(0, weight=1)
        self.frame_sb_GX_results.rowconfigure(1, weight=1)
        self.frame_sb_GX_results.columnconfigure(0, weight=0)
        self.frame_sb_GX_results.columnconfigure(1, weight=5)
        self.frame_sb_GX_results.columnconfigure(2, weight=0)
        self.frame_sb_GX_results.columnconfigure(3, weight=1)
        # Genexys Stats Area
        tk.Label(self.frame_sb_GX_results, text="Binomial Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["VCF: Binom Proportion"] = tk.Label(self.frame_sb_GX_results, textvariable=self.variant["VCF: Binom Proportion"], relief='groove', anchor='center')
        self.labels["VCF: Binom Proportion"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_GX_results, text="p-val.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["VCF: Binom P Value"] = tk.Label(self.frame_sb_GX_results, textvariable=self.variant["VCF: Binom P Value"], relief='groove', anchor='center')
        self.labels["VCF: Binom P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_GX_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["VCF: Fisher Odds Ratio"] = tk.Label(self.frame_sb_GX_results, textvariable=self.variant["VCF: Fisher Odds Ratio"], relief='groove', anchor='center')
        self.labels["VCF: Fisher Odds Ratio"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_GX_results, text="p-val.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["VCF: Fisher P Value"] = tk.Label(self.frame_sb_GX_results, textvariable=self.variant["VCF: Fisher P Value"], relief='groove', anchor='center')
        self.labels["VCF: Fisher P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        # Q20 Read Bias Area
        self.frame_sb_Q20 = tk.LabelFrame(self.frame_genexys, text="Filtered M-Pileup")
        self.frame_sb_Q20.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frame_sb_Q20.rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frame_sb_Q20.columnconfigure(x, weight=1)
        tk.Label(self.frame_sb_Q20, text='Q20', width=8, font=('bold', 20, 'bold')).grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        tk.Label(self.frame_sb_Q20, text='Forward').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frame_sb_Q20, text='Reverse').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frame_sb_Q20, text='Reference', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q20, text='Variant', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Variant Forward Read Depth"] = tk.Label(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Variant Forward Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Filtered Variant Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Variant Reverse Read Depth"] = tk.Label(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Variant Reverse Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Filtered Variant Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Reference Forward Read Depth"] = tk.Label(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Reference Forward Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Filtered Reference Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Reference Reverse Read Depth"] = tk.Label(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Reference Reverse Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Filtered Reference Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)
        # Separator
        ttk.Separator(self.frame_sb_Q20, orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frame_sb_Q20_results = tk.Frame(self.frame_sb_Q20)
        self.frame_sb_Q20_results.grid(column=0, row=5, columnspan=4, sticky='news')
        self.frame_sb_Q20_results.rowconfigure(0, weight=1)
        self.frame_sb_Q20_results.rowconfigure(1, weight=1)
        self.frame_sb_Q20_results.columnconfigure(0, weight=0)
        self.frame_sb_Q20_results.columnconfigure(1, weight=5)
        self.frame_sb_Q20_results.columnconfigure(2, weight=0)
        self.frame_sb_Q20_results.columnconfigure(3, weight=1)
        # Q20 Stats Area
        tk.Label(self.frame_sb_Q20_results, text="Binomial Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["Mpileup Qual: Filtered Variant Binomial Proportion"] = tk.Label(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial Proportion"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Filtered Variant Binomial Proportion"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q20_results, text="p-val.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["Mpileup Qual: Filtered Variant Binomial P Value"] = tk.Label(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial P Value"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Filtered Variant Binomial P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q20_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["Mpileup Qual: Filtered Variant Fishers Odds Ratio"] = tk.Label(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers Odds Ratio"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Filtered Variant Fishers Odds Ratio"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q20_results, text="p-val.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["Mpileup Qual: Filtered Variant Fishers P Value"] = tk.Label(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers P Value"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Filtered Variant Fishers P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        # Q1 Read Bias Area
        self.frame_sb_Q1 = tk.LabelFrame(self.frame_genexys, text="Unfiltered M-Pileup")
        self.frame_sb_Q1.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frame_sb_Q1.rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frame_sb_Q1.columnconfigure(x, weight=1)
        tk.Label(self.frame_sb_Q1, text='Q1', width=8, font=('bold', 20, 'bold')).grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        tk.Label(self.frame_sb_Q1, text='Forward').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frame_sb_Q1, text='Reverse').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frame_sb_Q1, text='Reference', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q1, text='Variant', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Reference Forward Read Depth"] = tk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Reference Forward Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Unfiltered Reference Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Reference Reverse Read Depth"] = tk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Reference Reverse Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Unfiltered Reference Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Forward Read Depth"] = tk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Forward Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Unfiltered Variant Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Reverse Read Depth"] = tk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Reverse Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Unfiltered Variant Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        # Separator
        ttk.Separator(self.frame_sb_Q1, orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frame_sb_Q1_results = tk.Frame(self.frame_sb_Q1)
        self.frame_sb_Q1_results.grid(column=0, row=5, columnspan=4, sticky='news')
        self.frame_sb_Q1_results.rowconfigure(0, weight=1)
        self.frame_sb_Q1_results.rowconfigure(1, weight=1)
        self.frame_sb_Q1_results.columnconfigure(0, weight=0)
        self.frame_sb_Q1_results.columnconfigure(1, weight=5)
        self.frame_sb_Q1_results.columnconfigure(2, weight=0)
        self.frame_sb_Q1_results.columnconfigure(3, weight=1)
        # Q1 Stats Area
        tk.Label(self.frame_sb_Q1_results, text="Binomial Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Binomial Proportion"] = tk.Label(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial Proportion"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Unfiltered Variant Binomial Proportion"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q1_results, text="p-val.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["Mpileup Qual: Unfiltered Variant Binomial P Value"] = tk.Label(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial P Value"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Unfiltered Variant Binomial P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q1_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"] = tk.Label(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q1_results, text="p-val.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["Mpileup Qual: Unfiltered Variant Fishers P Value"] = tk.Label(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers P Value"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Unfiltered Variant Fishers P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)

        # MPL Info Frame------------------------------------------------
        self.frame_other = tk.LabelFrame(self.frame_middle, text='Other Data')
        self.frame_other.pack(side='left',expand=True, fill='both')
        self.frame_other.columnconfigure(0, weight=0)
        self.frame_other.columnconfigure(1, weight=3)
        self.frame_other.columnconfigure(2, weight=0)
        self.frame_other.columnconfigure(3, weight=1)
        tk.Label(self.frame_other, text="Allele Fraction", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["VCF: AF"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: AF"], relief='groove')
        self.labels["VCF: AF"].grid(column=1, columnspan=3, row=0, sticky='news')
        tk.Label(self.frame_other, text="FAO", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["VCF: FAO"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: FAO"], relief='groove')
        self.labels["VCF: FAO"].grid(column=1, columnspan=3, row=1, sticky='news')
        tk.Label(self.frame_other, text="FDP", anchor='e').grid(column=0, row=2, sticky='news', padx=5)
        self.labels["VCF: FDP"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: FDP"], relief='groove')
        self.labels["VCF: FDP"].grid(column=1, columnspan=3, row=2, sticky='news')
        tk.Label(self.frame_other, text="HRUN", anchor='e').grid(column=0, row=3, sticky='news', padx=5)
        self.labels["VCF: HRUN"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: HRUN"], relief='groove')
        self.labels["VCF: HRUN"].grid(column=1, columnspan=3, row=3, sticky='news')
        tk.Label(self.frame_other, text="Filter (Genexys)", anchor='e').grid(column=0, row=4, sticky='news', padx=5)
        self.labels["VCF: Filter"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: Filter"], relief='groove')
        self.labels["VCF: Filter"].grid(column=1, columnspan=3, row=4, sticky='news')
        tk.Label(self.frame_other, text="Genotype", anchor='e').grid(column=0, row=5, sticky='news', padx=5)
        self.labels["VCF: Genotype"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: Genotype"], relief='groove')
        self.labels["VCF: Genotype"].grid(column=1, columnspan=3, row=5, sticky='news')
        tk.Label(self.frame_other, text="Length of Variant (BP)", anchor='e').grid(column=0, row=6, sticky='news', padx=5)
        self.labels["VCF: LEN"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: LEN"], relief='groove')
        self.labels["VCF: LEN"].grid(column=1, columnspan=3, row=6, sticky='news')
        tk.Label(self.frame_other, text="QD", anchor='e').grid(column=0, row=7, sticky='news', padx=5)
        self.labels["VCF: QD"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: QD"], relief='groove')
        self.labels["VCF: QD"].grid(column=1, columnspan=3, row=7, sticky='news')
        tk.Label(self.frame_other, text="Strand Bias Calc. (Genexys)", anchor='e').grid(column=0, row=8, sticky='news', padx=5)
        self.labels["VCF: STB"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: STB"], relief='groove')
        self.labels["VCF: STB"].grid(column=1, row=8, sticky='news')
        tk.Label(self.frame_other, text="p-val.", anchor='e').grid(column=2, row=8, sticky='news', padx=5)
        self.labels["VCF: STBP"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: STBP"], relief='groove')
        self.labels["VCF: STBP"].grid(column=3, row=8, sticky='news')
        tk.Label(self.frame_other, text="SVTYPE (Unused)", anchor='e').grid(column=0, row=10, sticky='news', padx=5)
        self.labels["VCF: SVTYPE"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: SVTYPE"], relief='groove')
        self.labels["VCF: SVTYPE"].grid(column=1, columnspan=3, row=10, sticky='news')
        tk.Label(self.frame_other, text="Variant Type", anchor='e').grid(column=0, row=11, sticky='news', padx=5)
        self.labels["VCF: TYPE"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: TYPE"], relief='groove')
        self.labels["VCF: TYPE"].grid(column=1, columnspan=3, row=11, sticky='news')
        tk.Label(self.frame_other, text="Quality Score", anchor='e').grid(column=0, row=12, sticky='news', padx=5)
        self.labels["VCF: QUAL"] = tk.Label(self.frame_other, textvariable=self.variant["VCF: QUAL"], relief='groove')
        self.labels["VCF: QUAL"].grid(column=1, columnspan=3, row=12, sticky='news')
        tk.Label(self.frame_other, text="Total Read Depth", anchor='e').grid(column=0, row=13, sticky='news', padx=5)
        self.labels["Mpileup Qual: Read Depth"] = tk.Label(self.frame_other, textvariable=self.variant["Mpileup Qual: Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Read Depth"].grid(column=1, columnspan=3, row=13, sticky='news')
        tk.Label(self.frame_other, text="Read Start-Point Count", anchor='e').grid(column=0, row=14, sticky='news', padx=5)
        self.labels["Mpileup Qual: Start Reads"] = tk.Label(self.frame_other, textvariable=self.variant["Mpileup Qual: Start Reads"], relief='groove')
        self.labels["Mpileup Qual: Start Reads"].grid(column=1, columnspan=3, row=14, sticky='news')
        tk.Label(self.frame_other, text="Read End-Point Count", anchor='e').grid(column=0, row=15, sticky='news', padx=5)
        self.labels["Mpileup Qual: Stop Reads"] = tk.Label(self.frame_other, textvariable=self.variant["Mpileup Qual: Stop Reads"], relief='groove')
        self.labels["Mpileup Qual: Stop Reads"].grid(column=1, columnspan=3, row=15, sticky='news')
        tk.Label(self.frame_other, text="Variant Annotation: Coding", anchor='e').grid(column=0, row=17, sticky='news', padx=5)
        self.labels["Variant Annotation: Coding"] = tk.Label(self.frame_other, textvariable=self.variant["Variant Annotation: Coding"], relief='groove')
        self.labels["Variant Annotation: Coding"].grid(column=1, columnspan=3, row=17, sticky='news')
        tk.Label(self.frame_other, text="Variant Annotation: Sequence Ontology", anchor='e').grid(column=0, row=18, sticky='news', padx=5)
        self.labels["Variant Annotation: Sequence"] = tk.Label(self.frame_other, textvariable=self.variant["Variant Annotation: Sequence Ontology"], relief='groove')
        self.labels["Variant Annotation: Sequence"].grid(column=1, columnspan=3, row=18, sticky='news')
        tk.Label(self.frame_other, text="Variant Annotation: Transcript", anchor='e').grid(column=0, row=19, sticky='news', padx=5)
        self.labels["Variant Annotation: Transcript"] = tk.Label(self.frame_other, textvariable=self.variant["Variant Annotation: Transcript"], relief='groove')
        self.labels["Variant Annotation: Transcript"].grid(column=1, columnspan=3, row=19, sticky='news')
        tk.Label(self.frame_other, text="Variant Annotation: All Mappings", anchor='e').grid(column=0, row=20, sticky='news', padx=5)
        self.labels["Variant Annotation: All Mappings"] = tk.Label(self.frame_other, textvariable=self.variant["Variant Annotation: All Mappings"], relief='groove', wraplength=800)
        self.labels["Variant Annotation: All Mappings"].grid(column=1, columnspan=3, row=20, sticky='news')
        tk.Label(self.frame_other, text="UniProt (GENE): Accession Number", anchor='e').grid(column=0, row=21, sticky='news', padx=5)
        self.labels["UniProt (GENE): Accession Number"] = tk.Label(self.frame_other, textvariable=self.variant["UniProt (GENE): Accession Number"], relief='groove')
        self.labels["UniProt (GENE): Accession Number"].grid(column=1, columnspan=3, row=21, sticky='news')
        tk.Label(self.frame_other, text="dbSNP: rsID", anchor='e').grid(column=0, row=22, sticky='news', padx=5)
        self.labels["dbSNP: rsID"] = tk.Label(self.frame_other, textvariable=self.variant["dbSNP: rsID"], relief='groove')
        self.labels["dbSNP: rsID"].grid(column=1, columnspan=3, row=22, sticky='news')
        tk.Label(self.frame_other, text="MDL: Sample Count", anchor='e').grid(column=0, row=23, sticky='news', padx=5)
        self.labels["MDL: Sample Count"] = tk.Label(self.frame_other, textvariable=self.variant["MDL: Sample Count"], relief='groove')
        self.labels["MDL: Sample Count"].grid(column=1, columnspan=3, row=23, sticky='news')
        tk.Label(self.frame_other, text="MDL: Variant Frequency", anchor='e').grid(column=0, row=24, sticky='news', padx=5)
        self.labels["MDL: Variant Frequency"]  = tk.Label(self.frame_other, textvariable=self.variant["MDL: Variant Frequency"], relief='groove')
        self.labels["MDL: Variant Frequency"].grid(column=1, columnspan=3, row=24, sticky='news')
        tk.Label(self.frame_other, text="MDL: Sample List", anchor='e').grid(column=0, row=25, sticky='news', padx=5)
        self.labels["MDL: Sample List"] = tk.Label(self.frame_other, textvariable=self.variant["MDL: Sample List"], relief='groove', wraplength=800)
        self.labels["MDL: Sample List"].grid(column=1, columnspan=3, row=25, sticky='news')

        # # MPL Listed Stats
        self.frame_bottom = tk.LabelFrame(self.frame_right, text='Web Information')
        self.frame_bottom.pack(side='bottom', expand=False, fill='both', padx=5, pady=5)
        self.frame_bottom.columnconfigure(0, weight=1)
        self.frame_bottom.columnconfigure(1, weight=1)
        self.frame_bottom_l = tk.Frame(self.frame_bottom)
        self.frame_bottom_l.grid(column=0, row=0, sticky='news')
        self.frame_bottom_2 = tk.Frame(self.frame_bottom)
        self.frame_bottom_2.grid(column=1, row=0, sticky='news')

        # COSMIC Tissue Variant Count Region
        self.labels["COSMIC: Variant Count (Tissue)"] = tk.Label(self.frame_bottom_l, textvariable=self.variant["COSMIC: Variant Count (Tissue)"], relief='groove', wraplength=600)
        self.labels["COSMIC: Variant Count (Tissue)"].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        # COSMIC Area
        self.frame_web_cosmic = ttk.LabelFrame(self.frame_bottom_2, text='COSMIC')
        self.frame_web_cosmic.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_cosmic, text="ID", anchor='center').pack(side='top', expand=False, fill='x', padx=5)
        self.labels["COSMIC: ID"] = tk.Label(self.frame_web_cosmic, textvariable=self.variant["COSMIC: ID"], relief='groove', width=12)
        self.labels["COSMIC: ID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_cosmic, text="Count").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["COSMIC: Variant Count"] = tk.Label(self.frame_web_cosmic, textvariable=self.variant["COSMIC: Variant Count"], relief='groove')
        self.labels["COSMIC: Variant Count"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # Clinvar Area
        self.frame_web_clinvar = ttk.LabelFrame(self.frame_bottom_2, text='ClinVar')
        self.frame_web_clinvar.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_clinvar, text="ID").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["ClinVar: ClinVar ID"] = tk.Label(self.frame_web_clinvar, textvariable=self.variant["ClinVar: ClinVar ID"], relief='groove')
        self.labels["ClinVar: ClinVar ID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_clinvar, text="Significance").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["ClinVar: Clinical Significance"] = tk.Label(self.frame_web_clinvar, textvariable=self.variant["ClinVar: Clinical Significance"], relief='groove')
        self.labels["ClinVar: Clinical Significance"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # Gnomad Area
        self.frame_web_gnomad = ttk.LabelFrame(self.frame_bottom_2, text='GnomAD')
        self.frame_web_gnomad.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_gnomad, text="Global AF").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["gnomAD3: Global AF"] = tk.Label(self.frame_web_gnomad, textvariable=self.variant["gnomAD3: Global AF"], relief='groove')
        self.labels["gnomAD3: Global AF"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # CADD Area
        self.frame_web_cadd = ttk.LabelFrame(self.frame_bottom_2, text='CADD')
        self.frame_web_cadd.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_cadd, text="Phred Score").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["CADD: Phred"] = tk.Label(self.frame_web_cadd, textvariable=self.variant["CADD: Phred"], relief='groove')
        self.labels["CADD: Phred"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # PolyPhen Area
        self.frame_web_polyphen = ttk.LabelFrame(self.frame_bottom_2, text='PolyPhen-2')
        self.frame_web_polyphen.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_polyphen, text="HDIV").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["PolyPhen-2: HDIV Prediction"] = tk.Label(self.frame_web_polyphen, textvariable=self.variant["PolyPhen-2: HDIV Prediction"], relief='groove')
        self.labels["PolyPhen-2: HDIV Prediction"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # SIFT Area
        self.frame_web_sift = ttk.LabelFrame(self.frame_bottom_2, text='SIFT')
        self.frame_web_sift.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_sift, text="Prediction").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["SIFT: Prediction"] = tk.Label(self.frame_web_sift, textvariable=self.variant["SIFT: Prediction"], relief='groove')
        self.labels["SIFT: Prediction"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        
        for key,value in tooltips.items():
            CreateToolTip(self.labels[key], value)

        return
    
    def validate_cells(self):

        for x in vcf_columns:
            self.labels[x]['bg'] = self.color_enabled
            self.labels[x]['fg'] = self.color_normal

            if not self.variant[x].get():
                self.labels[x]['bg'] = self.color_disabled
                continue

            if x in self.validation['p-values']:
                if float(self.variant[x].get()) > 0.05:
                    self.labels[x]['fg'] = self.color_warning

        # # P-Value Fields
        # if self.variant["VCF: Binom P Value"].get():
        #     if float(self.variant["VCF: Binom P Value"].get()) > 0.05:
        #         self.labels["VCF: Binom P Value"]['fg'] = self.color_warning
        # else:
        #     self.variant["VCF: Binom P Value"]['bg'] = self.color_disabled

        # if self.variant["VCF: Fisher P Value"].get():
        #     if float(self.variant["VCF: Fisher P Value"].get()) > 0.05:
        #         self.labels["VCF: Fisher P Value"]['fg'] = self.color_warning

        # if self.variant["Mpileup Qual: Filtered Variant Binomial P Value"].get():
        #     if float(self.variant["Mpileup Qual: Filtered Variant Binomial P Value"].get()) > 0.05:
        #         self.labels["Mpileup Qual: Filtered Variant Binomial P Value"]['fg'] = self.color_warning

        # if self.variant["Mpileup Qual: Filtered Variant Fishers P Value"].get():
        #     if float(self.variant["Mpileup Qual: Filtered Variant Fishers P Value"].get()) > 0.05:
        #         self.labels["Mpileup Qual: Filtered Variant Fishers P Value"]['fg'] = self.color_warning

        # if self.variant["Mpileup Qual: Unfiltered Variant Binomial P Value"].get():
        #     if float(self.variant["Mpileup Qual: Unfiltered Variant Binomial P Value"].get()) > 0.05:
        #         self.labels["Mpileup Qual: Unfiltered Variant Binomial P Value"]['fg'] = self.color_warning

        # if self.variant["Mpileup Qual: Unfiltered Variant Fishers P Value"].get():
        #     if float(self.variant["Mpileup Qual: Unfiltered Variant Fishers P Value"].get()) > 0.05:
        #         self.labels["Mpileup Qual: Unfiltered Variant Fishers P Value"]['fg'] = self.color_warning

        # if self.variant["VCF: STBP"].get():
        #     if float(self.variant["VCF: STBP"].get()) > 0.05:
        #         self.labels["VCF: STBP"]['fg'] = self.color_warning

        return

    def loadCSV(self):

        csv_dict = dict()
        self.vars['filename'].set(str(fd.askopenfilename(filetypes=[('CSV','*.csv')])))
        with open(self.vars['filename'].get(), 'r') as csv_file:
            counter = 0
            for row in csv.DictReader(csv_file, fieldnames=vcf_columns, delimiter='\t'):
                if counter != 0:
                    csv_dict[counter] = row
                    values_list = list()
                    values_list.append("None")
                    for key, value in csv_dict[counter].items():
                        try:
                            values_list.append(int(value))
                        except:
                            try:
                                values_list.append(round(float(value),3))
                            except:
                                values_list.append(value)
                    self.treeview_variant_list.insert('', tk.END, values=values_list)
                counter += 1

        return
    
    def item_selected(self, event):

        for selected_item in self.treeview_variant_list.selection():
            item = self.treeview_variant_list.item(selected_item)
            record = item['values']

            for x in range(len(vcf_columns)):
                self.variant[vcf_columns[x]].set(record[x])

        self.validate_cells()

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
