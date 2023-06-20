# vcf_data_viewer/view.py
''' The view of the VCF Data Viewer application, comprised of the tkinter portion. '''

# IMPORTS ------------------------------------------------

import ttkbootstrap as tk
from ttkbootstrap import tableview as tbv
from tkinter import Widget
from tkinter import filedialog as fd
from tkinter.constants import RIGHT, LEFT
from .global_variables import *
from .tool_tip import ToolTip, CreateToolTip

# VARIABLES ----------------------------------------------

# CLASSES ------------------------------------------------

class RecordView(tk.Frame):

    def __init__(self, parent, **kwargs) -> None:
        super().__init__()
        # Variables ------------------------------------------------------------------------

        # Holder dictionary for tk variables and widgets to be used by the view.  Variant dict Must match the model's fields. (VCF_FIELDS)
        self.variant = dict()
        for x in VCF_FIELDS:
            self.variant[x] = tk.StringVar()
        self.variant['Disposition'] = tk.StringVar()

        self.variables = dict()
        self.variables['filename'] = tk.StringVar()
        self.variables['status_bar'] = tk.StringVar()
        self.variables['Disposition'] = dict()
        for x in DISPOSITIONS:
            self.variables['Disposition'][x] = tk.IntVar()

        self.labels = dict()
        for x in VCF_FIELDS:
            self.labels[x] = tk.Label()
        self.labels['Disposition'] = tk.Label()

        self.buttons = dict()
        self.frames = dict()
        self.radio_buttons = dict()
        self.treeviews = dict()
        self.scrollbars = dict()

        # Frames and Widgets ----------------------------------------------------------

        # Base Frame
        self.frames['base'] = tk.Frame(parent)
        self.frames['base'].pack(expand=True, fill='both',ipadx=10, ipady=10)

        # Left Frame
        self.frames['left'] = tk.LabelFrame(self.frames['base'], text="VCF File Info", relief='groove')
        self.frames['left'].pack(side='left', expand=False, fill='y',ipadx=10, ipady=10, padx=5, pady=5)

        #File load button
        self.labels['filename'] = tk.Label(self.frames['left'], anchor='c', textvariable=self.variables['filename'], relief='groove', width=24, wraplength=220)
        self.labels['filename'].pack(side='top', expand=False, fill='x',ipady=5, padx=5, pady=5)
        self.buttons['load_file'] = tk.Button(self.frames['left'], text="Load a File", command=self.open_file)
        self.buttons['load_file'].pack(side='top', expand=False, fill='x', ipady=5, padx=5, pady=5)

        # Treeview Frame
        self.frames['treeview'] = tk.Frame(self.frames['left'])
        self.frames['treeview'].pack(side='top',expand=True,fill='both', padx=5)

        # Treeview list
        view_columns = VCF_FIELDS
        view_columns.append('Disposition')
        self.treeviews['variant_list'] = tk.Treeview(self.frames['treeview'], columns=view_columns, displaycolumns=[4,69], selectmode='browse', show='headings')
        # self.treeviews['variant_list'] = tbv.tableview.Tableview(self.frames['treeview'], coldata=VCF_FIELDS, displaycolumns=[5,0], selectmode='browse', show='headings')
        for x in VCF_FIELDS:
            self.treeviews['variant_list'].heading(x, text=x, anchor='center')
        self.treeviews['variant_list'].column(column=4, width=100, anchor='center')
        self.treeviews['variant_list'].column(column=69, width=100, anchor='center')
        self.treeviews['variant_list'].pack(side='left', expand=True, fill='both')
        self.treeviews['variant_list'].bind('<<TreeviewSelect>>', self.record_selected)
        self.treeviews['variant_list'].tag_configure('None', background="#c4c4c4")
        self.treeviews['variant_list'].tag_configure('Hotspot', background="#f92134")
        self.treeviews['variant_list'].tag_configure('VUS', background="#f0aa44")
        self.treeviews['variant_list'].tag_configure('Low VAF Variants', background="#70aaff")
        self.treeviews['variant_list'].tag_configure('Harmful', background="#fc6622")
        self.treeviews['variant_list'].tag_configure('FLT3 ITD', background="#f794fa")

        # Treeview Scrollbar
        self.scrollbars['variant_list'] = tk.Scrollbar(self.frames['treeview'], orient=tk.VERTICAL, command=self.treeviews['variant_list'].yview)
        self.treeviews['variant_list'].configure(yscroll=self.scrollbars['variant_list'].set)
        self.scrollbars['variant_list'].pack(side='left', expand=False, fill='y')

        # Disposition Frame
        self.frames['disposition'] = tk.LabelFrame(self.frames['left'], text="Variant Disposition", relief='groove')
        self.frames['disposition'].pack(side='top', expand=False, fill='x', padx=5)
        self.frames['dispo_1'] = tk.Frame(self.frames['disposition'])
        self.frames['dispo_1'].pack(side='top', expand=False, fill='x')
        self.frames['dispo_2'] = tk.Frame(self.frames['disposition'])
        self.frames['dispo_2'].pack(side='top', expand=False, fill='x')
        self.frames['dispo_3'] = tk.Frame(self.frames['disposition'])
        self.frames['dispo_3'].pack(side='top', expand=False, fill='x')
        self.frames['dispo_4'] = tk.Frame(self.frames['disposition'])
        self.frames['dispo_4'].pack(side='top', expand=False, fill='x')
        self.frames['dispo_5'] = tk.Frame(self.frames['disposition'])
        self.frames['dispo_5'].pack(side='top', expand=False, fill='x')
        self.frames['dispo_6'] = tk.Frame(self.frames['disposition'])
        self.frames['dispo_6'].pack(side='top', expand=False, fill='x')

        # Disposition labels
        self.labels["None"] = tk.Label(self.frames['dispo_1'], anchor='c', textvariable=self.variables['Disposition']['None'], width=5, relief='groove')
        self.labels["None"].pack(side='left', expand=False, fill='y', padx=5, pady=5)
        self.labels["Low VAF Variants"] = tk.Label(self.frames['dispo_2'], anchor='c', textvariable=self.variables['Disposition']['None'], width=5, relief='groove')
        self.labels["Low VAF Variants"].pack(side='left', expand=False, fill='y', padx=5, pady=5)
        self.labels["VUS"] = tk.Label(self.frames['dispo_3'], anchor='c', textvariable=self.variables['Disposition']['None'], width=5, relief='groove')
        self.labels["VUS"].pack(side='left', expand=False, fill='y', padx=5, pady=5)
        self.labels["Harmful"] = tk.Label(self.frames['dispo_4'], anchor='c', textvariable=self.variables['Disposition']['None'], width=5, relief='groove')
        self.labels["Harmful"].pack(side='left', expand=False, fill='y', padx=5, pady=5)
        self.labels["FLT3 ITDs"] = tk.Label(self.frames['dispo_5'], anchor='c', textvariable=self.variables['Disposition']['None'], width=5, relief='groove')
        self.labels["FLT3 ITDs"].pack(side='left', expand=False, fill='y', padx=5, pady=5)
        self.labels["Hotspot Exceptions"] = tk.Label(self.frames['dispo_6'], anchor='c', textvariable=self.variables['Disposition']['None'], width=5, relief='groove')
        self.labels["Hotspot Exceptions"].pack(side='left', expand=False, fill='y', padx=5, pady=5)

        # Radio buttons for disposition
        self.radio_buttons["None"] = tk.Radiobutton(self.frames['dispo_1'], text="None (Unassigned)", variable=self.variant['Disposition'], value='None')
        self.radio_buttons["None"].pack(side='left', expand=False, fill='both')
        self.radio_buttons["Low VAF"] = tk.Radiobutton(self.frames['dispo_2'], text="Low VAF", variable=self.variant['Disposition'], value='Low VAF')
        self.radio_buttons["Low VAF"].pack(side='left', expand=False, fill='both')
        self.radio_buttons["VUS"] = tk.Radiobutton(self.frames['dispo_3'], text="VUS", variable=self.variant['Disposition'], value='VUS')
        self.radio_buttons["VUS"].pack(side='left', expand=False, fill='both')
        self.radio_buttons["Harmful"] = tk.Radiobutton(self.frames['dispo_4'], text="Harmful", variable=self.variant['Disposition'], value='Harmful')
        self.radio_buttons["Harmful"].pack(side='left', expand=False, fill='both')
        self.radio_buttons["FLT3 ITDs"] = tk.Radiobutton(self.frames['dispo_5'], text="FLT3 ITDs", variable=self.variant['Disposition'], value='FLT3 ITDs')
        self.radio_buttons["FLT3 ITDs"].pack(side='left', expand=False, fill='both')
        self.radio_buttons["Hotspot Exceptions"] = tk.Radiobutton(self.frames['dispo_6'], text="Hotspot Exception", variable=self.variant['Disposition'], value='Hotspot Exception')
        self.radio_buttons["Hotspot Exceptions"].pack(side='left', expand=False, fill='both')
        # self.radio_buttons["None"].select()

        # Process output files button
        self.buttons['save_disposition'] = tk.Button(self.frames['left'], text="Save Disposition", command=None, state='disabled')
        self.buttons['save_disposition'].pack(side='top', expand=False, fill='x', padx=5, pady=5, ipady=5)

        # Process output files button
        # tk.Button(self.frames['left'], text="Create Disposition Lists").pack(side='top', expand=False, fill='x', padx=5, pady=5, ipady=5)

        # Right Frame
        self.frames['right'] = tk.Frame(self.frames['base'])
        self.frames['right'].pack(side='right', expand=True, fill='both',ipadx=10, ipady=10)

        # Basic Info Frame
        self.frames['basic_info'] = tk.LabelFrame(self.frames['right'], text='Locus Info')
        self.frames['basic_info'].pack(side='top', expand=False, fill='x', padx=5, pady=5)
        self.frames['basic_info_gene'] = tk.Frame(self.frames['basic_info'])
        self.frames['basic_info_gene'].pack(side='left',expand=False, fill='both', padx=5, pady=5)
        tk.Label(self.frames['basic_info_gene'], text="Gene").pack(side='top',expand=False,fill='x')
        self.labels["Variant Annotation: Gene"] = tk.Label(self.frames['basic_info_gene'], width=8, anchor='c', textvariable=self.variant["Variant Annotation: Gene"], relief='groove', font=('bold', 24, 'bold'))
        self.labels["Variant Annotation: Gene"].pack(side='top',expand=True,fill='both')
        self.frames['basic_info_chrom'] = tk.Frame(self.frames['basic_info'])
        self.frames['basic_info_chrom'].pack(side='left',expand=False,fill='both', padx=5, pady=5)
        tk.Label(self.frames['basic_info_chrom'], text="Chromosome").pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Chrom"] = tk.Label(self.frames['basic_info_chrom'], width=6, anchor='c', textvariable=self.variant["Original Input: Chrom"], relief='groove')
        self.labels["Original Input: Chrom"].pack(side='top',expand=False, fill='x')
        tk.Label(self.frames['basic_info_chrom'], text="Base Pair").pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Pos"] = tk.Label(self.frames['basic_info_chrom'], width=12, anchor='c', textvariable=self.variant["Original Input: Pos"], relief='groove')
        self.labels["Original Input: Pos"].pack(side='top',expand=False, fill='x')
        self.frames['basic_info_changes'] = tk.Frame(self.frames['basic_info'])
        self.frames['basic_info_changes'].pack(side='left',expand=False,fill='both', padx=5, pady=5)
        tk.Label(self.frames['basic_info_changes'], text="DNA Change (c-dot)").pack(side='top',expand=False, fill='x')
        self.labels["Variant Annotation: cDNA change"] = tk.Label(self.frames['basic_info_changes'], text="C-dot", anchor='c', textvariable=self.variant["Variant Annotation: cDNA change"], relief='groove')
        self.labels["Variant Annotation: cDNA change"].pack(side='top',expand=False, fill='x')
        tk.Label(self.frames['basic_info_changes'], text="Protein Change (p-dot)").pack(side='top',expand=False, fill='x')
        self.labels["Variant Annotation: Protein Change"] = tk.Label(self.frames['basic_info_changes'], text="P-dot", width=24, anchor='c', textvariable=self.variant["Variant Annotation: Protein Change"], relief='groove')
        self.labels["Variant Annotation: Protein Change"].pack(side='top',expand=False, fill='x')
        self.frames['basic_info_alleles'] = tk.Frame(self.frames['basic_info'])
        self.frames['basic_info_alleles'].pack(side='left',expand=True,fill='both', padx=5, pady=5)
        tk.Label(self.frames['basic_info_alleles'], text="Ref Allele", anchor='nw').pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Reference allele"] = tk.Label(self.frames['basic_info_alleles'], anchor='c', textvariable=self.variant["Original Input: Reference allele"], relief='groove')
        self.labels["Original Input: Reference allele"].pack(side='top',expand=False, fill='x')
        tk.Label(self.frames['basic_info_alleles'], text="Variant Allele", anchor='w').pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Alternate allele"] = tk.Label(self.frames['basic_info_alleles'], anchor='c', textvariable=self.variant["Original Input: Alternate allele"], relief='groove')
        self.labels["Original Input: Alternate allele"].pack(side='top',expand=False, fill='x')

        # middle frame
        self.frames['middle'] = tk.Frame(self.frames['right'])
        self.frames['middle'].pack(side='top',expand=True,fill='both', padx=5, pady=5)

        # Strand Bias Frame
        self.frames['genexys'] = tk.LabelFrame(self.frames['middle'], text='Strand Bias Data', relief='groove')
        self.frames['genexys'].pack(side='left', expand=False, fill='both', padx=(0,10))
        self.frames['genexys_sb_calc'] = tk.Frame(self.frames['genexys'])
        self.frames['genexys_sb_calc'].pack(side='top', expand=False, fill='both', padx=5, pady=5)
        self.frames['genexys_sb_calc'].rowconfigure(0, weight=1)
        self.frames['genexys_sb_calc'].rowconfigure(1, weight=1)
        self.frames['genexys_sb_calc'].columnconfigure(0, weight=0)
        self.frames['genexys_sb_calc'].columnconfigure(1, weight=5)
        self.frames['genexys_sb_calc'].columnconfigure(2, weight=0)
        self.frames['genexys_sb_calc'].columnconfigure(3, weight=1)
        tk.Label(self.frames['genexys_sb_calc'], text="SB (reported)", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["VCF: STB"] = tk.Label(self.frames['genexys_sb_calc'], anchor='c', textvariable=self.variant["VCF: STB"], relief='groove')
        self.labels["VCF: STB"].grid(column=1, row=0, sticky='news')
        tk.Label(self.frames['genexys_sb_calc'], text="p.", anchor='e').grid(column=2, row=0, sticky='news', padx=5)
        self.labels["VCF: STBP"] = tk.Label(self.frames['genexys_sb_calc'], anchor='c', textvariable=self.variant["VCF: STBP"], relief='groove', width=5)
        self.labels["VCF: STBP"].grid(column=3, row=0, sticky='news')

        # Genexys strand Bias Area
        self.frames['sb_GX'] = tk.LabelFrame(self.frames['genexys'], text="Genexys (calculated)")
        self.frames['sb_GX'].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frames['sb_GX'].rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frames['sb_GX'].columnconfigure(x, weight=1)
        tk.Label(self.frames['sb_GX'], text='Genexys', width=8).grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['sb_GX'], text='Fwd').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frames['sb_GX'], text='Rev').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frames['sb_GX'], text='Ref', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_GX'], text='Var', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSRF'] = tk.Label(self.frames['sb_GX'], anchor='c', textvariable=self.variant["VCF: FSRF"], relief='groove')
        self.labels['VCF: FSRF'].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSRR'] = tk.Label(self.frames['sb_GX'], anchor='c', textvariable=self.variant["VCF: FSRR"], relief='groove')
        self.labels['VCF: FSRR'].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSAF'] = tk.Label(self.frames['sb_GX'], anchor='c', textvariable=self.variant["VCF: FSAF"], relief='groove')
        self.labels['VCF: FSAF'].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels['VCF: FSAR'] = tk.Label(self.frames['sb_GX'], anchor='c', textvariable=self.variant["VCF: FSAR"], relief='groove')
        self.labels['VCF: FSAR'].grid(column=3, row=2, sticky='news', pady=5, padx=5)

        # Separator
        tk.Separator(self.frames['sb_GX'], orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frames['sb_GX_results'] = tk.Frame(self.frames['sb_GX'])
        self.frames['sb_GX_results'].grid(column=0, row=5, columnspan=4, sticky='news')
        self.frames['sb_GX_results'].rowconfigure(0, weight=1)
        self.frames['sb_GX_results'].rowconfigure(1, weight=1)
        self.frames['sb_GX_results'].columnconfigure(0, weight=0)
        self.frames['sb_GX_results'].columnconfigure(1, weight=5)
        self.frames['sb_GX_results'].columnconfigure(2, weight=0)
        self.frames['sb_GX_results'].columnconfigure(3, weight=1)

        # Genexys Stats Area
        tk.Label(self.frames['sb_GX_results'], text="Binom. Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["VCF: Binom Proportion"] = tk.Label(self.frames['sb_GX_results'], anchor='c', textvariable=self.variant["VCF: Binom Proportion"], relief='groove')
        self.labels["VCF: Binom Proportion"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_GX_results'], text="p.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["VCF: Binom P Value"] = tk.Label(self.frames['sb_GX_results'], anchor='c', textvariable=self.variant["VCF: Binom P Value"], relief='groove', width=5)
        self.labels["VCF: Binom P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_GX_results'], text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["VCF: Fisher Odds Ratio"] = tk.Label(self.frames['sb_GX_results'], anchor='c', textvariable=self.variant["VCF: Fisher Odds Ratio"], relief='groove')
        self.labels["VCF: Fisher Odds Ratio"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_GX_results'], text="p.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["VCF: Fisher P Value"] = tk.Label(self.frames['sb_GX_results'], anchor='c', textvariable=self.variant["VCF: Fisher P Value"], relief='groove', width=5)
        self.labels["VCF: Fisher P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)

        # Q20 Read Bias Area
        self.frames['sb_Q_20'] = tk.LabelFrame(self.frames['genexys'], text="Filtered M-Pileup (calculated)")
        self.frames['sb_Q_20'].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frames['sb_Q_20'].rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frames['sb_Q_20'].columnconfigure(x, weight=1)
        tk.Label(self.frames['sb_Q_20'], text='Q20', width=8, anchor='c').grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['sb_Q_20'], text='Fwd').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frames['sb_Q_20'], text='Rev').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frames['sb_Q_20'], text='Ref', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_Q_20'], text='Var', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Reference Forward Read Depth"] = tk.Label(self.frames['sb_Q_20'], anchor='c', textvariable=self.variant["Mpileup Qual: Filtered Reference Forward Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Filtered Reference Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Reference Reverse Read Depth"] = tk.Label(self.frames['sb_Q_20'], anchor='c', textvariable=self.variant["Mpileup Qual: Filtered Reference Reverse Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Filtered Reference Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Variant Forward Read Depth"] = tk.Label(self.frames['sb_Q_20'], anchor='c', textvariable=self.variant["Mpileup Qual: Filtered Variant Forward Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Filtered Variant Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Filtered Variant Reverse Read Depth"] = tk.Label(self.frames['sb_Q_20'], anchor='c', textvariable=self.variant["Mpileup Qual: Filtered Variant Reverse Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Filtered Variant Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)

        # Separator
        tk.Separator(self.frames['sb_Q_20'], orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frames['sb_Q_20_results'] = tk.Frame(self.frames['sb_Q_20'])
        self.frames['sb_Q_20_results'].grid(column=0, row=5, columnspan=4, sticky='news')
        self.frames['sb_Q_20_results'].rowconfigure(0, weight=1)
        self.frames['sb_Q_20_results'].rowconfigure(1, weight=1)
        self.frames['sb_Q_20_results'].columnconfigure(0, weight=0)
        self.frames['sb_Q_20_results'].columnconfigure(1, weight=5)
        self.frames['sb_Q_20_results'].columnconfigure(2, weight=0)
        self.frames['sb_Q_20_results'].columnconfigure(3, weight=1)

        # Q20 Stats Area
        tk.Label(self.frames['sb_Q_20_results'], text="Binom. Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["Mpileup Qual: Filtered Variant Binomial Proportion"] = tk.Label(self.frames['sb_Q_20_results'], anchor='c', textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial Proportion"], relief='groove')
        self.labels["Mpileup Qual: Filtered Variant Binomial Proportion"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_Q_20_results'], text="p.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["Mpileup Qual: Filtered Variant Binomial P Value"] = tk.Label(self.frames['sb_Q_20_results'], anchor='c', textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial P Value"], relief='groove', width=5)
        self.labels["Mpileup Qual: Filtered Variant Binomial P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_Q_20_results'], text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["Mpileup Qual: Filtered Variant Fishers Odds Ratio"] = tk.Label(self.frames['sb_Q_20_results'], anchor='c', textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers Odds Ratio"], relief='groove')
        self.labels["Mpileup Qual: Filtered Variant Fishers Odds Ratio"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_Q_20_results'], text="p.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["Mpileup Qual: Filtered Variant Fishers P Value"] = tk.Label(self.frames['sb_Q_20_results'], anchor='c', textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers P Value"], relief='groove', width=5)
        self.labels["Mpileup Qual: Filtered Variant Fishers P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)

        # Q1 Read Bias Area
        self.frames['sb_Q_1'] = tk.LabelFrame(self.frames['genexys'], text="Unfiltered M-Pileup (calculated)")
        self.frames['sb_Q_1'].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frames['sb_Q_1'].rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frames['sb_Q_1'].columnconfigure(x, weight=1)
        tk.Label(self.frames['sb_Q_1'], text='Q1', width=8, anchor='c').grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['sb_Q_1'], text='Fwd').grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frames['sb_Q_1'], text='Rev').grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        tk.Label(self.frames['sb_Q_1'], text='Ref', anchor='e').grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_Q_1'], text='Var', anchor='e').grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Reference Forward Read Depth"] = tk.Label(self.frames['sb_Q_1'], width=5, anchor='c', textvariable=self.variant["Mpileup Qual: Unfiltered Reference Forward Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Unfiltered Reference Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Reference Reverse Read Depth"] = tk.Label(self.frames['sb_Q_1'], width=5, anchor='c', textvariable=self.variant["Mpileup Qual: Unfiltered Reference Reverse Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Unfiltered Reference Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Forward Read Depth"] = tk.Label(self.frames['sb_Q_1'], width=5, anchor='c', textvariable=self.variant["Mpileup Qual: Unfiltered Variant Forward Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Unfiltered Variant Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Reverse Read Depth"] = tk.Label(self.frames['sb_Q_1'], width=5, anchor='c', textvariable=self.variant["Mpileup Qual: Unfiltered Variant Reverse Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Unfiltered Variant Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)

        # Separator
        tk.Separator(self.frames['sb_Q_1'], orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        self.frames['sb_Q_1_results'] = tk.Frame(self.frames['sb_Q_1'])
        self.frames['sb_Q_1_results'].grid(column=0, row=5, columnspan=4, sticky='news')
        self.frames['sb_Q_1_results'].rowconfigure(0, weight=1)
        self.frames['sb_Q_1_results'].rowconfigure(1, weight=1)
        self.frames['sb_Q_1_results'].columnconfigure(0, weight=0)
        self.frames['sb_Q_1_results'].columnconfigure(1, weight=5)
        self.frames['sb_Q_1_results'].columnconfigure(2, weight=0)
        self.frames['sb_Q_1_results'].columnconfigure(3, weight=1)

        # Q1 Stats Area
        tk.Label(self.frames['sb_Q_1_results'], text="Binom. Prop.", anchor='e').grid(column=0, row=0, sticky='news', padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Binomial Proportion"] = tk.Label(self.frames['sb_Q_1_results'], anchor='c', textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial Proportion"], relief='groove')
        self.labels["Mpileup Qual: Unfiltered Variant Binomial Proportion"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_Q_1_results'], text="p.", anchor='e').grid(column=2, row=0, sticky='news')
        self.labels["Mpileup Qual: Unfiltered Variant Binomial P Value"] = tk.Label(self.frames['sb_Q_1_results'], anchor='c', textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial P Value"], relief='groove', width=5)
        self.labels["Mpileup Qual: Unfiltered Variant Binomial P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_Q_1_results'], text="Fishers OR", anchor='e').grid(column=0, row=1, sticky='news', padx=5)
        self.labels["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"] = tk.Label(self.frames['sb_Q_1_results'], anchor='c', textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"], relief='groove')
        self.labels["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        tk.Label(self.frames['sb_Q_1_results'], text="p.", anchor='e').grid(column=2, row=1, sticky='news')
        self.labels["Mpileup Qual: Unfiltered Variant Fishers P Value"] = tk.Label(self.frames['sb_Q_1_results'], anchor='c', textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers P Value"], relief='groove', width=5)
        self.labels["Mpileup Qual: Unfiltered Variant Fishers P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)

        # Genexys info frame
        self.frames['gx_info'] = tk.LabelFrame(self.frames['middle'], text='Genexys Information')
        self.frames['gx_info'].pack(side='top', expand=False, fill='both', pady=(0,5))
        for x in range(1,5,2):
            self.frames['gx_info'].rowconfigure(x, weight=1)
        for x in range(6):
            self.frames['gx_info'].columnconfigure(x, weight=1)

        # gx info top area
        tk.Label(self.frames['gx_info'], text="Allele Fraction").grid(row=0, column=0, sticky='news', padx=5)
        self.labels["VCF: AF"] = tk.Label(self.frames['gx_info'], anchor='c', textvariable=self.variant["VCF: AF"], relief='groove')
        self.labels["VCF: AF"].grid(row=1, column=0, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['gx_info'], text="Variant Type").grid(row=0, column=1, sticky='news', padx=5)
        self.labels["VCF: TYPE"] = tk.Label(self.frames['gx_info'], anchor='c', textvariable=self.variant["VCF: TYPE"], relief='groove')
        self.labels["VCF: TYPE"].grid(row=1, column=1, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['gx_info'], text="Length of Variant (BP)").grid(row=0, column=2, sticky='news', padx=5)
        self.labels["VCF: LEN"] = tk.Label(self.frames['gx_info'], anchor='c', textvariable=self.variant["VCF: LEN"], relief='groove')
        self.labels["VCF: LEN"].grid(row=1, column=2, sticky='news', padx=5, pady=5)

        tk.Label(self.frames['gx_info'], text="Genotype").grid(row=0, column=3, sticky='news', padx=5)
        self.labels["VCF: Genotype"] = tk.Label(self.frames['gx_info'], anchor='c', textvariable=self.variant["VCF: Genotype"], relief='groove')
        self.labels["VCF: Genotype"].grid(row=1, column=3, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['gx_info'], text="Filter (Genexys)").grid(row=0, column=4, sticky='news', padx=5)
        self.labels["VCF: Filter"] = tk.Label(self.frames['gx_info'], anchor='c', textvariable=self.variant["VCF: Filter"], relief='groove')
        self.labels["VCF: Filter"].grid(row=1, column=4, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['gx_info'], text="Quality Score").grid(row=0, column=5, sticky='news', padx=5)
        self.labels["VCF: QUAL"] = tk.Label(self.frames['gx_info'], anchor='c', textvariable=self.variant["VCF: QUAL"], relief='groove')
        self.labels["VCF: QUAL"].grid(row=1, column=5, rowspan=4, sticky='news', padx=5, pady=5)

        # Separator
        tk.Separator(self.frames['gx_info'], orient='horizontal').grid(row=2, column=0, columnspan=5, sticky='news')

        # gx info bottom area
        tk.Label(self.frames['gx_info'], text="FAO").grid(row=3, column=0, sticky='news', padx=5)
        self.labels["VCF: FAO"] = tk.Label(self.frames['gx_info'], anchor='c', textvariable=self.variant["VCF: FAO"], relief='groove')
        self.labels["VCF: FAO"].grid(row=4, column=0, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['gx_info'], text="FDP").grid(row=3, column=1, sticky='news', padx=5)
        self.labels["VCF: FDP"] = tk.Label(self.frames['gx_info'], anchor='c', textvariable=self.variant["VCF: FDP"], relief='groove')
        self.labels["VCF: FDP"].grid(row=4, column=1, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['gx_info'], text="HRUN").grid(row=3, column=2, sticky='news', padx=5)
        self.labels["VCF: HRUN"] = tk.Label(self.frames['gx_info'], anchor='c', textvariable=self.variant["VCF: HRUN"], relief='groove')
        self.labels["VCF: HRUN"].grid(row=4, column=2, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['gx_info'], text="QD").grid(row=3, column=3, sticky='news', padx=5)
        self.labels["VCF: QD"] = tk.Label(self.frames['gx_info'], anchor='c', textvariable=self.variant["VCF: QD"], relief='groove')
        self.labels["VCF: QD"].grid(row=4, column=3, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['gx_info'], text="SVTYPE (Unused)").grid(row=3, column=4, sticky='news', padx=5)
        self.labels["VCF: SVTYPE"] = tk.Label(self.frames['gx_info'], anchor='c', textvariable=self.variant["VCF: SVTYPE"], relief='groove')
        self.labels["VCF: SVTYPE"].grid(row=4, column=4, sticky='news', padx=5, pady=5)

        # mpileup info frame
        self.frames['mpl_info'] = tk.LabelFrame(self.frames['middle'], text='M-Pileup Information')
        self.frames['mpl_info'].pack(side='top', expand=False, fill='both', pady=5)
        for x in [1,2,4]:
            self.frames['mpl_info'].columnconfigure(x, weight=1)
        for x in range(2):
            self.frames['mpl_info'].rowconfigure(x, weight=1)
        tk.Label(self.frames['mpl_info'], text="Filtered VAF (Q20)", anchor='e').grid(column=0, row=0, sticky='news', padx=5, pady=5)
        self.labels["Mpileup Qual: Filtered VAF"] = tk.Label(self.frames['mpl_info'], anchor='c', textvariable=self.variant["Mpileup Qual: Filtered VAF"], relief='groove')
        self.labels["Mpileup Qual: Filtered VAF"].grid(column=1, row=0, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['mpl_info'], text="Unfiltered VAF (Q1)", anchor='e').grid(column=0, row=1, sticky='news', padx=5, pady=5)
        self.labels["Mpileup Qual: Unfiltered VAF"] = tk.Label(self.frames['mpl_info'], anchor='c', textvariable=self.variant["Mpileup Qual: Unfiltered VAF"], relief='groove')
        self.labels["Mpileup Qual: Unfiltered VAF"].grid(column=1, row=1, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['mpl_info'], text="Total Read Depth", anchor='c').grid(column=2, row=0, sticky='news', padx=5, pady=5)
        self.labels["Mpileup Qual: Read Depth"] = tk.Label(self.frames['mpl_info'], anchor='c', textvariable=self.variant["Mpileup Qual: Read Depth"], relief='groove')
        self.labels["Mpileup Qual: Read Depth"].grid(column=2, row=1, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['mpl_info'], text="Count: Read Starts").grid(column=3, row=0, sticky='news', padx=5, pady=5)
        self.labels["Mpileup Qual: Start Reads"] = tk.Label(self.frames['mpl_info'], anchor='c', textvariable=self.variant["Mpileup Qual: Start Reads"], relief='groove')
        self.labels["Mpileup Qual: Start Reads"].grid(column=4, row=0, sticky='news', padx=5, pady=5)
        tk.Label(self.frames['mpl_info'], text="Count: Read Ends").grid(column=3, row=1, sticky='news', padx=5, pady=5)
        self.labels["Mpileup Qual: Stop Reads"] = tk.Label(self.frames['mpl_info'], anchor='c', textvariable=self.variant["Mpileup Qual: Stop Reads"], relief='groove')
        self.labels["Mpileup Qual: Stop Reads"].grid(column=4, row=1, sticky='news', padx=5, pady=5)

        # Variant Annotation Info Frame
        self.frames['other'] = tk.Frame(self.frames['middle'])
        self.frames['other'].pack(side='top',expand=True, fill='both')
        self.frames['var_annot'] = tk.LabelFrame(self.frames['other'], text='Variant Annotation')
        self.frames['var_annot'].pack(side='left',expand=True, fill='both', padx=(0,5))
        for x in range(4):
            self.frames['var_annot'].columnconfigure(x, weight=1)
        self.frames['var_annot'].rowconfigure(3, weight=99)
        tk.Label(self.frames['var_annot'], text="Coding Region").grid(column=0, row=0, sticky='news', padx=5)
        self.labels["Variant Annotation: Coding"] = tk.Label(self.frames['var_annot'], anchor='c', textvariable=self.variant["Variant Annotation: Coding"], relief='groove')
        self.labels["Variant Annotation: Coding"].grid(column=0, row=1, sticky='news', padx=5)
        tk.Label(self.frames['var_annot'], text="Variant Type (Seq. Ontology)").grid(column=1, row=0, sticky='news', padx=5)
        self.labels["Variant Annotation: Sequence"] = tk.Label(self.frames['var_annot'], anchor='c', textvariable=self.variant["Variant Annotation: Sequence Ontology"], relief='groove')
        self.labels["Variant Annotation: Sequence"].grid(column=1, row=1, sticky='news', padx=5)
        tk.Label(self.frames['var_annot'], text="Transcript").grid(column=2, row=0, sticky='news', padx=5)
        self.labels["Variant Annotation: Transcript"] = tk.Label(self.frames['var_annot'], anchor='c', textvariable=self.variant["Variant Annotation: Transcript"], relief='groove')
        self.labels["Variant Annotation: Transcript"].grid(column=2, row=1, sticky='news', padx=5)
        tk.Label(self.frames['var_annot'], text="RefSeq").grid(column=3, row=0, sticky='news', padx=5)
        self.labels["Variant Annotation: RefSeq"] = tk.Label(self.frames['var_annot'], anchor='c', textvariable=self.variant["VCF: LEN"], relief='groove')
        self.labels["Variant Annotation: RefSeq"].grid(column=3, row=1, sticky='news', padx=5)
        tk.Label(self.frames['var_annot'], text="All Mappings").grid(column=0, row=2, columnspan=3, sticky='news', padx=5)
        self.labels["Variant Annotation: All Mappings"] = tk.Label(self.frames['var_annot'], anchor='c', textvariable=self.variant["Variant Annotation: All Mappings"], relief='groove', wraplength=500)
        self.labels["Variant Annotation: All Mappings"].grid(column=0, columnspan=4, row=3, sticky='news', padx=5, pady=(0,5))

        # MDL Info area
        self.frames['mdl'] = tk.LabelFrame(self.frames['other'], text='MDL Info')
        self.frames['mdl'].pack(side='left',expand=True, fill='both', padx=(5,0))
        self.frames['mdl'].rowconfigure(3, weight=99)
        self.frames['mdl'].columnconfigure(0, weight=1)
        self.frames['mdl'].columnconfigure(1, weight=1)
        tk.Label(self.frames['mdl'], text="Sample Count").grid(column=0, row=0, sticky='news', padx=5)
        self.labels["MDL: Sample Count"] = tk.Label(self.frames['mdl'], anchor='c', textvariable=self.variant["MDL: Sample Count"], relief='groove')
        self.labels["MDL: Sample Count"].grid(column=0, row=1, sticky='news', padx=5)
        tk.Label(self.frames['mdl'], text="Variant Frequency").grid(column=1, row=0, sticky='news', padx=5)
        self.labels["MDL: Variant Frequency"]  = tk.Label(self.frames['mdl'], anchor='c', textvariable=self.variant["MDL: Variant Frequency"], relief='groove')
        self.labels["MDL: Variant Frequency"].grid(column=1, row=1, sticky='news', padx=5)
        tk.Label(self.frames['mdl'], text="Sample List").grid(column=0, columnspan=2, row=2, sticky='news', padx=5)
        self.labels["MDL: Sample List"] = tk.Label(self.frames['mdl'], anchor='c', textvariable=self.variant["MDL: Sample List"], relief='groove', wraplength=500)
        self.labels["MDL: Sample List"].grid(column=0, columnspan=2, row=3, sticky='news', padx=5, pady=(0,5))

        # Web Resources Stats
        self.frames['bottom'] = tk.LabelFrame(self.frames['right'], text='Database Information')
        self.frames['bottom'].pack(side='bottom', expand=False, fill='both', padx=5, pady=5)
        self.frames['bottom'].columnconfigure(0, weight=1)
        self.frames['bottom'].columnconfigure(1, weight=1)
        self.frames['bottom_l'] = tk.Frame(self.frames['bottom'])
        self.frames['bottom_l'].grid(column=0, row=0, sticky='news')
        self.frames['bottom_2'] = tk.Frame(self.frames['bottom'])
        self.frames['bottom_2'].grid(column=1, row=0, sticky='news')

        # COSMIC Tissue Variant Count Region
        self.labels["COSMIC: Variant Count (Tissue)"] = tk.Label(self.frames['bottom_l'], anchor='c', textvariable=self.variant["COSMIC: Variant Count (Tissue)"], relief='groove', wraplength=600)
        self.labels["COSMIC: Variant Count (Tissue)"].pack(side='left', expand=True, fill='both', padx=5, pady=5)

        # COSMIC Area
        self.frames['web_cosmic'] = tk.LabelFrame(self.frames['bottom_2'], text='COSMIC')
        self.frames['web_cosmic'].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frames['web_cosmic'], text="ID", anchor='center').pack(side='top', expand=False, fill='x', padx=5)
        self.labels["COSMIC: ID"] = tk.Label(self.frames['web_cosmic'], anchor='c', textvariable=self.variant["COSMIC: ID"], relief='groove', width=12)
        self.labels["COSMIC: ID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frames['web_cosmic'], text="Count").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["COSMIC: Variant Count"] = tk.Label(self.frames['web_cosmic'], anchor='c', textvariable=self.variant["COSMIC: Variant Count"], relief='groove')
        self.labels["COSMIC: Variant Count"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # Clinvar Area
        self.frames['web_clinvar'] = tk.LabelFrame(self.frames['bottom_2'], text='ClinVar')
        self.frames['web_clinvar'].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frames['web_clinvar'], text="ID").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["ClinVar: ClinVar ID"] = tk.Label(self.frames['web_clinvar'], anchor='c', textvariable=self.variant["ClinVar: ClinVar ID"], relief='groove')
        self.labels["ClinVar: ClinVar ID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frames['web_clinvar'], text="Significance").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["ClinVar: Clinical Significance"] = tk.Label(self.frames['web_clinvar'], anchor='c', textvariable=self.variant["ClinVar: Clinical Significance"], relief='groove')
        self.labels["ClinVar: Clinical Significance"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # Gnomad Area
        self.frames['web_gnomad'] = tk.LabelFrame(self.frames['bottom_2'], text='GnomAD')
        self.frames['web_gnomad'].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frames['web_gnomad'], text="Global AF").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["gnomAD3: Global AF"] = tk.Label(self.frames['web_gnomad'], anchor='c', textvariable=self.variant["gnomAD3: Global AF"], relief='groove')
        self.labels["gnomAD3: Global AF"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # CADD Area
        self.frames['web_cadd'] = tk.LabelFrame(self.frames['bottom_2'], text='CADD')
        self.frames['web_cadd'].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frames['web_cadd'], text="Phred Score").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["CADD: Phred"] = tk.Label(self.frames['web_cadd'], anchor='c', textvariable=self.variant["CADD: Phred"], relief='groove')
        self.labels["CADD: Phred"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # PolyPhen Area
        self.frames['web_polyphen'] = tk.LabelFrame(self.frames['bottom_2'], text='PolyPhen-2')
        self.frames['web_polyphen'].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frames['web_polyphen'], text="HDIV").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["PolyPhen-2: HDIV Prediction"] = tk.Label(self.frames['web_polyphen'], anchor='c', textvariable=self.variant["PolyPhen-2: HDIV Prediction"], relief='groove')
        self.labels["PolyPhen-2: HDIV Prediction"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # SIFT Area
        self.frames['web_sift'] = tk.LabelFrame(self.frames['bottom_2'], text='SIFT')
        self.frames['web_sift'].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frames['web_sift'], text="Prediction").pack(side='top', expand=False, fill='x', padx=5)
        self.labels["SIFT: Prediction"] = tk.Label(self.frames['web_sift'], anchor='c', textvariable=self.variant["SIFT: Prediction"], relief='groove')
        self.labels["SIFT: Prediction"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # dbSNP Area
        self.frames['web_dbsnp'] = tk.LabelFrame(self.frames['bottom_2'], text='dbSNP')
        self.frames['web_dbsnp'].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frames['web_dbsnp'], text="rsID").pack(side='top', expand=False, fill='both', padx=5)
        self.labels["dbSNP: rsID"] = tk.Label(self.frames['web_dbsnp'], anchor='c', textvariable=self.variant["dbSNP: rsID"], relief='groove')
        self.labels["dbSNP: rsID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # UniProt Area
        self.frames['web_dbsnp'] = tk.LabelFrame(self.frames['bottom_2'], text='UniProt (GENE)')
        self.frames['web_dbsnp'].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frames['web_dbsnp'], text="Accession Number").pack(side='top', expand=False, fill='both', padx=5)
        self.labels["UniProt (GENE): Accession Number"] = tk.Label(self.frames['web_dbsnp'], anchor='c', textvariable=self.variant["UniProt (GENE): Accession Number"], relief='groove')
        self.labels["UniProt (GENE): Accession Number"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # PhyloP Vertscore Area
        self.frames['web_dbsnp'] = tk.LabelFrame(self.frames['bottom_2'], text='PhyloP')
        self.frames['web_dbsnp'].pack(side='left', expand=True, fill='both', padx=5, pady=5)
        tk.Label(self.frames['web_dbsnp'], text="Vert Score").pack(side='top', expand=False, fill='both', padx=5)
        self.labels["PhyloP: Vert Score"] = tk.Label(self.frames['web_dbsnp'], anchor='c', textvariable=self.variant["PhyloP: Vert Score"], relief='groove')
        self.labels["PhyloP: Vert Score"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # Status bar
        self.labels['status_bar'] = tk.Label(parent, anchor='c', textvariable=self.variables['status_bar'], relief='sunken').pack(side='bottom', expand=False, fill='x', padx=5, pady=5)

        # Create tooltips for labels
        for key,value in TOOLTIPS.items():
            if type(self.labels[key]) is type(dict()):
                pass
            else:
                CreateToolTip(self.labels[key], value)

        return
    
    def open_file(self):
        self.variables['filename'].set(str(fd.askopenfilename(filetypes=[('XLSX','*.xlsx')])))
        self.event_generate('<<FileSelect>>')
        return
    
    def load_treeview(self, variant_list):
        for item in self.treeviews['variant_list'].get_children():
            self.treeviews['variant_list'].delete(item)
        for variant in variant_list:
            values_list = list()
            for key in VCF_FIELDS:
                test_me = variant[key]
                try:
                    if float(test_me) == int(test_me):
                        values_list.append(int(variant[key]))
                    else:
                        values_list.append(round(float(variant[key]),3))
                except:
                    values_list.append(variant[key])
            self.treeviews['variant_list'].insert('', tk.END, values=values_list, tags=(values_list[-1]))
        self.treeviews['variant_list'].selection_set(self.treeviews['variant_list'].get_children()[0])
        # self.count_dispositions()
        return
    
    def clear_view(self, *args, **kwargs):
        for item in self.treeviews['variant_list'].get_children():
            self.treeviews['variant_list'].delete(item)
        for x in VCF_FIELDS:
            self.variant[x].set(None)
            self.labels[x].configure(bootstyle='normal.TLabel')
        self.variant['Disposition'].set(0)
        self.variables = dict()
        self.variables['filename'] = ""
        self.variables['status_bar'] = "Records view cleared."
        # for x in DISPOSITIONS:
        #     self.variables['Disposition'][x] = 0
        return
 
    def record_selected(self, *args, **kwargs):
        for selected_item in self.treeviews['variant_list'].selection():
            item = self.treeviews['variant_list'].item(selected_item)
            record = item['values']
            for x in range(len(VCF_FIELDS)):
                self.variant[VCF_FIELDS[x]].set(record[x])
        try:
            self.variant['Disposition'].set(record[-1])  # Disposition needs to always be last
        except:
            pass
        if self.variant['Disposition'].get():
            self.buttons['save_disposition']['state'] = 'normal'
        self.validate_cells()
        return

    def validate_cells(self):

        for x in VCF_FIELDS:
            self.labels[x].configure(bootstyle='normal.TLabel')
            if self.variant[x].get() == "None":
                self.labels[x].configure(bootstyle='inverse.TLabel')
                continue
            if x in VALIDATION['p_values']:
                if float(self.variant[x].get()) > VALIDATION['cutoffs']['p_value']:
                    self.labels[x].configure(bootstyle='danger.inverse.TLabel')
            if x in VALIDATION['strand_read_depth']:
                try:
                    if int(self.variant[x].get()) <= VALIDATION['cutoffs']['strand_read_depth']:
                        self.labels[x].configure(bootstyle='danger.inverse.TLabel')
                except:
                    pass
            if x in VALIDATION['locus_read_depth']:
                if int(self.variant[x].get()) <= VALIDATION['cutoffs']['locus_read_depth']:
                    self.labels[x].configure(bootstyle='danger.inverse.TLabel')
            if x in VALIDATION['minimum_vaf']:
                if float(self.variant[x].get()) < VALIDATION['cutoffs']['vaf_threshold']:
                    self.labels[x].configure(bootstyle='danger.inverse.TLabel')
            if x in VALIDATION['web_links']:
                self.labels[x].configure(bootstyle = 'info.inverse')
        return


# MAIN LOOP ----------------------------------------------

def main():

    pass

    return

if __name__ == '__main__':
    main()