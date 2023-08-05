#!/usr/bin/env python3

import sys

from fire import Fire
#------display
import ROOT
import numpy as np

from console import fg, bg, fx

import re # find livetime and a and b
from gregory_online.histo_global_cont import histograms

import math


def clear( h ):
    """
    histogram
    """
    for i in range( h.GetXaxis().GetNbins()+1 ):
        h.SetBinContent(i,0)
        h.SetBinError(i,0)
    return h



def get_range_from_calib(h,a,b):
    """
    avoid GetXmax ... it is a calib
    deduce really from max bin number
    """
    return a*0+b, a*h.GetXaxis().GetNbins()+b



def apply_calib(h1, xmin, xmax):
    if (xmin!=h1.GetXaxis().GetXmin() ) or (xmax!=h1.GetXaxis().GetXmax() ):
        print(f"i... calibration => {h1.GetXaxis().GetXmin()}->{xmin} ;{h1.GetXaxis().GetXmax()}->{xmax}")
        #print("i... limits before calib",xmin,xmax,h1.GetXaxis().GetXmin(),h1.GetXaxis().GetXmax())
        # calibrate ALL
        h1.GetXaxis().SetLimits(xmin,xmax)
        #print("i... limits after:",h1.GetXaxis().GetXmin(),h1.GetXaxis().GetXmax())




def get_np_from_h( h ):
    """
    return np
    """
    bins =  h.GetXaxis().GetNbins()
    hnp = np.zeros( bins )
    enp = np.zeros( bins )
    #print(len(hnp), hnp)
    for i in range(1, h.GetXaxis().GetNbins()+1 ): # no under, no over, last
        hnp[i-1] = h.GetBinContent(i)
        enp[i-1] = h.GetBinError(i)
        #if i<10: print("get",hnp[i-1],  enp[i-1])
    #print(hnp)
    return hnp,enp


def fill_h_with_np(h1np, hname="total" , runtime = None, errors=None, limits_calib=None, title = None):
    """
     histo treatment, histo is in gDirectory, treated by ROOT
    """
    global histograms
    mytitle = title

    if ROOT.gDirectory.FindObject(hname):
        #print(f"i... {hname} is there")
        histograms[hname] = ROOT.gDirectory.FindObject(hname)
    else:
        if mytitle is None: mytitle = hname
        print(f"{fg.cyan}X... histo={hname} is NOT there, we create now{fg.default}")
        histograms[hname] = ROOT.TH1D(hname,f"{hname}:{mytitle}", len(h1np)-2, 0, len(h1np)-2 )
        # print(f"i... {hname} is created now")

    suma = 0
    for i in range( len(h1np) ):
        suma+=h1np[i]
        histograms[hname].SetBinContent(i,h1np[i])
        if not errors is None:
            histograms[hname].SetBinError(i,errors[i]*0.999) # no y scale blinking
        else:
            histograms[hname].SetBinError(i, math.sqrt(h1np[i])*0.999 )# no y scale blinking
            #if i<10:  print( "fill",h1np[i], errors[i] )
        # self.h1_diff.SetBinContent(i, self.h1np_diff[i] )
        # #self.h1_dif1.SetBinContent(i, self.h1np_1mdiff[i] )
        # self.h1_dif2.SetBinContent(i, self.h1np_2mdiff[i] )
    histograms[hname].SetEntries(suma)

    if limits_calib is not None:
        xmin,xmax = limits_calib[0],limits_calib[1]
    else:
        xmin,xmax = 0,histograms[hname],GetXaxis().GetXmax() # this is the calib from h
    apply_calib(histograms[hname], xmin, xmax)


    #sqrt_done=False
    #if hname != "backg":  # do not repeat it for bg
    #    print("i... doing sumw2==0")
    #if errors is None:
        #histograms[hname].Sumw2(0) # THIS FOrces sqrt errors
    #     #sqrt_done = True
    #     #if sqrt_done:
    #     #print("i... doing sumw2==1")

        # CHECK THIS!!!!!!!!!!!!!!!!!!!!!!!!
    #    histograms[hname].Sumw2(1) # THIS LET IT TO BE SENSITIVE TO BackG and SCALE



    lowerror_cut = 0.6
    nonzero_mine = 0
    nonzero_min = 0
    if not(h1np is None) and  (len(h1np.nonzero())>1) and (h1np.nonzero()[0].min() >=0):
        if errors is None:
            nonzero_mine = np.sqrt( h1np.nonzero()[0].min() )*lowerror_cut
        else:
            nonzero_mine =  errors.nonzero()[0].min() * lowerror_cut

        # FIND nonezro minimum - error * factor=0.6
        if len(h1np.nonzero()[0])>0:
            nonzero_min = h1np.nonzero()[0].min() - nonzero_mine
        if  (runtime is not None) and (runtime>0.1): # SCALE ALSO ERRORS
            if len(h1np.nonzero()[0])>0 :
                nonzero_min = h1np.nonzero()[0].min()/runtime - nonzero_mine/runtime

    # ----------------- scale with runtime
    if h1np is not None and  runtime is not None:
        histograms[hname].Scale( 1/runtime)
        if len(h1np.nonzero()[0])>0 :
            if runtime>0: # crashed after server restart
                nonzero_min = h1np.nonzero()[0].min()/runtime - nonzero_mine/runtime



    # ------------ this prevents y-axis wobble in rate histogram
    binmx = histograms[hname].GetMaximumBin()
    binco = histograms[hname].GetBinContent( binmx)
    biner = histograms[hname].GetBinError( binmx)

    histomax = 1.01*(binco+biner)
    # histograms[hname].GetYaxis().GetXmin()
    #print(f"D... nonzero_min =   {nonzero_min}")
    #-----------I have a problem with that
    #histograms[hname].GetYaxis().SetRangeUser( nonzero_min, histomax )



def main():
    return

if __name__=="__main__":
    Fire(main)
