import os
import re
import io

FOLDER = 'reference'
FILENAME = 'infotrack_data_dump.tsv'

COLUMNS = [
    ' mol_num', 
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
    'test_tissue'
]


