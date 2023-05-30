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
        self.warning_color = '#CC0000'
        self.normal_color = '#000000'


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

        self.labels = dict()
        for x in vcf_columns:
            self.labels[x] = tk.Label()
        
        # FRAMES ------------------------------------------------------------------------

        # Base Frame
        self.frame_base = tk.Frame(self)
        self.frame_base.pack(expand=True, fill='both',ipadx=10, ipady=10)
        # Left Frame
        self.frame_left = tk.LabelFrame(self.frame_base, text="VCF File Info", relief='groove')
        self.frame_left.pack(side='left', expand=False, fill='y',ipadx=10, ipady=10, padx=5, pady=5)
        #File load button
        self.label_filename = tk.Label(self.frame_left, textvariable=self.filename, relief='groove')
        self.label_filename.pack(side='top', expand=False, fill='x',ipady=5, padx=5, pady=5)
        tk.Button(self.frame_left, text="Load a CSV File", command=self.loadCSV).pack(side='top', expand=False, fill='x', ipady=5, padx=5, pady=5)
        CreateToolTip(self.label_filename, text = 'VCF processing output file currently loaded for viewing.')
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
        self.label_none_count = tk.Label(self.frame_dispo_1, textvariable=self.dispo_none_count, width=5)
        self.label_none_count.pack(side='left', expand=False, fill='y')
        self.label_low_vaf_count = tk.Label(self.frame_dispo_2, textvariable=self.dispo_unknown_count, width=5)
        self.label_low_vaf_count.pack(side='left', expand=False, fill='y')
        self.label_vus_count = tk.Label(self.frame_dispo_3, textvariable=self.dispo_VUS_count, width=5)
        self.label_vus_count.pack(side='left', expand=False, fill='y')
        self.label_mutation_count = tk.Label(self.frame_dispo_4, textvariable=self.dispo_mutation_count, width=5)
        self.label_mutation_count.pack(side='left', expand=False, fill='y')
        # Radio buttons for disposition
        self.radio_none = tk.Radiobutton(self.frame_dispo_1, text="Unassigned", variable=self.disposition, anchor='w')
        self.radio_none.pack(side='left', expand=False, fill='both')
        self.radio_unknown = tk.Radiobutton(self.frame_dispo_2, text="Low VAF", variable=self.disposition, anchor='w')
        self.radio_unknown.pack(side='left', expand=False, fill='both')
        self.radio_VUS = tk.Radiobutton(self.frame_dispo_3, text="VUS", variable=self.disposition, anchor='w')
        self.radio_VUS.pack(side='left', expand=False, fill='both')
        self.radio_mutation = tk.Radiobutton(self.frame_dispo_4, text="Harmful", variable=self.disposition, anchor='w')
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
        self.label_gene = tk.Label(self.frame_basic_info_gene, width=8, textvariable=self.variant_info["Variant Annotation: Gene"], relief='groove', font=('bold', 24, 'bold'))
        self.label_gene.pack(side='top',expand=True,fill='both')
        CreateToolTip(self.label_gene, text = 'Gene currently selected from the variant list.')
        tk.Label(self.frame_basic_info_chrom, text="Chromosome").pack(side='top',expand=False, fill='x')
        self.label_chrom = tk.Label(self.frame_basic_info_chrom, width=6, textvariable=self.variant_info["Original Input: Chrom"], relief='groove')
        self.label_chrom.pack(side='top',expand=False, fill='x')
        CreateToolTip(self.label_chrom, text = 'Chromosome on which this gene is located.')
        tk.Label(self.frame_basic_info_chrom, text="Base Pair").pack(side='top',expand=False, fill='x')
        self.label_base_pair = tk.Label(self.frame_basic_info_chrom, width=12, textvariable=self.variant_info["Original Input: Pos"], relief='groove')
        self.label_base_pair.pack(side='top',expand=False, fill='x')
        CreateToolTip(self.label_base_pair, text = 'Base pair location for gene on this chromosome.')
        tk.Label(self.frame_basic_info_alleles, text="Ref Allele", anchor='nw').pack(side='top',expand=False, fill='x')
        self.label_ref_allele = tk.Label(self.frame_basic_info_alleles, anchor='w', textvariable=self.variant_info["Original Input: Reference allele"], relief='groove')
        self.label_ref_allele.pack(side='top',expand=False, fill='x')
        CreateToolTip(self.label_ref_allele, text = 'Reference allele found at this location.')
        tk.Label(self.frame_basic_info_alleles, text="Variant Allele", anchor='w').pack(side='top',expand=False, fill='x')
        self.label_alt_allele = tk.Label(self.frame_basic_info_alleles, anchor='w', textvariable=self.variant_info["Original Input: Alternate allele"], relief='groove')
        self.label_alt_allele.pack(side='top',expand=False, fill='x')
        CreateToolTip(self.label_alt_allele, text = 'Variant allele encountered in sequencing.')
        tk.Label(self.frame_basic_info_changes, text="DNA Change (c-dot)").pack(side='top',expand=False, fill='x')
        self.label_cdot = tk.Label(self.frame_basic_info_changes, text="C-dot", textvariable=self.variant_info["Variant Annotation: cDNA change"], relief='groove')
        self.label_cdot.pack(side='top',expand=False, fill='x')
        CreateToolTip(self.label_cdot, text = 'DNA change nomenclature.')
        tk.Label(self.frame_basic_info_changes, text="Protein Change (p-dot)").pack(side='top',expand=False, fill='x')
        self.label_pdot = tk.Label(self.frame_basic_info_changes, text="P-dot", width=24, textvariable=self.variant_info["Variant Annotation: Protein Change"], relief='groove')
        self.label_pdot.pack(side='top',expand=False, fill='x')
        CreateToolTip(self.label_pdot, text = 'Protein change nomenclature.')

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
        tk.Label(self.frame_sb_GX, textvariable=self.variant_info["VCF: FSRF"], relief='groove').grid(column=2, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_GX, textvariable=self.variant_info["VCF: FSRR"], relief='groove').grid(column=3, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_GX, textvariable=self.variant_info["VCF: FSAF"], relief='groove').grid(column=2, row=2, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_GX, textvariable=self.variant_info["VCF: FSAR"], relief='groove').grid(column=3, row=2, sticky='news', pady=5, padx=5)
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
        self.label_GX_binom_GX = tk.Label(self.frame_sb_GX_results, textvariable=self.variant_info["VCF: Fisher Odds Ratio"], relief='groove', anchor='center')
        self.label_GX_binom_GX.grid(column=1, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_GX_results, text="p-val.", anchor='e').grid(column=2, row=0, sticky='news')
        self.label_GX_binom_pval = tk.Label(self.frame_sb_GX_results, textvariable=self.variant_info["VCF: Fisher P Value"], relief='groove', anchor='center')
        self.label_GX_binom_pval.grid(column=3, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_GX_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.label_GX_fisher_or = tk.Label(self.frame_sb_GX_results, textvariable=self.variant_info["VCF: Binom Proportion"], relief='groove', anchor='center')
        self.label_GX_fisher_or.grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_GX_results, text="p-val.", anchor='e').grid(column=2, row=1, sticky='news')
        self.label_GX_fisher_or_pval = tk.Label(self.frame_sb_GX_results, textvariable=self.variant_info["VCF: Binom P Value"], relief='groove', anchor='center')
        self.label_GX_fisher_or_pval.grid(column=3, row=1, sticky='news', pady=5, padx=5)
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
        tk.Label(self.frame_sb_Q20, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Forward Read Depth"], relief='groove').grid(column=2, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q20, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Reverse Read Depth"], relief='groove').grid(column=3, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q20, textvariable=self.variant_info["Mpileup Qual: Filtered Reference Forward Read Depth"], relief='groove').grid(column=2, row=2, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q20, textvariable=self.variant_info["Mpileup Qual: Filtered Reference Reverse Read Depth"], relief='groove').grid(column=3, row=2, sticky='news', pady=5, padx=5)
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
        self.label_mpl_binom_Q20 = tk.Label(self.frame_sb_Q20_results, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Binomial Proportion"], relief='groove', anchor='center')
        self.label_mpl_binom_Q20.grid(column=1, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q20_results, text="p-val.", anchor='e').grid(column=2, row=0, sticky='news')
        self.label_mpl_binom_pval_Q20 = tk.Label(self.frame_sb_Q20_results, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Binomial P Value"], relief='groove', anchor='center')
        self.label_mpl_binom_pval_Q20.grid(column=3, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q20_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.label_mpl_fisher_or_Q20 = tk.Label(self.frame_sb_Q20_results, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Fishers Odds Ratio"], relief='groove', anchor='center')
        self.label_mpl_fisher_or_Q20.grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q20_results, text="p-val.", anchor='e').grid(column=2, row=1, sticky='news')
        self.label_mpl_fisher_or_pval_Q20 = tk.Label(self.frame_sb_Q20_results, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Fishers P Value"], relief='groove', anchor='center')
        self.label_mpl_fisher_or_pval_Q20.grid(column=3, row=1, sticky='news', pady=5, padx=5)
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
        tk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant_info["Mpileup Qual: Unfiltered Reference Forward Read Depth"], relief='groove').grid(column=2, row=2, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant_info["Mpileup Qual: Unfiltered Reference Reverse Read Depth"], relief='groove').grid(column=3, row=2, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Forward Read Depth"], relief='groove').grid(column=2, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Reverse Read Depth"], relief='groove').grid(column=3, row=1, sticky='news', pady=5, padx=5)
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
        self.label_mpl_binom_Q1 = tk.Label(self.frame_sb_Q1_results, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Binomial Proportion"], relief='groove', anchor='center')
        self.label_mpl_binom_Q1.grid(column=1, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q1_results, text="p-val.", anchor='e').grid(column=2, row=0, sticky='news')
        self.label_mpl_binom_pval_Q1 = tk.Label(self.frame_sb_Q1_results, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Binomial P Value"], relief='groove', anchor='center')
        self.label_mpl_binom_pval_Q1.grid(column=3, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q1_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.label_mpl_fisher_or_Q1 = tk.Label(self.frame_sb_Q1_results, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"], relief='groove', anchor='center')
        self.label_mpl_fisher_or_Q1.grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frame_sb_Q1_results, text="p-val.", anchor='e').grid(column=2, row=1, sticky='news')
        self.label_mpl_fisher_or_pval_Q1 = tk.Label(self.frame_sb_Q1_results, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Fishers P Value"], relief='groove', anchor='center')
        self.label_mpl_fisher_or_pval_Q1.grid(column=3, row=1, sticky='news', pady=5, padx=5)

        # MPL Info Frame------------------------------------------------
        self.frame_other = tk.LabelFrame(self.frame_middle, text='Other Data')
        self.frame_other.pack(side='left',expand=True, fill='both')
        self.frame_other.columnconfigure(0, weight=0)
        self.frame_other.columnconfigure(1, weight=3)
        self.frame_other.columnconfigure(2, weight=0)
        self.frame_other.columnconfigure(3, weight=1)
        tk.Label(self.frame_other, text="Allele Fraction", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: AF"], relief='groove').grid(column=1, columnspan=3, row=0, sticky='news')
        tk.Label(self.frame_other, text="FAO", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: FAO"], relief='groove').grid(column=1, columnspan=3, row=1, sticky='news')
        tk.Label(self.frame_other, text="FDP", anchor='e').grid(column=0, row=2, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: FDP"], relief='groove').grid(column=1, columnspan=3, row=2, sticky='news')
        tk.Label(self.frame_other, text="HRUN", anchor='e').grid(column=0, row=3, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: HRUN"], relief='groove').grid(column=1, columnspan=3, row=3, sticky='news')
        tk.Label(self.frame_other, text="Filter (Genexys)", anchor='e').grid(column=0, row=4, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: Filter"], relief='groove').grid(column=1, columnspan=3, row=4, sticky='news')
        tk.Label(self.frame_other, text="Genotype", anchor='e').grid(column=0, row=5, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: Genotype"], relief='groove').grid(column=1, columnspan=3, row=5, sticky='news')
        tk.Label(self.frame_other, text="Length of Variant (BP)", anchor='e').grid(column=0, row=6, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: LEN"], relief='groove').grid(column=1, columnspan=3, row=6, sticky='news')
        tk.Label(self.frame_other, text="QD", anchor='e').grid(column=0, row=7, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: QD"], relief='groove').grid(column=1, columnspan=3, row=7, sticky='news')
        tk.Label(self.frame_other, text="Strand Bias Calc. (Genexys)", anchor='e').grid(column=0, row=8, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: STB"], relief='groove').grid(column=1, row=8, sticky='news')
        tk.Label(self.frame_other, text="p-val.", anchor='e').grid(column=2, row=8, sticky='news', padx=5)
        self.label_sb_vcf_pval = tk.Label(self.frame_other, textvariable=self.variant_info["VCF: STBP"], relief='groove')
        self.label_sb_vcf_pval.grid(column=3, row=8, sticky='news')
        tk.Label(self.frame_other, text="SVTYPE (Unused)", anchor='e').grid(column=0, row=10, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: SVTYPE"], relief='groove').grid(column=1, columnspan=3, row=10, sticky='news')
        tk.Label(self.frame_other, text="Variant Type", anchor='e').grid(column=0, row=11, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: TYPE"], relief='groove').grid(column=1, columnspan=3, row=11, sticky='news')
        tk.Label(self.frame_other, text="Quality Score", anchor='e').grid(column=0, row=12, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["VCF: QUAL"], relief='groove').grid(column=1, columnspan=3, row=12, sticky='news')
        tk.Label(self.frame_other, text="Total Read Depth", anchor='e').grid(column=0, row=13, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["Mpileup Qual: Read Depth"], relief='groove').grid(column=1, columnspan=3, row=13, sticky='news')
        tk.Label(self.frame_other, text="Read Start-Point Count", anchor='e').grid(column=0, row=14, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["Mpileup Qual: Start Reads"], relief='groove').grid(column=1, columnspan=3, row=14, sticky='news')
        tk.Label(self.frame_other, text="Read End-Point Count", anchor='e').grid(column=0, row=15, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["Mpileup Qual: Stop Reads"], relief='groove').grid(column=1, columnspan=3, row=15, sticky='news')
        tk.Label(self.frame_other, text="Variant Annotation: Coding", anchor='e').grid(column=0, row=17, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["Variant Annotation: Coding"], relief='groove').grid(column=1, columnspan=3, row=17, sticky='news')
        tk.Label(self.frame_other, text="Variant Annotation: Sequence Ontology", anchor='e').grid(column=0, row=18, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["Variant Annotation: Sequence Ontology"], relief='groove').grid(column=1, columnspan=3, row=18, sticky='news')
        tk.Label(self.frame_other, text="Variant Annotation: Transcript", anchor='e').grid(column=0, row=19, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["Variant Annotation: Transcript"], relief='groove').grid(column=1, columnspan=3, row=19, sticky='news')
        tk.Label(self.frame_other, text="Variant Annotation: All Mappings", anchor='e').grid(column=0, row=20, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["Variant Annotation: All Mappings"], relief='groove', wraplength=800).grid(column=1, columnspan=3, row=20, sticky='news')
        tk.Label(self.frame_other, text="UniProt (GENE): Accession Number", anchor='e').grid(column=0, row=21, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["UniProt (GENE): Accession Number"], relief='groove').grid(column=1, columnspan=3, row=21, sticky='news')
        tk.Label(self.frame_other, text="dbSNP: rsID", anchor='e').grid(column=0, row=22, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["dbSNP: rsID"], relief='groove').grid(column=1, columnspan=3, row=22, sticky='news')
        tk.Label(self.frame_other, text="MDL: Sample Count", anchor='e').grid(column=0, row=23, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["MDL: Sample Count"], relief='groove').grid(column=1, columnspan=3, row=23, sticky='news')
        tk.Label(self.frame_other, text="MDL: Variant Frequency", anchor='e').grid(column=0, row=24, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["MDL: Variant Frequency"], relief='groove').grid(column=1, columnspan=3, row=24, sticky='news')
        tk.Label(self.frame_other, text="MDL: Sample List", anchor='e').grid(column=0, row=25, sticky='news', padx=5)
        tk.Label(self.frame_other, textvariable=self.variant_info["MDL: Sample List"], relief='groove', wraplength=800).grid(column=1, columnspan=3, row=25, sticky='news')

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
        self.label_cosmic_count_tissue = tk.Label(self.frame_bottom_l, textvariable=self.variant_info["COSMIC: Variant Count (Tissue)"], relief='groove', wraplength=600)
        self.label_cosmic_count_tissue.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        # COSMIC Area
        self.frame_web_cosmic = ttk.LabelFrame(self.frame_bottom_2, text='COSMIC')
        self.frame_web_cosmic.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_cosmic, text="ID", anchor='center').pack(side='top', expand=False, fill='x', padx=5)
        self.label_cosmic_id = tk.Label(self.frame_web_cosmic, textvariable=self.variant_info["COSMIC: ID"], relief='groove', width=12)
        self.label_cosmic_id.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_cosmic, text="Count").pack(side='top', expand=False, fill='x', padx=5)
        self.label_cosmic_count = tk.Label(self.frame_web_cosmic, textvariable=self.variant_info["COSMIC: Variant Count"], relief='groove')
        self.label_cosmic_count.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # Clinvar Area
        self.frame_web_clinvar = ttk.LabelFrame(self.frame_bottom_2, text='ClinVar')
        self.frame_web_clinvar.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_clinvar, text="ID").pack(side='top', expand=False, fill='x', padx=5)
        self.label_clinvar_id = tk.Label(self.frame_web_clinvar, textvariable=self.variant_info["ClinVar: ClinVar ID"], relief='groove')
        self.label_clinvar_id.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_clinvar, text="Significance").pack(side='top', expand=False, fill='x', padx=5)
        self.label_clinvar_sig = tk.Label(self.frame_web_clinvar, textvariable=self.variant_info["ClinVar: Clinical Significance"], relief='groove')
        self.label_clinvar_sig.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # Gnomad Area
        self.frame_web_gnomad = ttk.LabelFrame(self.frame_bottom_2, text='GnomAD')
        self.frame_web_gnomad.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_gnomad, text="Global AF").pack(side='top', expand=False, fill='x', padx=5)
        self.label_gnomad_global_af = tk.Label(self.frame_web_gnomad, textvariable=self.variant_info["gnomAD3: Global AF"], relief='groove')
        self.label_gnomad_global_af.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # CADD Area
        self.frame_web_cadd = ttk.LabelFrame(self.frame_bottom_2, text='CADD')
        self.frame_web_cadd.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_cadd, text="Phred Score").pack(side='top', expand=False, fill='x', padx=5)
        self.label_cadd_phred = tk.Label(self.frame_web_cadd, textvariable=self.variant_info["CADD: Phred"], relief='groove')
        self.label_cadd_phred.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # PolyPhen Area
        self.frame_web_polyphen = ttk.LabelFrame(self.frame_bottom_2, text='PolyPhen-2')
        self.frame_web_polyphen.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_polyphen, text="HDIV").pack(side='top', expand=False, fill='x', padx=5)
        self.label_polyphen_predict = tk.Label(self.frame_web_polyphen, textvariable=self.variant_info["PolyPhen-2: HDIV Prediction"], relief='groove')
        self.label_polyphen_predict.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # SIFT Area
        self.frame_web_sift = ttk.LabelFrame(self.frame_bottom_2, text='SIFT')
        self.frame_web_sift.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frame_web_sift, text="Prediction").pack(side='top', expand=False, fill='x', padx=5)
        self.label_sift_predict = tk.Label(self.frame_web_sift, textvariable=self.variant_info["SIFT: Prediction"], relief='groove')
        self.label_sift_predict.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        
        return
    
    def validate_cells(self):

        for x in vcf_columns:
            self.labels[x]['bg'] = 'white'
            self.labels[x]['fg'] = 'black'

        # P-Value Fields
        self.label_GX_binom_pval['fg'] = 'black'
        if self.variant_info["VCF: Binom P Value"].get():
            if float(self.variant_info["VCF: Binom P Value"].get()) > 0.05:
                self.label_GX_binom_pval['fg'] = self.warning_color

        self.label_GX_fisher_or_pval['fg'] = 'black'
        if self.variant_info["VCF: Fisher P Value"].get():
            if float(self.variant_info["VCF: Fisher P Value"].get()) > 0.05:
                self.label_GX_fisher_or_pval['fg'] = self.warning_color

        self.label_mpl_binom_pval_Q20['fg'] = 'black'
        if self.variant_info["Mpileup Qual: Filtered Variant Binomial P Value"].get():
            if float(self.variant_info["Mpileup Qual: Filtered Variant Binomial P Value"].get()) > 0.05:
                self.label_mpl_binom_pval_Q20['fg'] = self.warning_color

        self.label_mpl_fisher_or_pval_Q20['fg'] = 'black'
        if self.variant_info["Mpileup Qual: Filtered Variant Fishers P Value"].get():
            if float(self.variant_info["Mpileup Qual: Filtered Variant Fishers P Value"].get()) > 0.05:
                self.label_mpl_fisher_or_pval_Q20['fg'] = self.warning_color

        self.label_mpl_binom_pval_Q1['fg'] = 'black'
        if self.variant_info["Mpileup Qual: Unfiltered Variant Binomial P Value"].get():
            if float(self.variant_info["Mpileup Qual: Unfiltered Variant Binomial P Value"].get()) > 0.05:
                self.label_mpl_binom_pval_Q1['fg'] = self.warning_color

        self.label_mpl_fisher_or_pval_Q1['fg'] = 'black'
        if self.variant_info["Mpileup Qual: Unfiltered Variant Fishers P Value"].get():
            if float(self.variant_info["Mpileup Qual: Unfiltered Variant Fishers P Value"].get()) > 0.05:
                self.label_mpl_fisher_or_pval_Q1['fg'] = self.warning_color

        self.label_sb_vcf_pval['fg'] = 'black'
        if self.variant_info["VCF: STBP"].get():
            if float(self.variant_info["VCF: STBP"].get()) > 0.05:
                self.label_sb_vcf_pval['fg'] = self.warning_color

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
                self.variant_info[vcf_columns[x]].set(record[x])

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
