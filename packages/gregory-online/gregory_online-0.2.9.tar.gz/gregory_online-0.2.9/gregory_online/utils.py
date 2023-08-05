#!/usr/bin/env python3

from fire import Fire
from gregory_online.version import __version__


from pyfromroot import  prun
from console import fg,bg

import os

#
#  taken from flashcam and stackoveerflow
import math

def is_int(n):
    # try:
    #     if math.isnan(n):
    #         return False
    # except:
    #     return False

    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n


def is_float(n):
    try:
        float_n = float(n)
        #print(n, float_n)
    except ValueError:
        print(f"X... not float /{n}/ ... false ret")
        return False
    else:
        #print("true block", n)
        if n is None:
            print("X... isfloat ... NONE")
            return False

        retval = True
        try:
            if type(n) is not str and math.isnan(n): # if Nan comes, it can sort it out, else it crashes with string.
                print("X... math ... NAN float")
                retval = False
        except:
            print("X... crashed math NaN")
            retval = False
        return retval # normally true


def is_bool(n):
    if type(n) is str and n=="False": return True
    if type(n) is str and n=="True": return True
    return False




def ecalibration( calist, overridefile = ""):
    ECALIB = calist
    if len(ECALIB)==0:
        return 1,0
    if len(ECALIB)==1:
        ECALIBb = 0
        ECALIBa = ECALIB[0][0] / ECALIB[0][1]
        return ECALIBa, ECALIBb
    elif len(ECALIB)==2:
        ECALIBa = (ECALIB[0][0] - ECALIB[1][0]) / ( ECALIB[0][1] - ECALIB[1][1] )
        ECALIBb = ECALIB[0][0] - ECALIBa* ECALIB[0][1]
        return ECALIBa, ECALIBb
    else:
        print("i... LINEAR REGRESSION needed now")
        fname,fnamefull = None,None
        if overridefile == "": # ---create file to load --
            fname = "/tmp/tmp_ecalib"
            fnamefull = f"{fname}.txt"
            with open(fnamefull,"w") as f:
                for pair in ECALIB:
                    f.write( f"{pair[0]} {pair[1]} {pair[2]}\n")

        else: # OR ------** just take some other file **
            fnamefull = overridefile
            fname = os.path.splitext(fnamefull)[0]

        # and do fit
        prun.loadpy("load",f"{fnamefull} y,x")
        print(f"i...  {bg.green} _________________loaded___________{bg.default}")
        res = prun.loadpy("fit",f"{fname} pol1", canvas="ecalibration")
        #print(res)
        print()
        print(res.keys())
        return res["a"],res["b"]
        #prun.loadpy("draw","tmp_ecalib")
        #print("press enter")
        #input()
        #prun.do("draw","/tmp/tmp_ecalib", canvas = "cn2")

def main( txt , overridefile = ""):
    print( "f : ",is_float(txt) )
    print( "i : ",is_int(txt) )
    print( "b : ",is_bool(txt) )

    calist = [[1764.5, 2967.1799251154357, 0.1], [1460.8, 2456.0100724765166, 0.2], [609.3, 1023.7130926318914, 0.05], [351.9, 591.028749200901, 0.3]]
    ecalibration (calist , overridefile = overridefile)
    print("say ENTER 1")
    input()
    print("----{bg.yellow} ---------------------------- {bg.default}")
    ecalibration (calist , overridefile = overridefile)
    print("say ENTER")
    input()


if __name__=="__main__":
    Fire(main)
