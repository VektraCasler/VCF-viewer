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
        self.variables['selection_disposition'] = "None"
        self.variables['selection_index'] = 0
        return
    
    def load_file(self, *args, **kwargs):
        """ Recieves the filename from the view, attempts to load. """
        workbook = openpyxl.load_workbook(self.variables['filename'], data_only=True, read_only=True)
        self.variables['variant_list'] = list()
        for disposition in workbook.sheetnames:
            sheet = workbook[disposition]
            for row in sheet.iter_rows(min_row=2):
                row_dict = dict()
                for x in range(len(VCF_FIELDS[:-1])):  # Have to subtract one here because the disposition field is last, but not in the original file
                    row_dict[VCF_FIELDS[x]] = row[x].value
                if disposition in DISPOSITIONS:
                    row_dict['Disposition'] = disposition
                else:
                    row_dict['Disposition'] = "None"
                self.variables['variant_list'].append(row_dict.copy())
        return
    
    def save_file(self, *args, **kwargs):
        """ Writes the sorted data out to disk with marker on the filename to denote file has been processed. """

        # appending a note to the filename 
        if SETTINGS['FILE']['filename_addon'] in self.variables['filename']:
            filename = self.variables['filename']
        else:
            filename = self.variables['filename'][:-(len(SETTINGS['FILE']['excel_extension']))] + SETTINGS['FILE']['filename_addon'] + SETTINGS['FILE']['excel_extension']

        # Openpyxl package work
        wb = openpyxl.Workbook()
        for tab in SETTINGS['DISPOSITIONS']:
            wb.create_sheet(tab)
            wb.active = wb[tab]
            ws = wb.active
            row = [column for column in SETTINGS['VCF_FIELDS']]
            ws.append(row)
            for entry in self.variables['variant_list']:
                if entry['Disposition'] == tab:
                    row = [entry[x] for x in SETTINGS['VCF_FIELDS']]
                    ws.append(row)

        wb.remove_sheet(wb.get_sheet_by_name('Sheet')) # removing the default "Sheet" from openpyxl
        wb.save(filename)

        return

    def change_disposition(self, *args, **kwargs):
        self.variables['variant_list'][self.variables['selection_index']]['Disposition'] = self.variables['selection_disposition']
        return

    def count_dispositions(self, disposition, *args, **kwargs):
        counter = 0
        for row in self.variables['variant_list']:
            if disposition == row['Disposition']:
                counter += 1
        return counter
    
    def output_text_files(self, *args, **kwargs):
        pass
        return


# MAIN LOOP ----------------------------------------------

def main():

    pass

    return

if __name__ == '__main__':
    main()