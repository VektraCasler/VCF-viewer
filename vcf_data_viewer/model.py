# vcf_data_viewer.py
''' This holds the data model for the vcf-data-viewer application. '''

# IMPORTS ------------------------------------------------

from .global_variables import *
import openpyxl

# VARIABLES ----------------------------------------------

# CLASSES ------------------------------------------------

class DataModel():

    def __init__(self) -> None:
        self.filename = str()
        self.selected = dict()
        for x in VCF_FIELDS:
            self.selected[x] = None
        self.disposition_counts = dict()
        for x in DISPOSITIONS:
            self.disposition_counts[x] = 0
        self.variant_list = dict()
        return
    
    def _select_variant(self, index:int):
        if index == None:
            for x in VCF_FIELDS:
                self.selected[x] = None
        else:
            for x in VCF_FIELDS:
                self.selected[x] = self.variant_list[index][x]
        
    def _load_file(self, filename):
        """ Recieves the filename from the view, attempts to load. """
        self.filename = filename
        if ".XLSX" in str(self.filename).upper():
            try:
                self._read_excel_file_to_dictionary(self.filename)
            except:
                print("File not read correctly.")
        return
        
    def _read_excel_file_to_dictionary(self, filename:str):
        """ Loads an Excel worksheet, then reads all sheets for variant information. """
        workbook = openpyxl.load_workbook(filename, data_only=True, read_only=True)
        self.variant_list = list()
        for disposition in workbook.sheetnames:
            sheet = workbook[disposition]
            for row in sheet.iter_rows(min_row=2):
                row_dict = dict()
                for x in range(len(VCF_FIELDS)):
                    row_dict[VCF_FIELDS[x]] = row[x].value
                row_dict['Disposition'] = disposition
                self.variant_list.append(row_dict.copy())
        return
    
    def _count_dispositions(self):
        for x in DISPOSITIONS:
            self.disposition_counts[x] = 0
            for variant in self.variant_list:
                self.disposition_counts[variant['Disposition']] += 1
        return

# MAIN LOOP ----------------------------------------------

def main():

    pass

    return

if __name__ == '__main__':
    main()