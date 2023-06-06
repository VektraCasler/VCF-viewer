import pandas as pd

self_vars = dict()
self_vars['filename'] = "test_data/481-20_J3316158.final.report.xlsx"


try:
    xlsx = pd.ExcelFile(self_vars['filename'])
    DF = pd.DataFrame()
    for sheet in xlsx.sheet_names:
        DF_sheet = xlsx.parse(sheet)
        if sheet == "Hotspots":
            DF_sheet['Disposition'] = "Hotspot"
        elif sheet == "FLT3 ITD":
            DF_sheet['Disposition'] = "FLT3 ITD"
        elif sheet == "Low VAF":
            DF_sheet['Disposition'] = "Low VAF"
        else:
            DF_sheet['Disposition'] = "None"
        if DF.empty:
            DF = DF_sheet
        else:
            DF = pd.concat([DF, DF_sheet], axis=0)
    print("It worked.")
except:
    print("Excel file format not detected.")


# Create disposition

# for item in treeview_variant_list.get_children():
#     treeview_variant_list.delete(item)
# csv_dict = dict()
# vars['filename'].set(str(fd.askopenfilename(filetypes=[('XLSX','*.xlsx')])))
# with open(vars['filename'].get(), 'r') as file_input:
#     counter = 0
