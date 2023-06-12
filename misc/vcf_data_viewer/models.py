# model.py
''' Structure to hold the data model for the VCF Viewer application. '''

# IMPORTS ------------------------------------------------

import csv
from pathlib import Path
from datetime import datetime
import os
from .constants import FieldTypes as FT
import json
import pandas as pd

# VARIABLES ----------------------------------------------

# CLASSES ------------------------------------------------

class SettingsModel:
    '''A model for saving settings'''
    
    fields = {
        'boolean 1': {'type':'bool', 'value':True},
        'boolean 2': {'type':'bool', 'value': True}
    }

    def __init__(self):
        filename = 'settings.json'
        self.filepath = Path.home() / filename
        self.load()
    
    def load(self):
        if not self.filepath.exists():
            return
        
        with open(self.filepath, 'r') as file_handle:
            raw_values = json.load(file_handle)
        
        for key in self.fields:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.fields[key]['value'] = raw_value
                
    def save(self):
        with open(self.filepath, 'w') as file_handle:
            json.dump(self.fields, file_handle)

    def set(self, key, value):
        if (
            key in self.fields and
            type(value).__name__ == self.fields[key]['type']
        ):
            self.fields[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")

class VariantModel():

    def __init__(self, disposition) -> None:
        """ Creates a blank dictionary, populated with the proper keys for holding information about a variant. """
        global VARIANT_COLUMNS
        self.datafields = dict()
        for entry in VARIANT_COLUMNS:
            self.datafields[entry] = None
        self.datafields['Disposition'] = None
        return

class VariantListModel():

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

class DataModel:
    ''' CSV file storage '''

    fields = {
        "Original Input: Chrom":{
            'req': True,
            'type': FT.string,
            'tooltip': 'Chromosome on which this gene is found.',    
        },
        "Original Input: Pos":{
            'req': True,
            'type': FT.integer,
            'tooltip': 'Base pair position of the gene on the chromosome.',    
        },
        "Original Input: Reference allele":{
            'req': False,
            'type': FT.string,
            'tooltip': 'Expected finding at this base pair location.',    
        },
        "Original Input: Alternate allele":{
            'req': True,
            'type': FT.string,
            'tooltip': 'Specimen finding at this base pair location.',    
        },
        "Variant Annotation: Gene":{
            'req': True,
            'type': FT.string,
            'tooltip': 'Gene currently selected from the variant list.',    
        },
        "Variant Annotation: cDNA change":{
            'req': False,
            'type': FT.string,
            'tooltip': 'Alteration in the DNA at this location.',    
        },
        "Variant Annotation: Protein Change":{
            'req': False,
            'type': FT.string,
            'tooltip': 'Resultant alteration in the protein at this location.',    
        },
        "VCF: AF":{
            'req': False,
            'type': FT.decimal,
            'tooltip': 'Allele fraction of reads with this variant.',    
            'min': 0.02,
        },
        "VCF: FAO":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Variant read depth at this base pair location, reported by Genexus.",    
            'min': 10,
        },
        "VCF: FDP":{
            'req': False,
            'type': FT.string,
            'tooltip': "Total read depth at this base pair location, reported by Genexus",    
            'min': 500,
        },
        "VCF: HRUN":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Homopolymer run count, reported by Genexus.",    
        },
        "VCF: Filter":{
            'req': False,
            'type': FT.string,
            'tooltip': "Final filter disposition as given by the Genexus.\n Preferred value: 'PASS'",    
            'values': ['PASS','NOCALL', 'ABSENT_HET_RV']
        },
        "VCF: Genotype":{
            'req': False,
            'type': FT.string,
            'tooltip':"Genotype distinction made by the Genexus analyzer.",
            'values':['1/1', '0/1', '0/0', './.']    
        },
        "COSMIC: ID":{
            'req': False,
            'type': FT.string,
            'tooltip': "COSMIC website ID for this variant.",    
        },
        "COSMIC: Variant Count":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Times this variant has been reported to COSMIC.",    
        },
        "COSMIC: Variant Count (Tissue)":{
            'req': False,
            'type': FT.long_string, # Very long text, needs wordwrap
            'tooltip': "JSON-style dictionary breakdown of tissue types reported to COSMIC for this variant.",    
        }, 
        "ClinVar: ClinVar ID":{
            'req': False,
            'type': FT.string,
            'tooltip': "ClinVar website ID for this variant.",    
        },
        "ClinVar: Clinical Significance":{
            'req': False,
            'type': FT.string,
            'tooltip': "Clinical significance as reported by ClinVar website.",
            'values': ['Pathogenic', 'Pathogenic/Likely pathogenic','Uncertain significance', 'Benign']
        },
        "gnomAD3: Global AF":{
            'req': False,
            'type': FT.decimal,
            'tooltip': "Frequency of this variant being found in the human population, as reported by GnomAD website.",    
        },
        "PhyloP: Vert Score":{
            'req': False,
            'type': FT.string,
            'tooltip': "Vertebrate score for gene conservancy, as reported by web resources.",    
        },
        "CADD: Phred":{
            'req': False,
            'type': FT.decimal,
            'tooltip': "Combine Annotation Dependent Depletion score, rating pathogenicity.\nRange: 0 = Benign, 48 = Pathogenic",    
        },
        "PolyPhen-2: HDIV Prediction":{
            'req': False,
            'type': FT.string,
            'tooltip': "Score assessing the possible change in phenotype of the protein structure, based on AA change.",    
        },
        "SIFT: Prediction":{
            'req': False,
            'type': FT.string,
            'tooltip':"SNP mutagenesis prediction score based on AA change, as reported by SIFT website.",    
        },
        "VCF: FSAF":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Forward Variant Read Depth, reported by Genexus\nValid value: > 10",   
            'min': 10, 
        },
        "VCF: FSAR":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Reverse Variant Read Depth, reported by Genexus\nValid value: > 10",    
            'min': 10, 
        },
        "VCF: FSRF":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Forward Reference Read Depth, reported by Genexus.",    
            'min': 10, 
        },
        "VCF: FSRR":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Reverse Reference Read Depth, reported by Genexus.",    
            'min': 10, 
        },
        "VCF: Fisher Odds Ratio":{
            'req': False,
            'type': FT.decimal,
            'tooltip': "Fisher's odds ratio calculation, based on Genexus read depth data.",
        },
        "VCF: Fisher P Value":{
            'req': False,
            'type': FT.decimal,
            'tooltip': "Statistical p-value.\nLess than 0.05 is preferred.",
            'max': 0.05,
        },
        "VCF: Binom Proportion":{
            'req': False,
            'type': FT.decimal,
            'tooltip': "Binomial proportion caclucation, based on Genexus read depth data.",    
        },
        "VCF: Binom P Value":{
            'req': False,
            'type': FT.decimal,
            'tooltip': "Statistical p-value.\nLess than 0.05 is preferred.",    
            'max': 0.05,
        },
        "Mpileup Qual: Read Depth":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Total read depth, as reported by M-Pileup data.\nValid: > 500",    
            'min': 500,
        },
        "Mpileup Qual: Start Reads":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Count of read start signals (strand termination), as reported in the M-Pileup data.",    
        },
        "Mpileup Qual: Stop Reads":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Cout of read stop signals (strand initiation), as reported in the M-Pileup data.",    
        },
        "Mpileup Qual: Filtered Reference Forward Read Depth":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Forward Reference Read Depth, reported by M-Pileup, @Q20\nValid value: > 10",    
            'min': 10,
        },
        "Mpileup Qual: Filtered Reference Reverse Read Depth":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Reverse Reference Read Depth, reported by M-Pileup, @Q20\nValid value: > 10",    
            'min': 10,
        },
        "Mpileup Qual: Unfiltered Reference Forward Read Depth":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Forward Reference Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",    
            'min': 10,
        },
        "Mpileup Qual: Unfiltered Reference Reverse Read Depth":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Reverse Reference Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",    
            'min': 10,
        },
        "Mpileup Qual: Filtered Variant Forward Read Depth":{
            'req': False,
            'type': FT.integer,
            'tooltip': "Forward Variant Read Depth, reported by M-Pileup, @Q20\nValid value: > 10",    
            'min': 10,
        },
        "Mpileup Qual: Filtered Variant Reverse Read Depth":{
            'req': False,
            'type': FT.integer,
            'tooltip':"Reverse Variant Read Depth, reported by M-Pileup, @Q20\nValid value: > 10",    
            'min': 10,
        },
        "Mpileup Qual: Filtered Variant Binomial Proportion":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"Binomial proportion caclucation, based on filtered M-Pileup read depth data.",    
        },
        "Mpileup Qual: Filtered Variant Binomial P Value":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"Statistical p-value.\nLess than 0.05 is preferred.",    
            'max': 0.05,
        },
        "Mpileup Qual: Filtered Variant Fishers Odds Ratio":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"Fisher's odds ratio calculation, based on filtered M-Pileup read depth data.",    
        },
        "Mpileup Qual: Filtered Variant Fishers P Value":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"Statistical p-value.\nLess than 0.05 is preferred.",    
            'max': 0.05,
        },
        "Mpileup Qual: Unfiltered Variant Forward Read Depth":{
            'req': False,
            'type': FT.integer,
            'tooltip':"Forward Variant Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",    
            'min': 10,
        },
        "Mpileup Qual: Unfiltered Variant Reverse Read Depth":{
            'req': False,
            'type': FT.integer,
            'tooltip':"Reverse Variant Read Depth, reported by M-Pileup, @Q1\nValid value: > 10",    
            'min': 10,
        },
        "Mpileup Qual: Unfiltered Variant Binomial Proportion":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"Binomial proportion caclucation, based on unfiltered M-Pileup read depth data.",    
        },
        "Mpileup Qual: Unfiltered Variant Binomial P Value":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"Statistical p-value.\nLess than 0.05 is preferred.",    
            'max': 0.05,
        },
        "Mpileup Qual: Unfiltered Variant Fishers Odds Ratio":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"Fisher's odds ratio calculation, based on unfiltered M-Pileup read depth data.",    
        },
        "Mpileup Qual: Unfiltered Variant Fishers P Value":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"Statistical p-value.\nLess than 0.05 is preferred.",    
            'max': 0.05,
        },
        "VCF: LEN":{
            'req': False,
            'type': FT.integer,
            'tooltip':"Length of the variant, as reported by Genexus.",    
        },
        "VCF: QD":{
            'req': False,
            'type': FT.string,
            'tooltip':"???",    
        },
        "VCF: STB":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"Proprietary strand bias calculation, as reported by Genexus.",    
        },
        "VCF: STBP":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"Statistical p-value.\nLess than 0.05 is preferred.",    
        },
        "VCF: SVTYPE":{
            'req': False,
            'type': FT.string,
            'tooltip':"Unused data field from the Genexus report.",    
        },
        "VCF: TYPE":{
            'req': False,
            'type': FT.string,
            'tooltip':"Type of variant, as reported by Genexus.",    
            'values': ['del','snp','complex','ins'],
        },
        "VCF: QUAL":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"Quality determination tag, as reported by Genexus.",    
        },
        "Variant Annotation: Coding":{
            'req': False,
            'type': FT.string,
            'tooltip':"Reported coding region variant, as reported by Genexus.",    
            'values': ['Y','']
        },
        "Variant Annotation: Sequence Ontology":{
            'req': False,
            'type': FT.string,
            'tooltip':"Type of variant/mutation encountered.\n Possible Types: MIS, INT, FSI, IND, SYN, SPL ",
            'values': ['MIS','INT','FSI','IND','SYN','SPL']
    
        },
        "Variant Annotation: Transcript":{
            'req': False,
            'type': FT.string,
            'tooltip':"Ensembl transcript designation code.",    
        },
        "Variant Annotation: All Mappings":{
            'req': False,
            'type': FT.long_string, # Very long text, needs wordwrap
            'tooltip':"JSON-style dictionary breakdown of tissue types present in ??? knowledgebase for this variant.",    
        }, 
        "UniProt (GENE): Accession Number":{
            'req': False,
            'type': FT.string,
            'tooltip':"UniProt web resource for the affected protein and biological functions.",    
        },
        "dbSNP: rsID":{
            'req': False,
            'type': FT.string,
            'tooltip':"ID number for the free dbSNP web resource listing of this variant.",    
        },
        "MDL: Sample Count":{
            'req': False,
            'type': FT.integer,
            'tooltip':"Instance count of samples with this variant present",
        },
        "MDL: Variant Frequency":{
            'req': False,
            'type': FT.decimal,
            'tooltip':"",    
        },
        "MDL: Sample List":{
            'req': False,
            'type': FT.long_string, # Very long text, needs wordwrap
            'tooltip':"JSON-style dictionary breakdown of tissue types present in ??? knowledgebase for this variant.",    
        },
        "Disposition":{
            'req': False,
            'type': FT.string,
            'tooltip':'How to categorize this variant.',    
        },
    }

    def __init__(self, filename=None):

        self.vars = dict()

        for key,value in fields.items():
            self.vars = FT.
# MAIN LOOP ----------------------------------------------

def main():
    pass
    return

if __name__ == '__main__':
    main()