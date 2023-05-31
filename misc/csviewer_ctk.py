# CSViewer.py
''' An application to view a csv file. '''

# IMPORTS ------------------------------------------------

import tkinter as tk 
from tkinter import filedialog as fd
# import tkinter.ttk as ttk 
# import ttkbootstrap as ttk 
from tkinter.ttk import Treeview, Scrollbar
import customtkinter as ttk
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
    "VCF: FAO":"Variant read depth at this base pair location, reported by Genexys.",
    "VCF: FDP":"Total read depth at this base pair location, reported by Genexys",
    "VCF: HRUN":"Homopolymer run count, reported by Genexys.",
    "VCF: Filter":"Final filter disposition as given by the Genexys.\n Preferred value: 'PASS'",
    "VCF: Genotype":"Genotype distinction made by the Genexys analyzer.\n 1/1 = homozygous, 0/1 = heterozygous, 0/0 = ???, ./. = ???",
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
    "VCF: FSAF":"Forward Variant Read Depth, reported by Genexys\nValid value: > 10",
    "VCF: FSAR":"Reverse Variant Read Depth, reported by Genexys\nValid value: > 10",
    "VCF: FSRF":"Forward Reference Read Depth, reported by Genexys.",
    "VCF: FSRR":"Reverse Reference Read Depth, reported by Genexys.",
    "VCF: Fisher Odds Ratio":"Fisher's odds ratio calculation, based on Genexys read depth data.",
    "VCF: Fisher P Value":"Statistical p-value.\nLess than 0.05 is preferred.",
    "VCF: Binom Proportion":"Binomial proportion caclucation, based on Genexys read depth data.",
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
    "VCF: LEN":"Length of the variant, as reported by Genexys.",
    "VCF: QD":"???",
    "VCF: STB":"Proprietary strand bias calculation, as reported by Genexys.",
    "VCF: STBP":"Statistical p-value.\nLess than 0.05 is preferred.",
    "VCF: SVTYPE":"Unused data field from the Genexys report.",
    "VCF: TYPE":"Type of variant, as reported by Genexys.",
    "VCF: QUAL":"Quality determination tag, as reported by Genexys.",
    "Variant Annotation: Coding":"Reported coding region variant, as reported by Genexys.",
    "Variant Annotation: Sequence Ontology":"Type of variant/mutation encountered.\n Possible Types: MIS, INT, FSI, IND, SYN, SPL ",
    "Variant Annotation: Transcript":"Ensembl transcript designation code.",
    "Variant Annotation: All Mappings":"JSON-style dictionary breakdown of tissue types present in ??? knowledgebase for this variant.", # Very long text, needs wordwrap
    "UniProt (GENE): Accession Number":"UniProt web resource for the affected protein and biological functions.",
    "dbSNP: rsID":"ID number for the free dbSNP web resource listing of this variant.",
    "MDL: Sample Count":"Instance count of samples with this variant in ",
    "MDL: Variant Frequency":"",
    "MDL: Sample List":"JSON-style dictionary breakdown of tissue types present in ??? knowledgebase for this variant.", # Very long text, needs wordwrap
}

# CLASSES ------------------------------------------------

