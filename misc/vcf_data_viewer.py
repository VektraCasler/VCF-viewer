# vcf_data_viewer.py
''' Main script file for the VCF data viewer application. '''

__author__ = "Vektra Casler MD"
__version__ = "0.2.0"
__license__ = "Built for use at University of Rochester Medical Center"

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