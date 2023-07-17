# reference/bed_db.py
''' Creates a lookup data class to help further annotate variants with some static information. '''

# IMPORTS ------------------------------------------------

import os
import pandas as pd

# VARIABLES ----------------------------------------------

BED_REF_FOLDER = "reference"
BED_REF_FILENAME = "Genexus_bed_working.xlsx"
BED_REF_COLUMNS = [
    'Chrom',
    'bp_start',
    'bp_end',
    'amp_ID',
    'N_A',
    'amp_info',
    'Gene',
    'Cytoband',
    'Refseq (GRCh38)',
    'MANE_transcript (GRCh38)',
    'Genexus_transcript (GRCh37)',
    'Genexus_Exon(s)',
    'Genexus_codons',
] # listed here just for convenience while coding

# CLASSES ------------------------------------------------

class BedLookupTable():
    """ Brings in the lookup table for finding the additional pieces of data for the variant from the bed file. """

    def __init__(self) -> None:

        # read in the file
        file_path = os.path.join(BED_REF_FOLDER, BED_REF_FILENAME)
        self.DF = pd.read_excel(file_path)
        self.columns = self.DF.columns

        return None
    
    def get_data(self, gene: str, bp: int, column: str) -> str:

        # first make a much smaller temp DF
        temp_DF = self.DF[self.DF['Gene'] == gene]

        # iterate through the rows to compare the bp between start and stop
        for ind in temp_DF.index:
            if int(temp_DF['bp_start'][ind]) <= bp <= int(temp_DF['bp_end'][ind]):
                return str(temp_DF[column][ind])
        
        return ""


# MAIN LOOP ----------------------------------------------

def main():

    lut = BedLookupTable()

    test_list = [
        ('DNMT3A', 25468887),
        ('DNMT3A', 25468888),
        ('MYD88', 38182600),
    ]

    for x in test_list:
        print(
            x[0], 
            x[1], 
            lut.get_data(x[0], x[1], 'Cytoband'), 
            lut.get_data(x[0], x[1], 'MANE_transcript (GRCh38)'), 
            lut.get_data(x[0], x[1], 'Genexus_transcript (GRCh37)'), 
            lut.get_data(x[0], x[1], 'Genexus_Exon(s)'), 
            lut.get_data(x[0], x[1], 'Genexus_codons')
        )

    return

if __name__ == '__main__':
    main()