# vcf_data_viewer.py
''' This holds the data model for the vcf-data-viewer application. '''

# IMPORTS ------------------------------------------------

from .global_variables import *
from .infotrack_db import *
from .bed_db import *
import openpyxl

# VARIABLES ----------------------------------------------

ADDON_LIST = [
    'amp_ID', 
    'Cytoband', 
    'MANE_transcript (GRCh38)', 
    'Genexus_transcript (GRCh37)', 
    'Genexus_Exon(s)', 
    'Genexus_codons',
    'tier',
    'test_tissue',
]
TEST_FILE = 'test_data/50-22.final.report.xlsx'

# CLASSES ------------------------------------------------

class DataModel():

    def __init__(self) -> None:

        self.variables = dict()
        self.variables['filename'] = str()
        self.variables['selection_disposition'] = "None"
        self.variables['selection_index'] = 0

        self.bdb = BedLookupTable()
        self.idb = InfotrackLookupTable()
        
        self.DATA_FIELDS = list()

        return None

    def determine_data_fields(self, excel_columns) -> None:
        """ Method to determine if this is an already annotated excel file, or if it is an original one.  Sets the data field (columns) list appropriately. """

        return None

    def load_file(self, *args, **kwargs) -> None:
        """ Recieves the filename from the view, attempts to load. """

        workbook = openpyxl.load_workbook(self.variables['filename'], data_only=True, read_only=True)
        self.variables['variant_list'] = list()

        column_list = [cell.value for cell in workbook[1]]
        print(column_list)

        # capturing the workbook sheet names as dispositions 
        for disposition in workbook.sheetnames:

            # Grab the appropriate worksheet and make it active
            sheet = workbook[disposition]

            for row in sheet.iter_rows(min_row=2):

                # prep a dictionary to hold row data
                row_dict = dict()

                # Step through all VCF fields
                for x in range(len(VCF_FIELDS[:-1])):  # Have to subtract one here because the disposition field is last, but not in the original file
                    row_dict[VCF_FIELDS[x]] = row[x].value

                # ignores any sheet names that "non-standard" dispositions.  
                # The first sheet in the excel file typically has such a name.
                if disposition in DISPOSITIONS:
                    row_dict['Disposition'] = disposition
                else:
                    row_dict['Disposition'] = "None"

                # ANNOTATING FROM THE BED FILE

                # making some temp variables for clarity during coding
                gene = row_dict['Variant Annotation: Gene']
                bp = row_dict['Original Input: Pos']
                c_dot = row_dict["Variant Annotation: cDNA change"]

                # Now reference the lookup table to include the missing pieces of information
                for item in ADDON_LIST[:-2]:
                    row_dict[item] = self.bdb.get_data(gene, bp, item)

                # ANNOTATING FROM THE INFOTRACK DB FILE
                
                # Now let's add annotations from the infotrack file
                row_dict['tier'] = self.idb.recommend_tier(gene, c_dot, 'Blood') # Genexys is just blood samples currently
                row_dict['infotrack_tissues'] = self.idb.get_tissue_list(gene, c_dot)

        return None

    def save_file(self, *args, **kwargs) -> None:
        """ Writes the sorted data out to disk with marker on the filename to denote file has been processed. """

        # appending a "(sorted)" note to the filename, but checking if that note is already there
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

        return None
    
    def change_disposition(self, selection: str, disposition: str, update_dict: dict, *args, **kwargs) -> None:
        """ Updates the disposition of the selected record. """

        # Updating all the fields in the model instance of the record
        for vcf_field in VCF_FIELDS:
            self.variables['variant_list'][selection][vcf_field] = update_dict[vcf_field]
        self.variables['variant_list'][selection]['Disposition'] = disposition

        return None

    def count_dispositions(self, disposition, *args, **kwargs) -> int:
        """ Method to count the number of records in the variant list with the passed disposition. """

        counter = 0

        for row in self.variables['variant_list']:
            if disposition == row['Disposition']:
                counter += 1

        return counter

    def output_text_files(self, *args, **kwargs) -> None:
        """ Placeholder method which will eventually output the needed text files for the reporting script. """

        pass

        return None

# MAIN LOOP ----------------------------------------------

def main() -> None:

    model = DataModel()

    return None

if __name__ == '__main__':
    main()