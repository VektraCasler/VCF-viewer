# vcf_data_viewer/view.py
''' The view of the VCF Data Viewer application, comprised of the tkinter portion. '''

# IMPORTS ------------------------------------------------

import ttkbootstrap as tk
# from ttkbootstrap import tableview as tbv
from tkinter import Widget
from tkinter import filedialog as fd
from .global_variables import *
from .tool_tip import ToolTip, CreateToolTip

# VARIABLES ----------------------------------------------

# CLASSES ------------------------------------------------

class RecordView(tk.Frame):

    def _event(self, sequence):
        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback

    def __init__(self, parent, **kwargs) -> None:
        super().__init__()
        # Variables ------------------------------------------------------------------------

        # Holder dictionary for tk variables and widgets to be used by the view.  Variant dict Must match the model's fields. (VCF_FIELDS)

        self.variables = dict()
        self.variables['filename'] = tk.StringVar()
        self.variables['status_bar'] = tk.StringVar()
        self.variables['Disposition'] = dict()
        self.variables['selection_index'] = tk.IntVar()
        for x in DISPOSITIONS:
            self.variables['Disposition'][x] = tk.IntVar()

        self.variant = dict()
        self.labels = dict()
        self.entries = dict()
        self.buttons = dict()
        self.radio_buttons = dict()
        self.treeviews = dict()
        self.scrollbars = dict()
        self.textboxes = dict()

        for x in VCF_FIELDS:
            self.variant[x] = tk.StringVar()
            self.entries[x] = tk.Entry()
            self.labels[x] = tk.Label()
        self.entries['Disposition'] = tk.Entry()
        self.labels['Disposition'] = tk.Label()
        self.variant['Disposition'] = tk.StringVar()

        for x in TEXTBOXES:
            self.textboxes[x] = tk.ScrolledText()

        # Frames and Widgets ----------------------------------------------------------
        self.create_frames(parent=parent)

        #File load button
        self.entries['filename'] = tk.Entry(self.frames['left'], textvariable=self.variables['filename'], width=24)
        self.entries['filename'].grid(row=0, column=0, columnspan=2, sticky='news', padx=5, pady=5)
        self.buttons['load_file'] = tk.Button(self.frames['left'], text="Open a File", command=self._event('<<FileLoad>>'))
        self.buttons['load_file'].grid(row=1, column=0, columnspan=2, sticky='news', padx=5, pady=5)

        # Treeview list
        view_columns = VCF_FIELDS
        view_columns.append('Disposition')
        self.treeviews['variant_list'] = tk.Treeview(self.frames['left'], columns=view_columns, displaycolumns=[4,69], selectmode='browse', show='headings')
        # self.treeviews['variant_list'] = tk.tableview.Tableview(self.frames['treeview'], coldata=VCF_FIELDS, displaycolumns=[5,0], selectmode='browse', show='headings')
        for x in VCF_FIELDS:
            self.treeviews['variant_list'].heading(x, text=x, anchor='center')
        self.treeviews['variant_list'].column(column=4, width=100, anchor='center')
        self.treeviews['variant_list'].column(column=69, width=100, anchor='center')
        self.treeviews['variant_list'].grid(row=2, column=0, columnspan=2, sticky='news', padx=5, pady=5)
        self.treeviews['variant_list'].bind('<<TreeviewSelect>>', self.record_selected)
        self.treeviews['variant_list'].tag_configure('None', background="#c4c4c4")
        self.treeviews['variant_list'].tag_configure('Hotspot_Exceptions', background="#f92134")
        self.treeviews['variant_list'].tag_configure('VUS', background="#f0aa44")
        self.treeviews['variant_list'].tag_configure('Low_VAF_Variants', background="#70aaff")
        self.treeviews['variant_list'].tag_configure('Harmful', background="#fc6622")
        self.treeviews['variant_list'].tag_configure('FLT3_ITDs', background="#f794fa")

        # Treeview Scrollbar
        # self.scrollbars['variant_list'] = tk.Scrollbar(self.frames['treeview'], orient=tk.VERTICAL, command=self.treeviews['variant_list'].yview)
        # self.treeviews['variant_list'].configure(yscroll=self.scrollbars['variant_list'].set)
        # self.scrollbars['variant_list'].pack(side='left', expand=False, fill='y')

        # Disposition labels
        self.labels['disposition_label'] = tk.Label(self.frames['left'], text="Assign Disposition", bootstyle='secondary.inverse')
        self.labels['disposition_label'].grid(row=3, column=0, columnspan=2, sticky='news', padx=5, pady=5)
        self.entries["None"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['None'], width=5)
        self.entries["None"].grid(row=4, column=0, sticky='news', padx=5, pady=5)
        self.entries["Low VAF Variants"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['Low VAF Variants'], width=5)
        self.entries["Low VAF Variants"].grid(row=5, column=0, sticky='news', padx=5, pady=5)
        self.entries["VUS"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['VUS'], width=5)
        self.entries["VUS"].grid(row=6, column=0, sticky='news', padx=5, pady=5)
        self.entries["Harmful"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['Harmful'], width=5)
        self.entries["Harmful"].grid(row=7, column=0, sticky='news', padx=5, pady=5)
        self.entries["FLT3 ITDs"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['FLT3 ITDs'], width=5)
        self.entries["FLT3 ITDs"].grid(row=8, column=0, sticky='news', padx=5, pady=5)
        self.entries["Hotspot Exceptions"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['Hotspot Exceptions'], width=5)
        self.entries["Hotspot Exceptions"].grid(row=9, column=0, sticky='news', padx=5, pady=5)

        # Radio buttons for disposition
        self.radio_buttons["None"] = tk.Radiobutton(self.frames['left'], text="None (Unassigned)", variable=self.variant['Disposition'], value='None', bootstyle='toolbutton')
        self.radio_buttons["None"].grid(row=4, column=1, sticky='news', padx=5, pady=5)
        self.radio_buttons["Low VAF"] = tk.Radiobutton(self.frames['left'], text="Low VAF Variants", variable=self.variant['Disposition'], value='Low VAF Variants', bootstyle='toolbutton')
        self.radio_buttons["Low VAF"].grid(row=5, column=1, sticky='news', padx=5, pady=5)
        self.radio_buttons["VUS"] = tk.Radiobutton(self.frames['left'], text="VUS", variable=self.variant['Disposition'], value='VUS', bootstyle='toolbutton')
        self.radio_buttons["VUS"].grid(row=6, column=1, sticky='news', padx=5, pady=5)
        self.radio_buttons["Harmful"] = tk.Radiobutton(self.frames['left'], text="Harmful", variable=self.variant['Disposition'], value='Harmful', bootstyle='toolbutton')
        self.radio_buttons["Harmful"].grid(row=7, column=1, sticky='news', padx=5, pady=5)
        self.radio_buttons["FLT3 ITDs"] = tk.Radiobutton(self.frames['left'], text="FLT3 ITDs", variable=self.variant['Disposition'], value='FLT3 ITDs', bootstyle='toolbutton')
        self.radio_buttons["FLT3 ITDs"].grid(row=8, column=1, sticky='news', padx=5, pady=5)
        self.radio_buttons["Hotspot Exceptions"] = tk.Radiobutton(self.frames['left'], text="Hotspot Exceptions", variable=self.variant['Disposition'], value='Hotspot Exceptions', bootstyle='toolbutton')
        self.radio_buttons["Hotspot Exceptions"].grid(row=9, column=1, sticky='news', padx=5, pady=5)
        # self.radio_buttons["None"].select()

        # Process output files button
        self.buttons['save_disposition'] = tk.Button(self.frames['left'], text="Save Disposition", command=self._event('<<DispoSave>>'), state='disabled')
        self.buttons['save_disposition'].grid(row=10, column=0, columnspan=2, sticky='news', padx=5, pady=5)

        # Basic Information Area
        self.labels["Variant Annotation: Gene"] = tk.Label(self.frames['basic_info_gene'], text="Gene")
        self.labels["Variant Annotation: Gene"].pack(side='top',expand=False,fill='x')
        self.entries["Variant Annotation: Gene"] = tk.Entry(self.frames['basic_info_gene'], width=8, textvariable=self.variant["Variant Annotation: Gene"], font=('bold', 24, 'bold'))
        self.entries["Variant Annotation: Gene"].pack(side='top',expand=True,fill='both')
        self.labels["Original Input: Chrom"] = tk.Label(self.frames['basic_info_chrom'], text="Chromosome")
        self.labels["Original Input: Chrom"].pack(side='top',expand=False, fill='x')
        self.entries["Original Input: Chrom"] = tk.Entry(self.frames['basic_info_chrom'], width=6, textvariable=self.variant["Original Input: Chrom"])
        self.entries["Original Input: Chrom"].pack(side='top',expand=False, fill='x')
        self.labels["Original Input: Pos"] = tk.Label(self.frames['basic_info_chrom'], text="Base Pair")
        self.labels["Original Input: Pos"].pack(side='top',expand=False, fill='x')
        self.entries["Original Input: Pos"] = tk.Entry(self.frames['basic_info_chrom'], width=12, textvariable=self.variant["Original Input: Pos"])
        self.entries["Original Input: Pos"].pack(side='top',expand=False, fill='x')
        self.labels[''] = tk.Label(self.frames['basic_info_changes'], text="DNA Change (c-dot)")
        self.labels[''].pack(side='top',expand=False, fill='x')
        self.entries["Variant Annotation: cDNA change"] = tk.Entry(self.frames['basic_info_changes'], text="C-dot", textvariable=self.variant["Variant Annotation: cDNA change"])
        self.entries["Variant Annotation: cDNA change"].pack(side='top',expand=False, fill='x')
        self.labels[''] = tk.Label(self.frames['basic_info_changes'], text="Protein Change (p-dot)")
        self.labels[''].pack(side='top',expand=False, fill='x')
        self.entries["Variant Annotation: Protein Change"] = tk.Entry(self.frames['basic_info_changes'], text="P-dot", width=24, textvariable=self.variant["Variant Annotation: Protein Change"])
        self.entries["Variant Annotation: Protein Change"].pack(side='top',expand=False, fill='x')
        self.labels[''] = tk.Label(self.frames['basic_info_alleles'], text="Ref Allele", anchor='nw')
        self.labels[''].pack(side='top',expand=False, fill='x')
        self.entries["Original Input: Reference allele"] = tk.Entry(self.frames['basic_info_alleles'], justify=tk.LEFT, textvariable=self.variant["Original Input: Reference allele"])
        self.entries["Original Input: Reference allele"].pack(side='top',expand=False, fill='x')
        self.labels[''] = tk.Label(self.frames['basic_info_alleles'], text="Variant Allele", anchor='w')
        self.labels[''].pack(side='top',expand=False, fill='x')
        self.entries["Original Input: Alternate allele"] = tk.Entry(self.frames['basic_info_alleles'], justify=tk.LEFT, textvariable=self.variant["Original Input: Alternate allele"])
        self.entries["Original Input: Alternate allele"].pack(side='top',expand=False, fill='x')

        self.labels[''] = tk.Label(self.frames['genexys_sb_calc'], text="SB (reported)", anchor='e')
        self.labels[''].grid(column=0, row=0, sticky='news', padx=5)
        self.entries["VCF: STB"] = tk.Entry(self.frames['genexys_sb_calc'], textvariable=self.variant["VCF: STB"])
        self.entries["VCF: STB"].grid(column=1, row=0, sticky='news')
        self.labels[''] = tk.Label(self.frames['genexys_sb_calc'], text="p.", anchor='e')
        self.labels[''].grid(column=2, row=0, sticky='news', padx=5)
        self.entries["VCF: STBP"] = tk.Entry(self.frames['genexys_sb_calc'], textvariable=self.variant["VCF: STBP"], width=5)
        self.entries["VCF: STBP"].grid(column=3, row=0, sticky='news')

        # Genexys strand Bias Area
        self.labels[''] = tk.Label(self.frames['sb_GX'], text='Genexys', width=8)
        self.labels[''].grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['sb_GX'], text='Fwd')
        self.labels[''].grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        self.labels[''] = tk.Label(self.frames['sb_GX'], text='Rev')
        self.labels[''].grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        self.labels[''] = tk.Label(self.frames['sb_GX'], text='Ref', anchor='e')
        self.labels[''].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_GX'], text='Var', anchor='e')
        self.labels[''].grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.entries['VCF: FSRF'] = tk.Entry(self.frames['sb_GX'], textvariable=self.variant["VCF: FSRF"])
        self.entries['VCF: FSRF'].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.entries['VCF: FSRR'] = tk.Entry(self.frames['sb_GX'], textvariable=self.variant["VCF: FSRR"])
        self.entries['VCF: FSRR'].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.entries['VCF: FSAF'] = tk.Entry(self.frames['sb_GX'], textvariable=self.variant["VCF: FSAF"])
        self.entries['VCF: FSAF'].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.entries['VCF: FSAR'] = tk.Entry(self.frames['sb_GX'], textvariable=self.variant["VCF: FSAR"])
        self.entries['VCF: FSAR'].grid(column=3, row=2, sticky='news', pady=5, padx=5)

        # Separator
        tk.Separator(self.frames['sb_GX'], orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)
        # Genexys Stats Area
        self.labels[''] = tk.Label(self.frames['sb_GX_results'], text="Binom. Prop.", anchor='e')
        self.labels[''].grid(column=0, row=0, sticky='news', padx=5)
        self.entries["VCF: Binom Proportion"] = tk.Entry(self.frames['sb_GX_results'], textvariable=self.variant["VCF: Binom Proportion"])
        self.entries["VCF: Binom Proportion"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_GX_results'], text="p.", anchor='e')
        self.labels[''].grid(column=2, row=1, sticky='news')
        self.entries["VCF: Binom P Value"] = tk.Entry(self.frames['sb_GX_results'], textvariable=self.variant["VCF: Binom P Value"], width=5)
        self.entries["VCF: Binom P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_GX_results'], text="Fishers OR", anchor='e')
        self.labels[''].grid(column=0, row=1, sticky='news', padx=5)
        self.entries["VCF: Fisher Odds Ratio"] = tk.Entry(self.frames['sb_GX_results'], textvariable=self.variant["VCF: Fisher Odds Ratio"])
        self.entries["VCF: Fisher Odds Ratio"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_GX_results'], text="p.", anchor='e')
        self.labels[''].grid(column=2, row=0, sticky='news')
        self.entries["VCF: Fisher P Value"] = tk.Entry(self.frames['sb_GX_results'], textvariable=self.variant["VCF: Fisher P Value"], width=5)
        self.entries["VCF: Fisher P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)

        self.labels[''] = tk.Label(self.frames['sb_Q_20'], text='Q20', width=8, anchor='c')
        self.labels[''].grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_20'], text='Fwd')
        self.labels[''].grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_20'], text='Rev')
        self.labels[''].grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_20'], text='Ref', anchor='e')
        self.labels[''].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_20'], text='Var', anchor='e')
        self.labels[''].grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Filtered Reference Forward Read Depth"] = tk.Entry(self.frames['sb_Q_20'], textvariable=self.variant["Mpileup Qual: Filtered Reference Forward Read Depth"])
        self.entries["Mpileup Qual: Filtered Reference Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Filtered Reference Reverse Read Depth"] = tk.Entry(self.frames['sb_Q_20'], textvariable=self.variant["Mpileup Qual: Filtered Reference Reverse Read Depth"])
        self.entries["Mpileup Qual: Filtered Reference Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Filtered Variant Forward Read Depth"] = tk.Entry(self.frames['sb_Q_20'], textvariable=self.variant["Mpileup Qual: Filtered Variant Forward Read Depth"])
        self.entries["Mpileup Qual: Filtered Variant Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Filtered Variant Reverse Read Depth"] = tk.Entry(self.frames['sb_Q_20'], textvariable=self.variant["Mpileup Qual: Filtered Variant Reverse Read Depth"])
        self.entries["Mpileup Qual: Filtered Variant Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)

        # Separator
        tk.Separator(self.frames['sb_Q_20'], orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)

        # Q20 Stats Area
        self.labels[''] = tk.Label(self.frames['sb_Q_20_results'], text="Binom. Prop.", anchor='e')
        self.labels[''].grid(column=0, row=0, sticky='news', padx=5)
        self.entries["Mpileup Qual: Filtered Variant Binomial Proportion"] = tk.Entry(self.frames['sb_Q_20_results'], textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial Proportion"])
        self.entries["Mpileup Qual: Filtered Variant Binomial Proportion"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_20_results'], text="p.", anchor='e')
        self.labels[''].grid(column=2, row=0, sticky='news')
        self.entries["Mpileup Qual: Filtered Variant Binomial P Value"] = tk.Entry(self.frames['sb_Q_20_results'], textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial P Value"], width=5)
        self.entries["Mpileup Qual: Filtered Variant Binomial P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_20_results'], text="Fishers OR", anchor='e')
        self.labels[''].grid(column=0, row=1, sticky='news', padx=5)
        self.entries["Mpileup Qual: Filtered Variant Fishers Odds Ratio"] = tk.Entry(self.frames['sb_Q_20_results'], textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers Odds Ratio"])
        self.entries["Mpileup Qual: Filtered Variant Fishers Odds Ratio"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_20_results'], text="p.", anchor='e')
        self.labels[''].grid(column=2, row=1, sticky='news')
        self.entries["Mpileup Qual: Filtered Variant Fishers P Value"] = tk.Entry(self.frames['sb_Q_20_results'], textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers P Value"], width=5)
        self.entries["Mpileup Qual: Filtered Variant Fishers P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)

        self.labels[''] = tk.Label(self.frames['sb_Q_1'], text='Q1', width=8, anchor='c')
        self.labels[''].grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_1'], text='Fwd')
        self.labels[''].grid(column=2, row=0, sticky='news', pady=(5,0), padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_1'], text='Rev')
        self.labels[''].grid(column=3, row=0, sticky='news', pady=(5,0), padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_1'], text='Ref', anchor='e')
        self.labels[''].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_1'], text='Var', anchor='e')
        self.labels[''].grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Reference Forward Read Depth"] = tk.Entry(self.frames['sb_Q_1'], width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Reference Forward Read Depth"])
        self.entries["Mpileup Qual: Unfiltered Reference Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Reference Reverse Read Depth"] = tk.Entry(self.frames['sb_Q_1'], width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Reference Reverse Read Depth"])
        self.entries["Mpileup Qual: Unfiltered Reference Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Variant Forward Read Depth"] = tk.Entry(self.frames['sb_Q_1'], width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Forward Read Depth"])
        self.entries["Mpileup Qual: Unfiltered Variant Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Variant Reverse Read Depth"] = tk.Entry(self.frames['sb_Q_1'], width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Reverse Read Depth"])
        self.entries["Mpileup Qual: Unfiltered Variant Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)

        # Separator
        tk.Separator(self.frames['sb_Q_1'], orient='horizontal').grid(column=0, row=4, columnspan=4, sticky='ew', pady=5)

        # Q1 Stats Area
        self.labels[''] = tk.Label(self.frames['sb_Q_1_results'], text="Binom. Prop.", anchor='e')
        self.labels[''].grid(column=0, row=0, sticky='news', padx=5)
        self.entries["Mpileup Qual: Unfiltered Variant Binomial Proportion"] = tk.Entry(self.frames['sb_Q_1_results'], textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial Proportion"])
        self.entries["Mpileup Qual: Unfiltered Variant Binomial Proportion"].grid(column=1, row=0, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_1_results'], text="p.", anchor='e')
        self.labels[''].grid(column=2, row=0, sticky='news')
        self.entries["Mpileup Qual: Unfiltered Variant Binomial P Value"] = tk.Entry(self.frames['sb_Q_1_results'], textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial P Value"], width=5)
        self.entries["Mpileup Qual: Unfiltered Variant Binomial P Value"].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_1_results'], text="Fishers OR", anchor='e')
        self.labels[''].grid(column=0, row=1, sticky='news', padx=5)
        self.entries["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"] = tk.Entry(self.frames['sb_Q_1_results'], textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"])
        self.entries["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        self.labels[''] = tk.Label(self.frames['sb_Q_1_results'], text="p.", anchor='e')
        self.labels[''].grid(column=2, row=1, sticky='news')
        self.entries["Mpileup Qual: Unfiltered Variant Fishers P Value"] = tk.Entry(self.frames['sb_Q_1_results'], textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers P Value"], width=5)
        self.entries["Mpileup Qual: Unfiltered Variant Fishers P Value"].grid(column=3, row=1, sticky='news', pady=5, padx=5)

        # gx info top area
        self.labels[''] = tk.Label(self.frames['gx_info'], text="Allele Fraction")
        self.labels[''].grid(row=0, column=0, sticky='news', padx=5)
        self.entries["VCF: AF"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: AF"])
        self.entries["VCF: AF"].grid(row=1, column=0, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['gx_info'], text="Variant Type")
        self.labels[''].grid(row=0, column=1, sticky='news', padx=5)
        self.entries["VCF: TYPE"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: TYPE"])
        self.entries["VCF: TYPE"].grid(row=1, column=1, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['gx_info'], text="Length of Variant (BP)")
        self.labels[''].grid(row=0, column=2, sticky='news', padx=5)
        self.entries["VCF: LEN"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: LEN"])
        self.entries["VCF: LEN"].grid(row=1, column=2, sticky='news', padx=5, pady=5)

        self.labels[''] = tk.Label(self.frames['gx_info'], text="Genotype")
        self.labels[''].grid(row=0, column=3, sticky='news', padx=5)
        self.entries["VCF: Genotype"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: Genotype"])
        self.entries["VCF: Genotype"].grid(row=1, column=3, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['gx_info'], text="Filter (Genexys)")
        self.labels[''].grid(row=0, column=4, sticky='news', padx=5)
        self.entries["VCF: Filter"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: Filter"])
        self.entries["VCF: Filter"].grid(row=1, column=4, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['gx_info'], text="Quality Score")
        self.labels[''].grid(row=0, column=5, sticky='news', padx=5)
        self.entries["VCF: QUAL"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: QUAL"])
        self.entries["VCF: QUAL"].grid(row=1, column=5, rowspan=4, sticky='news', padx=5, pady=5)

        # Separator
        tk.Separator(self.frames['gx_info'], orient='horizontal').grid(row=2, column=0, columnspan=5, sticky='news')

        # gx info bottom area
        self.labels[''] = tk.Label(self.frames['gx_info'], text="FAO")
        self.labels[''].grid(row=3, column=0, sticky='news', padx=5)
        self.entries["VCF: FAO"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: FAO"])
        self.entries["VCF: FAO"].grid(row=4, column=0, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['gx_info'], text="FDP")
        self.labels[''].grid(row=3, column=1, sticky='news', padx=5)
        self.entries["VCF: FDP"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: FDP"])
        self.entries["VCF: FDP"].grid(row=4, column=1, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['gx_info'], text="HRUN")
        self.labels[''].grid(row=3, column=2, sticky='news', padx=5)
        self.entries["VCF: HRUN"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: HRUN"])
        self.entries["VCF: HRUN"].grid(row=4, column=2, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['gx_info'], text="QD")
        self.labels[''].grid(row=3, column=3, sticky='news', padx=5)
        self.entries["VCF: QD"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: QD"])
        self.entries["VCF: QD"].grid(row=4, column=3, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['gx_info'], text="SVTYPE (Unused)")
        self.labels[''].grid(row=3, column=4, sticky='news', padx=5)
        self.entries["VCF: SVTYPE"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: SVTYPE"])
        self.entries["VCF: SVTYPE"].grid(row=4, column=4, sticky='news', padx=5, pady=5)

        self.labels[''] = tk.Label(self.frames['mpl_info'], text="Filtered VAF (Q20)", anchor='e')
        self.labels[''].grid(column=0, row=0, sticky='news', padx=5, pady=5)
        self.entries["Mpileup Qual: Filtered VAF"] = tk.Entry(self.frames['mpl_info'], textvariable=self.variant["Mpileup Qual: Filtered VAF"])
        self.entries["Mpileup Qual: Filtered VAF"].grid(column=1, row=0, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['mpl_info'], text="Unfiltered VAF (Q1)", anchor='e')
        self.labels[''].grid(column=0, row=1, sticky='news', padx=5, pady=5)
        self.entries["Mpileup Qual: Unfiltered VAF"] = tk.Entry(self.frames['mpl_info'], textvariable=self.variant["Mpileup Qual: Unfiltered VAF"])
        self.entries["Mpileup Qual: Unfiltered VAF"].grid(column=1, row=1, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['mpl_info'], text="Total Read Depth", anchor='c')
        self.labels[''].grid(column=2, row=0, sticky='news', padx=5, pady=5)
        self.entries["Mpileup Qual: Read Depth"] = tk.Entry(self.frames['mpl_info'], textvariable=self.variant["Mpileup Qual: Read Depth"])
        self.entries["Mpileup Qual: Read Depth"].grid(column=2, row=1, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['mpl_info'], text="Count: Read Starts")
        self.labels[''].grid(column=3, row=0, sticky='news', padx=5, pady=5)
        self.entries["Mpileup Qual: Start Reads"] = tk.Entry(self.frames['mpl_info'], textvariable=self.variant["Mpileup Qual: Start Reads"])
        self.entries["Mpileup Qual: Start Reads"].grid(column=4, row=0, sticky='news', padx=5, pady=5)
        self.labels[''] = tk.Label(self.frames['mpl_info'], text="Count: Read Ends")
        self.labels[''].grid(column=3, row=1, sticky='news', padx=5, pady=5)
        self.entries["Mpileup Qual: Stop Reads"] = tk.Entry(self.frames['mpl_info'], textvariable=self.variant["Mpileup Qual: Stop Reads"])
        self.entries["Mpileup Qual: Stop Reads"].grid(column=4, row=1, sticky='news', padx=5, pady=5)

        self.labels[''] = tk.Label(self.frames['var_annot'], text="Coding Region")
        self.labels[''].grid(column=0, row=0, sticky='news', padx=5)
        self.entries["Variant Annotation: Coding"] = tk.Entry(self.frames['var_annot'], textvariable=self.variant["Variant Annotation: Coding"])
        self.entries["Variant Annotation: Coding"].grid(column=0, row=1, sticky='news', padx=5)
        self.labels[''] = tk.Label(self.frames['var_annot'], text="Variant Type (Seq. Ontology)")
        self.labels[''].grid(column=1, row=0, sticky='news', padx=5)
        self.entries["Variant Annotation: Sequence Ontology"] = tk.Entry(self.frames['var_annot'], textvariable=self.variant["Variant Annotation: Sequence Ontology"])
        self.entries["Variant Annotation: Sequence Ontology"].grid(column=1, row=1, sticky='news', padx=5)
        self.labels[''] = tk.Label(self.frames['var_annot'], text="Transcript")
        self.labels[''].grid(column=2, row=0, sticky='news', padx=5)
        self.entries["Variant Annotation: Transcript"] = tk.Entry(self.frames['var_annot'], textvariable=self.variant["Variant Annotation: Transcript"])
        self.entries["Variant Annotation: Transcript"].grid(column=2, row=1, sticky='news', padx=5)
        self.labels[''] = tk.Label(self.frames['var_annot'], text="RefSeq")
        self.labels[''].grid(column=3, row=0, sticky='news', padx=5)
        self.entries["Variant Annotation: RefSeq"] = tk.Entry(self.frames['var_annot'], textvariable=self.variant["VCF: LEN"])
        self.entries["Variant Annotation: RefSeq"].grid(column=3, row=1, sticky='news', padx=5)
        self.labels[''] = tk.Label(self.frames['var_annot'], text="All Mappings")
        self.labels[''].grid(column=0, row=2, columnspan=3, sticky='news', padx=5)
        self.textboxes["Variant Annotation: All Mappings"] = tk.ScrolledText(self.frames['var_annot'], height=1)
        self.textboxes["Variant Annotation: All Mappings"].grid(column=0, columnspan=4, row=3, sticky='news', padx=5, pady=(0,5))

        self.labels[''] = tk.Label(self.frames['mdl'], text="Sample Count")
        self.labels[''].grid(column=0, row=0, sticky='news', padx=5)
        self.entries["MDL: Sample Count"] = tk.Entry(self.frames['mdl'], textvariable=self.variant["MDL: Sample Count"])
        self.entries["MDL: Sample Count"].grid(column=0, row=1, sticky='news', padx=5)
        self.labels[''] = tk.Label(self.frames['mdl'], text="Variant Frequency")
        self.labels[''].grid(column=1, row=0, sticky='news', padx=5)
        self.entries["MDL: Variant Frequency"]  = tk.Entry(self.frames['mdl'], textvariable=self.variant["MDL: Variant Frequency"])
        self.entries["MDL: Variant Frequency"].grid(column=1, row=1, sticky='news', padx=5)
        self.labels[''] = tk.Label(self.frames['mdl'], text="Sample List")
        self.labels[''].grid(column=0, columnspan=2, row=2, sticky='news', padx=5)
        self.textboxes["MDL: Sample List"] = tk.ScrolledText(self.frames['mdl'], height=1)
        self.textboxes["MDL: Sample List"].grid(column=0, columnspan=2, row=3, sticky='news', padx=5, pady=(0,5))

        # ClinVar Area
        self.labels['ClinVar: ClinVar ID'] = tk.Label(self.frames['ClinVar: ClinVar ID'], text="ID")
        self.labels['ClinVar: ClinVar ID'].pack(side='top', expand=False, fill='x', padx=5)
        self.entries["ClinVar: ClinVar ID"] = tk.Entry(self.frames['ClinVar: ClinVar ID'], textvariable=self.variant["ClinVar: ClinVar ID"])
        self.entries["ClinVar: ClinVar ID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        self.labels['ClinVar: Clinical Significance'] = tk.Label(self.frames['ClinVar: ClinVar ID'], text="Significance")
        self.labels['ClinVar: Clinical Significance'].pack(side='top', expand=False, fill='x', padx=5)
        self.entries["ClinVar: Clinical Significance"] = tk.Entry(self.frames['ClinVar: ClinVar ID'], textvariable=self.variant["ClinVar: Clinical Significance"])
        self.entries["ClinVar: Clinical Significance"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # PolyPhen Area
        self.labels['gnomAD3: Global AF'] = tk.Label(self.frames['gnomAD3: Global AF'], text="Global AF")
        self.labels['gnomAD3: Global AF'].pack(side='top', expand=False, fill='x', padx=5)
        self.entries["gnomAD3: Global AF"] = tk.Entry(self.frames['gnomAD3: Global AF'], textvariable=self.variant["gnomAD3: Global AF"])
        self.entries["gnomAD3: Global AF"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        self.labels['CADD: Phred'] = tk.Label(self.frames['CADD: Phred'], text="Phred Score")
        self.labels['CADD: Phred'].pack(side='top', expand=False, fill='x', padx=5)
        self.entries["CADD: Phred"] = tk.Entry(self.frames['CADD: Phred'], textvariable=self.variant["CADD: Phred"])
        self.entries["CADD: Phred"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        self.labels['PolyPhen-2: HDIV Prediction'] = tk.Label(self.frames['PolyPhen-2: HDIV Prediction'], text="HDIV")
        self.labels['PolyPhen-2: HDIV Prediction'].pack(side='top', expand=False, fill='x', padx=5)
        self.entries["PolyPhen-2: HDIV Prediction"] = tk.Entry(self.frames['PolyPhen-2: HDIV Prediction'], textvariable=self.variant["PolyPhen-2: HDIV Prediction"])
        self.entries["PolyPhen-2: HDIV Prediction"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # SIFT Area
        self.labels['SIFT: Prediction'] = tk.Label(self.frames['SIFT: Prediction'], text="Prediction")
        self.labels['SIFT: Prediction'].pack(side='top', expand=False, fill='x', padx=5)
        self.entries["SIFT: Prediction"] = tk.Entry(self.frames['SIFT: Prediction'], textvariable=self.variant["SIFT: Prediction"])
        self.entries["SIFT: Prediction"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # dpSNP Area
        self.labels['dbSNP'] = tk.Label(self.frames['dbSNP: rsID'], text="dbSNP")
        self.labels['dbSNP'].pack(side='top', expand=False, fill='both', padx=5)
        self.labels['rsID'] = tk.Label(self.frames['dbSNP: rsID'], text="rsID")
        self.labels['rsID'].pack(side='top', expand=False, fill='both', padx=5)
        self.entries["dbSNP: rsID"] = tk.Entry(self.frames['dbSNP: rsID'], textvariable=self.variant["dbSNP: rsID"])
        self.entries["dbSNP: rsID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # UniProt Area
        self.labels['UniProt (GENE)'] = tk.Label(self.frames['UniProt (GENE): Accession Number'], text="UniProt (Gene)")
        self.labels['UniProt (GENE)'].pack(side='top', expand=False, fill='both', padx=5)
        self.labels['Accession Number'] = tk.Label(self.frames['UniProt (GENE): Accession Number'], text="Accession Number")
        self.labels['Accession Number'].pack(side='top', expand=False, fill='both', padx=5)
        self.entries["UniProt (GENE): Accession Number"] = tk.Entry(self.frames['UniProt (GENE): Accession Number'], textvariable=self.variant["UniProt (GENE): Accession Number"])
        self.entries["UniProt (GENE): Accession Number"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # PhyloP Vertscore Area
        self.labels['PhyloP'] = tk.Label(self.frames['PhyloP: Vert Score'], text="PhyloP")
        self.labels['PhyloP'].pack(side='top', expand=False, fill='both', padx=5)
        self.labels['Vert Score'] = tk.Label(self.frames['PhyloP: Vert Score'], text="Vert Score")
        self.labels['Vert Score'].pack(side='top', expand=False, fill='both', padx=5)
        self.entries["PhyloP: Vert Score"] = tk.Entry(self.frames['PhyloP: Vert Score'], textvariable=self.variant["PhyloP: Vert Score"])
        self.entries["PhyloP: Vert Score"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # COSMIC Area
        self.labels['COSMIC: ID'] = tk.Label(self.frames['COSMIC: ID'], text="ID", anchor='center')
        self.labels['COSMIC: ID'].pack(side='top', expand=False, fill='x', padx=5)
        self.entries["COSMIC: ID"] = tk.Entry(self.frames['COSMIC: ID'], textvariable=self.variant["COSMIC: ID"], width=12)
        self.entries["COSMIC: ID"].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        self.labels['COSMIC: Variant Count'] = tk.Label(self.frames['COSMIC: ID'], text="Count")
        self.labels['COSMIC: Variant Count'].pack(side='top', expand=False, fill='x', padx=5)
        self.entries["COSMIC: Variant Count"] = tk.Entry(self.frames['COSMIC: ID'], textvariable=self.variant["COSMIC: Variant Count"])
        self.entries["COSMIC: Variant Count"].pack(side='top', expand=True, fill='both', padx=5, pady=5)

        # COSMIC Tissue Variant Count Region
        self.textboxes["COSMIC: Variant Count (Tissue)"] = tk.ScrolledText(self.frames['bottom'], height=1)
        self.textboxes["COSMIC: Variant Count (Tissue)"].grid(column=9, row=0, padx=5, pady=5, sticky='news')

        # Status bar
        self.entries['status_bar'] = tk.Entry(parent, textvariable=self.variables['status_bar'])

        self.create_tooltips()
        self.create_weblinks()

        return
    
    def create_frames(self, parent):

        self.frames = dict()

        # Base Frame
        self.frames['base'] = tk.Frame(parent)
        self.frames['base'].pack(expand=True, fill='both',ipadx=10, ipady=10)

        # Left Frame
        self.frames['left'] = tk.Frame(self.frames['base'], bootstyle='secondary')
        self.frames['left'].pack(side='left', expand=False, fill='y',ipadx=10, ipady=10, padx=5, pady=5)
        self.frames['left'].rowconfigure(2, weight=99)

        # Right Frame
        self.frames['right'] = tk.Frame(self.frames['base'])
        self.frames['right'].pack(side='right', expand=True, fill='both',ipadx=10, ipady=10)

        # Basic Info Frame
        self.frames['basic_info'] = tk.Frame(self.frames['right'])
        # self.frames['basic_info'] = tk.LabelFrame(self.frames['right'], text='Locus Info')
        self.frames['basic_info'].pack(side='top', expand=False, fill='x', padx=5, pady=5)

        self.frames['basic_info_gene'] = tk.Frame(self.frames['basic_info'])
        self.frames['basic_info_gene'].pack(side='left',expand=False, fill='both', padx=5, pady=5)
        self.frames['basic_info_chrom'] = tk.Frame(self.frames['basic_info'])
        self.frames['basic_info_chrom'].pack(side='left',expand=False,fill='both', padx=5, pady=5)
        self.frames['basic_info_changes'] = tk.Frame(self.frames['basic_info'])
        self.frames['basic_info_changes'].pack(side='left',expand=False,fill='both', padx=5, pady=5)
        self.frames['basic_info_alleles'] = tk.Frame(self.frames['basic_info'])
        self.frames['basic_info_alleles'].pack(side='left',expand=True,fill='both', padx=5, pady=5)

        # middle frame
        self.frames['middle'] = tk.Frame(self.frames['right'])
        self.frames['middle'].pack(side='top',expand=True,fill='both', padx=5, pady=5)

        # Strand Bias Frame
        self.frames['genexys'] = tk.Frame(self.frames['middle'])
        # self.frames['genexys'] = tk.LabelFrame(self.frames['middle'], text='Strand Bias Data')
        self.frames['genexys'].pack(side='left', expand=False, fill='both', padx=(0,10))
        self.frames['genexys_sb_calc'] = tk.Frame(self.frames['genexys'])
        self.frames['genexys_sb_calc'].pack(side='top', expand=False, fill='both', padx=5, pady=5)
        self.frames['genexys_sb_calc'].rowconfigure(0, weight=1)
        self.frames['genexys_sb_calc'].rowconfigure(1, weight=1)
        self.frames['genexys_sb_calc'].columnconfigure(0, weight=0)
        self.frames['genexys_sb_calc'].columnconfigure(1, weight=5)
        self.frames['genexys_sb_calc'].columnconfigure(2, weight=0)
        self.frames['genexys_sb_calc'].columnconfigure(3, weight=1)

        self.frames['sb_GX'] = tk.Frame(self.frames['genexys'])
        # self.frames['sb_GX'] = tk.LabelFrame(self.frames['genexys'], text="Genexys (calculated)")
        self.frames['sb_GX'].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frames['sb_GX'].rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frames['sb_GX'].columnconfigure(x, weight=1)

        self.frames['sb_GX_results'] = tk.Frame(self.frames['sb_GX'])
        self.frames['sb_GX_results'].grid(column=0, row=5, columnspan=4, sticky='news')
        self.frames['sb_GX_results'].rowconfigure(0, weight=1)
        self.frames['sb_GX_results'].rowconfigure(1, weight=1)
        self.frames['sb_GX_results'].columnconfigure(0, weight=0)
        self.frames['sb_GX_results'].columnconfigure(1, weight=5)
        self.frames['sb_GX_results'].columnconfigure(2, weight=0)
        self.frames['sb_GX_results'].columnconfigure(3, weight=1)

        # Q20 Read Bias Area
        self.frames['sb_Q_20'] = tk.Frame(self.frames['genexys'])
        # self.frames['sb_Q_20'] = tk.LabelFrame(self.frames['genexys'], text="Filtered M-Pileup (calculated)")
        self.frames['sb_Q_20'].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frames['sb_Q_20'].rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frames['sb_Q_20'].columnconfigure(x, weight=1)

        self.frames['sb_Q_20_results'] = tk.Frame(self.frames['sb_Q_20'])
        self.frames['sb_Q_20_results'].grid(column=0, row=5, columnspan=4, sticky='news')
        self.frames['sb_Q_20_results'].rowconfigure(0, weight=1)
        self.frames['sb_Q_20_results'].rowconfigure(1, weight=1)
        self.frames['sb_Q_20_results'].columnconfigure(0, weight=0)
        self.frames['sb_Q_20_results'].columnconfigure(1, weight=5)
        self.frames['sb_Q_20_results'].columnconfigure(2, weight=0)
        self.frames['sb_Q_20_results'].columnconfigure(3, weight=1)

        # Q1 Read Bias Area
        self.frames['sb_Q_1'] = tk.Frame(self.frames['genexys'])
        # self.frames['sb_Q_1'] = tk.LabelFrame(self.frames['genexys'], text="Unfiltered M-Pileup (calculated)")
        self.frames['sb_Q_1'].pack(side='top', expand=True, fill='both', padx=5, pady=5)
        for x in range(3):
            self.frames['sb_Q_1'].rowconfigure(x, weight=1)
        for x in range(2,4):
            self.frames['sb_Q_1'].columnconfigure(x, weight=1)

        self.frames['sb_Q_1_results'] = tk.Frame(self.frames['sb_Q_1'])
        self.frames['sb_Q_1_results'].grid(column=0, row=5, columnspan=4, sticky='news')
        self.frames['sb_Q_1_results'].rowconfigure(0, weight=1)
        self.frames['sb_Q_1_results'].rowconfigure(1, weight=1)
        self.frames['sb_Q_1_results'].columnconfigure(0, weight=0)
        self.frames['sb_Q_1_results'].columnconfigure(1, weight=5)
        self.frames['sb_Q_1_results'].columnconfigure(2, weight=0)
        self.frames['sb_Q_1_results'].columnconfigure(3, weight=1)

        # Genexys info frame
        self.frames['gx_info'] = tk.Frame(self.frames['middle'])
        # self.frames['gx_info'] = tk.LabelFrame(self.frames['middle'], text='Genexys Information')
        self.frames['gx_info'].pack(side='top', expand=False, fill='both', pady=(0,5))
        for x in range(1,5,2):
            self.frames['gx_info'].rowconfigure(x, weight=1)
        for x in range(6):
            self.frames['gx_info'].columnconfigure(x, weight=1)

        # mpileup info frame
        self.frames['mpl_info'] = tk.Frame(self.frames['middle'])
        # self.frames['mpl_info'] = tk.LabelFrame(self.frames['middle'], text='M-Pileup Information')
        self.frames['mpl_info'].pack(side='top', expand=False, fill='both', pady=5)
        for x in [1,2,4]:
            self.frames['mpl_info'].columnconfigure(x, weight=1)
        for x in range(2):
            self.frames['mpl_info'].rowconfigure(x, weight=1)

        # Variant Annotation Info Frame
        self.frames['other'] = tk.Frame(self.frames['middle'])
        self.frames['other'].pack(side='top',expand=True, fill='both')
        self.frames['var_annot'] = tk.Frame(self.frames['other'])
        # self.frames['var_annot'] = tk.LabelFrame(self.frames['other'], text='Variant Annotation')
        self.frames['var_annot'].pack(side='left',expand=True, fill='both', padx=(0,5))
        for x in range(4):
            self.frames['var_annot'].columnconfigure(x, weight=1)
        self.frames['var_annot'].rowconfigure(3, weight=99)

        # MDL Info area
        self.frames['mdl'] = tk.Frame(self.frames['other'])
        # self.frames['mdl'] = tk.LabelFrame(self.frames['other'], text='MDL Info')
        self.frames['mdl'].pack(side='left',expand=True, fill='both', padx=(5,0))
        self.frames['mdl'].rowconfigure(3, weight=99)
        self.frames['mdl'].columnconfigure(0, weight=1)
        self.frames['mdl'].columnconfigure(1, weight=1)

        # Web Resources Stats
        self.frames['bottom'] = tk.Frame(self.frames['right'])
        # self.frames['bottom'] = tk.LabelFrame(self.frames['right'], text='Database Information')
        self.frames['bottom'].pack(side='bottom', expand=False, fill='both', padx=5, pady=5)
        for x in range(10):
            self.frames['bottom'].columnconfigure(x, weight=1)

        # Clinvar Area
        self.frames['ClinVar: ClinVar ID'] = tk.Frame(self.frames['bottom'])
        # self.frames['web_clinvar'] = tk.LabelFrame(self.frames['bottom'], text='ClinVar')
        self.frames['ClinVar: ClinVar ID'].grid(column=0, row=0, padx=5, pady=5, sticky='news')

        # Gnomad Area
        self.frames['gnomAD3: Global AF'] = tk.Frame(self.frames['bottom'])
        # self.frames['web_gnomad'] = tk.LabelFrame(self.frames['bottom'], text='GnomAD')
        self.frames['gnomAD3: Global AF'].grid(column=1, row=0, padx=5, pady=5, sticky='news')

        # CADD Area
        self.frames['CADD: Phred'] = tk.Frame(self.frames['bottom'])
        # self.frames['web_cadd'] = tk.LabelFrame(self.frames['bottom'], text='CADD')
        self.frames['CADD: Phred'].grid(column=2, row=0, padx=5, pady=5, sticky='news')

        # PolyPhen Area
        self.frames['PolyPhen-2: HDIV Prediction'] = tk.Frame(self.frames['bottom'])
        # self.frames['web_polyphen'] = tk.LabelFrame(self.frames['bottom'], text='PolyPhen-2')
        self.frames['PolyPhen-2: HDIV Prediction'].grid(column=3, row=0, padx=5, pady=5, sticky='news')

        # SIFT Area
        self.frames['SIFT: Prediction'] = tk.Frame(self.frames['bottom'])
        # self.frames['SIFT: Prediction'] = tk.LabelFrame(self.frames['bottom'], text='SIFT')
        self.frames['SIFT: Prediction'].grid(column=4, row=0, padx=5, pady=5, sticky='news')

        # dbSNP Area
        self.frames['dbSNP: rsID'] = tk.Frame(self.frames['bottom'])
        # self.frames['dbSNP: rsID'] = tk.LabelFrame(self.frames['bottom'], text='dbSNP')
        self.frames['dbSNP: rsID'].grid(column=5, row=0, padx=5, pady=5, sticky='news')

        # UniProt Area
        self.frames['UniProt (GENE): Accession Number'] = tk.Frame(self.frames['bottom'])
        # self.frames['UniProt (GENE): Accession Number'] = tk.LabelFrame(self.frames['bottom'], text='UniProt (GENE)')
        self.frames['UniProt (GENE): Accession Number'].grid(column=6, row=0, padx=5, pady=5, sticky='news')

        # PhyloP Vertscore Area
        self.frames['PhyloP: Vert Score'] = tk.Frame(self.frames['bottom'])
        # self.frames['web_dbsnp'] = tk.LabelFrame(self.frames['bottom'], text='PhyloP')
        self.frames['PhyloP: Vert Score'].grid(column=7, row=0, padx=5, pady=5, sticky='news')

        # COSMIC Area
        self.frames['COSMIC: ID'] = tk.Frame(self.frames['bottom'])
        # self.frames['web_cosmic'] = tk.LabelFrame(self.frames['bottom'], text='COSMIC')
        self.frames['COSMIC: ID'].grid(column=8, row=0, padx=5, pady=5, sticky='news')


        return

    def create_tooltips(self):
        # Create tooltips for labels
        for key,value in TOOLTIPS.items():
            if type(self.labels[key]) is type(dict()):
                pass
            else:
                CreateToolTip(self.labels[key], value)
        return
    
    def create_weblinks(self):
        for label in VALIDATION['web_links'].keys():
            self.labels[label].configure(cursor='hand2')
        return

    def load_file(self):
        self.variables['filename'].set(str(fd.askopenfilename(filetypes=[('XLSX','*.xlsx')])))
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
            self.treeviews['variant_list'].insert('', tk.END, values=values_list, tags=(str(variant['Disposition'])).replace(" ","_"))
        self.treeviews['variant_list'].selection_set(self.treeviews['variant_list'].get_children()[0])
        # self.count_dispositions()
        return
    
    def clear_view(self, *args, **kwargs):
        for item in self.treeviews['variant_list'].get_children():
            self.treeviews['variant_list'].delete(item)
        for x in VCF_FIELDS:
            self.variant[x].set("")
            self.labels[x].configure(bootstyle='normal.TLabel')
        self.variant['Disposition'].set(0)
        # self.variables = dict()
        self.variables['filename'].set("")
        self.variables['status_bar'].set("Records view cleared.")
        # for x in DISPOSITIONS:
        #     self.variables['Disposition'][x] = 0
        return
 
    def record_selected(self, *args, **kwargs):
        for selected_item in self.treeviews['variant_list'].selection():
            item = self.treeviews['variant_list'].item(selected_item)
            record = item['values']
            for x in range(len(VCF_FIELDS)):
                self.variant[VCF_FIELDS[x]].set(record[x])
        self.variables['selection_index'].set(self.treeviews['variant_list'].index(self.treeviews['variant_list'].focus()))
        try:
            self.variant['Disposition'].set(record[-1])  # Disposition needs to always be last
        except:
            pass
        if self.variant['Disposition'].get():
            self.buttons['save_disposition']['state'] = 'normal'
        try:
            self.validate_cells()
        except:
            pass
        self.textboxes['COSMIC: Variant Count (Tissue)'].delete("1.0", tk.END)
        self.textboxes['COSMIC: Variant Count (Tissue)'].insert(tk.END, self.variant["COSMIC: Variant Count (Tissue)"].get())
        self.textboxes['MDL: Sample List'].delete("1.0", tk.END)
        self.textboxes['MDL: Sample List'].insert(tk.END, self.variant["COSMIC: Variant Count (Tissue)"].get())
        self.textboxes['Variant Annotation: All Mappings'].delete("1.0", tk.END)
        self.textboxes['Variant Annotation: All Mappings'].insert(tk.END, self.variant["COSMIC: Variant Count (Tissue)"].get())
        return

    def validate_cells(self):

        for x in VCF_FIELDS:
            self.entries[x].configure(bootstyle='normal')
            if self.variant[x].get() == "None":
                self.entries[x].configure(bootstyle='readonly')
                continue
            if x in VALIDATION['p_values']:
                try:
                    if float(self.variant[x].get()) > VALIDATION['cutoffs']['p_value']:
                        self.entries[x].configure(bootstyle='danger')
                except:
                    pass
            if x in VALIDATION['strand_read_depth']:
                try:
                    if int(self.variant[x].get()) <= VALIDATION['cutoffs']['strand_read_depth']:
                        self.entries[x].configure(bootstyle='danger')
                except:
                    pass
            if x in VALIDATION['locus_read_depth']:
                try:
                    if int(self.variant[x].get()) <= VALIDATION['cutoffs']['locus_read_depth']:
                        self.entries[x].configure(bootstyle='danger')
                except:
                    pass
            if x in VALIDATION['minimum_vaf']:
                try:
                    if float(self.variant[x].get()) < VALIDATION['cutoffs']['vaf_threshold']:
                        self.entries[x].configure(bootstyle='danger')
                except:
                    pass
            if x in VALIDATION['web_links'].keys():
                self.entries[x].configure(bootstyle = 'info')
        return


# MAIN LOOP ----------------------------------------------

def main():
    pass
    return

if __name__ == '__main__':
    main()