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
import webbrowser
import pandas as pd

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
    "Variant Annotations: RefSeq",
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
    "Variant Annotation: All Mappings", # Very long text, needs wordwrap
    "UniProt (GENE): Accession Number",
    "dbSNP: rsID",
    "MDL: Sample Count",
    "MDL: Variant Frequency",
    "MDL: Sample List", # Very long text, needs wordwrap
    "Disposition",
]

tooltips = {
    "Original Input: Chrom":'Chromosome on which this gene is found.',
    "Original Input: Pos":'Base pair position of the gene on the chromosome.',
    "Original Input: Reference allele":'Expected finding at this base pair location.',
    "Original Input: Alternate allele":'Specimen finding at this base pair location.',
    "Variant Annotation: Gene":'Gene currently selected from the variant list.',
    "Variant Annotation: cDNA change":'Alteration in the DNA at this location.',
    "Variant Annotation: Protein Change":'Resultant alteration in the protein at this location.',
    "VCF: AF":'Allele fraction of reads with this variant.',
    "VCF: FAO":"Variant read depth at this base pair location, reported by Genexus.",
    "VCF: FDP":"Total read depth at this base pair location, reported by Genexus",
    "VCF: HRUN":"Homopolymer run count, reported by Genexus.",
    "VCF: Filter":"Final filter disposition as given by the Genexus.\n Preferred value: 'PASS'",
    "VCF: Genotype":"Genotype distinction made by the Genexus analyzer.\n 1/1 = homozygous, 0/1 = heterozygous, 0/0 = ???, ./. = ???",
    "COSMIC: ID":"COSMIC website ID for this variant.",
    "COSMIC: Variant Count":"Times this variant has been reported to COSMIC.",
    "COSMIC: Variant Count (Tissue)":"JSON-style dictionary breakdown of tissue types reported to COSMIC for this variant.", # Very long text, needs wordwrap
    "ClinVar: ClinVar ID":"ClinVar website ID for this variant.",
    "ClinVar: Clinical Significance":"Clinical significance as reported by ClinVar website.",
    "gnomAD3: Global AF":"Frequency of this variant being found in the human population, as reported by GnomAD website.",
    "PhyloP: Vert Score":"Vertebrate score for gene conservancy, as reported by web resources.",
    "CADD: Phred":"Combine Annotation Dependent Depletion score, rating pathogenicity.\nRange: 0 = Benign, 48 = Pathogenic",
    "PolyPhen-2: HDIV Prediction":"Score assessing the possible change in phenotype of the protein structure, based on AA change.",
    "SIFT: Prediction":"SNP mutagenesis prediction score based on AA change, as reported by SIFT website.",
    "VCF: FSAF":"Forward Variant Read Depth, reported by Genexus\nValid value: > 10",
    "VCF: FSAR":"Reverse Variant Read Depth, reported by Genexus\nValid value: > 10",
    "VCF: FSRF":"Forward Reference Read Depth, reported by Genexus.",
    "VCF: FSRR":"Reverse Reference Read Depth, reported by Genexus.",
    "VCF: Fisher Odds Ratio":"Fisher's odds ratio calculation, based on Genexus read depth data.",
    "VCF: Fisher P Value":"Statistical p-value.\nLess than 0.05 is preferred.",
    "VCF: Binom Proportion":"Binomial proportion caclucation, based on Genexus read depth data.",
    "VCF: Binom P Value":"Statistical p-value.\nLess than 0.05 is preferred.",
    "Mpileup Qual: Read Depth":"Total read depth, as reported by M-Pileup data.\nValid: > 500",
    "Mpileup Qual: Start Reads":"Count of read start signals (strand termination), as reported in the M-Pileup data.",
    "Mpileup Qual: Stop Reads":"Cout of read stop signals (strand initiation), as reported in the M-Pileup data.",
    "Mpileup Qual: Filtered Reference Forward Read Depth":"Forward Reference Read Depth, reported by M-Pileup, @Q20\nValid value: > 10",
    "Mpileup Qual: Filtered Reference Reverse Read Depth":"Reverse Reference Read Depth, reported by M-Pileup, @Q20\nValid value: > 10",
    "Mpileup Qual: Unfiltered Reference Forward Read Depth":"Forward Reference Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",
    "Mpileup Qual: Unfiltered Reference Reverse Read Depth":"Reverse Reference Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",
    "Mpileup Qual: Filtered Variant Forward Read Depth":"Forward Variant Read Depth, reported by M-Pileup, @Q20\nValid value: > 10",
    "Mpileup Qual: Filtered Variant Reverse Read Depth":"Reverse Variant Read Depth, reported by M-Pileup, @Q20\nValid value: > 10",
    "Mpileup Qual: Filtered Variant Binomial Proportion":"Binomial proportion caclucation, based on filtered M-Pileup read depth data.",
    "Mpileup Qual: Filtered Variant Binomial P Value":"Statistical p-value.\nLess than 0.05 is preferred.",
    "Mpileup Qual: Filtered Variant Fishers Odds Ratio":"Fisher's odds ratio calculation, based on filtered M-Pileup read depth data.",
    "Mpileup Qual: Filtered Variant Fishers P Value":"Statistical p-value.\nLess than 0.05 is preferred.",
    "Mpileup Qual: Unfiltered Variant Forward Read Depth":"Forward Variant Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",
    "Mpileup Qual: Unfiltered Variant Reverse Read Depth":"Reverse Variant Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",
    "Mpileup Qual: Unfiltered Variant Binomial Proportion":"Binomial proportion caclucation, based on unfiltered M-Pileup read depth data.",
    "Mpileup Qual: Unfiltered Variant Binomial P Value":"Statistical p-value.\nLess than 0.05 is preferred.",
    "Mpileup Qual: Unfiltered Variant Fishers Odds Ratio":"Fisher's odds ratio calculation, based on unfiltered M-Pileup read depth data.",
    "Mpileup Qual: Unfiltered Variant Fishers P Value":"Statistical p-value.\nLess than 0.05 is preferred.",
    "VCF: LEN":"Length of the variant, as reported by Genexus.",
    "VCF: QD":"???",
    "VCF: STB":"Proprietary strand bias calculation, as reported by Genexus.",
    "VCF: STBP":"Statistical p-value.\nLess than 0.05 is preferred.",
    "VCF: SVTYPE":"Unused data field from the Genexus report.",
    "VCF: TYPE":"Type of variant, as reported by Genexus.",
    "VCF: QUAL":"Quality determination tag, as reported by Genexus.",
    "Variant Annotation: Coding":"Reported coding region variant, as reported by Genexus.",
    "Variant Annotation: Sequence Ontology":"Type of variant/mutation encountered.\n Possible Types: MIS, INT, FSI, IND, SYN, SPL ",
    "Variant Annotation: Transcript":"Ensembl transcript designation code.",
    "Variant Annotation: All Mappings":"JSON-style dictionary breakdown of tissue types present in ??? knowledgebase for this variant.", # Very long text, needs wordwrap
    "UniProt (GENE): Accession Number":"UniProt web resource for the affected protein and biological functions.",
    "dbSNP: rsID":"ID number for the free dbSNP web resource listing of this variant.",
    "MDL: Sample Count":"Instance count of samples with this variant in ",
    "MDL: Variant Frequency":"",
    "MDL: Sample List":"JSON-style dictionary breakdown of tissue types present in ??? knowledgebase for this variant.", # Very long text, needs wordwrap
    "Disposition":'What to call this variant.',
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
        self.tipwindow = tw = ttk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = ttk.Label(
            tw, 
            text=self.text, 
            justify=ttk.LEFT,
            relief=ttk.SOLID, 
            borderwidth=1,
            # font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class App(ttk.Window):

    def __init__(self) -> None:
        super().__init__()

        # Root Window
        self.title('VCF Result Viewer')
        self.style.theme_use('flatly')
        self.resizable(True, True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.geometry('800x600')

        # Menu Creation
        self.menubar = ttk.Menu(self)
        self.menu_file = ttk.Menu(self.menubar, tearoff=0)
        self.menu_file.add_command(label="Open", command=donothing)
        self.menu_file.add_command(label="Clear", command=donothing)
        self.menu_file.add_command(label="Save", command=donothing)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.menu_file)

        self.menu_theme = ttk.Menu(self.menubar, tearoff=0)
        # self.menu_theme.add_command(label='Cerculean', command=lambda: self.style.theme_use('cerculean'))
        self.menu_theme.add_command(label='Cosmo', command=lambda: self.style.theme_use('cosmo'))
        self.menu_theme.add_command(label='Flatly', command=lambda: self.style.theme_use('flatly'))
        self.menu_theme.add_command(label='Journal', command=lambda: self.style.theme_use('journal'))
        self.menu_theme.add_command(label='Litera', command=lambda: self.style.theme_use('litera'))
        self.menu_theme.add_command(label='Lumen', command=lambda: self.style.theme_use('lumen'))
        # self.menu_theme.add_command(label='Minty', command=lambda: self.style.theme_use('minty'))
        # self.menu_theme.add_command(label='Morph', command=lambda: self.style.theme_use('morph'))
        self.menu_theme.add_command(label='Pulse', command=lambda: self.style.theme_use('pulse'))
        self.menu_theme.add_command(label='Sandstone', command=lambda: self.style.theme_use('sandstone'))
        # self.menu_theme.add_command(label='Simplex', command=lambda: self.style.theme_use('simplex'))
        self.menu_theme.add_command(label='United', command=lambda: self.style.theme_use('united'))
        self.menu_theme.add_command(label='Yeti', command=lambda: self.style.theme_use('yeti'))
        self.menu_theme.add_separator()
        # self.menu_theme.add_command(label='Solar', command=lambda: self.style.theme_use('solar'))
        self.menu_theme.add_command(label='Superhero', command=lambda: self.style.theme_use('superhero'))
        self.menu_theme.add_command(label='Darkly', command=lambda: self.style.theme_use('darkly'))
        self.menu_theme.add_command(label='Cyborg', command=lambda: self.style.theme_use('cyborg'))
        # self.menu_theme.add_command(label='Vapor', command=lambda: self.style.theme_use('vapor'))
        self.menubar.add_cascade(label='Theme', menu=self.menu_theme)

        self.menu_output = ttk.Menu(self.menubar, tearoff=0)

        self.menu_help = ttk.Menu(self.menubar, tearoff=0)
        self.menu_help.add_command(label="Help Index", command=donothing)
        self.menu_help.add_command(label="About...", command=donothing)
        self.menubar.add_cascade(label="Help", menu=self.menu_help)

        self.config(menu=self.menubar)

        # Variables
        self.vars = dict()
        self.vars['filename'] = tk.StringVar()
        self.vars['filename'].set('No CSV File Loaded')
        self.vars['status_text'] = tk.StringVar()
        self.vars['Disposition'] = tk.StringVar()
        self.vars['dispo_none_count'] = tk.IntVar()
        self.vars['dispo_low_vaf_count'] = tk.IntVar()
        self.vars['dispo_vus_count'] = tk.IntVar()
        self.vars['dispo_mutation_count'] = tk.IntVar()
        self.vars['dispo_flt3_count'] = tk.IntVar()
        self.vars['dispo_hotspot_count'] = tk.IntVar()


        self.variant = dict()
        for x in vcf_columns:
            self.variant[x] = tk.StringVar()

        self.labels = dict()
        for x in vcf_columns:
            self.labels[x] = ttk.Label()
            
        self.buttons = dict()

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
        self.validation['read depth 10'] = [
            "VCF: FSAF",
            "VCF: FSAR",
            "Mpileup Qual: Filtered Variant Forward Read Depth",
            "Mpileup Qual: Filtered Variant Reverse Read Depth",
            "Mpileup Qual: Unfiltered Variant Forward Read Depth",
            "Mpileup Qual: Unfiltered Variant Reverse Read Depth",
            "VCF: FAO",
        ]
        self.validation['read depth 500'] = [
            "Mpileup Qual: Read Depth",
            "VCF: FDP",
        ]
        self.validation['low vaf']=[
            'VCF: FDP',
        ]
        self.validation['web links'] = [
            "Variant Annotation: Transcript",
            "COSMIC: ID",
            "ClinVar: ClinVar ID",
            "ClinVar: ClinVar ID",
            "dbSNP: rsID",
            "UniProt (GENE): Accession Number",
        ]
        self.big_text = ('bold', 14, 'bold')

        # Keybinds
        self.bind('<Right>', lambda event: self.goto_next_radio())
        self.bind('<Left>', lambda event: self.goto_prev_radio())
        self.bind('<space>', lambda event: self.save_disposition())
        
        # FRAMES ------------------------------------------------------------------------
        # Base Frame
        self.frame_base = ttk.Frame(self)
        self.frame_base.pack(expand=True, fill='both')
        # Left Frame
        self.frame_left = ttk.Frame(self.frame_base)
        self.frame_left.pack(side='left', expand=False, fill='y', padx=(5,0), pady=5)
        self.frame_file = ttk.Labelframe(self.frame_left, text="VCF File Info", relief='groove')
        self.frame_file.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        #File load button
        self.labels['filename'] = ttk.Label(self.frame_file, textvariable=self.vars['filename'], relief='groove', anchor='center', justify='right', width=10)
        self.labels['filename'].pack(side='top', expand=False, fill='x',ipady=5, padx=5, pady=5)
        self.buttons['open_file'] = ttk.Button(self.frame_file, text="Load an XLSX", command=self.open_file)
        self.buttons['open_file'].pack(side='top', expand=False, fill='x', ipady=5, padx=5, pady=5)
        # Treeview Frame
        self.frame_treeview = ttk.Frame(self.frame_file)
        self.frame_treeview.pack(side='top',expand=True,fill='both', padx=5, pady=5)
        # Treeview list
        self.treeview_variant_list = ttk.Treeview(self.frame_treeview, columns=vcf_columns, displaycolumns=[4,69], selectmode='browse', show='headings')
        for x in vcf_columns:
            self.treeview_variant_list.heading(x, text=x, anchor='center')
        self.treeview_variant_list.heading(4, text='Variant')
        self.treeview_variant_list.heading(69, text='Disposition')
        self.treeview_variant_list.column(column=69, width=100, anchor='center')
        self.treeview_variant_list.column(column=4, width=100, anchor='center')
        self.treeview_variant_list.pack(side='left', expand=True, fill='both')
        self.treeview_variant_list.bind('<<TreeviewSelect>>', self.item_selected)
        # Treeview Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_treeview, orient=tk.VERTICAL, command=self.treeview_variant_list.yview)
        self.treeview_variant_list.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side='left', expand=False, fill='y')
        self.treeview_variant_list.tag_configure('None', background="grey")
        self.treeview_variant_list.tag_configure('Hotspot', background="orange")
        self.treeview_variant_list.tag_configure('VUS', background="green")
        self.treeview_variant_list.tag_configure('Low VAF', background="blue")
        self.treeview_variant_list.tag_configure('Harmful', background="red")
        self.treeview_variant_list.tag_configure('FLT3 ITD', background="purple")

        # Disposition Frame
        self.frame_disposition = ttk.Labelframe(self.frame_left, text="Variant Disposition")
        self.frame_disposition.pack(side='top', expand=False, fill='x', padx=5, pady=5)
        self.frame_disposition.columnconfigure(0, weight=0)
        self.frame_disposition.columnconfigure(1, weight=1)
        for x in range(4):
            self.frame_disposition.rowconfigure(x, weight=1)
        # Disposition labels
        self.labels['none_count'] = ttk.Label(self.frame_disposition, textvariable=self.vars['dispo_none_count'], width=5, relief='groove', anchor='center')
        self.labels['none_count'].grid(row=0, column=0, sticky='news', padx=5, pady=5)
        self.labels['mutation_count'] = ttk.Label(self.frame_disposition, textvariable=self.vars['dispo_mutation_count'], width=5, relief='groove', anchor='center')
        self.labels['mutation_count'].grid(row=1, column=0, sticky='news', padx=5, pady=5)
        self.labels['vus_count'] = ttk.Label(self.frame_disposition, textvariable=self.vars['dispo_vus_count'], width=5, relief='groove', anchor='center')
        self.labels['vus_count'].grid(row=2, column=0, sticky='news', padx=5, pady=5)
        self.labels['low_vaf_count'] = ttk.Label(self.frame_disposition, textvariable=self.vars['dispo_low_vaf_count'], width=5, relief='groove', anchor='center')
        self.labels['low_vaf_count'].grid(row=3, column=0, sticky='news', padx=5, pady=5)
        self.labels['flt3_count'] = ttk.Label(self.frame_disposition, textvariable=self.vars['dispo_flt3_count'], width=5, relief='groove', anchor='center')
        self.labels['flt3_count'].grid(row=4, column=0, sticky='news', padx=5, pady=5)
        self.labels['hotspot_count'] = ttk.Label(self.frame_disposition, textvariable=self.vars['dispo_hotspot_count'], width=5, relief='groove', anchor='center')
        self.labels['hotspot_count'].grid(row=5, column=0, sticky='news', padx=5, pady=5)
        # Radio buttons for disposition
        self.radio_none = ttk.Radiobutton(self.frame_disposition, text="None (Unassigned)", variable=self.vars['Disposition'], value='None')
        self.radio_none.grid(row=0, column=1, sticky='news', padx=5, pady=5)
        self.radio_mutation = ttk.Radiobutton(self.frame_disposition, text="Harmful", variable=self.vars['Disposition'], value='Harmful')
        self.radio_mutation.grid(row=1, column=1, sticky='news', padx=5, pady=5)
        self.radio_VUS = ttk.Radiobutton(self.frame_disposition, text="VUS", variable=self.vars['Disposition'], value='VUS')
        self.radio_VUS.grid(row=2, column=1, sticky='news', padx=5, pady=5)
        self.radio_low_vaf = ttk.Radiobutton(self.frame_disposition, text="Low VAF", variable=self.vars['Disposition'], value='Low VAF')
        self.radio_low_vaf.grid(row=3, column=1, sticky='news', padx=5, pady=5)
        self.radio_flt3 = ttk.Radiobutton(self.frame_disposition, text="FLT3 ITD", variable=self.vars['Disposition'], value='FLT3 ITD')
        self.radio_flt3.grid(row=4, column=1, sticky='news', padx=5, pady=5)
        self.radio_hotspot = ttk.Radiobutton(self.frame_disposition, text="Hotspot", variable=self.vars['Disposition'], value='Hotspot')
        self.radio_hotspot.grid(row=5, column=1, sticky='news', padx=5, pady=5)
        # Process output files button
        self.buttons['save_disposition'] = ttk.Button(self.frame_left, text="Save Disposition", command=self.save_disposition, state='disabled')
        self.buttons['save_disposition'].pack(side='top', expand=False, fill='x', padx=5, pady=5, ipady=5)
        # Process output files button
        # Right Frame
        self.frame_right = ttk.Frame(self.frame_base)
        self.frame_right.pack(side='left', expand=True, fill='both',padx=5, pady=5)
        # Basic Info Frame
        self.frame_basic_info = ttk.Labelframe(self.frame_right, text='Locus Info')
        self.frame_basic_info.pack(side='top', expand=False, fill='x', padx=5, pady=5)
        self.frame_basic_info_gene = ttk.Frame(self.frame_basic_info)
        self.frame_basic_info_gene.pack(side='left',expand=False, fill='both', padx=5, pady=5)
        ttk.Label(self.frame_basic_info_gene, text="Gene", anchor='center').pack(side='top',expand=False,fill='x')
        self.labels["Variant Annotation: Gene"] = ttk.Label(self.frame_basic_info_gene, width=8, textvariable=self.variant["Variant Annotation: Gene"], relief='groove', anchor='center', font=('bold', 24, 'bold'))
        self.labels["Variant Annotation: Gene"].pack(side='top',expand=True,fill='both')
        self.frame_basic_info_chrom = ttk.Frame(self.frame_basic_info)
        self.frame_basic_info_chrom.pack(side='left',expand=False,fill='both', padx=5, pady=5)
        ttk.Label(self.frame_basic_info_chrom, anchor='center', text="Chromosome").pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Chrom"] = ttk.Label(self.frame_basic_info_chrom, width=6, textvariable=self.variant["Original Input: Chrom"], relief='groove', anchor='center')
        self.labels["Original Input: Chrom"].pack(side='top',expand=False, fill='x')
        ttk.Label(self.frame_basic_info_chrom, anchor='center', text="Base Pair").pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Pos"] = ttk.Label(self.frame_basic_info_chrom, width=12, textvariable=self.variant["Original Input: Pos"], relief='groove', anchor='center')
        self.labels["Original Input: Pos"].pack(side='top',expand=False, fill='x')
        self.frame_basic_info_changes = ttk.Frame(self.frame_basic_info)
        self.frame_basic_info_changes.pack(side='left',expand=False,fill='both', padx=5, pady=5)
        ttk.Label(self.frame_basic_info_changes, anchor='center', text="DNA Change (c-dot)").pack(side='top',expand=False, fill='x')
        self.labels["Variant Annotation: cDNA change"] = ttk.Label(self.frame_basic_info_changes, text="C-dot", textvariable=self.variant["Variant Annotation: cDNA change"], relief='groove', anchor='center')
        self.labels["Variant Annotation: cDNA change"].pack(side='top',expand=False, fill='x')
        ttk.Label(self.frame_basic_info_changes, anchor='center', text="Protein Change (p-dot)").pack(side='top',expand=False, fill='x')
        self.labels["Variant Annotation: Protein Change"] = ttk.Label(self.frame_basic_info_changes, text="P-dot", width=24, textvariable=self.variant["Variant Annotation: Protein Change"], relief='groove', anchor='center')
        self.labels["Variant Annotation: Protein Change"].pack(side='top',expand=False, fill='x')
        self.frame_basic_info_alleles = ttk.Frame(self.frame_basic_info)
        self.frame_basic_info_alleles.pack(side='left',expand=True,fill='both', padx=5, pady=5)
        ttk.Label(self.frame_basic_info_alleles, text="Ref Allele", anchor='w').pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Reference allele"] = ttk.Label(self.frame_basic_info_alleles, textvariable=self.variant["Original Input: Reference allele"], relief='groove', anchor='w')
        self.labels["Original Input: Reference allele"].pack(side='top',expand=False, fill='x')
        ttk.Label(self.frame_basic_info_alleles, text="Variant Allele", anchor='w').pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Alternate allele"] = ttk.Label(self.frame_basic_info_alleles, textvariable=self.variant["Original Input: Alternate allele"], relief='groove', anchor='w')
        self.labels["Original Input: Alternate allele"].pack(side='top',expand=False, fill='x')
        self.frame_basic_info_misc = ttk.Frame(self.frame_basic_info)
        self.frame_basic_info_misc.pack(side='left',expand=False,fill='both', padx=5, pady=5)
        ttk.Label(self.frame_basic_info_misc, anchor='center', text="Length of Variant (BP)").pack(side='top',expand=False, fill='x')
        self.labels["VCF: LEN"] = ttk.Label(self.frame_basic_info_misc, textvariable=self.variant["VCF: LEN"], relief='groove', anchor='center')
        self.labels["VCF: LEN"].pack(side='top',expand=True, fill='both')

        # middle frame
        self.frame_middle = ttk.Frame(self.frame_right)
        self.frame_middle.pack(side='top',expand=True,fill='both', padx=5, pady=5)
        # Strand Bias Frame
        self.frame_genexus = ttk.Labelframe(self.frame_middle, text='Strand Bias Data', relief='groove')
        self.frame_genexus.pack(side='left', expand=False, fill='both', padx=(0,10))
        self.frame_genexus_sb_calc = ttk.Frame(self.frame_genexus)
        self.frame_genexus_sb_calc.pack(side='top', expand=False, fill='both', padx=5, pady=5)
        self.frame_genexus_sb_calc.rowconfigure(0, weight=1)
        self.frame_genexus_sb_calc.rowconfigure(1, weight=1)
        self.frame_genexus_sb_calc.columnconfigure(0, weight=0)
        self.frame_genexus_sb_calc.columnconfigure(1, weight=5)
        self.frame_genexus_sb_calc.columnconfigure(2, weight=0)
        self.frame_genexus_sb_calc.columnconfigure(3, weight=1)
        ttk.Label(self.frame_genexus_sb_calc, text="SB (reported)", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["VCF: STB"] = ttk.Label(self.frame_genexus_sb_calc, textvariable=self.variant["VCF: STB"], relief='groove', anchor='center')
        self.labels["VCF: STB"].grid(column=1, row=0, sticky='news')
        ttk.Label(self.frame_genexus_sb_calc, text="p.", anchor='e').grid(column=2, row=0, sticky='news', padx=5)
        self.labels["VCF: STBP"] = ttk.Label(self.frame_genexus_sb_calc, textvariable=self.variant["VCF: STBP"], relief='groove', anchor='center', width=5)
        self.labels["VCF: STBP"].grid(column=3, row=0, sticky='news')
        # Genexus strand Bias Area
        self.frame_sb_GX = ttk.Labelframe(self.frame_genexus, text="Genexus (calculated)")
        self.frame_sb_GX.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frame_sb_GX.rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frame_sb_GX.columnconfigure(x, weight=1)
        ttk.Label(self.frame_sb_GX, anchor='center', text='Genexus', width=8, font=self.big_text).grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        ttk.Label(self.frame_sb_GX, anchor='center', text='Fwd').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.Label(self.frame_sb_GX, anchor='center', text='Rev').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.Label(self.frame_sb_GX, text='Ref', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_GX, text='Var', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSRF'] = ttk.Label(self.frame_sb_GX, textvariable=self.variant["VCF: FSRF"], relief='groove', anchor='center')
        self.labels['VCF: FSRF'].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSRR'] = ttk.Label(self.frame_sb_GX, textvariable=self.variant["VCF: FSRR"], relief='groove', anchor='center')
        self.labels['VCF: FSRR'].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSAF'] = ttk.Label(self.frame_sb_GX, textvariable=self.variant["VCF: FSAF"], relief='groove', anchor='center')
        self.labels['VCF: FSAF'].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSAR'] = ttk.Label(self.frame_sb_GX, textvariable=self.variant["VCF: FSAR"], relief='groove', anchor='center')
        self.labels['VCF: FSAR'].grid(column=3, row=2, sticky='news', pady=5, padx=5)
        # Separator
        ttk.Separator(self.frame_sb_GX, orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frame_sb_GX_results = ttk.Frame(self.frame_sb_GX)
        self.frame_sb_GX_results.grid(column=0, row=5, columnspan=4, sticky='news')
        self.frame_sb_GX_results.rowconfigure(0, weight=1)
        self.frame_sb_GX_results.rowconfigure(1, weight=1)
        self.frame_sb_GX_results.columnconfigure(0, weight=0)
        self.frame_sb_GX_results.columnconfigure(1, weight=5)
        self.frame_sb_GX_results.columnconfigure(2, weight=0)
        self.frame_sb_GX_results.columnconfigure(3, weight=1)
        # Genexus Stats Area
        ttk.Label(self.frame_sb_GX_results, text="Binom. Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["VCF: Binom Proportion"] = ttk.Label(self.frame_sb_GX_results, textvariable=self.variant["VCF: Binom Proportion"], relief='groove', anchor='center')
        self.labels["VCF: Binom Proportion"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_GX_results, text="p.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["VCF: Binom P Value"] = ttk.Label(self.frame_sb_GX_results, textvariable=self.variant["VCF: Binom P Value"], relief='groove', anchor='center', width=5)
        self.labels["VCF: Binom P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_GX_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["VCF: Fisher Odds Ratio"] = ttk.Label(self.frame_sb_GX_results, textvariable=self.variant["VCF: Fisher Odds Ratio"], relief='groove', anchor='center')
        self.labels["VCF: Fisher Odds Ratio"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_GX_results, text="p.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["VCF: Fisher P Value"] = ttk.Label(self.frame_sb_GX_results, textvariable=self.variant["VCF: Fisher P Value"], relief='groove', anchor='center', width=5)
        self.labels["VCF: Fisher P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        # Q20 Read Bias Area
        self.frame_sb_Q20 = ttk.Labelframe(self.frame_genexus, text="Filtered M-Pileup (calculated)")
        self.frame_sb_Q20.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frame_sb_Q20.rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frame_sb_Q20.columnconfigure(x, weight=1)
        ttk.Label(self.frame_sb_Q20, text='Q20', width=8, font=self.big_text, anchor='center').grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        ttk.Label(self.frame_sb_Q20, anchor='center', text='Fwd').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.Label(self.frame_sb_Q20, anchor='center', text='Rev').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.Label(self.frame_sb_Q20, text='Ref', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_Q20, text='Var', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Reference Forward Read Depth"] = ttk.Label(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Reference Forward Read Depth"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Filtered Reference Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Reference Reverse Read Depth"] = ttk.Label(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Reference Reverse Read Depth"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Filtered Reference Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Variant Forward Read Depth"] = ttk.Label(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Variant Forward Read Depth"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Filtered Variant Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Variant Reverse Read Depth"] = ttk.Label(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Variant Reverse Read Depth"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Filtered Variant Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)
        # Separator
        ttk.Separator(self.frame_sb_Q20, orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frame_sb_Q20_results = ttk.Frame(self.frame_sb_Q20)
        self.frame_sb_Q20_results.grid(column=0, row=5, columnspan=4, sticky='news')
        self.frame_sb_Q20_results.rowconfigure(0, weight=1)
        self.frame_sb_Q20_results.rowconfigure(1, weight=1)
        self.frame_sb_Q20_results.columnconfigure(0, weight=0)
        self.frame_sb_Q20_results.columnconfigure(1, weight=5)
        self.frame_sb_Q20_results.columnconfigure(2, weight=0)
        self.frame_sb_Q20_results.columnconfigure(3, weight=1)
        # Q20 Stats Area
        ttk.Label(self.frame_sb_Q20_results, text="Binom. Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["Mpileup Qual: Filtered Variant Binomial Proportion"] = ttk.Label(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial Proportion"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Filtered Variant Binomial Proportion"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_Q20_results, text="p.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["Mpileup Qual: Filtered Variant Binomial P Value"] = ttk.Label(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial P Value"], relief='groove', anchor='center', width=5)
        self.labels["Mpileup Qual: Filtered Variant Binomial P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_Q20_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["Mpileup Qual: Filtered Variant Fishers Odds Ratio"] = ttk.Label(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers Odds Ratio"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Filtered Variant Fishers Odds Ratio"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_Q20_results, text="p.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["Mpileup Qual: Filtered Variant Fishers P Value"] = ttk.Label(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers P Value"], relief='groove', anchor='center', width=5)
        self.labels["Mpileup Qual: Filtered Variant Fishers P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        # Q1 Read Bias Area
        self.frame_sb_Q1 = ttk.Labelframe(self.frame_genexus, text="Unfiltered M-Pileup (calculated)")
        self.frame_sb_Q1.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frame_sb_Q1.rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frame_sb_Q1.columnconfigure(x, weight=1)
        ttk.Label(self.frame_sb_Q1, text='Q1', width=8, font=self.big_text, anchor='center').grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        ttk.Label(self.frame_sb_Q1, anchor='center', text='Fwd').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.Label(self.frame_sb_Q1, anchor='center', text='Rev').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.Label(self.frame_sb_Q1, text='Ref', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_Q1, text='Var', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Reference Forward Read Depth"] = ttk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Reference Forward Read Depth"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Unfiltered Reference Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Reference Reverse Read Depth"] = ttk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Reference Reverse Read Depth"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Unfiltered Reference Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Forward Read Depth"] = ttk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Forward Read Depth"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Unfiltered Variant Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Reverse Read Depth"] = ttk.Label(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Reverse Read Depth"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Unfiltered Variant Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)
        # Separator
        ttk.Separator(self.frame_sb_Q1, orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frame_sb_Q1_results = ttk.Frame(self.frame_sb_Q1)
        self.frame_sb_Q1_results.grid(column=0, row=5, columnspan=4, sticky='news')
        self.frame_sb_Q1_results.rowconfigure(0, weight=1)
        self.frame_sb_Q1_results.rowconfigure(1, weight=1)
        self.frame_sb_Q1_results.columnconfigure(0, weight=0)
        self.frame_sb_Q1_results.columnconfigure(1, weight=5)
        self.frame_sb_Q1_results.columnconfigure(2, weight=0)
        self.frame_sb_Q1_results.columnconfigure(3, weight=1)
        # Q1 Stats Area
        ttk.Label(self.frame_sb_Q1_results, text="Binom. Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Binomial Proportion"] = ttk.Label(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial Proportion"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Unfiltered Variant Binomial Proportion"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_Q1_results, text="p.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["Mpileup Qual: Unfiltered Variant Binomial P Value"] = ttk.Label(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial P Value"], relief='groove', anchor='center', width=5)
        self.labels["Mpileup Qual: Unfiltered Variant Binomial P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_Q1_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"] = ttk.Label(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.Label(self.frame_sb_Q1_results, text="p.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["Mpileup Qual: Unfiltered Variant Fishers P Value"] = ttk.Label(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers P Value"], relief='groove', anchor='center', width=5)
        self.labels["Mpileup Qual: Unfiltered Variant Fishers P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)

        # Genexus info frame
        self.frame_gx_info = ttk.Labelframe(self.frame_middle, text='Genexus Information')
        self.frame_gx_info.pack(side='top', expand=False, fill='both', pady=(0,5))
        for x in range(1,5,2):
            self.frame_gx_info.rowconfigure(x, weight=1)
        for x in range(5):
            self.frame_gx_info.columnconfigure(x, weight=1)
        # gx info top area
        ttk.Label(self.frame_gx_info, anchor='center', text="Allele Fraction").grid(row=0, column=0, sticky='news', padx=5)
        self.labels["VCF: AF"] = ttk.Label(self.frame_gx_info, textvariable=self.variant["VCF: AF"], relief='groove', anchor='center')
        self.labels["VCF: AF"].grid(row=1, column=0, sticky='news', padx=5, pady=5)
        ttk.Label(self.frame_gx_info, anchor='center', text="Variant Type").grid(row=0, column=1, sticky='news', padx=5)
        self.labels["VCF: TYPE"] = ttk.Label(self.frame_gx_info, textvariable=self.variant["VCF: TYPE"], relief='groove', anchor='center')
        self.labels["VCF: TYPE"].grid(row=1, column=1, sticky='news', padx=5, pady=5)
        ttk.Label(self.frame_gx_info, anchor='center', text="Genotype").grid(row=0, column=2, sticky='news', padx=5)
        self.labels["VCF: Genotype"] = ttk.Label(self.frame_gx_info, textvariable=self.variant["VCF: Genotype"], relief='groove', anchor='center')
        self.labels["VCF: Genotype"].grid(row=1, column=2, sticky='news', padx=5, pady=5)
        ttk.Label(self.frame_gx_info, anchor='center', text="Filter (Genexus)").grid(row=0, column=3, sticky='news', padx=5)
        self.labels["VCF: Filter"] = ttk.Label(self.frame_gx_info, textvariable=self.variant["VCF: Filter"], relief='groove', anchor='center')
        self.labels["VCF: Filter"].grid(row=1, column=3, sticky='news', padx=5, pady=5)
        ttk.Label(self.frame_gx_info, anchor='center', text="Quality Score").grid(row=0, column=4, sticky='news', padx=5)
        self.labels["VCF: QUAL"] = ttk.Label(self.frame_gx_info, textvariable=self.variant["VCF: QUAL"], relief='groove', anchor='center')
        self.labels["VCF: QUAL"].grid(row=1, column=4, sticky='news', padx=5, pady=5)
        # Separator
        ttk.Separator(self.frame_gx_info, orient='horizontal').grid(row=2, column=0, columnspan=5, sticky='news')
        # gx info bottom area
        ttk.Label(self.frame_gx_info, anchor='center', text="FAO").grid(row=3, column=0, sticky='news', padx=5)
        self.labels["VCF: FAO"] = ttk.Label(self.frame_gx_info, textvariable=self.variant["VCF: FAO"], relief='groove', anchor='center')
        self.labels["VCF: FAO"].grid(row=4, column=0, sticky='news', padx=5, pady=5)
        ttk.Label(self.frame_gx_info, anchor='center', text="FDP").grid(row=3, column=1, sticky='news', padx=5)
        self.labels["VCF: FDP"] = ttk.Label(self.frame_gx_info, textvariable=self.variant["VCF: FDP"], relief='groove', anchor='center')
        self.labels["VCF: FDP"].grid(row=4, column=1, sticky='news', padx=5, pady=5)
        ttk.Label(self.frame_gx_info, anchor='center', text="HRUN").grid(row=3, column=2, sticky='news', padx=5)
        self.labels["VCF: HRUN"] = ttk.Label(self.frame_gx_info, textvariable=self.variant["VCF: HRUN"], relief='groove', anchor='center')
        self.labels["VCF: HRUN"].grid(row=4, column=2, sticky='news', padx=5, pady=5)
        ttk.Label(self.frame_gx_info, anchor='center', text="QD").grid(row=3, column=3, sticky='news', padx=5)
        self.labels["VCF: QD"] = ttk.Label(self.frame_gx_info, textvariable=self.variant["VCF: QD"], relief='groove', anchor='center')
        self.labels["VCF: QD"].grid(row=4, column=3, sticky='news', padx=5, pady=5)
        ttk.Label(self.frame_gx_info, anchor='center', text="SVTYPE (Unused)").grid(row=3, column=4, sticky='news', padx=5)
        self.labels["VCF: SVTYPE"] = ttk.Label(self.frame_gx_info, textvariable=self.variant["VCF: SVTYPE"], relief='groove', anchor='center')
        self.labels["VCF: SVTYPE"].grid(row=4, column=4, sticky='news', padx=5, pady=5)

        # mpileup info frame
        self.frame_mpl_info = ttk.Labelframe(self.frame_middle, text='M-Pileup Information')
        self.frame_mpl_info.pack(side='top', expand=False, fill='both', pady=5)
        self.frame_mpl_info_RD = ttk.Frame(self.frame_mpl_info)
        self.frame_mpl_info_RD.pack(side='left', expand=True, fill='both', pady=5, padx=5)
        ttk.Label(self.frame_mpl_info_RD, anchor='center', text="Total Read Depth").pack(side='left', expand=False, fill='both')
        self.labels["Mpileup Qual: Read Depth"] = ttk.Label(self.frame_mpl_info_RD, textvariable=self.variant["Mpileup Qual: Read Depth"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Read Depth"].pack(side='left', expand=True, fill='both', pady=5, padx=5)
        self.frame_mpl_info_starts = ttk.Frame(self.frame_mpl_info)
        self.frame_mpl_info_starts.pack(side='left', expand=True, fill='both', pady=5, padx=5)
        ttk.Label(self.frame_mpl_info_starts, anchor='center', text="Count: Read Starts").pack(side='left', expand=False, fill='both', pady=5, padx=5)
        self.labels["Mpileup Qual: Start Reads"] = ttk.Label(self.frame_mpl_info_starts, textvariable=self.variant["Mpileup Qual: Start Reads"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Start Reads"].pack(side='left', expand=True, fill='both', pady=5, padx=5)
        self.frame_mpl_info_ends = ttk.Frame(self.frame_mpl_info)
        self.frame_mpl_info_ends.pack(side='left', expand=True, fill='both', pady=5, padx=5)
        ttk.Label(self.frame_mpl_info_ends, anchor='center', text="Count: Read Ends").pack(side='left', expand=False, fill='both', pady=5, padx=5)
        self.labels["Mpileup Qual: Stop Reads"] = ttk.Label(self.frame_mpl_info_ends, textvariable=self.variant["Mpileup Qual: Stop Reads"], relief='groove', anchor='center')
        self.labels["Mpileup Qual: Stop Reads"].pack(side='left', expand=True, fill='both', pady=5, padx=5)

        # Variant DB Info Frame
        self.frame_other = ttk.Frame(self.frame_middle)
        self.frame_other.pack(side='top',expand=True, fill='both')
        self.frame_var_annot = ttk.Labelframe(self.frame_other, text='Variant Annotation')
        self.frame_var_annot.pack(side='left',expand=True, fill='both', padx=(0,5))
        for x in range(3):
            self.frame_var_annot.columnconfigure(x, weight=1)
        self.frame_var_annot.rowconfigure(3, weight=99)
        ttk.Label(self.frame_var_annot, anchor='center', text="Coding Region").grid(column=0, row=0, sticky='news', padx=5)
        self.labels["Variant Annotation: Coding"] = ttk.Label(self.frame_var_annot, textvariable=self.variant["Variant Annotation: Coding"], relief='groove', anchor='center')
        self.labels["Variant Annotation: Coding"].grid(column=0, row=1, sticky='news', padx=5)
        ttk.Label(self.frame_var_annot, anchor='center', text="Variant Type (Seq. Ontology)").grid(column=1, row=0, sticky='news', padx=5)
        self.labels["Variant Annotation: Sequence"] = ttk.Label(self.frame_var_annot, textvariable=self.variant["Variant Annotation: Sequence Ontology"], relief='groove', anchor='center')
        self.labels["Variant Annotation: Sequence"].grid(column=1, row=1, sticky='news', padx=5)
        ttk.Label(self.frame_var_annot, anchor='center', text="Transcript").grid(column=2, row=0, sticky='news', padx=5)
        self.labels["Variant Annotation: Transcript"] = ttk.Label(self.frame_var_annot, textvariable=self.variant["Variant Annotation: Transcript"], relief='groove', anchor='center')
        self.labels["Variant Annotation: Transcript"].grid(column=2, row=1, sticky='news', padx=5)
        self.labels["Variant Annotation: Transcript"].bind('<Button-1>', lambda cosmic: ENSTLink(self.variant["Variant Annotation: Transcript"].get()))
        ttk.Label(self.frame_var_annot, anchor='center', text="All Mappings").grid(column=0, row=2, columnspan=3, sticky='news', padx=5)
        self.labels["Variant Annotation: All Mappings"] = ttk.Label(self.frame_var_annot, textvariable=self.variant["Variant Annotation: All Mappings"], relief='groove', anchor='center', wraplength=500)
        self.labels["Variant Annotation: All Mappings"].grid(column=0, columnspan=3, row=3, sticky='news', padx=5, pady=(0,5))

        # MDL Info area
        self.frame_mdl = ttk.Labelframe(self.frame_other, text='MDL Info')
        self.frame_mdl.pack(side='left',expand=True, fill='both', padx=(5,0))
        self.frame_mdl.rowconfigure(3, weight=99)
        self.frame_mdl.columnconfigure(0, weight=1)
        self.frame_mdl.columnconfigure(1, weight=1)
        ttk.Label(self.frame_mdl, anchor='center', text="Sample Count").grid(column=0, row=0, sticky='news', padx=5)
        self.labels["MDL: Sample Count"] = ttk.Label(self.frame_mdl, textvariable=self.variant["MDL: Sample Count"], relief='groove', anchor='center')
        self.labels["MDL: Sample Count"].grid(column=0, row=1, sticky='news', padx=5)
        ttk.Label(self.frame_mdl, anchor='center', text="Variant Frequency").grid(column=1, row=0, sticky='news', padx=5)
        self.labels["MDL: Variant Frequency"]  = ttk.Label(self.frame_mdl, textvariable=self.variant["MDL: Variant Frequency"], relief='groove', anchor='center')
        self.labels["MDL: Variant Frequency"].grid(column=1, row=1, sticky='news', padx=5)
        ttk.Label(self.frame_mdl, anchor='center', text="Sample List").grid(column=0, columnspan=2, row=2, sticky='news', padx=5)
        self.labels["MDL: Sample List"] = ttk.Label(self.frame_mdl, textvariable=self.variant["MDL: Sample List"], relief='groove', anchor='center', wraplength=500)
        self.labels["MDL: Sample List"].grid(column=0, columnspan=2, row=3, sticky='news', padx=5, pady=(0,5))

        # Web Resources Stats
        self.frame_bottom = ttk.Labelframe(self.frame_right, text='Database Information')
        self.frame_bottom.pack(side='bottom', expand=False, fill='both', padx=5, pady=5)
        self.frame_bottom.columnconfigure(0, weight=1)
        self.frame_bottom.columnconfigure(1, weight=1)
        self.frame_bottom_l = ttk.Frame(self.frame_bottom)
        self.frame_bottom_l.grid(column=0, row=0, sticky='news')
        self.frame_bottom_2 = ttk.Frame(self.frame_bottom)
        self.frame_bottom_2.grid(column=1, row=0, sticky='news')
        # COSMIC Tissue Variant Count Region
        self.labels["COSMIC: Variant Count (Tissue)"] = ttk.Label(self.frame_bottom_l, textvariable=self.variant["COSMIC: Variant Count (Tissue)"], relief='groove', anchor='center', wraplength=500)
        self.labels["COSMIC: Variant Count (Tissue)"].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        # COSMIC Area
        self.frame_web_cosmic = ttk.LabelFrame(self.frame_bottom_2, text='COSMIC')
        self.frame_web_cosmic.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.Label(self.frame_web_cosmic, text="ID", anchor='center').pack(side='top', expand=False, fill='x', padx=5)
        self.labels["COSMIC: ID"] = ttk.Label(self.frame_web_cosmic, textvariable=self.variant["COSMIC: ID"], relief='groove', anchor='center', width=12)
        self.labels["COSMIC: ID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        self.labels['COSMIC: ID'].bind('<Button-1>', lambda cosmic: CosmicLink(self.variant["COSMIC: ID"].get()))
        ttk.Label(self.frame_web_cosmic, anchor='center', text="Count").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["COSMIC: Variant Count"] = ttk.Label(self.frame_web_cosmic, textvariable=self.variant["COSMIC: Variant Count"], relief='groove', anchor='center')
        self.labels["COSMIC: Variant Count"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # Clinvar Area
        self.frame_web_clinvar = ttk.LabelFrame(self.frame_bottom_2, text='ClinVar')
        self.frame_web_clinvar.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.Label(self.frame_web_clinvar, anchor='center', text="ID").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["ClinVar: ClinVar ID"] = ttk.Label(self.frame_web_clinvar, textvariable=self.variant["ClinVar: ClinVar ID"], relief='groove', anchor='center')
        self.labels["ClinVar: ClinVar ID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        self.labels['ClinVar: ClinVar ID'].bind('<Button-1>', lambda clinvar: ClinVarLink(self.variant["ClinVar: ClinVar ID"].get()))
        ttk.Label(self.frame_web_clinvar, anchor='center', text="Significance").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["ClinVar: Clinical Significance"] = ttk.Label(self.frame_web_clinvar, textvariable=self.variant["ClinVar: Clinical Significance"], relief='groove', anchor='center')
        self.labels["ClinVar: Clinical Significance"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # Gnomad Area
        self.frame_web_gnomad = ttk.LabelFrame(self.frame_bottom_2, text='GnomAD')
        self.frame_web_gnomad.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.Label(self.frame_web_gnomad, anchor='center', text="Global AF").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["gnomAD3: Global AF"] = ttk.Label(self.frame_web_gnomad, textvariable=self.variant["gnomAD3: Global AF"], relief='groove', anchor='center')
        self.labels["gnomAD3: Global AF"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # CADD Area
        self.frame_web_cadd = ttk.LabelFrame(self.frame_bottom_2, text='CADD')
        self.frame_web_cadd.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.Label(self.frame_web_cadd, anchor='center', text="Phred Score").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["CADD: Phred"] = ttk.Label(self.frame_web_cadd, textvariable=self.variant["CADD: Phred"], relief='groove', anchor='center')
        self.labels["CADD: Phred"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # PolyPhen Area
        self.frame_web_polyphen = ttk.LabelFrame(self.frame_bottom_2, text='PolyPhen-2')
        self.frame_web_polyphen.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.Label(self.frame_web_polyphen, anchor='center', text="HDIV").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["PolyPhen-2: HDIV Prediction"] = ttk.Label(self.frame_web_polyphen, textvariable=self.variant["PolyPhen-2: HDIV Prediction"], relief='groove', anchor='center')
        self.labels["PolyPhen-2: HDIV Prediction"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # SIFT Area
        self.frame_web_sift = ttk.LabelFrame(self.frame_bottom_2, text='SIFT')
        self.frame_web_sift.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.Label(self.frame_web_sift, anchor='center', text="Prediction").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["SIFT: Prediction"] = ttk.Label(self.frame_web_sift, textvariable=self.variant["SIFT: Prediction"], relief='groove', anchor='center')
        self.labels["SIFT: Prediction"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # dbSNP Area
        self.frame_web_dbsnp = ttk.LabelFrame(self.frame_bottom_2, text='dbSNP')
        self.frame_web_dbsnp.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.Label(self.frame_web_dbsnp, anchor='center', text="rsID").pack(side='top', expand=False, fill='both', padx=5)
        self.labels["dbSNP: rsID"] = ttk.Label(self.frame_web_dbsnp, textvariable=self.variant["dbSNP: rsID"], relief='groove', anchor='center')
        self.labels["dbSNP: rsID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        self.labels["dbSNP: rsID"].bind('<Button-1>', lambda clinvar: dbSNPLink(self.variant["dbSNP: rsID"].get()))
        # UniProt Area
        self.frame_web_dbsnp = ttk.LabelFrame(self.frame_bottom_2, text='UniProt (GENE)')
        self.frame_web_dbsnp.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.Label(self.frame_web_dbsnp, anchor='center', text="Accession Number").pack(side='top', expand=False, fill='both', padx=5)
        self.labels["UniProt (GENE): Accession Number"] = ttk.Label(self.frame_web_dbsnp, textvariable=self.variant["UniProt (GENE): Accession Number"], relief='groove', anchor='center')
        self.labels["UniProt (GENE): Accession Number"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        self.labels["UniProt (GENE): Accession Number"].bind('<Button-1>', lambda uniprot: UniProtLink(self.variant["UniProt (GENE): Accession Number"].get()))

        # self.create_tooltips()

        return

    def create_tooltips(self):
        """Creates tooltips for labels and widgets."""
        for key,value in tooltips.items():
            CreateToolTip(self.labels[key], value)
        return

    def validate_cells(self):

        for x in vcf_columns:
            self.labels[x].configure(bootstyle='normal.TLabel')
            if self.variant[x].get() == "":
                self.labels[x].configure(bootstyle='inverse.TLabel')
                continue
            if x in self.validation['p-values']:
                if float(self.variant[x].get()) > 0.05:
                    self.labels[x].configure(bootstyle='danger.inverse.TLabel')
            if x in self.validation['read depth 10']:
                if int(self.variant[x].get()) <= 10:
                    self.labels[x].configure(bootstyle='danger.inverse.TLabel')
            if x in self.validation['read depth 500']:
                if int(self.variant[x].get()) <= 500:
                    self.labels[x].configure(bootstyle='danger.inverse.TLabel')
            if x in self.validation['low vaf']:
                if float(self.variant[x].get()) < 0.02:
                    self.labels[x].configure(bootstyle='danger.inverse.TLabel')
            if x in self.validation['web links']:
                self.labels[x].configure(bootstyle = 'info.inverse')
        return

    def open_csv_file(self):
        for item in self.treeview_variant_list.get_children():
            self.treeview_variant_list.delete(item)
        csv_dict = dict()
        self.vars['filename'].set(str(fd.askopenfilename(filetypes=[('CSV','*.csv')])))
        with open(self.vars['filename'].get(), 'r') as csv_file:
            counter = 0 # need to use a counter here to skip the headers row
            for row in csv.DictReader(csv_file, fieldnames=vcf_columns, delimiter='\t'):
                if counter != 0: # second and later file lines only
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
        self.treeview_variant_list.selection_set('I001')
        self.count_dispositions()
        return
    
    def open_file(self):

        # Clear the treeview to prevent duplicate file loading.  Entries are not auto cleared.
        for item in self.treeview_variant_list.get_children():
            self.treeview_variant_list.delete(item)
        self.vars['filename'].set(str(fd.askopenfilename(filetypes=[('XLSX','*.xlsx'), ('CSV','*.csv')])))
        # update the title of the app to help show long filenames
        title = 'VCF Result Viewer - ' + self.vars['filename'].get()
        self.title(title)
        # portion for working with the xlsx file format
        if 'xlsx' in self.vars['filename'].get():
            try:
                xlsx = pd.ExcelFile(self.vars['filename'].get())
                self.DF = pd.DataFrame()
                for sheet in xlsx.sheet_names:
                    DF_sheet = xlsx.parse(sheet)
                    if sheet == "Hotspot Exceptions":
                        DF_sheet['Disposition'] = "Hotspot"
                    elif sheet == "FLT3 ITDs":
                        DF_sheet['Disposition'] = "FLT3 ITD"
                    elif sheet == "Low VAF Variants":
                        DF_sheet['Disposition'] = "Low VAF"
                    else:
                        DF_sheet['Disposition'] = "None"
                    if self.DF.empty:
                        self.DF = DF_sheet
                    else:
                        self.DF = pd.concat([self.DF, DF_sheet], axis=0)
                print("Excel file successfully loaded.")
            except:
                print("Excel file format not detected.")
                return
        else: # portion for working with .CSV files
            try:
                self.DF = pd.read_csv(self.vars['filename'].get())
                print("CSV file successfully loaded.")
            except:
                print("CSV file format not detected.")
                return

        for row in self.DF.iterrows():
            self.treeview_variant_list
            values_list = list()
            for col in self.DF.columns:
                values_list.append(row[1][col])
            self.treeview_variant_list.insert('', tk.END, values=values_list)
        self.treeview_variant_list.selection_set('I001')
        self.count_dispositions()
        return

    def item_selected(self, event):
        for selected_item in self.treeview_variant_list.selection():
            item = self.treeview_variant_list.item(selected_item)
            record = item['values']
            for x in range(len(vcf_columns)):
                self.variant[vcf_columns[x]].set(record[x])
        self.vars['Disposition'].set(self.variant['Disposition'].get())
        if self.vars['Disposition'].get():
            self.buttons['save_disposition']['state'] = 'normal'
        self.validate_cells()
        return
    
    def save_disposition(self):
        selection = self.treeview_variant_list.focus()
        self.treeview_variant_list.set(selection, column='Disposition', value=self.vars['Disposition'].get())
        self.count_dispositions()
        return

    def count_dispositions(self):
        "Function to inventory the count of dispositions present in the list.  Called whenever a disposition is updated."

        self.vars['dispo_none_count'].set(0)
        self.vars['dispo_low_vaf_count'].set(0)
        self.vars['dispo_vus_count'].set(0)
        self.vars['dispo_mutation_count'].set(0)
        self.vars['dispo_flt3_count'].set(0)
        self.vars['dispo_hotspot_count'].set(0)

        none_count = 0
        low_vaf = 0
        vus_count = 0
        mutation_count = 0
        flt3_count = 0
        hotspot_count = 0

        item_list = self.treeview_variant_list.get_children(item=None)

        for x in item_list:
            dispo = self.treeview_variant_list.set(x, column='Disposition')
            if dispo == 'Harmful':
                mutation_count += 1
            elif dispo == 'Low VAF':
                low_vaf += 1
            elif dispo == 'VUS':
                vus_count += 1
            elif dispo == 'FLT3 ITD':
                flt3_count += 1
            elif dispo == 'Hotspot':
                hotspot_count += 1
            else: # "None" disposition
                none_count += 1

        self.vars['dispo_none_count'].set(none_count)
        self.vars['dispo_low_vaf_count'].set(low_vaf)
        self.vars['dispo_vus_count'].set(vus_count)
        self.vars['dispo_mutation_count'].set(mutation_count)
        self.vars['dispo_flt3_count'].set(flt3_count)
        self.vars['dispo_hotspot_count'].set(hotspot_count)

        return

    def goto_next_radio(self):
        if not self.vars['Disposition'].get():
            pass
        elif self.vars['Disposition'].get() == 'None':
            self.radio_low_vaf.invoke()
            self.vars['Disposition'].set('Low VAF')
        elif self.vars['Disposition'].get() == 'Low VAF':
            self.radio_VUS.invoke()
            self.vars['Disposition'].set('VUS')
        elif self.vars['Disposition'].get() == 'VUS':
            self.radio_mutation.invoke()
            self.vars['Disposition'].set('Harmful')
        elif self.vars['Disposition'].get() == 'Harmful':
            self.radio_none.invoke()
            self.vars['Disposition'].set('None')
        return
    
    def goto_prev_radio(self):
        if not self.vars['Disposition'].get():
            pass
        elif self.vars['Disposition'].get() == 'Harmful':
            self.radio_VUS.invoke()
        elif self.vars['Disposition'].get() == 'VUS':
            self.radio_low_vaf.invoke()
        elif self.vars['Disposition'].get() == 'Low VAF':
            self.radio_none.invoke()
        elif self.vars['Disposition'].get() == 'None':
            self.radio_mutation.invoke()
        return

    def change_theme(self, theme_name:str):
        self.style.theme_use(theme_name)
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

def CosmicLink(ID:str):
    """Follow a link to COSMIC Database."""
    link_string = f"https://cancer.sanger.ac.uk/cosmic/mutation/overview?id={ID}"
    webbrowser.open(link_string)
    return

def ClinVarLink(ID:str):
    """Follow a link to COSMIC Database."""
    link_string = f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{ID}/"
    webbrowser.open(link_string)
    return

def dbSNPLink(ID:str):
    """Follow a link to the dbSNP Database."""
    link_string = f"https://www.ncbi.nlm.nih.gov/snp/{ID}"
    webbrowser.open(link_string)
    return

def UniProtLink(ID:str):
    """Follow a link to the UniProt Database."""
    link_string = f"https://www.uniprot.org/uniprotkb/{ID}/entry/"
    webbrowser.open(link_string)
    return

def ENSTLink(ID:str):
    """Follow a link to the UniProt Database."""
    link_string = f"http://useast.ensembl.org/Homo_sapiens/Transcript/Summary?t={ID}"
    webbrowser.open(link_string)
    return

def donothing():
    pass
    return

# MAIN LOOP ----------------------------------------------

def main():
    # Mainloop
    root = App()
    root.mainloop()    
    return

if __name__ == '__main__':
    main()
