# model.py
''' Structure to hold the data model for the VCF Viewer application. '''

# IMPORTS ------------------------------------------------

import pandas as pd

# VARIABLES ----------------------------------------------

# list of the original columns from the input files
VARIANT_COLUMNS = [
    'Original Input: Chrom',
    'Original Input: Pos',
    'Original Input: Reference allele',
    'Original Input: Alternate allele',
    'Variant Annotation: Gene',
    'Variant Annotation: cDNA change',
    'Variant Annotation: Protein Change',
    'Variant Annotation: RefSeq',
    'VCF: AF',
    'VCF: FAO',
    'VCF: FDP',
    'VCF: HRUN',
    'VCF: Filter',
    'VCF: Genotype',
    'COSMIC: ID',
    'COSMIC: Variant Count',
    'COSMIC: Variant Count (Tissue)',
    'ClinVar: ClinVar ID',
    'ClinVar: Clinical Significance',
    'gnomAD3: Global AF',
    'PhyloP: Vert Score',
    'CADD: Phred',
    'PolyPhen-2: HDIV Prediction',
    'SIFT: Prediction',
    'VCF: FSAF',
    'VCF: FSAR',
    'VCF: FSRF',
    'VCF: FSRR',
    'VCF: Fisher Odds Ratio',
    'VCF: Fisher P Value',
    'VCF: Binom Proportion',
    'VCF: Binom P Value',
    'Mpileup Qual: Read Depth',
    'Mpileup Qual: Start Reads',
    'Mpileup Qual: Stop Reads',
    'Mpileup Qual: Filtered Reference Forward Read Depth',
    'Mpileup Qual: Filtered Reference Reverse Read Depth',
    'Mpileup Qual: Unfiltered Reference Forward Read Depth',
    'Mpileup Qual: Unfiltered Reference Reverse Read Depth',
    'Mpileup Qual: Filtered Variant Forward Read Depth',
    'Mpileup Qual: Filtered Variant Reverse Read Depth',
    'Mpileup Qual: Filtered Variant Binomial Proportion',
    'Mpileup Qual: Filtered Variant Binomial P Value',
    'Mpileup Qual: Filtered Variant Fishers Odds Ratio',
    'Mpileup Qual: Filtered Variant Fishers P Value',
    'Mpileup Qual: Filtered VAF',
    'Mpileup Qual: Unfiltered Variant Forward Read Depth',
    'Mpileup Qual: Unfiltered Variant Reverse Read Depth',
    'Mpileup Qual: Unfiltered Variant Binomial Proportion',
    'Mpileup Qual: Unfiltered Variant Binomial P Value',
    'Mpileup Qual: Unfiltered Variant Fishers Odds Ratio',
    'Mpileup Qual: Unfiltered Variant Fishers P Value',
    'Mpileup Qual: Unfiltered VAF',
    'VCF: LEN',
    'VCF: QD',
    'VCF: STB',
    'VCF: STBP',
    'VCF: SVTYPE',
    'VCF: TYPE',
    'VCF: QUAL',
    'Variant Annotation: Coding',
    'Variant Annotation: Sequence Ontology',
    'Variant Annotation: Transcript',
    'Variant Annotation: All Mappings',
    'UniProt (GENE): Accession Number',
    'dbSNP: rsID',
    'MDL: Sample Count',
    'MDL: Variant Frequency',
    'MDL: Sample List',
]

active_variant = dict()
for entry in VARIANT_COLUMNS:
    active_variant

# CLASSES ------------------------------------------------

class Variant():

    def __init__(self, disposition) -> None:
        """ Creates a blank dictionary, populated with the proper keys for holding information about a variant. """
        global VARIANT_COLUMNS
        self.datafields = dict()
        for entry in VARIANT_COLUMNS:
            self.datafields[entry] = None
        self.datafields['Disposition'] = None
        return

class VariantList():

    def __init__(self) -> None:
        """ Creates a blank list to hold Variants in a list type format.  Will be used to populate the TreeView. """
        self.variant_list = list()
        self.vars = dict()
        self.vars['filename'] = None

    def load_file(self, filename):
        """ Handles the file input to the data model. """
        self.vars['filename'] = filename
        # Testing to see which type of file we're opening (XLSX, CSV, or JSON)
        if 'XLSX' in self.vars['filename'].upper():
            try:
                xlsx = pd.ExcelFile(self.vars['filename'])
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


# MAIN LOOP ----------------------------------------------

def main():

    pass

    return

if __name__ == '__main__':
    main()