class ToolTip(object):

    def __init__(self, widget):
        ttk.set_appearance_mode("light")
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
        label = ttk.CTkLabel(
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
        self.vars['filename'] = ttk.StringVar()
        self.vars['filename'].set('No CSV File Loaded')
        self.vars['status_text'] = ttk.StringVar()
        self.vars['Disposition'] = ttk.StringVar()
        self.vars['dispo_none_count'] = ttk.IntVar()
        self.vars['dispo_low_vaf_count'] = ttk.IntVar()
        self.vars['dispo_vus_count'] = ttk.IntVar()
        self.vars['dispo_mutation_count'] = ttk.IntVar()

        self.variant = dict()
        for x in vcf_columns:
            self.variant[x] = ttk.StringVar()

        self.labels = dict()
        for x in vcf_columns:
            self.labels[x] = ttk.CTkLabel(None)
            
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

        self.big_text = ('bold', 14, 'bold')
        
        # FRAMES ------------------------------------------------------------------------

        # Base Frame
        self.frame_base = ttk.CTkFrame(self)
        self.frame_base.pack(expand=True, fill='both',ipadx=10, ipady=10)
        # Left Frame
        self.frame_left = ttk.CTkFrame(self.frame_base)
        self.frame_left.pack(side='left', expand=False, fill='y',ipadx=10, ipady=10, padx=5, pady=5)
        #File load button
        self.labels['filename'] = ttk.CTkLabel(self.frame_left, textvariable=self.vars['filename'])
        self.labels['filename'].pack(side='top', expand=False, fill='x',ipady=5, padx=5, pady=5)
        self.buttons['load_csv'] = ttk.CTkButton(self.frame_left, text="Load a CSV File", command=self.loadCSV)
        self.buttons['load_csv'].pack(side='top', expand=False, fill='x', ipady=5, padx=5, pady=5)
        # Treeview Frame
        self.frame_treeview = ttk.CTkFrame(self.frame_left)
        self.frame_treeview.pack(side='top',expand=True,fill='both', padx=5)
        # Treeview list
        self.treeview_variant_list = Treeview(self.frame_treeview, columns=vcf_columns, displaycolumns=[5,0], selectmode='browse', show='headings')
        for x in vcf_columns:
            self.treeview_variant_list.heading(x, text=x, anchor='center')
        self.treeview_variant_list.heading(5, text='Variant')
        self.treeview_variant_list.heading(0, text='Disposition')
        self.treeview_variant_list.column(column=0, width=100, anchor='center')
        self.treeview_variant_list.column(column=5, width=100, anchor='center')
        self.treeview_variant_list.pack(side='left', expand=True, fill='both')
        self.treeview_variant_list.bind('<<TreeviewSelect>>', self.item_selected)
        # Treeview Scrollbar
        self.scrollbar = Scrollbar(self.frame_treeview, orient=tk.VERTICAL, command=self.treeview_variant_list.yview)
        self.treeview_variant_list.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side='left', expand=False, fill='y')
        # Disposition Frame
        self.frame_disposition = ttk.CTkFrame(self.frame_left)
        self.frame_disposition.pack(side='top', expand=False, fill='x', padx=5)
        self.frame_dispo_1 = ttk.CTkFrame(self.frame_disposition)
        self.frame_dispo_1.pack(side='top', expand=False, fill='x')
        self.frame_dispo_2 = ttk.CTkFrame(self.frame_disposition)
        self.frame_dispo_2.pack(side='top', expand=False, fill='x')
        self.frame_dispo_3 = ttk.CTkFrame(self.frame_disposition)
        self.frame_dispo_3.pack(side='top', expand=False, fill='x')
        self.frame_dispo_4 = ttk.CTkFrame(self.frame_disposition)
        self.frame_dispo_4.pack(side='top', expand=False, fill='x')
        # Disposition labels
        self.labels['none_count'] = ttk.CTkLabel(self.frame_dispo_1, textvariable=self.vars['dispo_none_count'], width=5)
        self.labels['none_count'].pack(side='left', expand=False, fill='y', padx=5, pady=5)
        self.labels['low_vaf_count'] = ttk.CTkLabel(self.frame_dispo_2, textvariable=self.vars['dispo_low_vaf_count'], width=5)
        self.labels['low_vaf_count'].pack(side='left', expand=False, fill='y', padx=5, pady=5)
        self.labels['vus_count'] = ttk.CTkLabel(self.frame_dispo_3, textvariable=self.vars['dispo_vus_count'], width=5)
        self.labels['vus_count'].pack(side='left', expand=False, fill='y', padx=5, pady=5)
        self.labels['mutation_count'] = ttk.CTkLabel(self.frame_dispo_4, textvariable=self.vars['dispo_mutation_count'], width=5)
        self.labels['mutation_count'].pack(side='left', expand=False, fill='y', padx=5, pady=5)
        # Radio buttons for disposition
        self.radio_none = tk.Radiobutton(self.frame_dispo_1, text="None (Unassigned)", variable=self.vars['Disposition'], anchor='w', value='None')
        self.radio_none.pack(side='left', expand=False, fill='both')
        self.radio_unknown = tk.Radiobutton(self.frame_dispo_2, text="Low VAF", variable=self.vars['Disposition'], anchor='w', value='Low VAF')
        self.radio_unknown.pack(side='left', expand=False, fill='both')
        self.radio_VUS = tk.Radiobutton(self.frame_dispo_3, text="VUS", variable=self.vars['Disposition'], anchor='w', value='VUS')
        self.radio_VUS.pack(side='left', expand=False, fill='both')
        self.radio_mutation = tk.Radiobutton(self.frame_dispo_4, text="Harmful", variable=self.vars['Disposition'], anchor='w', value='Harmful')
        self.radio_mutation.pack(side='left', expand=False, fill='both')
        self.radio_none.select()
        # Process output files button
        self.buttons['save_disposition'] = ttk.CTkButton(self.frame_left, text="Save Disposition", command=self.save_disposition, state='disabled')
        self.buttons['save_disposition'].pack(side='top', expand=False, fill='x', padx=5, pady=5, ipady=5)
        # Process output files button
        # ttk.CTkButton(self.frame_left, text="Create Disposition Lists").pack(side='top', expand=False, fill='x', padx=5, pady=5, ipady=5)
        # Right Frame
        self.frame_right = ttk.CTkFrame(self.frame_base)
        self.frame_right.pack(side='left', expand=True, fill='both',ipadx=10, ipady=10)
        # Basic Info Frame
        self.frame_basic_info = ttk.CTkFrame(self.frame_right)
        self.frame_basic_info.pack(side='top', expand=False, fill='x', padx=5, pady=5)
        self.frame_basic_info_gene = ttk.CTkFrame(self.frame_basic_info)
        self.frame_basic_info_gene.pack(side='left',expand=False, fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_basic_info_gene, text="Gene").pack(side='top',expand=False,fill='x')
        self.labels["Variant Annotation: Gene"] = ttk.CTkLabel(self.frame_basic_info_gene, width=8, textvariable=self.variant["Variant Annotation: Gene"], font=('bold', 24, 'bold'))
        self.labels["Variant Annotation: Gene"].pack(side='top',expand=True,fill='both')
        self.frame_basic_info_chrom = ttk.CTkFrame(self.frame_basic_info)
        self.frame_basic_info_chrom.pack(side='left',expand=False,fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_basic_info_chrom, text="Chromosome").pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Chrom"] = ttk.CTkLabel(self.frame_basic_info_chrom, width=6, textvariable=self.variant["Original Input: Chrom"])
        self.labels["Original Input: Chrom"].pack(side='top',expand=False, fill='x')
        ttk.CTkLabel(self.frame_basic_info_chrom, text="Base Pair").pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Pos"] = ttk.CTkLabel(self.frame_basic_info_chrom, width=12, textvariable=self.variant["Original Input: Pos"])
        self.labels["Original Input: Pos"].pack(side='top',expand=False, fill='x')
        self.frame_basic_info_changes = ttk.CTkFrame(self.frame_basic_info)
        self.frame_basic_info_changes.pack(side='left',expand=False,fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_basic_info_changes, text="DNA Change (c-dot)").pack(side='top',expand=False, fill='x')
        self.labels["Variant Annotation: cDNA change"] = ttk.CTkLabel(self.frame_basic_info_changes, text="C-dot", textvariable=self.variant["Variant Annotation: cDNA change"])
        self.labels["Variant Annotation: cDNA change"].pack(side='top',expand=False, fill='x')
        ttk.CTkLabel(self.frame_basic_info_changes, text="Protein Change (p-dot)").pack(side='top',expand=False, fill='x')
        self.labels["Variant Annotation: Protein Change"] = ttk.CTkLabel(self.frame_basic_info_changes, text="P-dot", width=24, textvariable=self.variant["Variant Annotation: Protein Change"])
        self.labels["Variant Annotation: Protein Change"].pack(side='top',expand=False, fill='x')
        self.frame_basic_info_alleles = ttk.CTkFrame(self.frame_basic_info)
        self.frame_basic_info_alleles.pack(side='left',expand=True,fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_basic_info_alleles, text="Ref Allele", anchor='nw').pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Reference allele"] = ttk.CTkLabel(self.frame_basic_info_alleles, anchor='w', textvariable=self.variant["Original Input: Reference allele"])
        self.labels["Original Input: Reference allele"].pack(side='top',expand=False, fill='x')
        ttk.CTkLabel(self.frame_basic_info_alleles, text="Variant Allele", anchor='w').pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Alternate allele"] = ttk.CTkLabel(self.frame_basic_info_alleles, anchor='w', textvariable=self.variant["Original Input: Alternate allele"])
        self.labels["Original Input: Alternate allele"].pack(side='top',expand=False, fill='x')
        self.frame_basic_info_misc = ttk.CTkFrame(self.frame_basic_info)
        self.frame_basic_info_misc.pack(side='left',expand=False,fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_basic_info_misc, text="Length of Variant (BP)").pack(side='top',expand=False, fill='x')
        self.labels["VCF: LEN"] = ttk.CTkLabel(self.frame_basic_info_misc, textvariable=self.variant["VCF: LEN"])
        self.labels["VCF: LEN"].pack(side='top',expand=True, fill='both')

        # middle frame
        self.frame_middle = ttk.CTkFrame(self.frame_right)
        self.frame_middle.pack(side='top',expand=True,fill='both', padx=5, pady=5)
        # Strand Bias Frame
        self.frame_genexys = ttk.CTkFrame(self.frame_middle)
        self.frame_genexys.pack(side='left', expand=False, fill='both', padx=(0,10))
        self.frame_genexys_sb_calc = ttk.CTkFrame(self.frame_genexys)
        self.frame_genexys_sb_calc.pack(side='top', expand=False, fill='both', padx=5, pady=5)
        self.frame_genexys_sb_calc.rowconfigure(0, weight=1)
        self.frame_genexys_sb_calc.rowconfigure(1, weight=1)
        self.frame_genexys_sb_calc.columnconfigure(0, weight=0)
        self.frame_genexys_sb_calc.columnconfigure(1, weight=5)
        self.frame_genexys_sb_calc.columnconfigure(2, weight=0)
        self.frame_genexys_sb_calc.columnconfigure(3, weight=1)
        ttk.CTkLabel(self.frame_genexys_sb_calc, text="SB (reported)", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["VCF: STB"] = ttk.CTkLabel(self.frame_genexys_sb_calc, textvariable=self.variant["VCF: STB"])
        self.labels["VCF: STB"].grid(column=1, row=0, sticky='news')
        ttk.CTkLabel(self.frame_genexys_sb_calc, text="p.", anchor='e').grid(column=2, row=0, sticky='news', padx=5)
        self.labels["VCF: STBP"] = ttk.CTkLabel(self.frame_genexys_sb_calc, textvariable=self.variant["VCF: STBP"], width=5)
        self.labels["VCF: STBP"].grid(column=3, row=0, sticky='news')
        # Genexys strand Bias Area
        self.frame_sb_GX = ttk.CTkFrame(self.frame_genexys)
        self.frame_sb_GX.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frame_sb_GX.rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frame_sb_GX.columnconfigure(x, weight=1)
        ttk.CTkLabel(self.frame_sb_GX, text='Genexys', width=8, font=self.big_text).grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        ttk.CTkLabel(self.frame_sb_GX, text='Fwd').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.CTkLabel(self.frame_sb_GX, text='Rev').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.CTkLabel(self.frame_sb_GX, text='Ref', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_GX, text='Var', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSRF'] = ttk.CTkLabel(self.frame_sb_GX, textvariable=self.variant["VCF: FSRF"])
        self.labels['VCF: FSRF'].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSRR'] = ttk.CTkLabel(self.frame_sb_GX, textvariable=self.variant["VCF: FSRR"])
        self.labels['VCF: FSRR'].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSAF'] = ttk.CTkLabel(self.frame_sb_GX, textvariable=self.variant["VCF: FSAF"])
        self.labels['VCF: FSAF'].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSAR'] = ttk.CTkLabel(self.frame_sb_GX, textvariable=self.variant["VCF: FSAR"])
        self.labels['VCF: FSAR'].grid(column=3, row=2, sticky='news', pady=5, padx=5)
        # Separator
        # ttk.Separator(self.frame_sb_GX, orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frame_sb_GX_results = ttk.CTkFrame(self.frame_sb_GX)
        self.frame_sb_GX_results.grid(column=0, row=5, columnspan=4, sticky='news')
        self.frame_sb_GX_results.rowconfigure(0, weight=1)
        self.frame_sb_GX_results.rowconfigure(1, weight=1)
        self.frame_sb_GX_results.columnconfigure(0, weight=0)
        self.frame_sb_GX_results.columnconfigure(1, weight=5)
        self.frame_sb_GX_results.columnconfigure(2, weight=0)
        self.frame_sb_GX_results.columnconfigure(3, weight=1)
        # Genexys Stats Area
        ttk.CTkLabel(self.frame_sb_GX_results, text="Binom. Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["VCF: Binom Proportion"] = ttk.CTkLabel(self.frame_sb_GX_results, textvariable=self.variant["VCF: Binom Proportion"], anchor='center')
        self.labels["VCF: Binom Proportion"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_GX_results, text="p.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["VCF: Binom P Value"] = ttk.CTkLabel(self.frame_sb_GX_results, textvariable=self.variant["VCF: Binom P Value"], anchor='center', width=5)
        self.labels["VCF: Binom P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_GX_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["VCF: Fisher Odds Ratio"] = ttk.CTkLabel(self.frame_sb_GX_results, textvariable=self.variant["VCF: Fisher Odds Ratio"], anchor='center')
        self.labels["VCF: Fisher Odds Ratio"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_GX_results, text="p.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["VCF: Fisher P Value"] = ttk.CTkLabel(self.frame_sb_GX_results, textvariable=self.variant["VCF: Fisher P Value"], anchor='center', width=5)
        self.labels["VCF: Fisher P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        # Q20 Read Bias Area
        self.frame_sb_Q20 = ttk.CTkFrame(self.frame_genexys)
        self.frame_sb_Q20.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frame_sb_Q20.rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frame_sb_Q20.columnconfigure(x, weight=1)
        ttk.CTkLabel(self.frame_sb_Q20, text='Q20', width=8, font=self.big_text).grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        ttk.CTkLabel(self.frame_sb_Q20, text='Fwd').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.CTkLabel(self.frame_sb_Q20, text='Rev').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.CTkLabel(self.frame_sb_Q20, text='Ref', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_Q20, text='Var', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Variant Forward Read Depth"] = ttk.CTkLabel(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Variant Forward Read Depth"])
        self.labels["Mpileup Qual: Filtered Variant Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Variant Reverse Read Depth"] = ttk.CTkLabel(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Variant Reverse Read Depth"])
        self.labels["Mpileup Qual: Filtered Variant Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Reference Forward Read Depth"] = ttk.CTkLabel(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Reference Forward Read Depth"])
        self.labels["Mpileup Qual: Filtered Reference Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Reference Reverse Read Depth"] = ttk.CTkLabel(self.frame_sb_Q20, textvariable=self.variant["Mpileup Qual: Filtered Reference Reverse Read Depth"])
        self.labels["Mpileup Qual: Filtered Reference Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)
        # Separator
        # ttk.Separator(self.frame_sb_Q20, orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frame_sb_Q20_results = ttk.CTkFrame(self.frame_sb_Q20)
        self.frame_sb_Q20_results.grid(column=0, row=5, columnspan=4, sticky='news')
        self.frame_sb_Q20_results.rowconfigure(0, weight=1)
        self.frame_sb_Q20_results.rowconfigure(1, weight=1)
        self.frame_sb_Q20_results.columnconfigure(0, weight=0)
        self.frame_sb_Q20_results.columnconfigure(1, weight=5)
        self.frame_sb_Q20_results.columnconfigure(2, weight=0)
        self.frame_sb_Q20_results.columnconfigure(3, weight=1)
        # Q20 Stats Area
        ttk.CTkLabel(self.frame_sb_Q20_results, text="Binom. Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["Mpileup Qual: Filtered Variant Binomial Proportion"] = ttk.CTkLabel(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial Proportion"], anchor='center')
        self.labels["Mpileup Qual: Filtered Variant Binomial Proportion"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_Q20_results, text="p.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["Mpileup Qual: Filtered Variant Binomial P Value"] = ttk.CTkLabel(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial P Value"], anchor='center', width=5)
        self.labels["Mpileup Qual: Filtered Variant Binomial P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_Q20_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["Mpileup Qual: Filtered Variant Fishers Odds Ratio"] = ttk.CTkLabel(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers Odds Ratio"], anchor='center')
        self.labels["Mpileup Qual: Filtered Variant Fishers Odds Ratio"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_Q20_results, text="p.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["Mpileup Qual: Filtered Variant Fishers P Value"] = ttk.CTkLabel(self.frame_sb_Q20_results, textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers P Value"], anchor='center', width=5)
        self.labels["Mpileup Qual: Filtered Variant Fishers P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        # Q1 Read Bias Area
        self.frame_sb_Q1 = ttk.CTkFrame(self.frame_genexys)
        self.frame_sb_Q1.pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frame_sb_Q1.rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frame_sb_Q1.columnconfigure(x, weight=1)
        ttk.CTkLabel(self.frame_sb_Q1, text='Q1', width=8, font=self.big_text).grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        ttk.CTkLabel(self.frame_sb_Q1, text='Fwd').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.CTkLabel(self.frame_sb_Q1, text='Rev').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        ttk.CTkLabel(self.frame_sb_Q1, text='Ref', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_Q1, text='Var', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Reference Forward Read Depth"] = ttk.CTkLabel(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Reference Forward Read Depth"])
        self.labels["Mpileup Qual: Unfiltered Reference Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Reference Reverse Read Depth"] = ttk.CTkLabel(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Reference Reverse Read Depth"])
        self.labels["Mpileup Qual: Unfiltered Reference Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Forward Read Depth"] = ttk.CTkLabel(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Forward Read Depth"])
        self.labels["Mpileup Qual: Unfiltered Variant Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Reverse Read Depth"] = ttk.CTkLabel(self.frame_sb_Q1, width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Reverse Read Depth"])
        self.labels["Mpileup Qual: Unfiltered Variant Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        # Separator
        # ttk.Separator(self.frame_sb_Q1, orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frame_sb_Q1_results = ttk.CTkFrame(self.frame_sb_Q1)
        self.frame_sb_Q1_results.grid(column=0, row=5, columnspan=4, sticky='news')
        self.frame_sb_Q1_results.rowconfigure(0, weight=1)
        self.frame_sb_Q1_results.rowconfigure(1, weight=1)
        self.frame_sb_Q1_results.columnconfigure(0, weight=0)
        self.frame_sb_Q1_results.columnconfigure(1, weight=5)
        self.frame_sb_Q1_results.columnconfigure(2, weight=0)
        self.frame_sb_Q1_results.columnconfigure(3, weight=1)
        # Q1 Stats Area
        ttk.CTkLabel(self.frame_sb_Q1_results, text="Binom. Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Binomial Proportion"] = ttk.CTkLabel(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial Proportion"], anchor='center')
        self.labels["Mpileup Qual: Unfiltered Variant Binomial Proportion"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_Q1_results, text="p.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["Mpileup Qual: Unfiltered Variant Binomial P Value"] = ttk.CTkLabel(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial P Value"], anchor='center', width=5)
        self.labels["Mpileup Qual: Unfiltered Variant Binomial P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_Q1_results, text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"] = ttk.CTkLabel(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"], anchor='center')
        self.labels["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        ttk.CTkLabel(self.frame_sb_Q1_results, text="p.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["Mpileup Qual: Unfiltered Variant Fishers P Value"] = ttk.CTkLabel(self.frame_sb_Q1_results, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers P Value"], anchor='center', width=5)
        self.labels["Mpileup Qual: Unfiltered Variant Fishers P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)

        # Genexys info frame
        self.frame_gx_info = ttk.CTkFrame(self.frame_middle)
        self.frame_gx_info.pack(side='top', expand=False, fill='both', pady=(0,5))
        for x in range(1,5,2):
            self.frame_gx_info.rowconfigure(x, weight=1)
        for x in range(5):
            self.frame_gx_info.columnconfigure(x, weight=1)
        # gx info top area
        ttk.CTkLabel(self.frame_gx_info, text="Allele Fraction").grid(row=0, column=0, sticky='news', padx=5)
        self.labels["VCF: AF"] = ttk.CTkLabel(self.frame_gx_info, textvariable=self.variant["VCF: AF"])
        self.labels["VCF: AF"].grid(row=1, column=0, sticky='news', padx=5, pady=5)
        ttk.CTkLabel(self.frame_gx_info, text="Variant Type").grid(row=0, column=1, sticky='news', padx=5)
        self.labels["VCF: TYPE"] = ttk.CTkLabel(self.frame_gx_info, textvariable=self.variant["VCF: TYPE"])
        self.labels["VCF: TYPE"].grid(row=1, column=1, sticky='news', padx=5, pady=5)
        ttk.CTkLabel(self.frame_gx_info, text="Genotype").grid(row=0, column=2, sticky='news', padx=5)
        self.labels["VCF: Genotype"] = ttk.CTkLabel(self.frame_gx_info, textvariable=self.variant["VCF: Genotype"])
        self.labels["VCF: Genotype"].grid(row=1, column=2, sticky='news', padx=5, pady=5)
        ttk.CTkLabel(self.frame_gx_info, text="Filter (Genexys)").grid(row=0, column=3, sticky='news', padx=5)
        self.labels["VCF: Filter"] = ttk.CTkLabel(self.frame_gx_info, textvariable=self.variant["VCF: Filter"])
        self.labels["VCF: Filter"].grid(row=1, column=3, sticky='news', padx=5, pady=5)
        ttk.CTkLabel(self.frame_gx_info, text="Quality Score").grid(row=0, column=4, sticky='news', padx=5)
        self.labels["VCF: QUAL"] = ttk.CTkLabel(self.frame_gx_info, textvariable=self.variant["VCF: QUAL"])
        self.labels["VCF: QUAL"].grid(row=1, column=4, sticky='news', padx=5, pady=5)
        # Separator
        # ttk.Separator(self.frame_gx_info, orient='horizontal').grid(row=2, column=0, columnspan=5, sticky='news')
        # gx info bottom area
        ttk.CTkLabel(self.frame_gx_info, text="FAO").grid(row=3, column=0, sticky='news', padx=5)
        self.labels["VCF: FAO"] = ttk.CTkLabel(self.frame_gx_info, textvariable=self.variant["VCF: FAO"])
        self.labels["VCF: FAO"].grid(row=4, column=0, sticky='news', padx=5, pady=5)
        ttk.CTkLabel(self.frame_gx_info, text="FDP").grid(row=3, column=1, sticky='news', padx=5)
        self.labels["VCF: FDP"] = ttk.CTkLabel(self.frame_gx_info, textvariable=self.variant["VCF: FDP"])
        self.labels["VCF: FDP"].grid(row=4, column=1, sticky='news', padx=5, pady=5)
        ttk.CTkLabel(self.frame_gx_info, text="HRUN").grid(row=3, column=2, sticky='news', padx=5)
        self.labels["VCF: HRUN"] = ttk.CTkLabel(self.frame_gx_info, textvariable=self.variant["VCF: HRUN"])
        self.labels["VCF: HRUN"].grid(row=4, column=2, sticky='news', padx=5, pady=5)
        ttk.CTkLabel(self.frame_gx_info, text="QD").grid(row=3, column=3, sticky='news', padx=5)
        self.labels["VCF: QD"] = ttk.CTkLabel(self.frame_gx_info, textvariable=self.variant["VCF: QD"])
        self.labels["VCF: QD"].grid(row=4, column=3, sticky='news', padx=5, pady=5)
        ttk.CTkLabel(self.frame_gx_info, text="SVTYPE (Unused)").grid(row=3, column=4, sticky='news', padx=5)
        self.labels["VCF: SVTYPE"] = ttk.CTkLabel(self.frame_gx_info, textvariable=self.variant["VCF: SVTYPE"])
        self.labels["VCF: SVTYPE"].grid(row=4, column=4, sticky='news', padx=5, pady=5)

        # mpileup info frame
        self.frame_mpl_info = ttk.CTkFrame(self.frame_middle)
        self.frame_mpl_info.pack(side='top', expand=False, fill='both', pady=5)
        self.frame_mpl_info_RD = ttk.CTkFrame(self.frame_mpl_info)
        self.frame_mpl_info_RD.pack(side='left', expand=True, fill='both', pady=5, padx=5)
        ttk.CTkLabel(self.frame_mpl_info_RD, text="Total Read Depth").pack(side='left', expand=False, fill='both')
        self.labels["Mpileup Qual: Read Depth"] = ttk.CTkLabel(self.frame_mpl_info_RD, textvariable=self.variant["Mpileup Qual: Read Depth"])
        self.labels["Mpileup Qual: Read Depth"].pack(side='left', expand=True, fill='both', pady=5, padx=5)
        self.frame_mpl_info_starts = ttk.CTkFrame(self.frame_mpl_info)
        self.frame_mpl_info_starts.pack(side='left', expand=True, fill='both', pady=5, padx=5)
        ttk.CTkLabel(self.frame_mpl_info_starts, text="Count: Read Starts").pack(side='left', expand=False, fill='both', pady=5, padx=5)
        self.labels["Mpileup Qual: Start Reads"] = ttk.CTkLabel(self.frame_mpl_info_starts, textvariable=self.variant["Mpileup Qual: Start Reads"])
        self.labels["Mpileup Qual: Start Reads"].pack(side='left', expand=True, fill='both', pady=5, padx=5)
        self.frame_mpl_info_ends = ttk.CTkFrame(self.frame_mpl_info)
        self.frame_mpl_info_ends.pack(side='left', expand=True, fill='both', pady=5, padx=5)
        ttk.CTkLabel(self.frame_mpl_info_ends, text="Count: Read Ends").pack(side='left', expand=False, fill='both', pady=5, padx=5)
        self.labels["Mpileup Qual: Stop Reads"] = ttk.CTkLabel(self.frame_mpl_info_ends, textvariable=self.variant["Mpileup Qual: Stop Reads"])
        self.labels["Mpileup Qual: Stop Reads"].pack(side='left', expand=True, fill='both', pady=5, padx=5)

        # MPL Info Frame
        self.frame_other = ttk.CTkFrame(self.frame_middle)
        self.frame_other.pack(side='top',expand=True, fill='both')
        self.frame_var_annot = ttk.CTkFrame(self.frame_other)
        self.frame_var_annot.pack(side='left',expand=True, fill='both', padx=(0,5))
        for x in range(3):
            self.frame_var_annot.columnconfigure(x, weight=1)
        self.frame_var_annot.rowconfigure(3, weight=99)
        ttk.CTkLabel(self.frame_var_annot, text="Coding Region").grid(column=0, row=0, sticky='news', padx=5)
        self.labels["Variant Annotation: Coding"] = ttk.CTkLabel(self.frame_var_annot, textvariable=self.variant["Variant Annotation: Coding"])
        self.labels["Variant Annotation: Coding"].grid(column=0, row=1, sticky='news', padx=5)
        ttk.CTkLabel(self.frame_var_annot, text="Variant Type (Seq. Ontology)").grid(column=1, row=0, sticky='news', padx=5)
        self.labels["Variant Annotation: Sequence"] = ttk.CTkLabel(self.frame_var_annot, textvariable=self.variant["Variant Annotation: Sequence Ontology"])
        self.labels["Variant Annotation: Sequence"].grid(column=1, row=1, sticky='news', padx=5)
        ttk.CTkLabel(self.frame_var_annot, text="Transcript").grid(column=2, row=0, sticky='news', padx=5)
        self.labels["Variant Annotation: Transcript"] = ttk.CTkLabel(self.frame_var_annot, textvariable=self.variant["Variant Annotation: Transcript"])
        self.labels["Variant Annotation: Transcript"].grid(column=2, row=1, sticky='news', padx=5)
        ttk.CTkLabel(self.frame_var_annot, text="All Mappings").grid(column=0, row=2, columnspan=3, sticky='news', padx=5)
        self.labels["Variant Annotation: All Mappings"] = ttk.CTkLabel(self.frame_var_annot, textvariable=self.variant["Variant Annotation: All Mappings"], wraplength=500)
        self.labels["Variant Annotation: All Mappings"].grid(column=0, columnspan=3, row=3, sticky='news', padx=5, pady=(0,5))

        # MDL Info area
        self.frame_mdl = ttk.CTkFrame(self.frame_other)
        self.frame_mdl.pack(side='left',expand=True, fill='both', padx=(5,0))
        self.frame_mdl.rowconfigure(3, weight=99)
        self.frame_mdl.columnconfigure(0, weight=1)
        self.frame_mdl.columnconfigure(1, weight=1)
        ttk.CTkLabel(self.frame_mdl, text="Sample Count").grid(column=0, row=0, sticky='news', padx=5)
        self.labels["MDL: Sample Count"] = ttk.CTkLabel(self.frame_mdl, textvariable=self.variant["MDL: Sample Count"])
        self.labels["MDL: Sample Count"].grid(column=0, row=1, sticky='news', padx=5)
        ttk.CTkLabel(self.frame_mdl, text="Variant Frequency").grid(column=1, row=0, sticky='news', padx=5)
        self.labels["MDL: Variant Frequency"]  = ttk.CTkLabel(self.frame_mdl, textvariable=self.variant["MDL: Variant Frequency"])
        self.labels["MDL: Variant Frequency"].grid(column=1, row=1, sticky='news', padx=5)
        ttk.CTkLabel(self.frame_mdl, text="Sample List").grid(column=0, columnspan=2, row=2, sticky='news', padx=5)
        self.labels["MDL: Sample List"] = ttk.CTkLabel(self.frame_mdl, textvariable=self.variant["MDL: Sample List"], wraplength=500)
        self.labels["MDL: Sample List"].grid(column=0, columnspan=2, row=3, sticky='news', padx=5, pady=(0,5))

        # Web Resources Stats
        self.frame_bottom = ttk.CTkFrame(self.frame_right)
        self.frame_bottom.pack(side='bottom', expand=False, fill='both', padx=5, pady=5)
        self.frame_bottom.columnconfigure(0, weight=1)
        self.frame_bottom.columnconfigure(1, weight=1)
        self.frame_bottom_l = ttk.CTkFrame(self.frame_bottom)
        self.frame_bottom_l.grid(column=0, row=0, sticky='news')
        self.frame_bottom_2 = ttk.CTkFrame(self.frame_bottom)
        self.frame_bottom_2.grid(column=1, row=0, sticky='news')
        # COSMIC Tissue Variant Count Region
        self.labels["COSMIC: Variant Count (Tissue)"] = ttk.CTkLabel(self.frame_bottom_l, textvariable=self.variant["COSMIC: Variant Count (Tissue)"], wraplength=600)
        self.labels["COSMIC: Variant Count (Tissue)"].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        # COSMIC Area
        self.frame_web_cosmic = ttk.CTkFrame(self.frame_bottom_2)
        self.frame_web_cosmic.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_web_cosmic, text="ID", anchor='center').pack(side='top', expand=False, fill='x', padx=5)
        self.labels["COSMIC: ID"] = ttk.CTkLabel(self.frame_web_cosmic, textvariable=self.variant["COSMIC: ID"], width=12)
        self.labels["COSMIC: ID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_web_cosmic, text="Count").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["COSMIC: Variant Count"] = ttk.CTkLabel(self.frame_web_cosmic, textvariable=self.variant["COSMIC: Variant Count"])
        self.labels["COSMIC: Variant Count"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # Clinvar Area
        self.frame_web_clinvar = ttk.CTkFrame(self.frame_bottom_2)
        self.frame_web_clinvar.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_web_clinvar, text="ID").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["ClinVar: ClinVar ID"] = ttk.CTkLabel(self.frame_web_clinvar, textvariable=self.variant["ClinVar: ClinVar ID"])
        self.labels["ClinVar: ClinVar ID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_web_clinvar, text="Significance").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["ClinVar: Clinical Significance"] = ttk.CTkLabel(self.frame_web_clinvar, textvariable=self.variant["ClinVar: Clinical Significance"])
        self.labels["ClinVar: Clinical Significance"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # Gnomad Area
        self.frame_web_gnomad = ttk.CTkFrame(self.frame_bottom_2)
        self.frame_web_gnomad.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_web_gnomad, text="Global AF").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["gnomAD3: Global AF"] = ttk.CTkLabel(self.frame_web_gnomad, textvariable=self.variant["gnomAD3: Global AF"])
        self.labels["gnomAD3: Global AF"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # CADD Area
        self.frame_web_cadd = ttk.CTkFrame(self.frame_bottom_2)
        self.frame_web_cadd.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_web_cadd, text="Phred Score").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["CADD: Phred"] = ttk.CTkLabel(self.frame_web_cadd, textvariable=self.variant["CADD: Phred"])
        self.labels["CADD: Phred"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # PolyPhen Area
        self.frame_web_polyphen = ttk.CTkFrame(self.frame_bottom_2)
        self.frame_web_polyphen.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_web_polyphen, text="HDIV").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["PolyPhen-2: HDIV Prediction"] = ttk.CTkLabel(self.frame_web_polyphen, textvariable=self.variant["PolyPhen-2: HDIV Prediction"])
        self.labels["PolyPhen-2: HDIV Prediction"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # SIFT Area
        self.frame_web_sift = ttk.CTkFrame(self.frame_bottom_2)
        self.frame_web_sift.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_web_sift, text="Prediction").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["SIFT: Prediction"] = ttk.CTkLabel(self.frame_web_sift, textvariable=self.variant["SIFT: Prediction"])
        self.labels["SIFT: Prediction"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # dbSNP Area
        self.frame_web_dbsnp = ttk.CTkFrame(self.frame_bottom_2)
        self.frame_web_dbsnp.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_web_dbsnp, text="rsID").pack(side='top', expand=False, fill='both', padx=5)
        self.labels["dbSNP: rsID"] = ttk.CTkLabel(self.frame_web_dbsnp, textvariable=self.variant["dbSNP: rsID"])
        self.labels["dbSNP: rsID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        # UniProt Area
        self.frame_web_dbsnp = ttk.CTkFrame(self.frame_bottom_2)
        self.frame_web_dbsnp.pack(side='left', expand=True, fill='both', padx=5, pady=5)
        ttk.CTkLabel(self.frame_web_dbsnp, text="Accession Number").pack(side='top', expand=False, fill='both', padx=5)
        self.labels["UniProt (GENE): Accession Number"] = ttk.CTkLabel(self.frame_web_dbsnp, textvariable=self.variant["UniProt (GENE): Accession Number"])
        self.labels["UniProt (GENE): Accession Number"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        
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
        
        item_list = self.treeview_variant_list.get_children(item=None)

        self.vars['dispo_none_count'].set(0)
        self.vars['dispo_low_vaf_count'].set(0)
        self.vars['dispo_vus_count'].set(0)
        self.vars['dispo_mutation_count'].set(0)

        none_count = 0
        low_vaf = 0
        vus_count = 0
        mutation_count = 0

        for x in item_list:
            dispo = self.treeview_variant_list.set(x, column='Disposition')

            if dispo == 'Harmful':
                mutation_count += 1
            elif dispo == 'Low VAF':
                low_vaf += 1
            elif dispo == 'VUS':
                vus_count += 1
            else:
                none_count += 1

        self.vars['dispo_none_count'].set(none_count)
        self.vars['dispo_low_vaf_count'].set(low_vaf)
        self.vars['dispo_vus_count'].set(vus_count)
        self.vars['dispo_mutation_count'].set(mutation_count)

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
