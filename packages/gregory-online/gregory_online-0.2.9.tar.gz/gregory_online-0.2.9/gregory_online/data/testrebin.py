#!/usr/bin/env python3

from fire import Fire
import numpy as np
import scipy.ndimage
#from scipy.ndimage.interpolation import shift
import matplotlib.pyplot as plt



def rebin_np( a , sca, shi, order = 3):
    b = scipy.ndimage.zoom(a, sca, order=order)
    b = scipy.ndimage.interpolation.shift(b, shi , cval=0, order = order)
    asu = a.sum()
    bsu = b.sum()
    b=b/bsu*asu
    df = len(b) - len(a)
    #print( f" b={len(b)}    a={len(a)}   df = {df}")
    while df<0:
        b = np.append( b,[0] )
        df = len(b) - len(a)
    if df>0:
        b = b[:-df]
    #print( len(a),"X" ,len(b),  f" 6 -->  {6*sca+shi}" )
    #print( len(a),"X" ,len(b),  f" 22 -->  {22*sca+shi}" )
    return b




def main():

    a = np.array( [2,2,4,5,6,12,41,17,5,4,3,2,1,2,4,3,5,4,2,3,4,11,44,43,14,2,3,2,3] )
    a = a.astype(float)
    print(a)


    b = rebin_np(a, 0.9, 2.2, order=1 )
    c = rebin_np(a, 0.9, 2.2, order=3 )

    db=b-a
    dc=c-a

    plt.plot(a)
    plt.plot(b,'y--')
    plt.plot(c,'r--')
    plt.plot(db,'y:')
    plt.plot(dc,'r:')
    plt.grid()
    plt.show()
    #print(b-a)

if __name__=="__main__":
    Fire(main)
