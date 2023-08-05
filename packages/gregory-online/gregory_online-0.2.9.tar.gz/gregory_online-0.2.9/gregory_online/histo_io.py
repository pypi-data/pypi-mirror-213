#!/usr/bin/env python3
"""
load and save operations
* load a textfile with LT A and B given in the filename
* verify under/overfl bin present
____
* definition of .details file INSIDE save_hist_txt
* real usage of .details file in     load_hist_txt with load_details
 : these are used in load_hist_txt
 - livetime
 - a
 - b
 - entries
 - rate
"""
from fire import Fire

import glob

from gregory_online.histo_global_cont import histograms

from gregory_online.histo_analyze import get_calib_coefs


from console import fg, bg, fx
import os
import numpy as np
import re # find livetime and a and b


#from gregory_online import histo_np_ops
from gregory_online.histo_np_ops import get_np_from_h
from gregory_online.histo_np_ops import fill_h_with_np
from gregory_online.histo_np_ops import get_range_from_calib

import datetime as dt

import pandas as pd

# --------------------------------------- for  tests -----------
import ROOT #  for tests here with gDirectory ls
import time
# JUST FOR TESTS
from  gregory_online.histo_displ import display_np, refresh_canvases
from gregory_online.histo_analyze import histo_fit,histo_zoomenergy
# --------------------------------------- for  tests -----------


def ispure2n( slen ,silent = False):
    """
    detect if it is 2^n bins or 2^n + 2 under/ovelrflow added
    """
    expon = 0
    pure2n = True
    for i in range(18): # max 2^18 ADC
        lend2 = slen/2**i
        if lend2<1.0:
            expon-=1
            break
        isint = lend2==int(lend2)
        if not isint:  pure2n = False
        # print("D... div2", expon,len(spe), lend2 , isint )
        expon+=1
    if not silent:
        print(f"D... ... ... : 2**{expon}=={2**expon} len=={slen} len==2^n: {pure2n}")
    return pure2n



def save_hist_txt( name , total_time , started, deadtime , errors = False):
    """
    if errors false:  one column, bin 1 to the last bin
    if errors true: three columns i,cont, err
    *.details file ... with DT LT ...
    """
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{name}_{stamp}"
    bmin =  1 # BIN 0 is underflow
    bmax =  histograms[ name ].GetXaxis().GetNbins() # last bin with data
    with open( fname+".txt", "w" ) as f:
        for i in range( bmin, bmax+1): # the last is not included..
            cont = histograms[ name ].GetBinContent( i )
            err={}
            if errors:
                err = histograms[ name ].GetBinError( i )
                f.write(f"{i} {cont} {err}\n")
            else:
                f.write(f"{cont}\n")
    print("i... 1/2 SAVED", fname+".txt")
    cont1 = histograms[ name ].GetBinContent( 0 )
    cont2 = histograms[ name ].GetBinContent( bmax+1 )
    print(f"D...  underfl={cont1} overflow={cont2}")
    with open( fname+".details", "w" ) as f:
        TTS = total_time
        DTP = deadtime*100
        DTS = total_time*deadtime
        LTS = TTS - DTS
        SUM = histograms[ name ].GetEntries()
        RATE = SUM/TTS
        now = dt.datetime.now()
        if RATE>100000:
            print(f"X... {fg.red} NON REALISTIC TOTAL TIME {fg.default} ")

        a,b = get_calib_coefs( histograms[ name ])
        f.write(f"totaltime {TTS:.2f}\n")
        f.write(f"livetime {LTS:.2f}\n")
        f.write(f"deadtimeprc {DTP:.2f}\n")
        f.write(f"a {a:.6f}\n")
        f.write(f"b {b:.3f}\n")
        f.write(f"entries {SUM}\n")
        f.write(f"rate {RATE:.2f}\n")
        f.write(f"started {started}\n")
        f.write(f"saved {now}\n")
        f.write(f"name {name}\n")
        f.write(f"fname {fname}\n")
        if errors:
            f.write(f"errors_column True\n")



    print("i... 2/2 SAVED", fname+".details")

    print()
    return



# -------------------------------------- for load interface
def list_spectra_disc():
    """
    look at spectra and details files. determine valid spectrum filename
    """
    avadisc = {}
    res = glob.glob("*.txt")
    red = glob.glob("*.details")
    num = 1
    for i in res:
        tst = os.path.splitext(i)[0]
        for j in red:
            if tst == os.path.splitext(j)[0]:
                avadisc[num] = tst
                num+=1
    return avadisc



def present_avadisc( avadisc ):
    print()
    col = 0

    for ke in sorted(avadisc.keys()):
        col+=1
        brk = ""
        if col%3==0:
            brk = "\n"
        print( f"  {bg.yellow}{fg.black} {ke} {fg.default}{bg.default}  {avadisc[ke]:35s} ", end=brk)
    print()
    print()


