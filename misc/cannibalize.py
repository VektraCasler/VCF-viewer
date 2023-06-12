# CSViewer.py
''' An application to view a csv file. '''

# IMPORTS ------------------------------------------------

import os 
import json
import webbrowser

# VARIABLES ----------------------------------------------

settings_filename = 'settings.json'
if os.path.exists(settings_filename):
    SETTINGS = json.load(settings_filename)
else:
    SETTINGS = {
        'VAF Threshold': 2.0,
        'Read Depth Threshold': 500,
        'Fwd/Rev RD Cutoff': 10,
    }

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

# Variables
variables = dict()
variables['filename'] = str()
variables['status_text'] = str()
variables['dispo_none_count'] = int()
variables['dispo_low_vaf_count'] = int()
variables['dispo_vus_count'] = int()
variables['dispo_mutation_count'] = int()
variables['dispo_flt3_count'] = int()
variables['dispo_hotspot_count'] = int()


# CLASSES ------------------------------------------------

class App():

    def __init__(self) -> None:

        self.var_data = dict()
        for x in vcf_columns:
            self.var_data[x] = str()

        self.labels = dict()
        for x in vcf_columns:
            self.labels[x] = str()
            
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
        self.validation['FWD/REV RD Cutoff'] = [
            "VCF: FSAF",
            "VCF: FSAR",
            "Mpileup Qual: Filtered Variant Forward Read Depth",
            "Mpileup Qual: Filtered Variant Reverse Read Depth",
            "Mpileup Qual: Unfiltered Variant Forward Read Depth",
            "Mpileup Qual: Unfiltered Variant Reverse Read Depth",
            "VCF: FAO",
        ]
        self.validation['Total Read Depth Threshold'] = [
            "Mpileup Qual: Read Depth",
            "VCF: FDP",
        ]
        self.validation['VAF Threshold']=[
            'VCF: FDP',
        ]
        self.validation['Web Links'] = [
            "Variant Annotation: Transcript",
            "COSMIC: ID",
            "ClinVar: ClinVar ID",
            "ClinVar: ClinVar ID",
            "dbSNP: rsID",
            "UniProt (GENE): Accession Number",
        ]

        return


# FUNCTIONS ----------------------------------------------

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
    """Placeholder function which does nothing."""
    pass
    return

# MAIN LOOP ----------------------------------------------

def main():
    # Mainloop
    root = App()
    return

if __name__ == '__main__':
    main()
