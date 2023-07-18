# VDV.py
''' Main script file for the VCF data viewer application. '''

__title__ = "VCF Data Viewer"
__author__ = "Vektra Casler MD"
__version__ = "1.0.0"
__license__ = "Built for use only at University of Rochester Medical Center in Rochester, NY."

# IMPORTS ------------------------------------------------

from vcf_data_viewer.application import Application

# VARIABLES ----------------------------------------------

# MAIN LOOP ----------------------------------------------

def main():

    app = Application()
    app.mainloop()

    return

if __name__ == '__main__':
    main()