def select_histo_to_load( num=None ):
    """
    full sequence list,present, load
    """
    avadisc = list_spectra_disc()
    present_avadisc(avadisc)
    if num is None:
        return
        #num = input()
    try:
        num = int(num)
    except:
        num = None
        print("X... no spectrum selected")
    if num in avadisc.keys():
        load_hist_txt( avadisc[num] , f"s{num}" )


# ----------------------------------- loading spectra/histogram

def load_details(fname):   # used in load_hist_txt: where histograms[hname] is created
                           # and rate interpretted
    res = None
    if os.path.exists(fname):
        with open(fname) as f:
            res = f.readlines()
        res = [ (x.strip().split(" ")[0],"_".join(x.strip().split(" ")[1:])) for x in res]
        res = dict(res)

        # the following are gonna be converted and cause a crash if error
        res["totaltime"] = float(res["totaltime"]) # not always needed?
        # not floatres["started"] = float(res["started"]) # not always needed
        res["livetime"] = float(res["livetime"])
        res["a"] = float(res["a"])
        res["b"] = float(res["b"])
        res["entries"] = float(res["entries"])
        res["rate"] = float(res["rate"])
    return res




def load_hist_txt( filename, hname , underoverflow = False):
    """
    loads histo : full or rate w. details file.
    histograms[] will get NORMALIZED version;  underover bit is appended just for TH1
    returns nparray without under over flow.
    """
    # I use pandas as in pr_load.py ...
    avadisc = list_spectra_disc()
    present_avadisc(avadisc)

    hole = os.path.splitext(filename)[0]
    if not os.path.exists(filename):
        print("X... no file ", filename, end=" ...")
        if os.path.exists(hole+".txt"):
            filename = hole+".txt"
            print("i... replacing with ", filename)
        else:
            print("X... no file ", filename)
            return None

    res = load_details( hole+".details")
    details = True
    if res is None: details = False


    df = pd.read_csv(filename, delimiter="\s+", header=None, comment="#", nrows=2)
    ncols = df.shape[1]
    print(f"D... file {filename} with {ncols} columns, details found = {details}")

    np_c = None
    np_e = None # for rate into th1f

    if (ncols==1):
        df = pd.read_csv(filename, delimiter="\s+", header=None, comment="#", names = ['cont'] )
        print(df)
        np_c = df['cont'].values
    if (ncols==3):
        df = pd.read_csv(filename, delimiter="\s+", header=None, comment="#", names = ['bin','cont','err'] )
        print(df)
        np_c = df['cont'].values
        np_e = df['err'].values

        # print( type(np_c), type(np_e), np_c)
        # df.to_csv("zest.txt", sep=' ', header = None)


    spe = np_c # ================= taking content
    pure2n = ispure2n( len(spe) )
    isunovf = ispure2n( len(spe)-2, silent = True )
    if pure2n:
        print("i... ...  seems no under/overflow bins in the file")

    # ------------------------------------------ this part is tricky, FOR UND OVF LOAD
    if underoverflow: print("I... supposing the UND/OVER FLOW bins are already present!!")
    if underoverflow and isunovf:
        print("D... Under/overflow bins detected and loading")
    if not(underoverflow) and isunovf:
        print(f"X... {fg.red} Under/overflow bins DETECTED but NOT loading {fg.default}")
    #
    if underoverflow and  pure2n:
        print(f"X... {fg.red} PROBLEM - file is 2^n but loading w U/OVF {fg.default}")
    if (not underoverflow) and  (not pure2n):
        print(f"X... {fg.red} PROBLEM - file is NOT 2^n but loading wout U/OVF {fg.default}")
    # ------------------------------------------ this part was tricky, FOR UND OVF LOAD

    if not underoverflow:
        print("D... adding artificially undeflow/overflow bins...")
        np_c = np.concatenate(([0],np_c,[0]))
        if np_e is not None:
            np_e = np.concatenate(([0],np_e,[0]))
    else:
        print("D... underflow/overflow bits (must be) already present in source file")

    h1np_backg = np_c
    rate = res['rate']
    if abs(h1np_backg.sum()-rate)/rate<0.1:
        print("i... ... already RATE histogram interpretation !!! ...")
        rate = res["rate"]
        res['livetime'] = 1
    else:
        if res['livetime'] is not None and res['livetime']>0:
            rate = h1np_backg.sum()/res['livetime']
    #print(f"i... LEN={len(h1np_backg)} rate={rate}" )
    # normalize
    #print(  res["b"] )
    #print( res["a"] )
    #print( float(res["a"])*(len(h1np_backg)-2) )
    #print( res["b"]  )

    #  create a normalized histo in the histograms[]
    fill_h_with_np( h1np_backg, hname,
                                 runtime = res["livetime"], errors = np_e,
                                 limits_calib=[res["b"], res["a"]*(len(h1np_backg)-2)+res["b"] ]
    )
    histograms[hname].SetEntries( res["entries"] )
    histograms[hname].SetTitle( hole)
    histograms[hname].Print()
    print(f" ... Name= {histograms[hname].GetName()}  Title={histograms[hname].GetTitle()}" )

    if not underoverflow:
        # artificialy added unovf, removing again
        return h1np_backg[1:-1]
    else:
        # already present in spe
        return h1np_backg[1:-1]




    # grp = re.search(r'[\w\d]+_lt([\d\.]+)_a([\d\.]+)_b([\-\d\.]+)\.txt',filename)
    # print(f"D... histo decoded  lt,a,b={fg.green} {grp.groups()} {fg.default}")
    # h1np_backg_lt = float(grp.groups()[0])
    # cala_bg = float(grp.groups()[1])
    # calb_bg = float(grp.groups()[2])

    # pure2n = True # is it pure 2^n?

    # if os.path.exists(filename):
    #     with open(filename) as f:
    #         spe = f.readlines()
    #     spe = [ float(x.strip()) for x in spe]
    #     # 2**15 32768

    #     #spe.append(0)
    #     #spe.append(0)
    #     pure2n = ispure2n( len(spe) )
    #     isunovf = ispure2n( len(spe)-2 )
    #     if underoverflow and isunovf:
    #         print("D... Under/overflow bins detected and loading")
    #     if not(underoverflow) and isunovf:
    #         print(f"X... {fg.red} Under/overflow bins DETECTED but NOT loading {fg.default}")
    #     # expon = 0
    #     # for i in range(18): # max 2^18 ADC
    #     #     lend2 = len(spe)/2**i
    #     #     lend2a = (len(spe)-2)/2**i
    #     #     if lend2<1.0:
    #     #         expon-=1
    #     #         break
    #     #     isint = lend2==int(lend2)
    #     #     if not isint:  pure2n = False
    #     #     # print("D... div2", expon,len(spe), lend2 , isint )
    #     #     expon+=1
    #     # print(f"D... calculated exp: 2**{expon}=={2**expon} len=={len(spe)} pure2n={pure2n}")

    #     if underoverflow and  pure2n:
    #         print(f"X... {fg.red} PROBLEM - file is 2^n but loading w U/OVF {fg.default}")
    #     if (not underoverflow) and  (not pure2n):
    #         print(f"X... {fg.red} PROBLEM - file is NOT 2^n but loading wout U/OVF {fg.default}")


    #     if not underoverflow:
    #         print("D... adding undeflow/overflow bins...")
    #         spe.insert(0,0) # to be compatible with underflow and overflow
    #         spe.append(0)
    #     else:
    #         print("D... underflow/overflow bits already present in source file")
    #     h1np_backg = np.array( spe )
    #     rate = 1
    #     if h1np_backg_lt is not None and h1np_backg_lt>0:
    #         rate = h1np_backg.sum()/h1np_backg_lt
    #     print(f"i... {h1np_backg} LEN={len(h1np_backg)} rate={rate}" )
    #     # normalize
    #     histo_np_ops.fill_h_with_np( h1np_backg, hname, h1np_backg_lt, limits_calib=[calb_bg, cala_bg*(len(h1np_backg)-2)+calb_bg ])

    # if not underoverflow:
    #     # artificialy added unovf, removing again
    #     return h1np_backg[1:-1]
    # else:
    #     # already present in spe
    #     return h1np_backg[1:-1]





def main():# fname, hname):
    """
    I can load txt file when lt a b  are in the filename...
    """
    #load_hist_txt(fname, hname)
    select_histo_to_load()
    ROOT.gDirectory.ls()

    for i in histograms.keys():
        # histograms[i].Draw()
        hnp,enp = get_np_from_h(histograms[i] )
        # this is in h already...
        a,b = get_calib_coefs( histograms[ i ])
        lo,hi = get_range_from_calib( histograms[ i ], a, b)
        print(hnp)
        print(enp)
        print("="*50)
        display_np( hnp, "q", "c_q" , errors=enp , limits_calib=(lo,hi) , filled=True, color=32)
        # display_np( hnp, "q", "c_q" , errors=enp  )
        # ------------  I can plot from here
        # ...
        # now fit test
        histo_zoomenergy( histograms[i], 1455,1468)
        #histo_zoomenergy( histograms[i], 929,939)
        res = histo_fit( histograms[i],  canvas = "fitresult")
        #print(res)
        break



    while True:  time.sleep(1)

if __name__=="__main__":
    Fire(main)
