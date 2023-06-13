# vcf_data_viewer.py
''' This holds the data model for the vcf-data-viewer application. '''

# IMPORTS ------------------------------------------------

from .global_variables import *
import openpyxl

# VARIABLES ----------------------------------------------

# CLASSES ------------------------------------------------

class DataModel():

    def __init__(self) -> None:
        self.variables = dict()
        self.variables['filename'] = str()
        return
    
    def _load_file(self, *args, **kwargs):
        """ Recieves the filename from the view, attempts to load. """
        workbook = openpyxl.load_workbook(self.variables['filename'], data_only=True, read_only=True)
        self.variables['variant_list'] = list()
        for disposition in workbook.sheetnames:
            sheet = workbook[disposition]
            for row in sheet.iter_rows(min_row=2):
                row_dict = dict()
                for x in range(len(VCF_FIELDS)-1):  # Have to subtract one here because the disposition field is last, but not in the original file
                    row_dict[VCF_FIELDS[x]] = row[x].value
                if disposition in DISPOSITIONS:
                    row_dict['Disposition'] = disposition
                else:
                    row_dict['Disposition'] = "None"
                self.variables['variant_list'].append(row_dict.copy())
        return


# MAIN LOOP ----------------------------------------------

def main():

    pass

    return

if __name__ == '__main__':
    main()