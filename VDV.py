# VDV.py
''' Main script file for the VCF data viewer application. '''

__author__ = "Vektra Casler MD"
__version__ = "0.2.0"
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