#!/usr/bin/env python3
"""
Container for Histograms - easier to handle than gDirectory...
"""
from fire import Fire

histograms = {} #  ----- histograms created by system
canvases = {}

range_and_peaks = {}  # for id. and fit
  # range_and_peaks["spe"] = "" #spectrum name
  # range_and_peaks["pks"] = "" #list np

gregory_started = None # launch time

# calibration via "c" comand; use global on change and import
ECALIB = []
ECALIBa = 1
ECALIBb = 0

ECALIBdb = {}
ECALIBdb['40K'] = 1460.82
ECALIBdb['214BIB'] = 609.31
ECALIBdb['214BIA'] = 1764.49
ECALIBdb['208TL'] = 2614.51
ECALIBdb['60COA'] = 1173.2
ECALIBdb['60COB'] = 1332.5
# ECALIBdb[''] =

# last fit result - useful bin for calib....
last_fit_res = {}

is_zoomed = [ False, 0.0 ] # yes or no; middle_energy

def main():
    print()

if __name__=="__main__":
    Fire(main)
