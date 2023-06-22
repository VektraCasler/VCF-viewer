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
        self.frames = dict()

        # Base Frame
        self.frames['base'] = tk.Frame(parent)
        self.frames['base'].pack(expand=True, fill='both',ipadx=10, ipady=10)

        # Left Frame
        self.frames['left'] = tk.Frame(self.frames['base'], bootstyle='secondary')
        self.frames['left'].pack(side='left', expand=False, fill='y', padx=5, pady=5)
        self.frames['left'].rowconfigure(3, weight=99)
        self.labels['file_info_label'] = tk.Label(self.frames['left'], text="VCF File Information", bootstyle='info.inverse', anchor='c')
        self.labels['file_info_label'].grid(row=0, column=0, columnspan=2, sticky='news', padx=5, pady=5)

        #File load button
        self.entries['filename'] = tk.Entry(self.frames['left'], textvariable=self.variables['filename'], width=24)
        self.entries['filename'].grid(row=1, column=0, columnspan=2, sticky='news', padx=5, pady=5)
        self.buttons['load_file'] = tk.Button(self.frames['left'], text="Open a File", command=self._event('<<FileLoad>>'))
        self.buttons['load_file'].grid(row=2, column=0, columnspan=2, sticky='news', padx=5, pady=5)

        # Treeview list
        view_columns = VCF_FIELDS
        view_columns.append('Disposition')
        self.treeviews['variant_list'] = tk.Treeview(self.frames['left'], columns=view_columns, displaycolumns=[4,69], selectmode='browse', show='headings')
        # self.treeviews['variant_list'] = tk.tableview.Tableview(self.frames['treeview'], coldata=VCF_FIELDS, displaycolumns=[5,0], selectmode='browse', show='headings')
        for x in VCF_FIELDS:
            self.treeviews['variant_list'].heading(x, text=x, anchor='center')
        self.treeviews['variant_list'].column(column=4, width=120, anchor='center')
        self.treeviews['variant_list'].column(column=69, width=140, anchor='center')
        self.treeviews['variant_list'].grid(row=3, column=0, columnspan=2, sticky='news', padx=5, pady=5)
        self.treeviews['variant_list'].bind('<<TreeviewSelect>>', self.record_selected)
        self.treeviews['variant_list'].tag_configure('None', background="#c4c4c4")
        self.treeviews['variant_list'].tag_configure('Hotspot_Exceptions', background="#f92134")
        self.treeviews['variant_list'].tag_configure('VUS', background="#f0aa44")
        self.treeviews['variant_list'].tag_configure('Low_VAF_Variants', background="#70aaff")
        self.treeviews['variant_list'].tag_configure('Harmful', background="#fc6622")
        self.treeviews['variant_list'].tag_configure('FLT3_ITDs', background="#f794fa")

        # Treeview Scrollbar
        self.scrollbars['variant_list'] = tk.Scrollbar(self.frames['left'], orient=tk.VERTICAL, command=self.treeviews['variant_list'].yview)
        self.treeviews['variant_list'].configure(yscroll=self.scrollbars['variant_list'].set)
        self.scrollbars['variant_list'].grid(row=3, column=1, sticky='nes')

        # Disposition labels
        self.labels['disposition_label'] = tk.Label(self.frames['left'], text="Assign Disposition", bootstyle='secondary.inverse', anchor='c')
        self.labels['disposition_label'].grid(row=4, column=0, columnspan=2, sticky='news', padx=5, pady=5)
        self.entries["None"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['None'], width=5)
        self.entries["None"].grid(row=5, column=0, sticky='news', padx=5, pady=5)
        self.entries["Low VAF Variants"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['Low VAF Variants'], width=5)
        self.entries["Low VAF Variants"].grid(row=6, column=0, sticky='news', padx=5, pady=5)
        self.entries["VUS"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['VUS'], width=5)
        self.entries["VUS"].grid(row=7, column=0, sticky='news', padx=5, pady=5)
        self.entries["Harmful"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['Harmful'], width=5)
        self.entries["Harmful"].grid(row=8, column=0, sticky='news', padx=5, pady=5)
        self.entries["FLT3 ITDs"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['FLT3 ITDs'], width=5)
        self.entries["FLT3 ITDs"].grid(row=9, column=0, sticky='news', padx=5, pady=5)
        self.entries["Hotspot Exceptions"] = tk.Entry(self.frames['left'], textvariable=self.variables['Disposition']['Hotspot Exceptions'], width=5)
        self.entries["Hotspot Exceptions"].grid(row=10, column=0, sticky='news', padx=5, pady=5)

        # Radio buttons for disposition
        self.radio_buttons["None"] = tk.Radiobutton(self.frames['left'], text="None (Unassigned)", variable=self.variant['Disposition'], value='None', bootstyle='toolbutton')
        self.radio_buttons["None"].grid(row=5, column=1, sticky='news', padx=5, pady=5)
        self.radio_buttons["Low VAF"] = tk.Radiobutton(self.frames['left'], text="Low VAF Variants", variable=self.variant['Disposition'], value='Low VAF Variants', bootstyle='toolbutton')
        self.radio_buttons["Low VAF"].grid(row=6, column=1, sticky='news', padx=5, pady=5)
        self.radio_buttons["VUS"] = tk.Radiobutton(self.frames['left'], text="VUS", variable=self.variant['Disposition'], value='VUS', bootstyle='toolbutton')
        self.radio_buttons["VUS"].grid(row=7, column=1, sticky='news', padx=5, pady=5)
        self.radio_buttons["Harmful"] = tk.Radiobutton(self.frames['left'], text="Harmful", variable=self.variant['Disposition'], value='Harmful', bootstyle='toolbutton')
        self.radio_buttons["Harmful"].grid(row=8, column=1, sticky='news', padx=5, pady=5)
        self.radio_buttons["FLT3 ITDs"] = tk.Radiobutton(self.frames['left'], text="FLT3 ITDs", variable=self.variant['Disposition'], value='FLT3 ITDs', bootstyle='toolbutton')
        self.radio_buttons["FLT3 ITDs"].grid(row=9, column=1, sticky='news', padx=5, pady=5)
        self.radio_buttons["Hotspot Exceptions"] = tk.Radiobutton(self.frames['left'], text="Hotspot Exceptions", variable=self.variant['Disposition'], value='Hotspot Exceptions', bootstyle='toolbutton')
        self.radio_buttons["Hotspot Exceptions"].grid(row=10, column=1, sticky='news', padx=5, pady=5)

        # Process output files button
        self.buttons['save_disposition'] = tk.Button(self.frames['left'], text="Save Disposition", command=self._event('<<DispoSave>>'), state='disabled')
        self.buttons['save_disposition'].grid(row=11, column=0, columnspan=2, sticky='news', padx=5, pady=5)

        # Right Frame
        self.frames['right'] = tk.Frame(self.frames['base'])
        self.frames['right'].pack(side='right', expand=True, fill='both')

        # Basic Information Area
        self.frames['basic_info'] = tk.Frame(self.frames['right'], bootstyle='secondary')
        self.frames['basic_info'].pack(side='top', expand=False, fill='x', padx=5, pady=5)
        for x in range(4):
            self.frames['basic_info'].columnconfigure(x, weight=1)
        self.labels['basic_info_frame_label'] = tk.Label(self.frames['basic_info'], text="Basic Genetic Information", anchor='c')
        self.labels['basic_info_frame_label'].grid(row=0, column=0, columnspan=4, sticky='news', padx=5, pady=5)
        self.labels["Variant Annotation: Gene"] = tk.Label(self.frames['basic_info'], text="Gene")
        self.labels["Variant Annotation: Gene"].grid(row=1, column=0, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.entries["Variant Annotation: Gene"] = tk.Entry(self.frames['basic_info'], width=8, textvariable=self.variant["Variant Annotation: Gene"], font=('bold', 24, 'bold'))
        self.entries["Variant Annotation: Gene"].grid(row=2, column=0, rowspan=3, columnspan=1, sticky='news', padx=5, pady=5)
        self.labels["Original Input: Chrom"] = tk.Label(self.frames['basic_info'], text="Chromosome")
        self.labels["Original Input: Chrom"].grid(row=1, column=1, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.entries["Original Input: Chrom"] = tk.Entry(self.frames['basic_info'], width=6, textvariable=self.variant["Original Input: Chrom"])
        self.entries["Original Input: Chrom"].grid(row=2, column=1, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.labels["Original Input: Pos"] = tk.Label(self.frames['basic_info'], text="Base Pair")
        self.labels["Original Input: Pos"].grid(row=3, column=1, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.entries["Original Input: Pos"] = tk.Entry(self.frames['basic_info'], width=12, textvariable=self.variant["Original Input: Pos"])
        self.entries["Original Input: Pos"].grid(row=4, column=1, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.labels['Variant Annotation: cDNA change'] = tk.Label(self.frames['basic_info'], text="DNA Change (c-dot)")
        self.labels['Variant Annotation: cDNA change'].grid(row=1, column=2, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.entries["Variant Annotation: cDNA change"] = tk.Entry(self.frames['basic_info'], text="C-dot", textvariable=self.variant["Variant Annotation: cDNA change"])
        self.entries["Variant Annotation: cDNA change"].grid(row=2, column=2, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.labels['Variant Annotation: Protein Change'] = tk.Label(self.frames['basic_info'], text="Protein Change (p-dot)")
        self.labels['Variant Annotation: Protein Change'].grid(row=3, column=2, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.entries["Variant Annotation: Protein Change"] = tk.Entry(self.frames['basic_info'], text="P-dot", width=24, textvariable=self.variant["Variant Annotation: Protein Change"])
        self.entries["Variant Annotation: Protein Change"].grid(row=4, column=2, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.labels['Original Input: Reference allele'] = tk.Label(self.frames['basic_info'], text="Ref Allele", anchor='nw')
        self.labels['Original Input: Reference allele'].grid(row=1, column=3, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.entries["Original Input: Reference allele"] = tk.Entry(self.frames['basic_info'], justify=tk.LEFT, textvariable=self.variant["Original Input: Reference allele"])
        self.entries["Original Input: Reference allele"].grid(row=2, column=3, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.labels['Original Input: Alternate allele'] = tk.Label(self.frames['basic_info'], text="Variant Allele", anchor='w')
        self.labels['Original Input: Alternate allele'].grid(row=3, column=3, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)
        self.entries["Original Input: Alternate allele"] = tk.Entry(self.frames['basic_info'], justify=tk.LEFT, textvariable=self.variant["Original Input: Alternate allele"])
        self.entries["Original Input: Alternate allele"].grid(row=4, column=3, rowspan=1, columnspan=1, sticky='news', padx=5, pady=5)

        # middle frame
        self.frames['middle'] = tk.Frame(self.frames['right'])
        self.frames['middle'].pack(side='top',expand=True,fill='both')

        # Strand Bias Frame
        self.frames['strand_bias'] = tk.Frame(self.frames['middle'], bootstyle='secondary')
        self.frames['strand_bias'].pack(side='left', expand=False, fill='both', padx=5, pady=5)
        for x in range(12):
            self.frames['strand_bias'].rowconfigure(x, weight=1)
        for x in range(4):
            self.frames['strand_bias'].columnconfigure(x, weight=1)        
        self.labels['sb_frame_label'] = tk.Label(self.frames['strand_bias'], text="Strand Bias Information", anchor='c')
        self.labels['sb_frame_label'].grid(column=0, row=0, columnspan=4, sticky='news', padx=5, pady=5)
        self.labels['VCF: STB'] = tk.Label(self.frames['strand_bias'], text="SB (reported)")
        self.labels['VCF: STB'].grid(column=0, row=1, sticky='news', padx=5, pady=5)
        self.entries["VCF: STB"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["VCF: STB"])
        self.entries["VCF: STB"].grid(column=1, row=1, sticky='news', padx=5, pady=5)
        self.labels['VCF: STBP'] = tk.Label(self.frames['strand_bias'], text="p.", width=3)
        self.labels['VCF: STBP'].grid(column=2, row=1, sticky='news', padx=5, pady=5)
        self.entries["VCF: STBP"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["VCF: STBP"])
        self.entries["VCF: STBP"].grid(column=3, row=1, sticky='news', padx=5, pady=5)

        # Genexus Strand Bias Chi Square Area
        self.frames['GX_sb_chi_square'] = tk.Frame(self.frames['strand_bias'], bootstyle='secondary')
        self.frames['GX_sb_chi_square'].grid(column=0, row=2, columnspan=4, sticky='news', pady=5, padx=5)
        for x in range(3):
            self.frames['GX_sb_chi_square'].rowconfigure(x, weight=1)
        for x in range(4):
            self.frames['GX_sb_chi_square'].columnconfigure(x, weight=1)
        self.labels['Genexus'] = tk.Label(self.frames['GX_sb_chi_square'], anchor='c', text='Genexus', width=8)
        self.labels['Genexus'].grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        self.labels['gx_fwd'] = tk.Label(self.frames['GX_sb_chi_square'], text='Fwd', width=3, anchor='c')
        self.labels['gx_fwd'].grid(column=2, row=0, sticky='news', padx=5, pady=5)
        self.labels['gx_rev'] = tk.Label(self.frames['GX_sb_chi_square'], text='Rev', width=3, anchor='c')
        self.labels['gx_rev'].grid(column=3, row=0, sticky='news', padx=5, pady=5)
        self.labels['gx_ref'] = tk.Label(self.frames['GX_sb_chi_square'], text='Ref', width=3, anchor='c')
        self.labels['gx_ref'].grid(column=1, row=1, sticky='news', padx=5, pady=5)
        self.labels['gx_var'] = tk.Label(self.frames['GX_sb_chi_square'], text='Var', width=3, anchor='c')
        self.labels['gx_var'].grid(column=1, row=2, sticky='news', padx=5, pady=5)        
        self.entries['VCF: FSRF'] = tk.Entry(self.frames['GX_sb_chi_square'], textvariable=self.variant["VCF: FSRF"], width=3)
        self.entries['VCF: FSRF'].grid(column=2, row=1, sticky='news', padx=5, pady=5)
        self.entries['VCF: FSRR'] = tk.Entry(self.frames['GX_sb_chi_square'], textvariable=self.variant["VCF: FSRR"], width=3)
        self.entries['VCF: FSRR'].grid(column=3, row=1, sticky='news', padx=5, pady=5)
        self.entries['VCF: FSAF'] = tk.Entry(self.frames['GX_sb_chi_square'], textvariable=self.variant["VCF: FSAF"], width=3)
        self.entries['VCF: FSAF'].grid(column=2, row=2, sticky='news', padx=5, pady=5)
        self.entries['VCF: FSAR'] = tk.Entry(self.frames['GX_sb_chi_square'], textvariable=self.variant["VCF: FSAR"], width=3)
        self.entries['VCF: FSAR'].grid(column=3, row=2, sticky='news', padx=5, pady=5)
        # Genexus Stats Area
        self.labels['VCF: Binom Proportion'] = tk.Label(self.frames['strand_bias'], text="Binom. Prop.", anchor='e')
        self.labels['VCF: Binom Proportion'].grid(column=0, row=3, sticky='news', padx=5)
        self.entries["VCF: Binom Proportion"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["VCF: Binom Proportion"])
        self.entries["VCF: Binom Proportion"].grid(column=1, row=3, sticky='news', pady=5, padx=5)
        self.labels['VCF: Binom P Value'] = tk.Label(self.frames['strand_bias'], text="p.", anchor='e')
        self.labels['VCF: Binom P Value'].grid(column=2, row=3, sticky='news')
        self.entries["VCF: Binom P Value"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["VCF: Binom P Value"], width=3)
        self.entries["VCF: Binom P Value"].grid(column=3, row=3, sticky='news', pady=5, padx=5)
        self.labels['VCF: Fisher Odds Ratio'] = tk.Label(self.frames['strand_bias'], text="Fishers OR", anchor='e')
        self.labels['VCF: Fisher Odds Ratio'].grid(column=0, row=4, sticky='news', padx=5)
        self.entries["VCF: Fisher Odds Ratio"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["VCF: Fisher Odds Ratio"])
        self.entries["VCF: Fisher Odds Ratio"].grid(column=1, row=4, sticky='news', pady=5, padx=5)
        self.labels['VCF: Fisher P Value'] = tk.Label(self.frames['strand_bias'], text="p.", anchor='e')
        self.labels['VCF: Fisher P Value'].grid(column=2, row=4, sticky='news')
        self.entries["VCF: Fisher P Value"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["VCF: Fisher P Value"], width=3)
        self.entries["VCF: Fisher P Value"].grid(column=3, row=4, sticky='news', pady=5, padx=5)

        # Q20 Strand Bias Chi Square Area
        self.frames['Q20_sb_chi_square'] = tk.Frame(self.frames['strand_bias'], bootstyle='secondary')
        self.frames['Q20_sb_chi_square'].grid(column=0, row=5, columnspan=4, rowspan=1, sticky='news', padx=5, pady=5)
        for x in range(3):
            self.frames['Q20_sb_chi_square'].rowconfigure(x, weight=1)
        for x in range(4):
            self.frames['Q20_sb_chi_square'].columnconfigure(x, weight=1)
        self.labels['Q20'] = tk.Label(self.frames['Q20_sb_chi_square'], text='Q20', width=8, anchor='c')
        self.labels['Q20'].grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        self.labels['Q20_fwd'] = tk.Label(self.frames['Q20_sb_chi_square'], text='Fwd', anchor='c', width=3)
        self.labels['Q20_fwd'].grid(column=2, row=0, sticky='news', pady=5, padx=5)
        self.labels['Q20_rev'] = tk.Label(self.frames['Q20_sb_chi_square'], text='Rev', anchor='c', width=3)
        self.labels['Q20_rev'].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        self.labels['Q20_ref'] = tk.Label(self.frames['Q20_sb_chi_square'], text='Ref', anchor='c', width=3)
        self.labels['Q20_ref'].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        self.labels['Q20_var'] = tk.Label(self.frames['Q20_sb_chi_square'], text='Var', anchor='c', width=3)
        self.labels['Q20_var'].grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Filtered Reference Forward Read Depth"] = tk.Entry(self.frames['Q20_sb_chi_square'], textvariable=self.variant["Mpileup Qual: Filtered Reference Forward Read Depth"])
        self.entries["Mpileup Qual: Filtered Reference Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Filtered Reference Reverse Read Depth"] = tk.Entry(self.frames['Q20_sb_chi_square'], textvariable=self.variant["Mpileup Qual: Filtered Reference Reverse Read Depth"])
        self.entries["Mpileup Qual: Filtered Reference Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Filtered Variant Forward Read Depth"] = tk.Entry(self.frames['Q20_sb_chi_square'], textvariable=self.variant["Mpileup Qual: Filtered Variant Forward Read Depth"])
        self.entries["Mpileup Qual: Filtered Variant Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Filtered Variant Reverse Read Depth"] = tk.Entry(self.frames['Q20_sb_chi_square'], textvariable=self.variant["Mpileup Qual: Filtered Variant Reverse Read Depth"])
        self.entries["Mpileup Qual: Filtered Variant Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)
        # Q20 Strand Bias Stats Area
        self.labels['Mpileup Qual: Filtered Variant Binomial Proportion'] = tk.Label(self.frames['strand_bias'], text="Binom. Prop.", anchor='e')
        self.labels['Mpileup Qual: Filtered Variant Binomial Proportion'].grid(column=0, row=6, sticky='news', padx=5)
        self.entries["Mpileup Qual: Filtered Variant Binomial Proportion"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial Proportion"])
        self.entries["Mpileup Qual: Filtered Variant Binomial Proportion"].grid(column=1, row=6, sticky='news', pady=5, padx=5)
        self.labels['Mpileup Qual: Filtered Variant Binomial P Value'] = tk.Label(self.frames['strand_bias'], text="p.", anchor='e')
        self.labels['Mpileup Qual: Filtered Variant Binomial P Value'].grid(column=2, row=6, sticky='news')
        self.entries["Mpileup Qual: Filtered Variant Binomial P Value"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["Mpileup Qual: Filtered Variant Binomial P Value"], width=5)
        self.entries["Mpileup Qual: Filtered Variant Binomial P Value"].grid(column=3, row=6, sticky='news', pady=5, padx=5)
        self.labels['Mpileup Qual: Filtered Variant Fishers Odds Ratio'] = tk.Label(self.frames['strand_bias'], text="Fishers OR", anchor='e')
        self.labels['Mpileup Qual: Filtered Variant Fishers Odds Ratio'].grid(column=0, row=7, sticky='news', padx=5)
        self.entries["Mpileup Qual: Filtered Variant Fishers Odds Ratio"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers Odds Ratio"])
        self.entries["Mpileup Qual: Filtered Variant Fishers Odds Ratio"].grid(column=1, row=7, sticky='news', pady=5, padx=5)
        self.labels['Mpileup Qual: Filtered Variant Fishers P Value'] = tk.Label(self.frames['strand_bias'], text="p.", anchor='e')
        self.labels['Mpileup Qual: Filtered Variant Fishers P Value'].grid(column=2, row=7, sticky='news')
        self.entries["Mpileup Qual: Filtered Variant Fishers P Value"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers P Value"], width=5)
        self.entries["Mpileup Qual: Filtered Variant Fishers P Value"].grid(column=3, row=7, sticky='news', pady=5, padx=5)

        # Q1 Strand Bias Chi Square Area
        self.frames['Q1_sb_chi_square'] = tk.Frame(self.frames['strand_bias'], bootstyle='secondary')
        self.frames['Q1_sb_chi_square'].grid(column=0, row=8, columnspan=4, rowspan=1, sticky='news', padx=5, pady=5)
        for x in range(3):
            self.frames['Q1_sb_chi_square'].rowconfigure(x, weight=1)
        for x in range(4):
            self.frames['Q1_sb_chi_square'].columnconfigure(x, weight=1)
        self.labels['Q1'] = tk.Label(self.frames['Q1_sb_chi_square'], text='Q1', width=8, anchor='c')
        self.labels['Q1'].grid(column=0, row=0, rowspan=3, sticky='news', padx=5, pady=5)
        self.labels['Q1_fwd'] = tk.Label(self.frames['Q1_sb_chi_square'], text='Fwd', anchor='c')
        self.labels['Q1_fwd'].grid(column=2, row=0, sticky='news', pady=5, padx=5)
        self.labels['Q1_rev'] = tk.Label(self.frames['Q1_sb_chi_square'], text='Rev', anchor='c')
        self.labels['Q1_rev'].grid(column=3, row=0, sticky='news', pady=5, padx=5)
        self.labels['Q1_ref'] = tk.Label(self.frames['Q1_sb_chi_square'], text='Ref', anchor='c')
        self.labels['Q1_ref'].grid(column=1, row=1, sticky='news', pady=5, padx=5)
        self.labels['Q1_var'] = tk.Label(self.frames['Q1_sb_chi_square'], text='Var', anchor='c')
        self.labels['Q1_var'].grid(column=1, row=2, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Reference Forward Read Depth"] = tk.Entry(self.frames['Q1_sb_chi_square'], width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Reference Forward Read Depth"])
        self.entries["Mpileup Qual: Unfiltered Reference Forward Read Depth"].grid(column=2, row=1, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Reference Reverse Read Depth"] = tk.Entry(self.frames['Q1_sb_chi_square'], width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Reference Reverse Read Depth"])
        self.entries["Mpileup Qual: Unfiltered Reference Reverse Read Depth"].grid(column=3, row=1, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Variant Forward Read Depth"] = tk.Entry(self.frames['Q1_sb_chi_square'], width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Forward Read Depth"])
        self.entries["Mpileup Qual: Unfiltered Variant Forward Read Depth"].grid(column=2, row=2, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Variant Reverse Read Depth"] = tk.Entry(self.frames['Q1_sb_chi_square'], width=5, textvariable=self.variant["Mpileup Qual: Unfiltered Variant Reverse Read Depth"])
        self.entries["Mpileup Qual: Unfiltered Variant Reverse Read Depth"].grid(column=3, row=2, sticky='news', pady=5, padx=5)
        # Q1 Strand Bias Stats Area
        self.labels['Mpileup Qual: Unfiltered Variant Binomial Proportion'] = tk.Label(self.frames['strand_bias'], text="Binom. Prop.", anchor='e')
        self.labels['Mpileup Qual: Unfiltered Variant Binomial Proportion'].grid(column=0, row=9, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Variant Binomial Proportion"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial Proportion"])
        self.entries["Mpileup Qual: Unfiltered Variant Binomial Proportion"].grid(column=1, row=9, sticky='news', pady=5, padx=5)
        self.labels['Mpileup Qual: Unfiltered Variant Binomial P Value'] = tk.Label(self.frames['strand_bias'], text="p.", anchor='e')
        self.labels['Mpileup Qual: Unfiltered Variant Binomial P Value'].grid(column=2, row=9, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Variant Binomial P Value"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["Mpileup Qual: Unfiltered Variant Binomial P Value"], width=5)
        self.entries["Mpileup Qual: Unfiltered Variant Binomial P Value"].grid(column=3, row=9, sticky='news', pady=5, padx=5)
        self.labels['Mpileup Qual: Unfiltered Variant Fishers Odds Ratio'] = tk.Label(self.frames['strand_bias'], text="Fishers OR", anchor='e')
        self.labels['Mpileup Qual: Unfiltered Variant Fishers Odds Ratio'].grid(column=0, row=10, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"])
        self.entries["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"].grid(column=1, row=10, sticky='news', pady=5, padx=5)
        self.labels['Mpileup Qual: Unfiltered Variant Fishers P Value'] = tk.Label(self.frames['strand_bias'], text="p.", anchor='e')
        self.labels['Mpileup Qual: Unfiltered Variant Fishers P Value'].grid(column=2, row=10, sticky='news', pady=5, padx=5)
        self.entries["Mpileup Qual: Unfiltered Variant Fishers P Value"] = tk.Entry(self.frames['strand_bias'], textvariable=self.variant["Mpileup Qual: Unfiltered Variant Fishers P Value"], width=5)
        self.entries["Mpileup Qual: Unfiltered Variant Fishers P Value"].grid(column=3, row=10, sticky='news', pady=5, padx=5)

        # Genexus info frame
        self.frames['gx_info'] = tk.Frame(self.frames['middle'], bootstyle='secondary')
        self.frames['gx_info'].pack(side='top', expand=False, fill='both', padx=5, pady=5)
        for x in range(5):
            self.frames['gx_info'].rowconfigure(x, weight=1)
        for x in range(6):
            self.frames['gx_info'].columnconfigure(x, weight=1)
        self.labels['gx_info_frame_label'] = tk.Label(self.frames['gx_info'], text="Genexus Reported Information", anchor='c')
        self.labels['gx_info_frame_label'].grid(row=0, column=0, columnspan=6, sticky='news', padx=5, pady=5)
        # gx info top area
        self.labels['VCF: AF'] = tk.Label(self.frames['gx_info'], text="Allele Fraction")
        self.labels['VCF: AF'].grid(row=1, column=0, sticky='news', padx=5, pady=5)
        self.entries["VCF: AF"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: AF"])
        self.entries["VCF: AF"].grid(row=2, column=0, sticky='news', padx=5, pady=5)
        self.labels['VCF: TYPE'] = tk.Label(self.frames['gx_info'], text="Variant Type")
        self.labels['VCF: TYPE'].grid(row=1, column=1, sticky='news', padx=5, pady=5)
        self.entries["VCF: TYPE"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: TYPE"])
        self.entries["VCF: TYPE"].grid(row=2, column=1, sticky='news', padx=5, pady=5)
        self.labels['VCF: LEN'] = tk.Label(self.frames['gx_info'], text="Length of Variant (BP)")
        self.labels['VCF: LEN'].grid(row=1, column=2, sticky='news', padx=5, pady=5)
        self.entries["VCF: LEN"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: LEN"])
        self.entries["VCF: LEN"].grid(row=2, column=2, sticky='news', padx=5, pady=5)
        self.labels['VCF: Genotype'] = tk.Label(self.frames['gx_info'], text="Genotype")
        self.labels['VCF: Genotype'].grid(row=1, column=3, sticky='news', padx=5, pady=5)
        self.entries["VCF: Genotype"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: Genotype"])
        self.entries["VCF: Genotype"].grid(row=2, column=3, sticky='news', padx=5, pady=5)
        self.labels['VCF: Filter'] = tk.Label(self.frames['gx_info'], text="Filter (Genexus)")
        self.labels['VCF: Filter'].grid(row=1, column=4, sticky='news', padx=5, pady=5)
        self.entries["VCF: Filter"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: Filter"])
        self.entries["VCF: Filter"].grid(row=2, column=4, sticky='news', padx=5, pady=5)
        self.labels['VCF: QUAL'] = tk.Label(self.frames['gx_info'], text="Quality Score")
        self.labels['VCF: QUAL'].grid(row=1, column=5, sticky='news', padx=5, pady=5)
        self.entries["VCF: QUAL"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: QUAL"])
        self.entries["VCF: QUAL"].grid(row=2, column=5, rowspan=4, sticky='news', padx=5, pady=5)
        # gx info bottom area
        self.labels['VCF: FAO'] = tk.Label(self.frames['gx_info'], text="FAO")
        self.labels['VCF: FAO'].grid(row=3, column=0, sticky='news', padx=5, pady=5)
        self.entries["VCF: FAO"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: FAO"])
        self.entries["VCF: FAO"].grid(row=4, column=0, sticky='news', padx=5, pady=5)
        self.labels['VCF: FDP'] = tk.Label(self.frames['gx_info'], text="FDP")
        self.labels['VCF: FDP'].grid(row=3, column=1, sticky='news', padx=5, pady=5)
        self.entries["VCF: FDP"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: FDP"])
        self.entries["VCF: FDP"].grid(row=4, column=1, sticky='news', padx=5, pady=5)
        self.labels['VCF: HRUN'] = tk.Label(self.frames['gx_info'], text="HRUN")
        self.labels['VCF: HRUN'].grid(row=3, column=2, sticky='news', padx=5, pady=5)
        self.entries["VCF: HRUN"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: HRUN"])
        self.entries["VCF: HRUN"].grid(row=4, column=2, sticky='news', padx=5, pady=5)
        self.labels['VCF: QD'] = tk.Label(self.frames['gx_info'], text="QD")
        self.labels['VCF: QD'].grid(row=3, column=3, sticky='news', padx=5, pady=5)
        self.entries["VCF: QD"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: QD"])
        self.entries["VCF: QD"].grid(row=4, column=3, sticky='news', padx=5, pady=5)
        self.labels['VCF: SVTYPE'] = tk.Label(self.frames['gx_info'], text="SVTYPE (Unused)")
        self.labels['VCF: SVTYPE'].grid(row=3, column=4, sticky='news', padx=5, pady=5)
        self.entries["VCF: SVTYPE"] = tk.Entry(self.frames['gx_info'], textvariable=self.variant["VCF: SVTYPE"])
        self.entries["VCF: SVTYPE"].grid(row=4, column=4, sticky='news', padx=5, pady=5)

        # mpileup info frame
        self.frames['mpl_info'] = tk.Frame(self.frames['middle'], bootstyle='secondary')
        self.frames['mpl_info'].pack(side='top', expand=False, fill='both', padx=5, pady=5)
        for x in range(5):
            self.frames['mpl_info'].columnconfigure(x, weight=1)
        for x in range(3):
            self.frames['mpl_info'].rowconfigure(x, weight=1)
        self.labels['mpl_info_label'] = tk.Label(self.frames['mpl_info'], text="Mpileup Reported Information", anchor='c')
        self.labels['mpl_info_label'].grid(column=0, row=0, columnspan=5, sticky='news', padx=5, pady=5)
        self.labels['Mpileup Qual: Filtered VAF'] = tk.Label(self.frames['mpl_info'], text="Filtered VAF (Q20)", anchor='c')
        self.labels['Mpileup Qual: Filtered VAF'].grid(column=0, row=1, sticky='news', padx=5, pady=5)
        self.entries["Mpileup Qual: Filtered VAF"] = tk.Entry(self.frames['mpl_info'], textvariable=self.variant["Mpileup Qual: Filtered VAF"])
        self.entries["Mpileup Qual: Filtered VAF"].grid(column=0, row=2, sticky='news', padx=5, pady=5)
        self.labels['Mpileup Qual: Unfiltered VAF'] = tk.Label(self.frames['mpl_info'], text="Unfiltered VAF (Q1)", anchor='c')
        self.labels['Mpileup Qual: Unfiltered VAF'].grid(column=1, row=1, sticky='news', padx=5, pady=5)
        self.entries["Mpileup Qual: Unfiltered VAF"] = tk.Entry(self.frames['mpl_info'], textvariable=self.variant["Mpileup Qual: Unfiltered VAF"])
        self.entries["Mpileup Qual: Unfiltered VAF"].grid(column=1, row=2, sticky='news', padx=5, pady=5)
        self.labels['Mpileup Qual: Read Depth'] = tk.Label(self.frames['mpl_info'], text="Total Read Depth", anchor='c')
        self.labels['Mpileup Qual: Read Depth'].grid(column=2, row=1, sticky='news', padx=5, pady=5)
        self.entries["Mpileup Qual: Read Depth"] = tk.Entry(self.frames['mpl_info'], textvariable=self.variant["Mpileup Qual: Read Depth"])
        self.entries["Mpileup Qual: Read Depth"].grid(column=2, row=2, sticky='news', padx=5, pady=5)
        self.labels['Mpileup Qual: Start Reads'] = tk.Label(self.frames['mpl_info'], text="Count: Read Starts", anchor='c')
        self.labels['Mpileup Qual: Start Reads'].grid(column=3, row=1, sticky='news', padx=5, pady=5)
        self.entries["Mpileup Qual: Start Reads"] = tk.Entry(self.frames['mpl_info'], textvariable=self.variant["Mpileup Qual: Start Reads"])
        self.entries["Mpileup Qual: Start Reads"].grid(column=3, row=2, sticky='news', padx=5, pady=5)
        self.labels['Mpileup Qual: Stop Reads'] = tk.Label(self.frames['mpl_info'], text="Count: Read Ends", anchor='c')
        self.labels['Mpileup Qual: Stop Reads'].grid(column=4, row=1, sticky='news', padx=5, pady=5)
        self.entries["Mpileup Qual: Stop Reads"] = tk.Entry(self.frames['mpl_info'], textvariable=self.variant["Mpileup Qual: Stop Reads"])
        self.entries["Mpileup Qual: Stop Reads"].grid(column=4, row=2, sticky='news', padx=5, pady=5)

        # Other frame, used as a spacer
        self.frames['other'] = tk.Frame(self.frames['middle'])
        self.frames['other'].pack(side='top',expand=True, fill='both')

        # Variant Annotation Info Frame
        self.frames['var_annot'] = tk.Frame(self.frames['other'], bootstyle='secondary')
        self.frames['var_annot'].pack(side='left',expand=True, fill='both', padx=5, pady=5)
        for x in range(4):
            self.frames['var_annot'].columnconfigure(x, weight=1)
        self.frames['var_annot'].rowconfigure(4, weight=99)
        self.labels['var_annot_label'] = tk.Label(self.frames['var_annot'], text="Variant Annotations", anchor='c')
        self.labels['var_annot_label'].grid(column=0, row=0, columnspan=4, sticky='news', padx=5, pady=5)
        self.labels['Variant Annotation: Coding'] = tk.Label(self.frames['var_annot'], text="Coding Region")
        self.labels['Variant Annotation: Coding'].grid(column=0, row=1, sticky='news', padx=5, pady=5)
        self.entries["Variant Annotation: Coding"] = tk.Entry(self.frames['var_annot'], textvariable=self.variant["Variant Annotation: Coding"])
        self.entries["Variant Annotation: Coding"].grid(column=0, row=2, sticky='news', padx=5, pady=5)
        self.labels['Variant Annotation: Sequence Ontology'] = tk.Label(self.frames['var_annot'], text="Var. Type (Seq. Ontol.)")
        self.labels['Variant Annotation: Sequence Ontology'].grid(column=1, row=1, sticky='news', padx=5, pady=5)
        self.entries["Variant Annotation: Sequence Ontology"] = tk.Entry(self.frames['var_annot'], textvariable=self.variant["Variant Annotation: Sequence Ontology"])
        self.entries["Variant Annotation: Sequence Ontology"].grid(column=1, row=2, sticky='news', padx=5, pady=5)
        self.labels['Variant Annotation: Transcript'] = tk.Label(self.frames['var_annot'], text="Transcript")
        self.labels['Variant Annotation: Transcript'].grid(column=2, row=1, sticky='news', padx=5, pady=5)
        self.entries["Variant Annotation: Transcript"] = tk.Entry(self.frames['var_annot'], textvariable=self.variant["Variant Annotation: Transcript"])
        self.entries["Variant Annotation: Transcript"].grid(column=2, row=2, sticky='news', padx=5, pady=5)
        self.labels['Variant Annotation: RefSeq'] = tk.Label(self.frames['var_annot'], text="RefSeq")
        self.labels['Variant Annotation: RefSeq'].grid(column=3, row=1, sticky='news', padx=5, pady=5)
        self.entries["Variant Annotation: RefSeq"] = tk.Entry(self.frames['var_annot'], textvariable=self.variant["VCF: LEN"])
        self.entries["Variant Annotation: RefSeq"].grid(column=3, row=2, sticky='news', padx=5, pady=5)
        self.labels['Variant Annotation: All Mappings'] = tk.Label(self.frames['var_annot'], text="All Mappings", anchor='c')
        self.labels['Variant Annotation: All Mappings'].grid(column=0, row=3, columnspan=4, sticky='news', padx=5, pady=5)
        self.textboxes["Variant Annotation: All Mappings"] = tk.ScrolledText(self.frames['var_annot'], height=1)
        self.textboxes["Variant Annotation: All Mappings"].grid(column=0, columnspan=4, row=4, sticky='news', padx=5, pady=5)

        # MDL Info area
        self.frames['mdl'] = tk.Frame(self.frames['other'], bootstyle='secondary')
        self.frames['mdl'].pack(side='left',expand=True, fill='both', padx=5, pady=5)
        self.frames['mdl'].rowconfigure(4, weight=99)
        self.frames['mdl'].columnconfigure(0, weight=1)
        self.frames['mdl'].columnconfigure(1, weight=1)
        self.labels['mdl_info_label'] = tk.Label(self.frames['mdl'], text="MDL Information", anchor='c')
        self.labels['mdl_info_label'].grid(column=0, row=0, columnspan=2, sticky='news', padx=5, pady=5)
        self.labels['MDL: Sample Count'] = tk.Label(self.frames['mdl'], text="Sample Count")
        self.labels['MDL: Sample Count'].grid(column=0, row=1, sticky='news', padx=5, pady=5)
        self.entries["MDL: Sample Count"] = tk.Entry(self.frames['mdl'], textvariable=self.variant["MDL: Sample Count"])
        self.entries["MDL: Sample Count"].grid(column=0, row=2, sticky='news', padx=5, pady=5)
        self.labels['MDL: Variant Frequency'] = tk.Label(self.frames['mdl'], text="Variant Frequency")
        self.labels['MDL: Variant Frequency'].grid(column=1, row=1, sticky='news', padx=5, pady=5)
        self.entries["MDL: Variant Frequency"]  = tk.Entry(self.frames['mdl'], textvariable=self.variant["MDL: Variant Frequency"])
        self.entries["MDL: Variant Frequency"].grid(column=1, row=2, sticky='news', padx=5, pady=5)
        self.labels['MDL: Sample List'] = tk.Label(self.frames['mdl'], text="Sample List", anchor='c')
        self.labels['MDL: Sample List'].grid(column=0, columnspan=2, row=3, sticky='news', padx=5, pady=5)
        self.textboxes["MDL: Sample List"] = tk.ScrolledText(self.frames['mdl'], height=1)
        self.textboxes["MDL: Sample List"].grid(column=0, columnspan=2, row=4, sticky='news', padx=5, pady=5)

        # Web Resources Stats
        self.frames['bottom'] = tk.Frame(self.frames['right'], bootstyle='secondary')
        self.frames['bottom'].pack(side='bottom', expand=False, fill='both', padx=5, pady=5)
        for x in range(10):
            self.frames['bottom'].columnconfigure(x, weight=1)
        for x in range(6):
            self.frames['bottom'].rowconfigure(x, weight=1)
        self.labels['web_info_label'] = tk.Label(self.frames['bottom'], text="Internet Resource Information and Links", anchor='c')
        self.labels['web_info_label'].grid(column=0, row=0, columnspan=10, sticky='news', padx=5, pady=5)

        # Clinvar Area
        self.labels['ClinVar:'] = tk.Label(self.frames['bottom'], text="ClinVar:")
        self.labels['ClinVar:'].grid(column=0, row=1, sticky='news', padx=5, pady=5)
        self.labels['ClinVar: ClinVar ID'] = tk.Label(self.frames['bottom'], text="ID")
        self.labels['ClinVar: ClinVar ID'].grid(column=0, row=2, sticky='news', padx=5, pady=5)
        self.entries["ClinVar: ClinVar ID"] = tk.Entry(self.frames['bottom'], textvariable=self.variant["ClinVar: ClinVar ID"])
        self.entries["ClinVar: ClinVar ID"].grid(column=0, row=3, sticky='news', padx=5, pady=5)
        self.labels['ClinVar: Clinical Significance'] = tk.Label(self.frames['bottom'], text="Significance")
        self.labels['ClinVar: Clinical Significance'].grid(column=0, row=4, sticky='news', padx=5, pady=5)
        self.entries["ClinVar: Clinical Significance"] = tk.Entry(self.frames['bottom'], textvariable=self.variant["ClinVar: Clinical Significance"])
        self.entries["ClinVar: Clinical Significance"].grid(column=0, row=5, sticky='news', padx=5, pady=5)

        # Gnomad Area
        self.labels['gnomAD3:'] = tk.Label(self.frames['bottom'], text="gnomAD3:")
        self.labels['gnomAD3:'].grid(column=1, row=1, sticky='news', padx=5, pady=5)
        self.labels['Global AF'] = tk.Label(self.frames['bottom'], text="Global AF")
        self.labels['Global AF'].grid(column=1, row=2, sticky='news', padx=5, pady=5)
        self.entries["gnomAD3: Global AF"] = tk.Entry(self.frames['bottom'], textvariable=self.variant["gnomAD3: Global AF"])
        self.entries["gnomAD3: Global AF"].grid(column=1, row=3, rowspan=3, sticky='news', padx=5, pady=5)

        # CADD Area
        self.labels['CADD:'] = tk.Label(self.frames['bottom'], text="CADD:")
        self.labels['CADD:'].grid(column=2, row=1, sticky='news', padx=5, pady=5)
        self.labels['Phred'] = tk.Label(self.frames['bottom'], text="Phred Score")
        self.labels['Phred'].grid(column=2, row=2, sticky='news', padx=5, pady=5)
        self.entries["CADD: Phred"] = tk.Entry(self.frames['bottom'], textvariable=self.variant["CADD: Phred"])
        self.entries["CADD: Phred"].grid(column=2, row=3, rowspan=3, sticky='news', padx=5, pady=5)

        # PolyPhen Area
        self.labels['PolyPhen-2:'] = tk.Label(self.frames['bottom'], text="PolyPhen-2:")
        self.labels['PolyPhen-2:'].grid(column=3, row=1, sticky='news', padx=5, pady=5)
        self.labels['HDIV Prediction'] = tk.Label(self.frames['bottom'], text="HDIV Predict.")
        self.labels['HDIV Prediction'].grid(column=3, row=2, sticky='news', padx=5, pady=5)
        self.entries["PolyPhen-2: HDIV Prediction"] = tk.Entry(self.frames['bottom'], textvariable=self.variant["PolyPhen-2: HDIV Prediction"])
        self.entries["PolyPhen-2: HDIV Prediction"].grid(column=3, row=3, rowspan=3, sticky='news', padx=5, pady=5)

        # SIFT Area
        self.labels['SIFT'] = tk.Label(self.frames['bottom'], text="SIFT:")
        self.labels['SIFT'].grid(column=4, row=1, sticky='news', padx=5, pady=5)
        self.labels['Prediction'] = tk.Label(self.frames['bottom'], text="Prediction")
        self.labels['Prediction'].grid(column=4, row=2, sticky='news', padx=5, pady=5)
        self.entries["SIFT: Prediction"] = tk.Entry(self.frames['bottom'], textvariable=self.variant["SIFT: Prediction"])
        self.entries["SIFT: Prediction"].grid(column=4, row=3, rowspan=3, sticky='news', padx=5, pady=5)

        # dbSNP Area
        self.labels['dbSNP:'] = tk.Label(self.frames['bottom'], text="dbSNP:")
        self.labels['dbSNP:'].grid(column=5, row=1, sticky='news', padx=5, pady=5)
        self.labels['rsID'] = tk.Label(self.frames['bottom'], text="rsID")
        self.labels['rsID'].grid(column=5, row=2, sticky='news', padx=5, pady=5)
        self.entries["dbSNP: rsID"] = tk.Entry(self.frames['bottom'], textvariable=self.variant["dbSNP: rsID"])
        self.entries["dbSNP: rsID"].grid(column=5, row=3, rowspan=3, sticky='news', padx=5, pady=5)

        # UniProt Area
        self.labels['UniProt (GENE):'] = tk.Label(self.frames['bottom'], text="UniProt (Gene):")
        self.labels['UniProt (GENE):'].grid(column=6, row=1, sticky='news', padx=5, pady=5)
        self.labels['Accession Number'] = tk.Label(self.frames['bottom'], text="Accession #")
        self.labels['Accession Number'].grid(column=6, row=2, sticky='news', padx=5, pady=5)
        self.entries["UniProt (GENE): Accession Number"] = tk.Entry(self.frames['bottom'], textvariable=self.variant["UniProt (GENE): Accession Number"])
        self.entries["UniProt (GENE): Accession Number"].grid(column=6, row=3, rowspan=3, sticky='news', padx=5, pady=5)

        # PhyloP Vertscore Area
        self.labels['PhyloP:'] = tk.Label(self.frames['bottom'], text="PhyloP:")
        self.labels['PhyloP:'].grid(column=7, row=1, sticky='news', padx=5, pady=5)
        self.labels['Vert Score'] = tk.Label(self.frames['bottom'], text="Vert Score")
        self.labels['Vert Score'].grid(column=7, row=2, sticky='news', padx=5, pady=5)
        self.entries["PhyloP: Vert Score"] = tk.Entry(self.frames['bottom'], textvariable=self.variant["PhyloP: Vert Score"])
        self.entries["PhyloP: Vert Score"].grid(column=7, row=3, rowspan=3, sticky='news', padx=5, pady=5)

        # COSMIC Area
        self.labels['COSMIC:'] = tk.Label(self.frames['bottom'], text="COSMIC:", anchor='center')
        self.labels['COSMIC:'].grid(column=8, row=1, sticky='news', padx=5, pady=5)
        self.labels['ID'] = tk.Label(self.frames['bottom'], text="ID", anchor='center')
        self.labels['ID'].grid(column=8, row=2, sticky='news', padx=5, pady=5)
        self.entries["COSMIC: ID"] = tk.Entry(self.frames['bottom'], textvariable=self.variant["COSMIC: ID"], width=12)
        self.entries["COSMIC: ID"].grid(column=8, row=3, sticky='news', padx=5, pady=5)
        self.labels['Variant Count'] = tk.Label(self.frames['bottom'], text="Var. Count")
        self.labels['Variant Count'].grid(column=8, row=4, sticky='news', padx=5, pady=5)
        self.entries["COSMIC: Variant Count"] = tk.Entry(self.frames['bottom'], textvariable=self.variant["COSMIC: Variant Count"])
        self.entries["COSMIC: Variant Count"].grid(column=8, row=5, sticky='news', padx=5, pady=5)

        # COSMIC Tissue Variant Count Region
        self.textboxes["COSMIC: Variant Count (Tissue)"] = tk.ScrolledText(self.frames['bottom'], height=1)
        self.textboxes["COSMIC: Variant Count (Tissue)"].grid(column=9, row=1, rowspan=5, sticky='news', padx=5, pady=5)

        # Adjust all the widgets.......
        for key,value in self.labels.items():
            value.configure(anchor='c', bootstyle='secondary.inverse')
        for key,value in self.entries.items():
            value.configure(justify=tk.CENTER, bootstyle='normal', width=5)
        for x in [
            'web_info_label',
            'mdl_info_label',
            'sb_frame_label',
            'gx_info_frame_label',
            'basic_info_frame_label',
            'var_annot_label',
            'mpl_info_label',
            'file_info_label',
            'disposition_label',
        ]:
            self.labels[x].configure(bootstyle='info.inverse')

        self.create_tooltips()
        self.create_weblinks()

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
        return
    
    def clear_view(self, *args, **kwargs):
        for item in self.treeviews['variant_list'].get_children():
            self.treeviews['variant_list'].delete(item)
        for x in VCF_FIELDS:
            self.variant[x].set("")
            self.labels[x].configure(bootstyle='normal.TLabel')
        self.variant['Disposition'].set(0)
        self.variables['filename'].set("")
        self.variables['status_bar'].set("Records view cleared.")
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
        # try:
        self.validate_cells()
        # except:
        #     pass
        self.textboxes['COSMIC: Variant Count (Tissue)'].delete("1.0", tk.END)
        self.textboxes['COSMIC: Variant Count (Tissue)'].insert(tk.END, self.variant["COSMIC: Variant Count (Tissue)"].get())
        self.textboxes['MDL: Sample List'].delete("1.0", tk.END)
        self.textboxes['MDL: Sample List'].insert(tk.END, self.variant["COSMIC: Variant Count (Tissue)"].get())
        self.textboxes['Variant Annotation: All Mappings'].delete("1.0", tk.END)
        self.textboxes['Variant Annotation: All Mappings'].insert(tk.END, self.variant["COSMIC: Variant Count (Tissue)"].get())
        return

    def validate_cells(self):

        for x in VCF_FIELDS:
            self.entries[x].configure(bootstyle='primary', foreground='black')
            if self.variant[x].get() == "None" or self.variant[x].get() == "":
                self.entries[x].configure(bootstyle='dark')
                continue
            if x in VALIDATION['p_values']:
                try:
                    if float(self.variant[x].get()) > VALIDATION['cutoffs']['p_value']:
                        self.entries[x].configure(bootstyle='danger', foreground='#bb0000')
                except:
                    pass
            if x in VALIDATION['strand_read_depth']:
                try:
                    if int(self.variant[x].get()) <= VALIDATION['cutoffs']['strand_read_depth']:
                        self.entries[x].configure(bootstyle='danger', foreground='#bb0000')
                except:
                    pass
            if x in VALIDATION['locus_read_depth']:
                try:
                    if int(self.variant[x].get()) <= VALIDATION['cutoffs']['locus_read_depth']:
                        self.entries[x].configure(bootstyle='danger', foreground='#bb0000')
                except:
                    pass
            if x in VALIDATION['minimum_vaf']:
                try:
                    if float(self.variant[x].get()) < VALIDATION['cutoffs']['vaf_threshold']:
                        self.entries[x].configure(bootstyle='danger', foreground='#bb0000')
                except:
                    pass
            if x in VALIDATION['web_links'].keys():
                self.entries[x].configure(bootstyle = 'info', foreground='#003499')
                # self.entries[x].style.colors.set('inputbg','red')
        return


# MAIN LOOP ----------------------------------------------

def main():
    pass
    return

if __name__ == '__main__':
    main()