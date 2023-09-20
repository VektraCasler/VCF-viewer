# variant_data_viewer/view.py
""" The view of the variant Data Viewer application, comprised of the tkinter portion. """

# IMPORTS ------------------------------------------------

import ttkbootstrap as tk
from tkinter import filedialog as fd

from .global_variables import *
from .tool_tip import ToolTip, CreateToolTip

import webbrowser

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
    "amp_ID",
    "Cytoband",
    "MANE_transcript (GRCh38)",
    "Genexus_transcript (GRCh37)",
    "Genexus_Exon(s)",
    "Genexus_codons",
    "tier",
    "test_tissue",
    "Disposition",
]

# CLASSES ------------------------------------------------


class RecordView(tk.Frame):
    def _event(self, sequence):
        """A stolen bit of magic that  creates a callback function for view-generated events."""

        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)

        return callback

    def __init__(self, parent, **kwargs) -> None:
        super().__init__()

        # Variables ------------------------------------------------------------------------

        # Holder dictionary for tk variables and widgets to be used by the \
        # view.  Variant dict Must match the model's fields. (DATA_FIELDS)

        self.filename = tk.StringVar()
        # self.variables = dict()
        self.disposition = dict()
        self.selection_index = tk.IntVar()
        for x in DISPOSITIONS:
            self.disposition[x] = tk.IntVar()

        self.variant = dict()
        self.labels = dict()
        self.entries = dict()
        self.buttons = dict()
        self.radio_buttons = dict()
        self.treeviews = dict()
        self.scrollbars = dict()
        self.textboxes = dict()

        for x in DATA_FIELDS:
            self.variant[x] = tk.StringVar()
            self.entries[x] = tk.Entry()
            self.labels[x] = tk.Label()
        self.entries["Disposition"] = tk.Entry()
        self.labels["Disposition"] = tk.Label()
        self.variant["Disposition"] = tk.StringVar()

        for x in TEXTBOXES:
            self.textboxes[x] = tk.ScrolledText()

        # Frames and Widgets ----------------------------------------------------------
        self.frames = dict()

        # Base Frame
        self.frames["base"] = tk.Frame(parent)
        self.frames["base"].pack(expand=True, fill="both", ipadx=10, ipady=10)

        # Left Frame
        self.frames["left"] = tk.Frame(self.frames["base"], bootstyle="secondary")
        self.frames["left"].pack(side="left", expand=False, fill="y", padx=5, pady=5)
        self.frames["left"].rowconfigure(3, weight=99)
        self.labels["file_info_label"] = tk.Label(
            self.frames["left"],
            text="Variant File Information",
            bootstyle="info.inverse",
            anchor="c",
        )
        self.labels["file_info_label"].grid(
            row=0, column=0, columnspan=2, sticky="news", padx=5, pady=5
        )

        # File load button
        self.entries["filename"] = tk.Entry(
            self.frames["left"], textvariable=self.filename, width=24
        )
        self.entries["filename"].grid(
            row=1, column=0, columnspan=2, sticky="news", padx=5, pady=5
        )
        self.buttons["load_file"] = tk.Button(
            self.frames["left"], text="Open a File", command=self._event("<<FileLoad>>")
        )
        self.buttons["load_file"].grid(
            row=2, column=0, columnspan=2, sticky="news", padx=5, pady=5
        )

        # Treeview list
        self.treeviews["variant_list"] = tk.Treeview(
            self.frames["left"],
            columns=DATA_FIELDS,
            displaycolumns=[4, 77],
            selectmode="browse",
            show="headings",
        )
        for x in DATA_FIELDS:
            self.treeviews["variant_list"].heading(x, text=x, anchor="center")
        self.treeviews["variant_list"].column(column=4, width=120, anchor="center")
        self.treeviews["variant_list"].column(column=77, width=140, anchor="center")
        self.treeviews["variant_list"].grid(
            row=3, column=0, columnspan=2, sticky="news", padx=5, pady=5
        )
        self.treeviews["variant_list"].bind("<<TreeviewSelect>>", self.record_selected)
        self.treeviews["variant_list"].tag_configure("None", background="#c4c4c4")
        self.treeviews["variant_list"].tag_configure(
            "Hotspot_Exceptions", background="#f92134"
        )
        self.treeviews["variant_list"].tag_configure("VUS", background="#f0aa44")
        self.treeviews["variant_list"].tag_configure(
            "Low_VAF_Variants", background="#70aaff"
        )
        self.treeviews["variant_list"].tag_configure("Oncogenic", background="#fc6622")
        self.treeviews["variant_list"].tag_configure("FLT3_ITDs", background="#f794fa")

        # Treeview Scrollbar
        self.scrollbars["variant_list"] = tk.Scrollbar(
            self.frames["left"],
            orient=tk.VERTICAL,
            command=self.treeviews["variant_list"].yview,
        )
        self.treeviews["variant_list"].configure(
            yscroll=self.scrollbars["variant_list"].set
        )
        self.scrollbars["variant_list"].grid(row=3, column=1, sticky="nes")

        # Disposition labels
        self.labels["disposition_label"] = tk.Label(
            self.frames["left"],
            text="Assign Disposition",
            bootstyle="secondary.inverse",
            anchor="c",
        )
        self.labels["disposition_label"].grid(
            row=4, column=0, columnspan=2, sticky="news", padx=5, pady=5
        )
        self.entries["None"] = tk.Entry(
            self.frames["left"], textvariable=self.disposition["None"], width=5
        )
        self.entries["None"].grid(row=5, column=0, sticky="news", padx=5, pady=5)
        self.entries["Low VAF Variants"] = tk.Entry(
            self.frames["left"],
            textvariable=self.disposition["Low VAF Variants"],
            width=5,
        )
        self.entries["Low VAF Variants"].grid(
            row=6, column=0, sticky="news", padx=5, pady=5
        )
        self.entries["VUS"] = tk.Entry(
            self.frames["left"], textvariable=self.disposition["VUS"], width=5
        )
        self.entries["VUS"].grid(row=7, column=0, sticky="news", padx=5, pady=5)
        self.entries["Oncogenic"] = tk.Entry(
            self.frames["left"], textvariable=self.disposition["Oncogenic"], width=5
        )
        self.entries["Oncogenic"].grid(row=8, column=0, sticky="news", padx=5, pady=5)
        self.entries["FLT3 ITDs"] = tk.Entry(
            self.frames["left"], textvariable=self.disposition["FLT3 ITDs"], width=5
        )
        self.entries["FLT3 ITDs"].grid(row=9, column=0, sticky="news", padx=5, pady=5)
        self.entries["Hotspot Exceptions"] = tk.Entry(
            self.frames["left"],
            textvariable=self.disposition["Hotspot Exceptions"],
            width=5,
        )
        self.entries["Hotspot Exceptions"].grid(
            row=10, column=0, sticky="news", padx=5, pady=5
        )

        # Radio buttons for disposition
        self.radio_buttons["None"] = tk.Radiobutton(
            self.frames["left"],
            text="None (Unassigned)",
            variable=self.variant["Disposition"],
            value="None",
            bootstyle="toolbutton",
        )
        self.radio_buttons["None"].grid(row=5, column=1, sticky="news", padx=5, pady=5)
        self.radio_buttons["Low VAF Variants"] = tk.Radiobutton(
            self.frames["left"],
            text="Low VAF Variants",
            variable=self.variant["Disposition"],
            value="Low VAF Variants",
            bootstyle="toolbutton",
        )
        self.radio_buttons["Low VAF Variants"].grid(
            row=6, column=1, sticky="news", padx=5, pady=5
        )
        self.radio_buttons["VUS"] = tk.Radiobutton(
            self.frames["left"],
            text="VUS",
            variable=self.variant["Disposition"],
            value="VUS",
            bootstyle="toolbutton",
        )
        self.radio_buttons["VUS"].grid(row=7, column=1, sticky="news", padx=5, pady=5)
        self.radio_buttons["Oncogenic"] = tk.Radiobutton(
            self.frames["left"],
            text="Oncogenic",
            variable=self.variant["Disposition"],
            value="Oncogenic",
            bootstyle="toolbutton",
        )
        self.radio_buttons["Oncogenic"].grid(
            row=8, column=1, sticky="news", padx=5, pady=5
        )
        self.radio_buttons["FLT3 ITDs"] = tk.Radiobutton(
            self.frames["left"],
            text="FLT3 ITDs",
            variable=self.variant["Disposition"],
            value="FLT3 ITDs",
            bootstyle="toolbutton",
        )
        self.radio_buttons["FLT3 ITDs"].grid(
            row=9, column=1, sticky="news", padx=5, pady=5
        )
        self.radio_buttons["Hotspot Exceptions"] = tk.Radiobutton(
            self.frames["left"],
            text="Hotspot Exceptions",
            variable=self.variant["Disposition"],
            value="Hotspot Exceptions",
            bootstyle="toolbutton",
        )
        self.radio_buttons["Hotspot Exceptions"].grid(
            row=10, column=1, sticky="news", padx=5, pady=5
        )

        # Process output files button
        self.buttons["save_disposition"] = tk.Button(
            self.frames["left"],
            text="Save Disposition",
            command=self._event("<<DispoSave>>"),
            state="disabled",
        )
        self.buttons["save_disposition"].grid(
            row=11, column=0, columnspan=2, sticky="news", padx=5, pady=5
        )

        # Right Frame
        self.frames["right"] = tk.Frame(self.frames["base"])
        self.frames["right"].pack(side="right", expand=True, fill="both")

        # Basic Information Area
        self.frames["basic_info"] = tk.Frame(
            self.frames["right"], bootstyle="secondary"
        )
        self.frames["basic_info"].pack(
            side="top", expand=False, fill="x", padx=5, pady=5
        )
        for x in range(6):
            self.frames["basic_info"].columnconfigure(x, weight=1)
        self.labels["basic_info_frame_label"] = tk.Label(
            self.frames["basic_info"], text="Basic Genetic Information", anchor="c"
        )
        self.labels["basic_info_frame_label"].grid(
            row=0, column=0, columnspan=6, sticky="news", padx=5, pady=5
        )
        self.labels["Variant Annotation: Gene"] = tk.Label(
            self.frames["basic_info"], text="Gene"
        )
        self.labels["Variant Annotation: Gene"].grid(
            row=1, column=0, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.entries["Variant Annotation: Gene"] = tk.Entry(
            self.frames["basic_info"],
            width=8,
            textvariable=self.variant["Variant Annotation: Gene"],
            font=("bold", 24, "bold"),
        )
        self.entries["Variant Annotation: Gene"].grid(
            row=2, column=0, rowspan=3, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.labels["Original Input: Chrom"] = tk.Label(
            self.frames["basic_info"], text="Chromosome"
        )
        self.labels["Original Input: Chrom"].grid(
            row=1, column=1, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.entries["Original Input: Chrom"] = tk.Entry(
            self.frames["basic_info"],
            width=6,
            textvariable=self.variant["Original Input: Chrom"],
        )
        self.entries["Original Input: Chrom"].grid(
            row=2, column=1, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.labels["Original Input: Pos"] = tk.Label(
            self.frames["basic_info"], text="Base Pair"
        )
        self.labels["Original Input: Pos"].grid(
            row=3, column=1, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.entries["Original Input: Pos"] = tk.Entry(
            self.frames["basic_info"],
            width=12,
            textvariable=self.variant["Original Input: Pos"],
        )
        self.entries["Original Input: Pos"].grid(
            row=4, column=1, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.labels["Variant Annotation: cDNA change"] = tk.Label(
            self.frames["basic_info"], text="DNA Change (c-dot)"
        )
        self.labels["Variant Annotation: cDNA change"].grid(
            row=1, column=2, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.entries["Variant Annotation: cDNA change"] = tk.Entry(
            self.frames["basic_info"],
            text="C-dot",
            textvariable=self.variant["Variant Annotation: cDNA change"],
        )
        self.entries["Variant Annotation: cDNA change"].grid(
            row=2, column=2, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.labels["Variant Annotation: Protein Change"] = tk.Label(
            self.frames["basic_info"], text="Protein Change (p-dot)"
        )
        self.labels["Variant Annotation: Protein Change"].grid(
            row=3, column=2, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.entries["Variant Annotation: Protein Change"] = tk.Entry(
            self.frames["basic_info"],
            text="P-dot",
            width=24,
            textvariable=self.variant["Variant Annotation: Protein Change"],
        )
        self.entries["Variant Annotation: Protein Change"].grid(
            row=4, column=2, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.labels["Original Input: Reference allele"] = tk.Label(
            self.frames["basic_info"], text="Ref Allele", anchor="nw"
        )
        self.labels["Original Input: Reference allele"].grid(
            row=1, column=3, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.entries["Original Input: Reference allele"] = tk.Entry(
            self.frames["basic_info"],
            justify=tk.LEFT,
            textvariable=self.variant["Original Input: Reference allele"],
        )
        self.entries["Original Input: Reference allele"].grid(
            row=2, column=3, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.labels["Original Input: Alternate allele"] = tk.Label(
            self.frames["basic_info"], text="Variant Allele", anchor="w"
        )
        self.labels["Original Input: Alternate allele"].grid(
            row=3, column=3, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.entries["Original Input: Alternate allele"] = tk.Entry(
            self.frames["basic_info"],
            justify=tk.LEFT,
            textvariable=self.variant["Original Input: Alternate allele"],
        )
        self.entries["Original Input: Alternate allele"].grid(
            row=4, column=3, rowspan=1, columnspan=1, sticky="news", padx=5, pady=5
        )
        self.labels["amp_ID"] = tk.Label(
            self.frames["basic_info"], text="Amplicon", anchor="nw"
        )
        self.labels["amp_ID"].grid(row=1, column=4, sticky="news", padx=5, pady=5)
        self.entries["amp_ID"] = tk.Entry(
            self.frames["basic_info"],
            justify=tk.LEFT,
            textvariable=self.variant["amp_ID"],
        )
        self.entries["amp_ID"].grid(row=2, column=4, sticky="news", padx=5, pady=5)
        self.labels["Cytoband"] = tk.Label(
            self.frames["basic_info"], text="Cytoband", anchor="nw"
        )
        self.labels["Cytoband"].grid(row=3, column=4, sticky="news", padx=5, pady=5)
        self.entries["Cytoband"] = tk.Entry(
            self.frames["basic_info"],
            justify=tk.LEFT,
            textvariable=self.variant["Cytoband"],
        )
        self.entries["Cytoband"].grid(row=4, column=4, sticky="news", padx=5, pady=5)
        self.labels["MANE_transcript (GRCh38)"] = tk.Label(
            self.frames["basic_info"], text="MANE Transcript (GRCh38)", anchor="nw"
        )
        self.labels["MANE_transcript (GRCh38)"].grid(
            row=1, column=5, sticky="news", padx=5, pady=5
        )
        self.entries["MANE_transcript (GRCh38)"] = tk.Entry(
            self.frames["basic_info"],
            justify=tk.LEFT,
            textvariable=self.variant["MANE_transcript (GRCh38)"],
        )
        self.entries["MANE_transcript (GRCh38)"].grid(
            row=2, column=5, sticky="news", padx=5, pady=5
        )
        self.labels["tier"] = tk.Label(
            self.frames["basic_info"], text="Proposed Tier", anchor="nw"
        )
        self.labels["tier"].grid(row=3, column=5, sticky="news", padx=5, pady=5)
        self.entries["tier"] = tk.Entry(
            self.frames["basic_info"],
            justify=tk.LEFT,
            textvariable=self.variant["tier"],
        )
        self.entries["tier"].grid(row=4, column=5, sticky="news", padx=5, pady=5)

        # middle frame
        self.frames["middle"] = tk.Frame(self.frames["right"])
        self.frames["middle"].pack(side="top", expand=True, fill="both")

        # Strand Bias Frame
        self.frames["strand_bias"] = tk.Frame(
            self.frames["middle"], bootstyle="secondary"
        )
        self.frames["strand_bias"].pack(
            side="left", expand=False, fill="both", padx=5, pady=5
        )
        for x in range(12):
            self.frames["strand_bias"].rowconfigure(x, weight=1)
        for x in range(4):
            self.frames["strand_bias"].columnconfigure(x, weight=1)
        self.labels["sb_frame_label"] = tk.Label(
            self.frames["strand_bias"], text="Strand Bias Information", anchor="c"
        )
        self.labels["sb_frame_label"].grid(
            column=0, row=0, columnspan=4, sticky="news", padx=5, pady=5
        )
        self.labels["VCF: STB"] = tk.Label(
            self.frames["strand_bias"], text="SB (reported)"
        )
        self.labels["VCF: STB"].grid(column=0, row=1, sticky="news", padx=5, pady=5)
        self.entries["VCF: STB"] = tk.Entry(
            self.frames["strand_bias"], textvariable=self.variant["VCF: STB"]
        )
        self.entries["VCF: STB"].grid(column=1, row=1, sticky="news", padx=5, pady=5)
        self.labels["VCF: STBP"] = tk.Label(
            self.frames["strand_bias"], text="p.", width=3
        )
        self.labels["VCF: STBP"].grid(column=2, row=1, sticky="news", padx=5, pady=5)
        self.entries["VCF: STBP"] = tk.Entry(
            self.frames["strand_bias"], textvariable=self.variant["VCF: STBP"]
        )
        self.entries["VCF: STBP"].grid(column=3, row=1, sticky="news", padx=5, pady=5)

        # Genexus Strand Bias Chi Square Area
        self.frames["GX_sb_chi_square"] = tk.Frame(
            self.frames["strand_bias"], bootstyle="secondary"
        )
        self.frames["GX_sb_chi_square"].grid(
            column=0, row=2, columnspan=4, sticky="news", pady=5, padx=5
        )
        for x in range(3):
            self.frames["GX_sb_chi_square"].rowconfigure(x, weight=1)
        for x in range(4):
            self.frames["GX_sb_chi_square"].columnconfigure(x, weight=1)
        self.labels["Genexus"] = tk.Label(
            self.frames["GX_sb_chi_square"], anchor="c", text="Genexus", width=8
        )
        self.labels["Genexus"].grid(
            column=0, row=0, rowspan=3, sticky="news", padx=5, pady=5
        )
        self.labels["gx_fwd"] = tk.Label(
            self.frames["GX_sb_chi_square"], text="Fwd", width=3, anchor="c"
        )
        self.labels["gx_fwd"].grid(column=2, row=0, sticky="news", padx=5, pady=5)
        self.labels["gx_rev"] = tk.Label(
            self.frames["GX_sb_chi_square"], text="Rev", width=3, anchor="c"
        )
        self.labels["gx_rev"].grid(column=3, row=0, sticky="news", padx=5, pady=5)
        self.labels["gx_ref"] = tk.Label(
            self.frames["GX_sb_chi_square"], text="Ref", width=3, anchor="c"
        )
        self.labels["gx_ref"].grid(column=1, row=1, sticky="news", padx=5, pady=5)
        self.labels["gx_var"] = tk.Label(
            self.frames["GX_sb_chi_square"], text="Var", width=3, anchor="c"
        )
        self.labels["gx_var"].grid(column=1, row=2, sticky="news", padx=5, pady=5)
        self.entries["VCF: FSRF"] = tk.Entry(
            self.frames["GX_sb_chi_square"],
            textvariable=self.variant["VCF: FSRF"],
            width=3,
        )
        self.entries["VCF: FSRF"].grid(column=2, row=1, sticky="news", padx=5, pady=5)
        self.entries["VCF: FSRR"] = tk.Entry(
            self.frames["GX_sb_chi_square"],
            textvariable=self.variant["VCF: FSRR"],
            width=3,
        )
        self.entries["VCF: FSRR"].grid(column=3, row=1, sticky="news", padx=5, pady=5)
        self.entries["VCF: FSAF"] = tk.Entry(
            self.frames["GX_sb_chi_square"],
            textvariable=self.variant["VCF: FSAF"],
            width=3,
        )
        self.entries["VCF: FSAF"].grid(column=2, row=2, sticky="news", padx=5, pady=5)
        self.entries["VCF: FSAR"] = tk.Entry(
            self.frames["GX_sb_chi_square"],
            textvariable=self.variant["VCF: FSAR"],
            width=3,
        )
        self.entries["VCF: FSAR"].grid(column=3, row=2, sticky="news", padx=5, pady=5)
        # Genexus Stats Area
        self.labels["VCF: Binom Proportion"] = tk.Label(
            self.frames["strand_bias"], text="Binom. Prop.", anchor="e"
        )
        self.labels["VCF: Binom Proportion"].grid(
            column=0, row=3, sticky="news", padx=5
        )
        self.entries["VCF: Binom Proportion"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant["VCF: Binom Proportion"],
        )
        self.entries["VCF: Binom Proportion"].grid(
            column=1, row=3, sticky="news", pady=5, padx=5
        )
        self.labels["VCF: Binom P Value"] = tk.Label(
            self.frames["strand_bias"], text="p.", anchor="e"
        )
        self.labels["VCF: Binom P Value"].grid(column=2, row=3, sticky="news")
        self.entries["VCF: Binom P Value"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant["VCF: Binom P Value"],
            width=3,
        )
        self.entries["VCF: Binom P Value"].grid(
            column=3, row=3, sticky="news", pady=5, padx=5
        )
        self.labels["VCF: Fisher Odds Ratio"] = tk.Label(
            self.frames["strand_bias"], text="Fishers OR", anchor="e"
        )
        self.labels["VCF: Fisher Odds Ratio"].grid(
            column=0, row=4, sticky="news", padx=5
        )
        self.entries["VCF: Fisher Odds Ratio"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant["VCF: Fisher Odds Ratio"],
        )
        self.entries["VCF: Fisher Odds Ratio"].grid(
            column=1, row=4, sticky="news", pady=5, padx=5
        )
        self.labels["VCF: Fisher P Value"] = tk.Label(
            self.frames["strand_bias"], text="p.", anchor="e"
        )
        self.labels["VCF: Fisher P Value"].grid(column=2, row=4, sticky="news")
        self.entries["VCF: Fisher P Value"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant["VCF: Fisher P Value"],
            width=3,
        )
        self.entries["VCF: Fisher P Value"].grid(
            column=3, row=4, sticky="news", pady=5, padx=5
        )

        # Q20 Strand Bias Chi Square Area
        self.frames["Q20_sb_chi_square"] = tk.Frame(
            self.frames["strand_bias"], bootstyle="secondary"
        )
        self.frames["Q20_sb_chi_square"].grid(
            column=0, row=5, columnspan=4, rowspan=1, sticky="news", padx=5, pady=5
        )
        for x in range(3):
            self.frames["Q20_sb_chi_square"].rowconfigure(x, weight=1)
        for x in range(4):
            self.frames["Q20_sb_chi_square"].columnconfigure(x, weight=1)
        self.labels["Q20"] = tk.Label(
            self.frames["Q20_sb_chi_square"], text="Q20", width=8, anchor="c"
        )
        self.labels["Q20"].grid(
            column=0, row=0, rowspan=3, sticky="news", padx=5, pady=5
        )
        self.labels["Q20_fwd"] = tk.Label(
            self.frames["Q20_sb_chi_square"], text="Fwd", anchor="c", width=3
        )
        self.labels["Q20_fwd"].grid(column=2, row=0, sticky="news", pady=5, padx=5)
        self.labels["Q20_rev"] = tk.Label(
            self.frames["Q20_sb_chi_square"], text="Rev", anchor="c", width=3
        )
        self.labels["Q20_rev"].grid(column=3, row=0, sticky="news", pady=5, padx=5)
        self.labels["Q20_ref"] = tk.Label(
            self.frames["Q20_sb_chi_square"], text="Ref", anchor="c", width=3
        )
        self.labels["Q20_ref"].grid(column=1, row=1, sticky="news", pady=5, padx=5)
        self.labels["Q20_var"] = tk.Label(
            self.frames["Q20_sb_chi_square"], text="Var", anchor="c", width=3
        )
        self.labels["Q20_var"].grid(column=1, row=2, sticky="news", pady=5, padx=5)
        self.entries["Mpileup Qual: Filtered Reference Forward Read Depth"] = tk.Entry(
            self.frames["Q20_sb_chi_square"],
            textvariable=self.variant[
                "Mpileup Qual: Filtered Reference Forward Read Depth"
            ],
        )
        self.entries["Mpileup Qual: Filtered Reference Forward Read Depth"].grid(
            column=2, row=1, sticky="news", pady=5, padx=5
        )
        self.entries["Mpileup Qual: Filtered Reference Reverse Read Depth"] = tk.Entry(
            self.frames["Q20_sb_chi_square"],
            textvariable=self.variant[
                "Mpileup Qual: Filtered Reference Reverse Read Depth"
            ],
        )
        self.entries["Mpileup Qual: Filtered Reference Reverse Read Depth"].grid(
            column=3, row=1, sticky="news", pady=5, padx=5
        )
        self.entries["Mpileup Qual: Filtered Variant Forward Read Depth"] = tk.Entry(
            self.frames["Q20_sb_chi_square"],
            textvariable=self.variant[
                "Mpileup Qual: Filtered Variant Forward Read Depth"
            ],
        )
        self.entries["Mpileup Qual: Filtered Variant Forward Read Depth"].grid(
            column=2, row=2, sticky="news", pady=5, padx=5
        )
        self.entries["Mpileup Qual: Filtered Variant Reverse Read Depth"] = tk.Entry(
            self.frames["Q20_sb_chi_square"],
            textvariable=self.variant[
                "Mpileup Qual: Filtered Variant Reverse Read Depth"
            ],
        )
        self.entries["Mpileup Qual: Filtered Variant Reverse Read Depth"].grid(
            column=3, row=2, sticky="news", pady=5, padx=5
        )
        # Q20 Strand Bias Stats Area
        self.labels["Mpileup Qual: Filtered Variant Binomial Proportion"] = tk.Label(
            self.frames["strand_bias"], text="Binom. Prop.", anchor="e"
        )
        self.labels["Mpileup Qual: Filtered Variant Binomial Proportion"].grid(
            column=0, row=6, sticky="news", padx=5
        )
        self.entries["Mpileup Qual: Filtered Variant Binomial Proportion"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant[
                "Mpileup Qual: Filtered Variant Binomial Proportion"
            ],
        )
        self.entries["Mpileup Qual: Filtered Variant Binomial Proportion"].grid(
            column=1, row=6, sticky="news", pady=5, padx=5
        )
        self.labels["Mpileup Qual: Filtered Variant Binomial P Value"] = tk.Label(
            self.frames["strand_bias"], text="p.", anchor="e"
        )
        self.labels["Mpileup Qual: Filtered Variant Binomial P Value"].grid(
            column=2, row=6, sticky="news"
        )
        self.entries["Mpileup Qual: Filtered Variant Binomial P Value"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant[
                "Mpileup Qual: Filtered Variant Binomial P Value"
            ],
            width=5,
        )
        self.entries["Mpileup Qual: Filtered Variant Binomial P Value"].grid(
            column=3, row=6, sticky="news", pady=5, padx=5
        )
        self.labels["Mpileup Qual: Filtered Variant Fishers Odds Ratio"] = tk.Label(
            self.frames["strand_bias"], text="Fishers OR", anchor="e"
        )
        self.labels["Mpileup Qual: Filtered Variant Fishers Odds Ratio"].grid(
            column=0, row=7, sticky="news", padx=5
        )
        self.entries["Mpileup Qual: Filtered Variant Fishers Odds Ratio"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant[
                "Mpileup Qual: Filtered Variant Fishers Odds Ratio"
            ],
        )
        self.entries["Mpileup Qual: Filtered Variant Fishers Odds Ratio"].grid(
            column=1, row=7, sticky="news", pady=5, padx=5
        )
        self.labels["Mpileup Qual: Filtered Variant Fishers P Value"] = tk.Label(
            self.frames["strand_bias"], text="p.", anchor="e"
        )
        self.labels["Mpileup Qual: Filtered Variant Fishers P Value"].grid(
            column=2, row=7, sticky="news"
        )
        self.entries["Mpileup Qual: Filtered Variant Fishers P Value"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant["Mpileup Qual: Filtered Variant Fishers P Value"],
            width=5,
        )
        self.entries["Mpileup Qual: Filtered Variant Fishers P Value"].grid(
            column=3, row=7, sticky="news", pady=5, padx=5
        )

        # Q1 Strand Bias Chi Square Area
        self.frames["Q1_sb_chi_square"] = tk.Frame(
            self.frames["strand_bias"], bootstyle="secondary"
        )
        self.frames["Q1_sb_chi_square"].grid(
            column=0, row=8, columnspan=4, rowspan=1, sticky="news", padx=5, pady=5
        )
        for x in range(3):
            self.frames["Q1_sb_chi_square"].rowconfigure(x, weight=1)
        for x in range(4):
            self.frames["Q1_sb_chi_square"].columnconfigure(x, weight=1)
        self.labels["Q1"] = tk.Label(
            self.frames["Q1_sb_chi_square"], text="Q1", width=8, anchor="c"
        )
        self.labels["Q1"].grid(
            column=0, row=0, rowspan=3, sticky="news", padx=5, pady=5
        )
        self.labels["Q1_fwd"] = tk.Label(
            self.frames["Q1_sb_chi_square"], text="Fwd", anchor="c"
        )
        self.labels["Q1_fwd"].grid(column=2, row=0, sticky="news", pady=5, padx=5)
        self.labels["Q1_rev"] = tk.Label(
            self.frames["Q1_sb_chi_square"], text="Rev", anchor="c"
        )
        self.labels["Q1_rev"].grid(column=3, row=0, sticky="news", pady=5, padx=5)
        self.labels["Q1_ref"] = tk.Label(
            self.frames["Q1_sb_chi_square"], text="Ref", anchor="c"
        )
        self.labels["Q1_ref"].grid(column=1, row=1, sticky="news", pady=5, padx=5)
        self.labels["Q1_var"] = tk.Label(
            self.frames["Q1_sb_chi_square"], text="Var", anchor="c"
        )
        self.labels["Q1_var"].grid(column=1, row=2, sticky="news", pady=5, padx=5)
        self.entries[
            "Mpileup Qual: Unfiltered Reference Forward Read Depth"
        ] = tk.Entry(
            self.frames["Q1_sb_chi_square"],
            width=5,
            textvariable=self.variant[
                "Mpileup Qual: Unfiltered Reference Forward Read Depth"
            ],
        )
        self.entries["Mpileup Qual: Unfiltered Reference Forward Read Depth"].grid(
            column=2, row=1, sticky="news", pady=5, padx=5
        )
        self.entries[
            "Mpileup Qual: Unfiltered Reference Reverse Read Depth"
        ] = tk.Entry(
            self.frames["Q1_sb_chi_square"],
            width=5,
            textvariable=self.variant[
                "Mpileup Qual: Unfiltered Reference Reverse Read Depth"
            ],
        )
        self.entries["Mpileup Qual: Unfiltered Reference Reverse Read Depth"].grid(
            column=3, row=1, sticky="news", pady=5, padx=5
        )
        self.entries["Mpileup Qual: Unfiltered Variant Forward Read Depth"] = tk.Entry(
            self.frames["Q1_sb_chi_square"],
            width=5,
            textvariable=self.variant[
                "Mpileup Qual: Unfiltered Variant Forward Read Depth"
            ],
        )
        self.entries["Mpileup Qual: Unfiltered Variant Forward Read Depth"].grid(
            column=2, row=2, sticky="news", pady=5, padx=5
        )
        self.entries["Mpileup Qual: Unfiltered Variant Reverse Read Depth"] = tk.Entry(
            self.frames["Q1_sb_chi_square"],
            width=5,
            textvariable=self.variant[
                "Mpileup Qual: Unfiltered Variant Reverse Read Depth"
            ],
        )
        self.entries["Mpileup Qual: Unfiltered Variant Reverse Read Depth"].grid(
            column=3, row=2, sticky="news", pady=5, padx=5
        )
        # Q1 Strand Bias Stats Area
        self.labels["Mpileup Qual: Unfiltered Variant Binomial Proportion"] = tk.Label(
            self.frames["strand_bias"], text="Binom. Prop.", anchor="e"
        )
        self.labels["Mpileup Qual: Unfiltered Variant Binomial Proportion"].grid(
            column=0, row=9, sticky="news", pady=5, padx=5
        )
        self.entries["Mpileup Qual: Unfiltered Variant Binomial Proportion"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant[
                "Mpileup Qual: Unfiltered Variant Binomial Proportion"
            ],
        )
        self.entries["Mpileup Qual: Unfiltered Variant Binomial Proportion"].grid(
            column=1, row=9, sticky="news", pady=5, padx=5
        )
        self.labels["Mpileup Qual: Unfiltered Variant Binomial P Value"] = tk.Label(
            self.frames["strand_bias"], text="p.", anchor="e"
        )
        self.labels["Mpileup Qual: Unfiltered Variant Binomial P Value"].grid(
            column=2, row=9, sticky="news", pady=5, padx=5
        )
        self.entries["Mpileup Qual: Unfiltered Variant Binomial P Value"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant[
                "Mpileup Qual: Unfiltered Variant Binomial P Value"
            ],
            width=5,
        )
        self.entries["Mpileup Qual: Unfiltered Variant Binomial P Value"].grid(
            column=3, row=9, sticky="news", pady=5, padx=5
        )
        self.labels["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"] = tk.Label(
            self.frames["strand_bias"], text="Fishers OR", anchor="e"
        )
        self.labels["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"].grid(
            column=0, row=10, sticky="news", pady=5, padx=5
        )
        self.entries["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant[
                "Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"
            ],
        )
        self.entries["Mpileup Qual: Unfiltered Variant Fishers Odds Ratio"].grid(
            column=1, row=10, sticky="news", pady=5, padx=5
        )
        self.labels["Mpileup Qual: Unfiltered Variant Fishers P Value"] = tk.Label(
            self.frames["strand_bias"], text="p.", anchor="e"
        )
        self.labels["Mpileup Qual: Unfiltered Variant Fishers P Value"].grid(
            column=2, row=10, sticky="news", pady=5, padx=5
        )
        self.entries["Mpileup Qual: Unfiltered Variant Fishers P Value"] = tk.Entry(
            self.frames["strand_bias"],
            textvariable=self.variant[
                "Mpileup Qual: Unfiltered Variant Fishers P Value"
            ],
            width=5,
        )
        self.entries["Mpileup Qual: Unfiltered Variant Fishers P Value"].grid(
            column=3, row=10, sticky="news", pady=5, padx=5
        )

        # Genexus info frame
        self.frames["gx_info"] = tk.Frame(self.frames["middle"], bootstyle="secondary")
        self.frames["gx_info"].pack(
            side="top", expand=False, fill="both", padx=5, pady=5
        )
        for x in range(7):
            self.frames["gx_info"].rowconfigure(x, weight=1)
        for x in range(6):
            self.frames["gx_info"].columnconfigure(x, weight=1)
        self.labels["gx_info_frame_label"] = tk.Label(
            self.frames["gx_info"], text="Genexus Reported Information", anchor="c"
        )
        self.labels["gx_info_frame_label"].grid(
            row=0, column=0, columnspan=6, sticky="news", padx=5, pady=5
        )
        # gx info top area
        self.labels["VCF: AF"] = tk.Label(
            self.frames["gx_info"], text="Allele Fraction"
        )
        self.labels["VCF: AF"].grid(row=1, column=0, sticky="news", padx=5, pady=5)
        self.entries["VCF: AF"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["VCF: AF"]
        )
        self.entries["VCF: AF"].grid(row=2, column=0, sticky="news", padx=5, pady=5)
        self.labels["VCF: TYPE"] = tk.Label(self.frames["gx_info"], text="Variant Type")
        self.labels["VCF: TYPE"].grid(row=1, column=1, sticky="news", padx=5, pady=5)
        self.entries["VCF: TYPE"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["VCF: TYPE"]
        )
        self.entries["VCF: TYPE"].grid(row=2, column=1, sticky="news", padx=5, pady=5)
        self.labels["VCF: LEN"] = tk.Label(
            self.frames["gx_info"], text="Length of Variant (BP)"
        )
        self.labels["VCF: LEN"].grid(row=1, column=2, sticky="news", padx=5, pady=5)
        self.entries["VCF: LEN"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["VCF: LEN"]
        )
        self.entries["VCF: LEN"].grid(row=2, column=2, sticky="news", padx=5, pady=5)
        self.labels["VCF: Genotype"] = tk.Label(self.frames["gx_info"], text="Genotype")
        self.labels["VCF: Genotype"].grid(
            row=1, column=3, sticky="news", padx=5, pady=5
        )
        self.entries["VCF: Genotype"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["VCF: Genotype"]
        )
        self.entries["VCF: Genotype"].grid(
            row=2, column=3, sticky="news", padx=5, pady=5
        )
        self.labels["VCF: Filter"] = tk.Label(
            self.frames["gx_info"], text="Filter (Genexus)"
        )
        self.labels["VCF: Filter"].grid(row=1, column=4, sticky="news", padx=5, pady=5)
        self.entries["VCF: Filter"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["VCF: Filter"]
        )
        self.entries["VCF: Filter"].grid(row=2, column=4, sticky="news", padx=5, pady=5)
        self.labels["VCF: QUAL"] = tk.Label(
            self.frames["gx_info"], text="Quality Score"
        )
        self.labels["VCF: QUAL"].grid(row=1, column=5, sticky="news", padx=5, pady=5)
        self.entries["VCF: QUAL"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["VCF: QUAL"]
        )
        self.entries["VCF: QUAL"].grid(
            row=2, column=5, rowspan=3, sticky="news", padx=5, pady=5
        )
        # gx info middle row
        self.labels["VCF: FAO"] = tk.Label(self.frames["gx_info"], text="FAO")
        self.labels["VCF: FAO"].grid(row=3, column=0, sticky="news", padx=5, pady=5)
        self.entries["VCF: FAO"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["VCF: FAO"]
        )
        self.entries["VCF: FAO"].grid(row=4, column=0, sticky="news", padx=5, pady=5)
        self.labels["VCF: FDP"] = tk.Label(self.frames["gx_info"], text="FDP")
        self.labels["VCF: FDP"].grid(row=3, column=1, sticky="news", padx=5, pady=5)
        self.entries["VCF: FDP"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["VCF: FDP"]
        )
        self.entries["VCF: FDP"].grid(row=4, column=1, sticky="news", padx=5, pady=5)
        self.labels["VCF: HRUN"] = tk.Label(self.frames["gx_info"], text="HRUN")
        self.labels["VCF: HRUN"].grid(row=3, column=2, sticky="news", padx=5, pady=5)
        self.entries["VCF: HRUN"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["VCF: HRUN"]
        )
        self.entries["VCF: HRUN"].grid(row=4, column=2, sticky="news", padx=5, pady=5)
        self.labels["VCF: QD"] = tk.Label(self.frames["gx_info"], text="QD")
        self.labels["VCF: QD"].grid(row=3, column=3, sticky="news", padx=5, pady=5)
        self.entries["VCF: QD"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["VCF: QD"]
        )
        self.entries["VCF: QD"].grid(row=4, column=3, sticky="news", padx=5, pady=5)
        self.labels["VCF: SVTYPE"] = tk.Label(
            self.frames["gx_info"], text="SVTYPE (Unused)"
        )
        self.labels["VCF: SVTYPE"].grid(row=3, column=4, sticky="news", padx=5, pady=5)
        self.entries["VCF: SVTYPE"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["VCF: SVTYPE"]
        )
        self.entries["VCF: SVTYPE"].grid(row=4, column=4, sticky="news", padx=5, pady=5)
        # GX info bottom row
        self.labels["Genexus_transcript (GRCh37)"] = tk.Label(
            self.frames["gx_info"], text="Genexus Transcript (GRCh37)"
        )
        self.labels["Genexus_transcript (GRCh37)"].grid(
            row=5, column=0, columnspan=2, sticky="news", padx=5, pady=5
        )
        self.entries["Genexus_transcript (GRCh37)"] = tk.Entry(
            self.frames["gx_info"],
            textvariable=self.variant["Genexus_transcript (GRCh37)"],
        )
        self.entries["Genexus_transcript (GRCh37)"].grid(
            row=6, column=0, columnspan=2, sticky="news", padx=5, pady=5
        )
        self.labels["Genexus_Exon(s)"] = tk.Label(
            self.frames["gx_info"], text="Genexus Exon(s)"
        )
        self.labels["Genexus_Exon(s)"].grid(
            row=5, column=2, columnspan=2, sticky="news", padx=5, pady=5
        )
        self.entries["Genexus_Exon(s)"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["Genexus_Exon(s)"]
        )
        self.entries["Genexus_Exon(s)"].grid(
            row=6, column=2, columnspan=2, sticky="news", padx=5, pady=5
        )
        self.labels["Genexus_codons"] = tk.Label(
            self.frames["gx_info"], text="Genexus Codons"
        )
        self.labels["Genexus_codons"].grid(
            row=5, column=4, columnspan=2, sticky="news", padx=5, pady=5
        )
        self.entries["Genexus_codons"] = tk.Entry(
            self.frames["gx_info"], textvariable=self.variant["Genexus_codons"]
        )
        self.entries["Genexus_codons"].grid(
            row=6, column=4, columnspan=2, sticky="news", padx=5, pady=5
        )

        # mpileup info frame
        self.frames["mpl_info"] = tk.Frame(self.frames["middle"], bootstyle="secondary")
        self.frames["mpl_info"].pack(
            side="top", expand=False, fill="both", padx=5, pady=5
        )
        for x in range(5):
            self.frames["mpl_info"].columnconfigure(x, weight=1)
        for x in range(3):
            self.frames["mpl_info"].rowconfigure(x, weight=1)
        self.labels["mpl_info_label"] = tk.Label(
            self.frames["mpl_info"], text="Mpileup Reported Information", anchor="c"
        )
        self.labels["mpl_info_label"].grid(
            column=0, row=0, columnspan=5, sticky="news", padx=5, pady=5
        )
        self.labels["Mpileup Qual: Filtered VAF"] = tk.Label(
            self.frames["mpl_info"], text="Filtered VAF (Q20)", anchor="c"
        )
        self.labels["Mpileup Qual: Filtered VAF"].grid(
            column=0, row=1, sticky="news", padx=5, pady=5
        )
        self.entries["Mpileup Qual: Filtered VAF"] = tk.Entry(
            self.frames["mpl_info"],
            textvariable=self.variant["Mpileup Qual: Filtered VAF"],
        )
        self.entries["Mpileup Qual: Filtered VAF"].grid(
            column=0, row=2, sticky="news", padx=5, pady=5
        )
        self.labels["Mpileup Qual: Unfiltered VAF"] = tk.Label(
            self.frames["mpl_info"], text="Unfiltered VAF (Q1)", anchor="c"
        )
        self.labels["Mpileup Qual: Unfiltered VAF"].grid(
            column=1, row=1, sticky="news", padx=5, pady=5
        )
        self.entries["Mpileup Qual: Unfiltered VAF"] = tk.Entry(
            self.frames["mpl_info"],
            textvariable=self.variant["Mpileup Qual: Unfiltered VAF"],
        )
        self.entries["Mpileup Qual: Unfiltered VAF"].grid(
            column=1, row=2, sticky="news", padx=5, pady=5
        )
        self.labels["Mpileup Qual: Read Depth"] = tk.Label(
            self.frames["mpl_info"], text="Total Read Depth", anchor="c"
        )
        self.labels["Mpileup Qual: Read Depth"].grid(
            column=2, row=1, sticky="news", padx=5, pady=5
        )
        self.entries["Mpileup Qual: Read Depth"] = tk.Entry(
            self.frames["mpl_info"],
            textvariable=self.variant["Mpileup Qual: Read Depth"],
        )
        self.entries["Mpileup Qual: Read Depth"].grid(
            column=2, row=2, sticky="news", padx=5, pady=5
        )
        self.labels["Mpileup Qual: Start Reads"] = tk.Label(
            self.frames["mpl_info"], text="Count: Read Starts", anchor="c"
        )
        self.labels["Mpileup Qual: Start Reads"].grid(
            column=3, row=1, sticky="news", padx=5, pady=5
        )
        self.entries["Mpileup Qual: Start Reads"] = tk.Entry(
            self.frames["mpl_info"],
            textvariable=self.variant["Mpileup Qual: Start Reads"],
        )
        self.entries["Mpileup Qual: Start Reads"].grid(
            column=3, row=2, sticky="news", padx=5, pady=5
        )
        self.labels["Mpileup Qual: Stop Reads"] = tk.Label(
            self.frames["mpl_info"], text="Count: Read Ends", anchor="c"
        )
        self.labels["Mpileup Qual: Stop Reads"].grid(
            column=4, row=1, sticky="news", padx=5, pady=5
        )
        self.entries["Mpileup Qual: Stop Reads"] = tk.Entry(
            self.frames["mpl_info"],
            textvariable=self.variant["Mpileup Qual: Stop Reads"],
        )
        self.entries["Mpileup Qual: Stop Reads"].grid(
            column=4, row=2, sticky="news", padx=5, pady=5
        )

        # Other frame, used as a spacer
        self.frames["other"] = tk.Frame(self.frames["middle"])
        self.frames["other"].pack(side="top", expand=True, fill="both")

        # Variant Annotation Info Frame
        self.frames["var_annot"] = tk.Frame(self.frames["other"], bootstyle="secondary")
        self.frames["var_annot"].pack(
            side="left", expand=True, fill="both", padx=5, pady=5
        )
        for x in range(4):
            self.frames["var_annot"].columnconfigure(x, weight=1)
        self.frames["var_annot"].rowconfigure(4, weight=99)
        self.labels["var_annot_label"] = tk.Label(
            self.frames["var_annot"], text="Variant Annotations", anchor="c"
        )
        self.labels["var_annot_label"].grid(
            column=0, row=0, columnspan=4, sticky="news", padx=5, pady=5
        )
        self.labels["Variant Annotation: Coding"] = tk.Label(
            self.frames["var_annot"], text="Coding Region"
        )
        self.labels["Variant Annotation: Coding"].grid(
            column=0, row=1, sticky="news", padx=5, pady=5
        )
        self.entries["Variant Annotation: Coding"] = tk.Entry(
            self.frames["var_annot"],
            textvariable=self.variant["Variant Annotation: Coding"],
        )
        self.entries["Variant Annotation: Coding"].grid(
            column=0, row=2, sticky="news", padx=5, pady=5
        )
        self.labels["Variant Annotation: Sequence Ontology"] = tk.Label(
            self.frames["var_annot"], text="Var. Type (Seq. Ontol.)"
        )
        self.labels["Variant Annotation: Sequence Ontology"].grid(
            column=1, row=1, sticky="news", padx=5, pady=5
        )
        self.entries["Variant Annotation: Sequence Ontology"] = tk.Entry(
            self.frames["var_annot"],
            textvariable=self.variant["Variant Annotation: Sequence Ontology"],
        )
        self.entries["Variant Annotation: Sequence Ontology"].grid(
            column=1, row=2, sticky="news", padx=5, pady=5
        )
        self.labels["Variant Annotation: Transcript"] = tk.Label(
            self.frames["var_annot"], text="ENST Transcript"
        )
        self.labels["Variant Annotation: Transcript"].grid(
            column=2, row=1, sticky="news", padx=5, pady=5
        )
        self.entries["Variant Annotation: Transcript"] = tk.Entry(
            self.frames["var_annot"],
            textvariable=self.variant["Variant Annotation: Transcript"],
        )
        self.entries["Variant Annotation: Transcript"].grid(
            column=2, row=2, sticky="news", padx=5, pady=5
        )
        self.labels["Variant Annotation: RefSeq"] = tk.Label(
            self.frames["var_annot"], text="RefSeq"
        )
        self.labels["Variant Annotation: RefSeq"].grid(
            column=3, row=1, sticky="news", padx=5, pady=5
        )
        self.entries["Variant Annotation: RefSeq"] = tk.Entry(
            self.frames["var_annot"],
            textvariable=self.variant["VCF: LEN"],
            bootstyle="primary",
        )
        self.entries["Variant Annotation: RefSeq"].grid(
            column=3, row=2, sticky="news", padx=5, pady=5
        )
        self.labels["Variant Annotation: All Mappings"] = tk.Label(
            self.frames["var_annot"], text="All Mappings", anchor="c"
        )
        self.labels["Variant Annotation: All Mappings"].grid(
            column=0, row=3, columnspan=4, sticky="news", padx=5, pady=5
        )
        self.textboxes["Variant Annotation: All Mappings"] = tk.ScrolledText(
            self.frames["var_annot"], height=1
        )
        self.textboxes["Variant Annotation: All Mappings"].grid(
            column=0, columnspan=4, row=4, sticky="news", padx=5, pady=5
        )

        # MDL Info area
        self.frames["mdl"] = tk.Frame(self.frames["other"], bootstyle="secondary")
        self.frames["mdl"].pack(side="left", expand=True, fill="both", padx=5, pady=5)
        self.frames["mdl"].rowconfigure(4, weight=99)
        self.frames["mdl"].columnconfigure(0, weight=1)
        self.frames["mdl"].columnconfigure(1, weight=1)
        self.labels["mdl_info_label"] = tk.Label(
            self.frames["mdl"], text="MDL Information", anchor="c"
        )
        self.labels["mdl_info_label"].grid(
            column=0, row=0, columnspan=2, sticky="news", padx=5, pady=5
        )
        self.labels["MDL: Sample Count"] = tk.Label(
            self.frames["mdl"], text="Sample Count"
        )
        self.labels["MDL: Sample Count"].grid(
            column=0, row=1, sticky="news", padx=5, pady=5
        )
        self.entries["MDL: Sample Count"] = tk.Entry(
            self.frames["mdl"], textvariable=self.variant["MDL: Sample Count"]
        )
        self.entries["MDL: Sample Count"].grid(
            column=0, row=2, sticky="news", padx=5, pady=5
        )
        self.labels["MDL: Variant Frequency"] = tk.Label(
            self.frames["mdl"], text="Variant Frequency"
        )
        self.labels["MDL: Variant Frequency"].grid(
            column=1, row=1, sticky="news", padx=5, pady=5
        )
        self.entries["MDL: Variant Frequency"] = tk.Entry(
            self.frames["mdl"], textvariable=self.variant["MDL: Variant Frequency"]
        )
        self.entries["MDL: Variant Frequency"].grid(
            column=1, row=2, sticky="news", padx=5, pady=5
        )
        self.labels["MDL: Sample List"] = tk.Label(
            self.frames["mdl"], text="Sample Numbers", anchor="c"
        )
        self.labels["MDL: Sample List"].grid(
            column=0, row=3, sticky="news", padx=5, pady=5
        )
        self.textboxes["MDL: Sample List"] = tk.ScrolledText(
            self.frames["mdl"], height=1
        )
        self.textboxes["MDL: Sample List"].grid(
            column=0, row=4, sticky="news", padx=5, pady=5
        )
        self.labels["test_tissue"] = tk.Label(
            self.frames["mdl"], text="Sample Tissues", anchor="c"
        )
        self.labels["test_tissue"].grid(column=1, row=3, sticky="news", padx=5, pady=5)
        self.textboxes["test_tissue"] = tk.ScrolledText(self.frames["mdl"], height=1)
        self.textboxes["test_tissue"].grid(
            column=1, row=4, sticky="news", padx=5, pady=5
        )

        # Web Resources Stats
        self.frames["bottom"] = tk.Frame(self.frames["right"], bootstyle="secondary")
        self.frames["bottom"].pack(
            side="bottom", expand=False, fill="both", padx=5, pady=5
        )
        for x in range(10):
            self.frames["bottom"].columnconfigure(x, weight=1)
        for x in range(6):
            self.frames["bottom"].rowconfigure(x, weight=1)
        self.labels["web_info_label"] = tk.Label(
            self.frames["bottom"],
            text="Internet Resource Information and Links",
            anchor="c",
        )
        self.labels["web_info_label"].grid(
            column=0, row=0, columnspan=10, sticky="news", padx=5, pady=5
        )

        # Clinvar Area
        self.labels["ClinVar: ClinVar ID"] = tk.Label(
            self.frames["bottom"], text="ClinVar:"
        )
        self.labels["ClinVar: ClinVar ID"].grid(
            column=0, row=1, sticky="news", padx=5, pady=5
        )
        self.labels["ClinVar ID"] = tk.Label(self.frames["bottom"], text="ID")
        self.labels["ClinVar ID"].grid(column=0, row=2, sticky="news", padx=5, pady=5)
        self.entries["ClinVar: ClinVar ID"] = tk.Entry(
            self.frames["bottom"], textvariable=self.variant["ClinVar: ClinVar ID"]
        )
        self.entries["ClinVar: ClinVar ID"].grid(
            column=0, row=3, sticky="news", padx=5, pady=5
        )
        self.labels["ClinVar: Clinical Significance"] = tk.Label(
            self.frames["bottom"], text="Significance"
        )
        self.labels["ClinVar: Clinical Significance"].grid(
            column=0, row=4, sticky="news", padx=5, pady=5
        )
        self.entries["ClinVar: Clinical Significance"] = tk.Entry(
            self.frames["bottom"],
            textvariable=self.variant["ClinVar: Clinical Significance"],
        )
        self.entries["ClinVar: Clinical Significance"].grid(
            column=0, row=5, sticky="news", padx=5, pady=5
        )

        # Gnomad Area
        self.labels["gnomAD3: Global AF"] = tk.Label(
            self.frames["bottom"], text="gnomAD3:"
        )
        self.labels["gnomAD3: Global AF"].grid(
            column=1, row=1, sticky="news", padx=5, pady=5
        )
        self.labels["Global AF"] = tk.Label(self.frames["bottom"], text="Global AF")
        self.labels["Global AF"].grid(column=1, row=2, sticky="news", padx=5, pady=5)
        self.entries["gnomAD3: Global AF"] = tk.Entry(
            self.frames["bottom"], textvariable=self.variant["gnomAD3: Global AF"]
        )
        self.entries["gnomAD3: Global AF"].grid(
            column=1, row=3, rowspan=3, sticky="news", padx=5, pady=5
        )

        # CADD Area
        self.labels["CADD:"] = tk.Label(self.frames["bottom"], text="CADD:")
        self.labels["CADD:"].grid(column=2, row=1, sticky="news", padx=5, pady=5)
        self.labels["Phred"] = tk.Label(self.frames["bottom"], text="Phred Score")
        self.labels["Phred"].grid(column=2, row=2, sticky="news", padx=5, pady=5)
        self.entries["CADD: Phred"] = tk.Entry(
            self.frames["bottom"], textvariable=self.variant["CADD: Phred"]
        )
        self.entries["CADD: Phred"].grid(
            column=2, row=3, rowspan=3, sticky="news", padx=5, pady=5
        )

        # PolyPhen Area
        self.labels["PolyPhen-2:"] = tk.Label(self.frames["bottom"], text="PolyPhen-2:")
        self.labels["PolyPhen-2:"].grid(column=3, row=1, sticky="news", padx=5, pady=5)
        self.labels["HDIV Prediction"] = tk.Label(
            self.frames["bottom"], text="HDIV Predict."
        )
        self.labels["HDIV Prediction"].grid(
            column=3, row=2, sticky="news", padx=5, pady=5
        )
        self.entries["PolyPhen-2: HDIV Prediction"] = tk.Entry(
            self.frames["bottom"],
            textvariable=self.variant["PolyPhen-2: HDIV Prediction"],
        )
        self.entries["PolyPhen-2: HDIV Prediction"].grid(
            column=3, row=3, rowspan=3, sticky="news", padx=5, pady=5
        )

        # SIFT Area
        self.labels["SIFT"] = tk.Label(self.frames["bottom"], text="SIFT:")
        self.labels["SIFT"].grid(column=4, row=1, sticky="news", padx=5, pady=5)
        self.labels["Prediction"] = tk.Label(self.frames["bottom"], text="Prediction")
        self.labels["Prediction"].grid(column=4, row=2, sticky="news", padx=5, pady=5)
        self.entries["SIFT: Prediction"] = tk.Entry(
            self.frames["bottom"], textvariable=self.variant["SIFT: Prediction"]
        )
        self.entries["SIFT: Prediction"].grid(
            column=4, row=3, rowspan=3, sticky="news", padx=5, pady=5
        )

        # dbSNP Area
        self.labels["dbSNP: rsID"] = tk.Label(self.frames["bottom"], text="dbSNP:")
        self.labels["dbSNP: rsID"].grid(column=5, row=1, sticky="news", padx=5, pady=5)
        self.labels["rsID"] = tk.Label(self.frames["bottom"], text="rsID")
        self.labels["rsID"].grid(column=5, row=2, sticky="news", padx=5, pady=5)
        self.entries["dbSNP: rsID"] = tk.Entry(
            self.frames["bottom"], textvariable=self.variant["dbSNP: rsID"]
        )
        self.entries["dbSNP: rsID"].grid(
            column=5, row=3, rowspan=3, sticky="news", padx=5, pady=5
        )

        # UniProt Area
        self.labels["UniProt (GENE): Accession Number"] = tk.Label(
            self.frames["bottom"], text="UniProt (Gene):"
        )
        self.labels["UniProt (GENE): Accession Number"].grid(
            column=6, row=1, sticky="news", padx=5, pady=5
        )
        self.labels["Accession Number"] = tk.Label(
            self.frames["bottom"], text="Accession #"
        )
        self.labels["Accession Number"].grid(
            column=6, row=2, sticky="news", padx=5, pady=5
        )
        self.entries["UniProt (GENE): Accession Number"] = tk.Entry(
            self.frames["bottom"],
            textvariable=self.variant["UniProt (GENE): Accession Number"],
        )
        self.entries["UniProt (GENE): Accession Number"].grid(
            column=6, row=3, rowspan=3, sticky="news", padx=5, pady=5
        )

        # PhyloP Vertscore Area
        self.labels["PhyloP:"] = tk.Label(self.frames["bottom"], text="PhyloP:")
        self.labels["PhyloP:"].grid(column=7, row=1, sticky="news", padx=5, pady=5)
        self.labels["Vert Score"] = tk.Label(self.frames["bottom"], text="Vert Score")
        self.labels["Vert Score"].grid(column=7, row=2, sticky="news", padx=5, pady=5)
        self.entries["PhyloP: Vert Score"] = tk.Entry(
            self.frames["bottom"], textvariable=self.variant["PhyloP: Vert Score"]
        )
        self.entries["PhyloP: Vert Score"].grid(
            column=7, row=3, rowspan=3, sticky="news", padx=5, pady=5
        )

        # COSMIC Area
        self.labels["COSMIC: ID"] = tk.Label(
            self.frames["bottom"], text="COSMIC:", anchor="center"
        )
        self.labels["COSMIC: ID"].grid(column=8, row=1, sticky="news", padx=5, pady=5)
        self.labels["ID"] = tk.Label(self.frames["bottom"], text="ID", anchor="center")
        self.labels["ID"].grid(column=8, row=2, sticky="news", padx=5, pady=5)
        self.entries["COSMIC: ID"] = tk.Entry(
            self.frames["bottom"], textvariable=self.variant["COSMIC: ID"], width=12
        )
        self.entries["COSMIC: ID"].grid(column=8, row=3, sticky="news", padx=5, pady=5)
        self.labels["Variant Count"] = tk.Label(
            self.frames["bottom"], text="Var. Count"
        )
        self.labels["Variant Count"].grid(
            column=8, row=4, sticky="news", padx=5, pady=5
        )
        self.entries["COSMIC: Variant Count"] = tk.Entry(
            self.frames["bottom"], textvariable=self.variant["COSMIC: Variant Count"]
        )
        self.entries["COSMIC: Variant Count"].grid(
            column=8, row=5, sticky="news", padx=5, pady=5
        )

        # COSMIC Tissue Variant Count Region
        self.textboxes["COSMIC: Variant Count (Tissue)"] = tk.ScrolledText(
            self.frames["bottom"], height=1
        )
        self.textboxes["COSMIC: Variant Count (Tissue)"].grid(
            column=9, row=1, rowspan=5, sticky="news", padx=5, pady=5
        )

        self.adjust_colors()
        self.create_tooltips()
        self.create_weblinks()

        return None

    def create_tooltips(self) -> None:
        """Create tooltips for labels."""

        for key, value in TOOLTIPS.items():
            if type(self.labels[key]) is type(dict()):
                pass
            else:
                CreateToolTip(self.labels[key], value)

        return None

    def adjust_colors(self) -> None:
        """Method to update the colors of the widgets."""

        # Adjust all the widgets
        for key, value in self.labels.items():
            value.configure(anchor="c", bootstyle="secondary.inverse")
        for key, value in self.entries.items():
            value.configure(justify=tk.CENTER, bootstyle="normal", width=5)
        for x in [
            "web_info_label",
            "mdl_info_label",
            "sb_frame_label",
            "gx_info_frame_label",
            "basic_info_frame_label",
            "var_annot_label",
            "mpl_info_label",
            "file_info_label",
            "disposition_label",
        ]:
            self.labels[x].configure(bootstyle="primary.inverse")
        for x in VALIDATION["web_links"].keys():
            self.labels[x].configure(bootstyle="info.inverse")
        for key, value in self.buttons.items():
            value.configure(bootstyle="success")

        return None

    def create_weblinks(self) -> None:
        """Method to create links to websites."""

        self.links = dict()

        for key, value in VALIDATION["web_links"].items():
            self.labels[key].configure(cursor="hand2")

        # Very manual here.  Trying to automate this produced bugs.
        self.labels["Variant Annotation: Transcript"].bind(
            "<Button-1>",
            lambda _: webbrowser.open(
                f"https://useast.ensembl.org/Homo_sapiens/Transcript/Summary?t={self.entries['Variant Annotation: Transcript'].get()}"
            ),
        )
        self.labels["COSMIC: ID"].bind(
            "<Button-1>",
            lambda _: webbrowser.open(
                f"https://cancer.sanger.ac.uk/cosmic/search?q={self.entries['COSMIC: ID'].get()}"
            ),
        )
        self.labels["ClinVar: ClinVar ID"].bind(
            "<Button-1>",
            lambda _: webbrowser.open(
                f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{self.entries['ClinVar: ClinVar ID'].get()}"
            ),
        )
        self.labels["dbSNP: rsID"].bind(
            "<Button-1>",
            lambda _: webbrowser.open(
                f"https://www.ncbi.nlm.nih.gov/snp/{self.entries['dbSNP: rsID'].get()}"
            ),
        )
        self.labels["UniProt (GENE): Accession Number"].bind(
            "<Button-1>",
            lambda _: webbrowser.open(
                f"https://www.uniprot.org/uniprotkb/{self.entries['UniProt (GENE): Accession Number'].get()}/entry"
            ),
        )

        # IGV linked from "Gene" Label, opens on local machine
        self.labels["Variant Annotation: Gene"].bind(
            "<Button-1>",
            lambda _: webbrowser.open(
                f"http://localhost:{60151}/goto?locus={self.entries['Variant Annotation: Gene'].get()}"
            ),
        )

        return None

    def load_file(self) -> None:
        """Simple method to open a filename dialog and store the value."""

        self.filename.set(str(fd.askopenfilename(filetypes=[("XLSX", "*.xlsx")])))

        return None

    def load_treeview(self, variant_list) -> None:
        """Loads the information from the model into the treeview widget."""

        # Clearing the treeview
        for item in self.treeviews["variant_list"].get_children():
            self.treeviews["variant_list"].delete(item)

        # Stepping through all variants and creating treeview entries
        for variant in variant_list:
            values_list = list()
            for key in DATA_FIELDS:
                # trying to sort the data elements into ints first, then floats if they're not ints, and lastly strings if neither.
                test_me = variant[key]
                try:
                    if float(test_me) == int(test_me):
                        values_list.append(int(variant[key]))
                    else:
                        values_list.append(
                            round(float(variant[key]), 3)
                        )  # Rounding to 3 decimals to prevent crazy long floats
                except:
                    values_list.append(variant[key])

            # lastly, add the values list to the treeview
            # Note: tags in treeviews cannot have spaces in them, hence the .replace() here
            self.treeviews["variant_list"].insert(
                "",
                tk.END,
                values=values_list,
                tags=(str(variant["Disposition"])).replace(" ", "_"),
            )

        self.treeviews["variant_list"].selection_set(
            self.treeviews["variant_list"].get_children()[0]
        )

        return None

    def clear_view(self) -> None:
        """Method to clear all data from the widgets."""

        for item in self.treeviews["variant_list"].get_children():
            self.treeviews["variant_list"].delete(item)

        # clearing data fields
        for x in DATA_FIELDS:
            self.variant[x].set("")
            self.entries[x].configure(bootstyle="normal.TLabel")

        self.variant["Disposition"].set(0)
        self.filename.set("")

        # Cleaning up the textbox widgets by reloading the text
        self.textboxes["COSMIC: Variant Count (Tissue)"].delete("1.0", tk.END)
        self.textboxes["MDL: Sample List"].delete("1.0", tk.END)
        self.textboxes["Variant Annotation: All Mappings"].delete("1.0", tk.END)
        self.textboxes["test_tissue"].delete("1.0", tk.END)

        return None

    def record_selected(self, *args) -> None:
        """Method for selecting a record from the variant list treeview to display."""

        # technically able to select multiple lines from the treeview...  We only want one
        # This will cycle through to the final selection.
        for selected_item in self.treeviews["variant_list"].selection():
            item = self.treeviews["variant_list"].item(selected_item)
            record = item["values"]
            for x in range(len(DATA_FIELDS)):
                self.variant[DATA_FIELDS[x]].set(record[x])

        self.selection_index.set(
            self.treeviews["variant_list"].index(self.treeviews["variant_list"].focus())
        )
        self.variant["Disposition"].set(
            record[-1]
        )  # Disposition needs to always be last in the list

        # deactivating the save dispo button if theres no data
        if self.variant["Disposition"].get():
            self.buttons["save_disposition"]["state"] = "normal"

        # updating the data validation
        self.validate_cells()

        # Cleaning up the textbox widgets by reloading the text
        self.textboxes["COSMIC: Variant Count (Tissue)"].delete("1.0", tk.END)
        self.textboxes["COSMIC: Variant Count (Tissue)"].insert(
            tk.END, self.variant["COSMIC: Variant Count (Tissue)"].get()
        )
        self.textboxes["MDL: Sample List"].delete("1.0", tk.END)
        self.textboxes["MDL: Sample List"].insert(
            tk.END, self.variant["MDL: Sample List"].get()
        )
        self.textboxes["Variant Annotation: All Mappings"].delete("1.0", tk.END)
        self.textboxes["Variant Annotation: All Mappings"].insert(
            tk.END, self.variant["Variant Annotation: All Mappings"].get()
        )
        self.textboxes["test_tissue"].delete("1.0", tk.END)
        self.textboxes["test_tissue"].insert(tk.END, self.variant["test_tissue"].get())

        return None

    def record_update(self) -> dict:
        """Method to return user-entered data into the record, in case things need to be updated."""

        # create an updated record from field widget information (which may have been updated) with disposition
        updated_record = dict()
        for field in DATA_FIELDS:
            updated_record[field] = self.variant[field].get()

        # now to put the data back into the treeview at the right location
        selected = self.treeviews["variant_list"].focus()
        self.treeviews["variant_list"].item(selected, text="", values=updated_record)

        return updated_record

    def validate_cells(self) -> None:
        """Data validation (lite) method.  Works by simply coloring widget fields appropriate to their validation values."""

        for x in DATA_FIELDS:
            # Reset all styles to "normal"
            self.entries[x].configure(bootstyle="primary")

            # Mark all empty fields as "dark"
            if self.variant[x].get() == "None" or self.variant[x].get() == "":
                self.entries[x].configure(bootstyle="dark")

            # p-value logic
            if x in VALIDATION["p_values"] and self.variant[x].get() != "None":
                if (
                    float(self.variant[x].get())
                    > VALIDATION["cutoffs"]["p_value_max_red"]
                ):
                    self.entries[x].configure(bootstyle="danger")
                if (
                    float(self.variant[x].get())
                    < VALIDATION["cutoffs"]["p_value_max_green"]
                ):
                    self.entries[x].configure(bootstyle="success")
                if (
                    float(self.variant[x].get())
                    < VALIDATION["cutoffs"]["p_value_max_gold"]
                ):
                    self.entries[x].configure(bootstyle="warning")

            # forward and reverse strand read depth needs to meet NYSDOH 10x coverage
            if x in VALIDATION["strand_read_depth"] and self.variant[x].get() != "None":
                if (
                    int(self.variant[x].get())
                    <= VALIDATION["cutoffs"]["strand_read_depth_min_yellow"]
                ):
                    self.entries[x].configure(bootstyle="warning")
                if (
                    int(self.variant[x].get())
                    <= VALIDATION["cutoffs"]["strand_read_depth_min_red"]
                ):
                    self.entries[x].configure(bootstyle="danger")

            # minimum read depth for locus
            if x in VALIDATION["locus_read_depth"] and self.variant[x].get() != "None":
                if (
                    int(self.variant[x].get())
                    <= VALIDATION["cutoffs"]["locus_read_depth_min_red"]
                ):
                    self.entries[x].configure(bootstyle="danger")

            # VAF cutoffs ('normal', 'low-vaf', 'too-low')
            if x in VALIDATION["minimum_vaf"] and self.variant[x].get() != "None":
                if (
                    float(self.variant[x].get())
                    < VALIDATION["cutoffs"]["vaf_threshold_min_yellow"]
                ):
                    self.entries[x].configure(bootstyle="warning")
                if (
                    float(self.variant[x].get())
                    < VALIDATION["cutoffs"]["vaf_threshold_min_red"]
                ):
                    self.entries[x].configure(bootstyle="danger")

            # Odds-Ratio max/min (min is reciprocal of max, 1 is balanced)
            if (
                x in VALIDATION["fisher_odds_ratios"]
                and self.variant[x].get() != "None"
            ):
                if (
                    float(self.variant[x].get())
                    < VALIDATION["cutoffs"]["odds_ratio_min"]
                ):
                    self.entries[x].configure(bootstyle="danger")
                if (
                    float(self.variant[x].get())
                    > VALIDATION["cutoffs"]["odds_ratio_max"]
                ):
                    self.entries[x].configure(bootstyle="danger")

            # Binomial Proportion max/min (min is reciprocal of max, 0.5 is balanced)
            if (
                x in VALIDATION["binomial_proportions"]
                and self.variant[x].get() != "None"
            ):
                if float(self.variant[x].get()) < VALIDATION["cutoffs"]["bi_prop_min"]:
                    self.entries[x].configure(bootstyle="danger")
                if float(self.variant[x].get()) > VALIDATION["cutoffs"]["bi_prop_max"]:
                    self.entries[x].configure(bootstyle="danger")

            # denoting web links with a blue color
            if x in VALIDATION["web_links"].keys():
                self.labels[x].configure(bootstyle="info.inverse")
                self.entries[x].configure(bootstyle="info")

        return None


# MAIN LOOP ----------------------------------------------


def main():
    pass
    return


if __name__ == "__main__":
    main()
