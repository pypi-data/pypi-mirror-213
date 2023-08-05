#!/usr/bin/env python3
"""
 This should be able to analyze spectrum
* area
* gauss fit
And send data to influx (stored at ~/.seread.discover8086 ++ )
"""
from fire import Fire
#from tdb_io import influxwrite
import tdb_io

# let's see if we can fit
from pyfromroot import  prun

import datetime as dt
import time

from console import fg,bg



def get_ene_range(h):
    """
    input: TH1
    """
    blo = h.GetXaxis().GetFirst()
    bhi = h.GetXaxis().GetLast()
    a,b = get_calib_coefs(h)
    return a*blo + b, a*bhi+b

def get_calib_coefs(h):
    """
    input: TH1
    """
    bins = h.GetXaxis().GetNbins()
    xlo = h.GetXaxis().GetXmin()
    xhi = h.GetXaxis().GetXmax()
    # E = a*k +b
    a = (xhi-xlo)/bins
    b = xhi - a*bins
    return a,b


def bin2ene( binn, h):
    """
    input: TH1
    """
    a,b = get_calib_coefs( h )
    return a*binn+b

def ene2bin( ene, h ):
    """
    input: TH1
    """
    a,b = get_calib_coefs( h )
    return round((ene - b)/a)

def histo_unzoom(h):
    """
    input: TH1
    """
    # UnZoom() is crap. ... does everything....
    #histo_details(h)

    # this is going with bins, not energy
    bins = h.GetXaxis().GetNbins()
    h.GetXaxis().SetRange( 1, bins )
    #
    #h.GetXaxis().SetRangeUser( xlo, xhi ) # using energy

    #histo_details(h)
    return

def histo_area( h, elo=None, ehi=None ):
    """
    input: TH1
    """
    if elo is None:
        elo = h.GetXaxis().GetXmin() # energy, not bins GetFirst is bin
    if ehi is None:
        ehi = h.GetXaxis().GetXmax() # energy, not bins GetLast is bin
    intg = h.Integral( ene2bin(elo,h), ene2bin(ehi,h) )
    return intg

def histo_zoomenergy( h, xlo, xhi ):
    """
    input: TH1
    """
    print(f"i... zooming with energy  {xlo}...{xhi}" )
    intg = h.Integral( )
    #print(f"i... integral before zoom = {intg:16.6f}")
    h.GetXaxis().SetRangeUser( xlo, xhi ) # using energy
    intg = h.Integral( ene2bin(xlo,h), ene2bin(xhi,h) )
    #print(f"i... integral after  zoom = {intg:16.6f}")

    return

def histo_zoombins( h, xlo, xhi ):
    """
     input: TH1
    """
    print(f"i... zooming with bins {xlo}...{xhi}" )
    intg = h.Integral( )
    #print(f"i... integral before zoom = {intg}")
    h.GetXaxis().SetRange( xlo, xhi ) # using bins
    intg = h.Integral( xlo, xhi)
    #print(f"i... integral after zoom = {intg}")
    return

def histo_details( h ):
    """
    input: TH1
    Info needed for fit etc.
    """
    bins = h.GetXaxis().GetNbins()
    xlo = h.GetXaxis().GetXmin()
    xhi = h.GetXaxis().GetXmax()
    xzlo =h.GetXaxis().GetFirst()
    xzhi =h.GetXaxis().GetLast()
    intg = h.Integral()

    # E = a*k +b
    a,b = get_calib_coefs( h )
    #a = (xhi-xlo)/bins
    #b = xhi - a*bins

    print(f"i... | - bins={bins};  xmin-xmax = {xlo} - {xhi}")
    print(f"i... | - calib: a={a:9.6f}  b={b:7.3f}")
    print(f"i... | - zoom bins: {xzlo} ... {xzhi}")
    print(f"i... | - zoom ene : {a*xzlo+b:.1f} ... {a*xzhi+b:.1f}")
    print(f"i... | - integral={intg}  [of the zoomed area]")


def histo_fit( h ,  canvas = None, zoomme = None):
    """
    input: TH1
    """
    hname = h.GetName()
    print("i... fitting gauss in the range")

    # zoom?
    res = prun.loadpy("fit",f"{hname} gpol1", canvas = canvas)

    if res['area']<0: res['area']=-res['area']

    if abs(res['diff_fit_int_proc'])>1:
        print(f"X...  {fg.yellow}BAD DESCRIPTION - DIFF MORE THAN 1%{fg.default} ")
        time.sleep(0.2)

    if not( res['noerror']):
        print(f"X...  {fg.red}BAD DESCRIPTION - SOME ERROR OF FIT{fg.default}")
        time.sleep(0.2)
        return

    elif abs(res['area']) <= 2*res['darea']:
        print(f"X...  {fg.red}BAD DESCRIPTION - Area error > area/2{fg.default}")
        time.sleep(0.2)

    # for rate .... can by small
    # elif res['area'] <= 7:
    #     print(f"X...  {fg.red}BAD DESCRIPTION - SMALL Area < 7{fg.default}")
    #     time.sleep(0.2)

    else:
        now = dt.datetime.now()
        # wri = f"{(now-started).total_seconds():8.1f} {res['E']:9.2f} {res['dE']:8.3f} {res['area']:12.2f} {res['darea']:10.2f} {res['Efwhm']:10.3f} {res['dEfwhm']:7.2f}\n"
        # print(wri)
        cala, calb = get_calib_coefs( h )
        res["E"]       = res["channel"]*cala + calb
        res["dE"]      = res["dchannel"]*cala
        res["Efwhm"]   = res["fwhm"]*cala
        res["dEfwhm"]  = res["dfwhm"]*cala
        res["fittime"] = now
        return res
    return None



def main():
    print()

if __name__=="__main__":
    Fire(main)
