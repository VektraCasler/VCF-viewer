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
        self.frame_left.columnconfigure(0, weight=5)
        self.frame_left.columnconfigure(1, weight=1)
        self.frame_left.rowconfigure(0, weight=1)
        self.frame_left.rowconfigure(1, weight=1)
        self.frame_left.rowconfigure(2, weight=99)

        # Left Frame widgets
        self.load_button = tk.Button(self.frame_left, text="Load a CSV File", command=self.loadCSV)
        self.load_button.grid(column=0, row=0, columnspan=2, sticky='news', padx=5, pady=5)
        self.filename_entry = tk.Label(self.frame_left, textvariable=self.filename, relief='sunken')
        self.filename_entry.grid(column=0, row=1, columnspan=2, sticky='news', padx=5, pady=5)

        # Treeview
        self.variant_tree = ttk.Treeview(self.frame_left, columns=vcf_columns, displaycolumns=[4], selectmode='browse', show='headings')
        for x in vcf_columns:
            self.variant_tree.heading(x, text=x, anchor='center')
        self.variant_tree.heading(4, text='Variant')
        self.variant_tree.grid(column=0, row=2, columnspan=1, sticky='nsew', padx=(5,0), pady=5)
        self.variant_tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Treeview Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_left, orient=tk.VERTICAL, command=self.variant_tree.yview)
        self.variant_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky='nse', padx=(0,5), pady=5)

        self.frame_left.grid(column=0, row=0, sticky='wens', ipadx=5, ipady=5)

        # Right Frame------------------------------------------------
        self.frame_right = tk.Frame(self.base_frame, bg='darkgray')
        self.frame_right.columnconfigure(0, weight=1)
        self.frame_right.columnconfigure(1, weight=1)
        self.frame_right.rowconfigure(0,weight=0)
        self.frame_right.rowconfigure(1,weight=1)
        self.frame_right.rowconfigure(2,weight=1)

        self.frame_right.grid(column=1, row=0, sticky='nsew', ipadx=5, ipady=5)

        # Basic Info Frame-------------------------------------------
        self.BI_frame = tk.LabelFrame(self.frame_right, text='Locus Info', padx=5, pady=5)
        self.BI_frame.columnconfigure(0, weight=1)
        self.BI_frame.columnconfigure(1, weight=1)
        self.BI_frame.columnconfigure(2, weight=3)
        self.BI_frame.columnconfigure(3, weight=0)
        self.BI_frame.columnconfigure(4, weight=3)
        self.BI_frame.rowconfigure(0, weight=1)
        self.BI_frame.rowconfigure(1, weight=1)
        self.BI_frame.rowconfigure(2, weight=1)
        self.BI_frame.rowconfigure(3, weight=1)

        tk.Label(self.BI_frame, text="Gene").grid(column=0, row=0, rowspan=1,sticky='news')
        tk.Label(self.BI_frame, width=6, textvariable=self.variant_info["Variant Annotation: Gene"], relief='raised', font=('bold', 24, 'bold')).grid(column=0, row=1, rowspan=3,sticky='news')
        tk.Label(self.BI_frame, text="Chromosome").grid(column=1, row=0, sticky='news')
        tk.Label(self.BI_frame, textvariable=self.variant_info["Original Input: Chrom"]).grid(column=1, row=1, sticky='news')
        tk.Label(self.BI_frame, text="Base Pair").grid(column=1, row=2, sticky='news')
        tk.Label(self.BI_frame, textvariable=self.variant_info["Original Input: Pos"]).grid(column=1, row=3, sticky='news')
        tk.Label(self.BI_frame, text="Ref Allele").grid(column=2, row=2, sticky='news')
        tk.Label(self.BI_frame, textvariable=self.variant_info["Original Input: Reference allele"]).grid(column=2, row=3, sticky='news')
        tk.Label(self.BI_frame, text="-->", fg='red').grid(column=3, row=3, sticky='news')
        tk.Label(self.BI_frame, text="Variant Allele").grid(column=4, row=2, sticky='news')
        tk.Label(self.BI_frame, textvariable=self.variant_info["Original Input: Alternate allele"]).grid(column=4, row=3, sticky='news')
        tk.Label(self.BI_frame, text="DNA Change (c-dot)").grid(column=2, row=0, sticky='news')
        tk.Label(self.BI_frame, text="C-dot", textvariable=self.variant_info["Variant Annotation: cDNA change"]).grid(column=2, row=1, sticky='news')
        tk.Label(self.BI_frame, text="Protein Change (p-dot)").grid(column=4, row=0, sticky='news')
        tk.Label(self.BI_frame, text="P-dot", textvariable=self.variant_info["Variant Annotation: Protein Change"]).grid(column=4, row=1, sticky='news')

        self.BI_frame.grid(column=0, row=0, columnspan=2, sticky='news')

        # VCF Info Frame------------------------------------------------
        self.VCF_frame = tk.LabelFrame(self.frame_right, text='VCF Data')

        tk.Label(self.VCF_frame, text="AF").grid(column=0, row=0, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: AF"]).grid(column=1, row=0, sticky='news')
        tk.Label(self.VCF_frame, text="FAO").grid(column=0, row=1, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: FAO"]).grid(column=1, row=1, sticky='news')
        tk.Label(self.VCF_frame, text="FDP").grid(column=0, row=2, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: FDP"]).grid(column=1, row=2, sticky='news')
        tk.Label(self.VCF_frame, text="HRUN").grid(column=0, row=3, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: HRUN"]).grid(column=1, row=3, sticky='news')
        tk.Label(self.VCF_frame, text="Filter").grid(column=0, row=4, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: Filter"]).grid(column=1, row=4, sticky='news')
        tk.Label(self.VCF_frame, text="Genotype").grid(column=0, row=5, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: Genotype"]).grid(column=1, row=5, sticky='news')
        tk.Label(self.VCF_frame, text="FSAF").grid(column=0, row=6, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: FSAF"]).grid(column=1, row=6, sticky='news')
        tk.Label(self.VCF_frame, text="FSAR").grid(column=0, row=7, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: FSAR"]).grid(column=1, row=7, sticky='news')
        tk.Label(self.VCF_frame, text="FSRF").grid(column=0, row=8, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: FSRF"]).grid(column=1, row=8, sticky='news')
        tk.Label(self.VCF_frame, text="FSRR").grid(column=0, row=9, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: FSRR"]).grid(column=1, row=9, sticky='news')
        tk.Label(self.VCF_frame, text="Fisher Odds Ratio").grid(column=0, row=10, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: Fisher Odds Ratio"]).grid(column=1, row=10, sticky='news')
        tk.Label(self.VCF_frame, text="Fisher P Value").grid(column=0, row=11, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: Fisher P Value"]).grid(column=1, row=11, sticky='news')
        tk.Label(self.VCF_frame, text="Binom Proportion").grid(column=0, row=12, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: Binom Proportion"]).grid(column=1, row=12, sticky='news')
        tk.Label(self.VCF_frame, text="Binom P Value").grid(column=0, row=13, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: Binom P Value"]).grid(column=1, row=13, sticky='news')
        tk.Label(self.VCF_frame, text="LEN").grid(column=0, row=14, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: LEN"]).grid(column=1, row=14, sticky='news')
        tk.Label(self.VCF_frame, text="QD").grid(column=0, row=15, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: QD"]).grid(column=1, row=15, sticky='news')
        tk.Label(self.VCF_frame, text="STB").grid(column=0, row=16, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: STB"]).grid(column=1, row=16, sticky='news')
        tk.Label(self.VCF_frame, text="STBP").grid(column=0, row=17, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: STBP"]).grid(column=1, row=17, sticky='news')
        tk.Label(self.VCF_frame, text="SVTYPE").grid(column=0, row=18, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: SVTYPE"]).grid(column=1, row=18, sticky='news')
        tk.Label(self.VCF_frame, text="TYPE").grid(column=0, row=19, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: TYPE"]).grid(column=1, row=19, sticky='news')
        tk.Label(self.VCF_frame, text="QUAL").grid(column=0, row=20, sticky='news')
        tk.Label(self.VCF_frame, textvariable=self.variant_info["VCF: QUAL"]).grid(column=1, row=20, sticky='news')

        self.VCF_frame.grid(column=0, row=1, padx=5, pady=5, sticky='news')

        # MPL Info Frame------------------------------------------------
        self.MPL_frame = tk.LabelFrame(self.frame_right, text='MPL Data')

        tk.Label(self.MPL_frame, text="Read Depth").grid(column=0, row=0, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Read Depth"]).grid(column=1, row=0, sticky='news')
        tk.Label(self.MPL_frame, text="Read Starts").grid(column=0, row=1, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Start Reads"]).grid(column=1, row=1, sticky='news')
        tk.Label(self.MPL_frame, text="Read Ends").grid(column=0, row=2, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Stop Reads"]).grid(column=1, row=2, sticky='news')
        tk.Label(self.MPL_frame, text="Q20 Ref Fwd RD").grid(column=0, row=3, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Reference Forward Read Depth"]).grid(column=1, row=3, sticky='news')
        tk.Label(self.MPL_frame, text="Q20 Ref Rev RD").grid(column=0, row=4, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Reference Reverse Read Depth"]).grid(column=1, row=4, sticky='news')
        tk.Label(self.MPL_frame, text="Q1 Ref Fwd RD").grid(column=0, row=5, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Reference Forward Read Depth"]).grid(column=1, row=5, sticky='news')
        tk.Label(self.MPL_frame, text="Q1 Ref Rev RD").grid(column=0, row=6, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Reference Reverse Read Depth"]).grid(column=1, row=6, sticky='news')
        tk.Label(self.MPL_frame, text="Q20 Var Fwd RD").grid(column=0, row=7, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Forward Read Depth"]).grid(column=1, row=7, sticky='news')
        tk.Label(self.MPL_frame, text="Q20 Var Rev RD").grid(column=0, row=8, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Reverse Read Depth"]).grid(column=1, row=8, sticky='news')
        tk.Label(self.MPL_frame, text="Q20 Var Binom Prop").grid(column=0, row=9, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Binomial Proportion"]).grid(column=1, row=9, sticky='news')
        tk.Label(self.MPL_frame, text="Q20 Var Binom P-val").grid(column=0, row=10, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Binomial P Value"]).grid(column=1, row=10, sticky='news')
        tk.Label(self.MPL_frame, text="Q20 Var Fishers OR").grid(column=0, row=11, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Fishers Odds Ratio"]).grid(column=1, row=11, sticky='news')
        tk.Label(self.MPL_frame, text="Q20 Var Fishers P-val").grid(column=0, row=12, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Filtered Variant Fishers P Value"]).grid(column=1, row=12, sticky='news')
        tk.Label(self.MPL_frame, text="Q1 Var Fwd RD").grid(column=0, row=13, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Forward Read Depth"]).grid(column=1, row=13, sticky='news')
        tk.Label(self.MPL_frame, text="Q1 Var Rev RD").grid(column=0, row=14, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Reverse Read Depth"]).grid(column=1, row=14, sticky='news')
        tk.Label(self.MPL_frame, text="Q1 Var Binom Prop").grid(column=0, row=15, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Binomial Proportion"]).grid(column=1, row=15, sticky='news')
        tk.Label(self.MPL_frame, text="Q1 Var Binom P-val").grid(column=0, row=16, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Binomial P Value"]).grid(column=1, row=16, sticky='news')
        tk.Label(self.MPL_frame, text="Q1 Var Fishers OR").grid(column=0, row=17, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"]).grid(column=1, row=17, sticky='news')
        tk.Label(self.MPL_frame, text="Q1 Var Fishers P-val").grid(column=0, row=18, sticky='news')
        tk.Label(self.MPL_frame, textvariable=self.variant_info["Mpileup Qual: Unfiltered Variant Fishers P Value"]).grid(column=1, row=18, sticky='news')

        self.MPL_frame.grid(column=1, row=1, padx=5, pady=5, sticky='news')

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




# MAIN LOOP ----------------------------------------------

def main():

    # Mainloop
    root = App()
    root.mainloop()    

    return

if __name__ == '__main__':
    main()
