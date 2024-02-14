import os.path
import tkinter as tk
from tkinter import filedialog
import pandas as pd

from .bed_db import BedLookupTable
from .global_variables import *

# CLASSES ---------------------------------------------------------------------

class LowCoverageTable:

    def __init__(self, original_file) -> None:

        self.original_file = original_file

        # Create a lookup table from the bed file
        self.lut = BedLookupTable()

        # get bedcov filename
        self._get_bedcov_filename()

        # create a dataframe
        self._create_bedcov_DF()

        # Create the low coverage table
        self._output_low_coverage_table()

        return None
    
    def _create_bedcov_DF(self) -> None:

        # Open a pandas DF ----------------------------------------------------
        columns = [
            "Chromosome",
            "BP_Begin",
            "BP_End",
            "Amplicon",
            "Something",
            "Gene_ID",
            "Something_2",
            "Depth",
        ]
        DF = pd.read_csv(self.bedcov_file, sep='\t', header=None)
        DF.columns = columns
        DF.drop(
            ['Chromosome', 'Something', 'Something_2', 'BP_End', 'Gene_ID'],
            axis=1,
            inplace=True,
            )

        # Filter DF to only entries with <500 in final column
        DF = DF[DF['Depth'] < 500]

        # Create the other columns
        DF['Gene'] = DF['Amplicon'].apply(lambda x: x.split("_")[0])
        DF['Exon'] = DF['Amplicon'].apply(lambda x: self.lut.lookup_by_amplicon(x, "Genexus_Exon(s)"))
        DF['Codon'] = DF['Amplicon'].apply(lambda x: self.lut.lookup_by_amplicon(x, "Genexus_codons"))

        # Rearrange to fit the expected headers
        self.DF = DF[['Gene', 'Amplicon', 'Exon', 'Codon', 'Depth']]

        return None
    
    def _get_bedcov_filename(self) -> None:

        # Get Filename of BedCov File 
        self.original_file = self.original_file

        # Find Root folder
        self.original_folder, self.original_name = os.path.split(self.original_file)

        # Up two folders
        for _ in range(2):
            self.bedcov_folder = os.path.dirname(self.original_folder)

        # Drill into bedcov files
        self.bedcov_folder = os.path.join(self.bedcov_folder, 'bedcov')
        self.bedcov_folder = self.bedcov_folder.replace("/", "\\")

        # Collect filenames of that folder
        files = os.listdir(self.bedcov_folder)

        # Find the file corresponding to this sample
        for file in files:
            if file.split('.')[0] in self.original_name:
                self.bedcov_file = os.path.join(self.bedcov_folder, file)

        return None

    def _output_low_coverage_table(self) -> None:

        self.sample_name = self.original_name.split('.')[0] 
        self.low_coverage_table_filename = self.sample_name + "_low_coverage.tsv"
        self.low_coverage_table_filepath = os.path.join(
            self.original_folder,
            "output",
            )

        # Create an output folder if it doesn't yet exist
        if not os.path.exists(self.low_coverage_table_filepath):
            os.mkdir(self.low_coverage_table_filepath)

        # Add the filename
        self.low_coverage_table_filepath = os.path.join(
            self.original_folder,
            "output",
            self.low_coverage_table_filename,
            )

        # Save out the DF
        self.DF.to_csv(self.low_coverage_table_filepath, index=False, sep='\t')

        return None

# MAIN LOOP -------------------------------------------------------------------

def main() -> None:
    """Testing function for module."""

    # Passed on init
    open_file = r"C:\Users\vcasler\Desktop\CWD\20231120\analysis\final_report\6854-23_N8270548.final.report.xlsx"
    lct = LowCoverageTable(open_file)
    del(lct)

    return None

if __name__ == "__main__":
    main()
