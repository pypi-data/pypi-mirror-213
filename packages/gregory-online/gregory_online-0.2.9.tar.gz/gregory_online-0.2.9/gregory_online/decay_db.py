#!/usr/bin/env python3
"""
This is a module that reads parquet (dcreated in nuphy2 from lara decay data
- prints a table
"""

from fire import Fire

import pandas as pd
from console import fg,bg
import importlib_resources # for data/*

from terminaltables import AsciiTable,SingleTable


PARQFILE = 'decay_lara.parquet'




def nicetime(t):
    suff = "s"
    if t>60:
        suff = "m"
        t = t/60
    if t>60:
        suff = "h"
        t = t/60
    if t>24:
        suff = "d"
        t = t/24
    if t>365:
        suff = "y"
        t = t/365

    if t>1e9:
        suff = "Gy"
        t = t/1e9
    if t>1e6:
        suff = "My"
        t = t/1e6
    if t>1e3:
        suff = "ky"
        t = t/1e3
    return f"{t:.2f} {suff}"



def candidates( dfo, e, de , t12low = 10, etrsh = 70, itrsh = 1):

    table = []
    print(f"i... {len(dfo)} gammas total", end="")
    dfo = dfo.loc[ dfo["E"]>etrsh ]

    df = dfo
    df = df.loc[ df["I"]>itrsh ]
    # df = df.loc[ df["E"]>etrsh ]
    df = df.loc[ df["T12"]>t12low ]
    print(f"i... limited to {len(dfo)}  E>{etrsh}; I>{itrsh}; t12>{nicetime(t12low)}", end="")

    df = df.loc[ (df["E"]>e-de) & (df["E"]<e+de) ]
    print(f"i... {len(df)} candidate(s) for dE={de:.2f}")#; limited E>{etrsh}; I>{itrsh}; t12>{nicetime(t12low)}")
    #print(f"i... {len(df)} candidates; limited E>{etrsh}; I>{itrsh}; t12>{nicetime(t12low)}")
    # susp = list(df['name'].values.tolist())


    table_data = []

    column=-1
    trow = -1
    shift = 30
    #table_data.append([]) # row 0

    for index, row in df.iterrows():
        column+=1
        currint = row['I']
        currene = row['E']
        currname  = row['name']
        ss = f"{fg.white}{currname}    {nicetime(row['T12'])} {fg.default}"
        table_data.append( [ss] )

        dfsel = dfo.loc[ (dfo['name']==currname) & (dfo['I']>=currint/3) ]
        if len(dfsel)>2:
            dfsel = dfsel.sort_values( ['I','E'] , ascending = False)

        trow = 0
        enepres = False
        mute = False
        for i2,r2 in dfsel.iterrows():
            trow+=1
            if trow>7: # thick to display not more 7, but add ene
                mute = True # demutes if green
            ss = ""
            if r2['E']==currene:
                ss+=f"{fg.green}"
                enepres = True
                mute = False
            else:
                ss+=f"{fg.default}"
            ss+= f"{r2['E']:8.2f}  {r2['I']:7.2f}"
            #if r2['E']==currene:
            ss+=f"{fg.default}"
            if not mute:
                table_data[-1].append( ss )
            #print(table_data)


    print( )
    #for i in range(len(table_data)):
    #    print(table_data[i])

    # before transposition, I need full square
    mx = 0
    for i in table_data:
        if mx<len(i):mx=len(i)
    #print(mx)
    for i in table_data:
        while len(i)<mx:i.append("")

    if len(table_data)>0:
        table_data = list(map(lambda *x: list(x), *table_data)) # transpose
    SingleTable( table_data )
    #print(table_data)

    table_instance = SingleTable(table_data, "candidates")
    # table_instance.justify_columns[2] = 'right'
    if column <6:
        print(table_instance.table)
    else:
        print(f"i... too many columns ({column+1})")





def decay_candidates( E, dE=1):
    """
    verify the parquet
    """
    #E = 121

    ret = importlib_resources.files("gregory_online").joinpath("data/"+PARQFILE)
    #print(ret)
    dfo = pd.read_parquet(ret)
    # dfo = dfo.loc[ dfo["E"]>70 ]

    candidates( dfo , E, dE)

    #pd.set_option("display.max_rows", None, "display.max_columns", 7)
    #df = df.sort_values( ["E","A"] )


    #print(df)

#def main():
    # load()



if __name__=="__main__":
    Fire( decay_candidates   )
