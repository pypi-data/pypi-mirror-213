#!/usr/bin/env python3
"""
display functions moved here
"""
from fire import Fire

from gregory_online.histo_global_cont import histograms
from gregory_online.histo_global_cont import canvases

from gregory_online.histo_analyze import get_calib_coefs

from console import fg, bg, fx
import os
import numpy as np


import datetime as dt

import pandas as pd

import ROOT #  for tests here with gDirectory ls
import time


# to fill if not displayable
from gregory_online.histo_np_ops import fill_h_with_np



def refresh_canvases():
    """
    unselectively refresh every canvas
    """
    maxc = ROOT.gROOT.GetListOfCanvases().GetEntries()
    for i in range(maxc):
        ci = ROOT.gROOT.GetListOfCanvases().At(i)
        ci.Modified()
        ci.Update()





def display_h_name( hname="tot", cname = "c_tot", filled = False , color = 39, title=None):
    """
    display (e.g. substracted) histograms NEVER USED
    """
    global histograms,canvases
    if not  ROOT.gDirectory.FindObject(hname): # this naver happens
        print(f"i... histo {hname} is NOT found")
        return

    if ROOT.gDirectory.FindObject(cname):
        print(f"i... CANVAS {cname} is found")
        canvases[cname] = ROOT.gDirectory.FindObject(cname)
        canvases[cname].cd()
    else:
        print(f"{fg.cyan}w... CANVAS {cname} is NOT there, we {fg.green}create now{fg.default}")
        canvases[cname] = ROOT.TCanvas(cname,cname)
        canvases[cname].Draw()

    if ROOT.gDirectory.FindObject(hname): # this naver happens
        print(f"i... histo {hname} is found")

        #histograms[hname].SetLineColor(2)
        #histograms[hname].Draw("EX0")
        #histograms[hname].SetFillColor(19)
        histograms[hname].SetMarkerStyle(7)
        #histograms[hname].SetLineColor(16) # gray
        if filled:
            histograms[hname].SetFillStyle(3001)
            histograms[hname].SetFillColor(39)
            histograms[hname].Draw("hEX0")
        else:
            histograms[hname].Draw("EX0")
        print("D... GRIDS HERE")
        ROOT.gPad.SetGridx()
        ROOT.gPad.SetGridy()
        ROOT.gPad.Modified()
        ROOT.gPad.Update()

    else:
        print(f"{fg.red}X... {hname} not found in gDirectory{fg.default}")
        ROOT.gDirectory.ls()
    #all reresh will be later
    #canvases[cname].SetGridx()
    #canvases[cname].SetGridy()
    canvases[cname].Modified()
    canvases[cname].Update()






def display_np(h1np, hname="tot", cname = "c_tot" , runtime=None, errors = None, limits_calib = None, filled = False, color = 16):
    """
    displaying needs a carefull treatment & histogram filling
    color 32, 48
    """
    global histograms,canvases
    if ROOT.gDirectory.FindObject(cname):
        print(f"i... CANVAS {cname} is found")
        canvases[cname] = ROOT.gDirectory.FindObject(cname)
        canvases[cname].cd()
    else:
        print(f"{fg.cyan}X... CANVAS {cname} is NOT there, we create now{fg.default}")
        canvases[cname] = ROOT.TCanvas(cname,cname)
        canvases[cname].Draw()

    if ROOT.gDirectory.FindObject(hname):
        print(f"i... histo {hname} is found")

        # histograms[hname].SetMarkerStyle(7)
        # histograms[hname].SetLineColor(16)
        # histograms[hname].Draw("EX0")

    else:
        #print(f"X... {hname} is NOT there, we run ")
        fill_h_with_np(h1np,hname, errors=errors, limits_calib=limits_calib, title = hname)
        #histograms[hname].Draw("HEX0") # E0 bars, X0 no 0,

    histograms[hname].SetMarkerStyle(7)
    histograms[hname].SetLineColor(color)
    if filled:
        histograms[hname].SetFillStyle(3001)
        histograms[hname].SetFillColor(color)
        histograms[hname].Draw("hEX0") # E0 bars, X0 no 0,
    else:
        histograms[hname].Draw("EX0") # E0 bars, X0 no 0,


    #all reresh will be later
    canvases[cname].Modified()
    canvases[cname].Update()




def main():
    print()

if __name__=="__main__":
    Fire(main)
