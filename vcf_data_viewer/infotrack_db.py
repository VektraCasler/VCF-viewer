# reference/infotrack_db.py
''' This dataclass holds a lookup table for the infotrack information to help annotate the variants. '''

# IMPORTS ------------------------------------------------

import os
import pandas as pd

# VARIABLES ----------------------------------------------

INFOTRACK_REF_FOLDER = "reference"
INFOTRACK_REF_FILENAME = "infotrack_data_dump.tsv"
INFOTRACK_REF_COLUMNS = [
    'mol_num',
    'sample_name', 
    'observed_variant_id', 
    'run_id', 
    'interpt_id', 
    'genes', 
    'coding', 
    'amino_acid_change', 
    'frequency', 
    'genotype', 
    'allele_coverage', 
    'coverage', 
    'include_in_report', 
    'tier', 
    'time_stamp', 
    'confirm_status', 
    'variant_allele', 
    'ref_allele', 
    'ref_var_strand_counts', 
    'strand', 
    'genetic_call', 
    'test_tissue',
] # listed here just for convenience while coding

# CLASSES ------------------------------------------------

class InfotrackLookupTable():
    """ Brings in the lookup table for finding the most likely Tier of the variant. """

    def __init__(self) -> None:

        # read in the file
        file_path = os.path.join(INFOTRACK_REF_FOLDER, INFOTRACK_REF_FILENAME)
        self.DF = pd.read_csv(file_path, sep='\t', encoding='ascii')
        self.columns = self.DF.columns

        return None

    def recommend_tier(self, gene: str, c_dot: str, tissue:str = 'blood') -> str:
        """ Method to recommend a tier for the variant based on the gene, c-dot number, and tissue type (default is 'blood'). """

        # make a temporary filtered DF
        temp_DF = self.DF.loc[(self.DF['genes'] == gene)]
        temp_DF = temp_DF.loc[(temp_DF['coding'] == c_dot)]
        temp_DF = temp_DF.loc[(temp_DF['test_tissue']) == 'Blood']
        
        # variant not found case
        if temp_DF.shape[0] == 0:
            return "NO DATA"
        
        # count up all the tier counts by type
        tier_types = ['Tier I', 'Tier II', 'Tier III']
        tier_counts = list()
        for tier in tier_types:
            count = temp_DF.loc[self.DF['tier'] == tier].shape[0]
            tier_counts.append(count)

        # make a dictionary with the counts as keys (enables max function on keys)
        tier_dict = dict(zip(tier_counts, tier_types))
        
        return tier_dict[max(tier_dict.keys())]
    
    def get_tissue_list(self, gene:str, c_dot:str) -> str:
        ''' Method to create a tissue dictionary for '''

        # make a temporary filtered DF
        temp_DF = self.DF.loc[(self.DF['genes'] == gene)]
        temp_DF = temp_DF.loc[(temp_DF['coding'] == c_dot)]
        
        # variant not found case
        if temp_DF.shape[0] == 0:
            return "novel variant"
        
        tissue_dict = dict()

        for tissue in set(temp_DF['test_tissue'].to_list()):
            if tissue not in tissue_dict.keys():
                tissue_dict[tissue] = 0
            tissue_dict[tissue] = temp_DF[temp_DF['test_tissue'] == tissue].shape[0]
        
        # return "Done"
        return str(tissue_dict)

# MAIN LOOP ----------------------------------------------

def main():

    lut = InfotrackLookupTable()

    print(lut.recommend_tier('ASXL1','c.1934delG'))
    print(lut.recommend_tier('ASXL1','c.1934dupG'))
    print(lut.get_tissue_list('ASXL1', 'c.1934dupG'))

    return

if __name__ == '__main__':
    main()