#!/usr/bin/env python3

from fire import Fire
import ROOT
import urllib.request
import json
import time
import datetime as dt
import numpy as np
import os
from console import fg,bg,fx
import socket
import threading
import re # decode title

class Histogram:
    """
    start2collect ... it loops.  Kills with do_run=False

    """

    def set_step(self, step):
        self.STEP = step
        print(f"i... poll step set to /{step}/")


    def __init__(self, url, spectrum="b0c00", peaksfile=None, calibrationfile=None, bgfile=None ):
        """
        init & first draw; calls self.wait at the end == runs in loop
        """

        self.started = None #  dt.datetime.now()
        self.tcp_fetch_time = None
        self.measurement = "hpge" # string in INFLUXDB

        self.realtime = None

        self.url = f'http://{url}:9009/{spectrum}/root.json'
        self.spectrumname = spectrum
        print(f"i... url = {self.url}")

        self.size = 2**15 # histogram size
        self.xmin = 0 # no calibration at the start, avoid crash in get_calib
        self.xmax = self.size

        self.maximum = 10 # default of histomax, but overriden immediat
        self.N_EMIN = 20 # 20keV noise end by definition
        self.e_window = 15 # +- Window to ZOOM and Analyze


        self.first_influx_omit = True # ONETIME TRIG

        self.bgfile = bgfile # others are used later....  BACKGROUND FILE
        self.bgfile = "bg88320.txt" # others are used later....  BACKGROUND FILE
        self.bgtime = 88320
        #-------------------- timing of display

        self.STEP = 2 # seconds THIS IS COLLECTION INTERVAL


        self.SECONDS = 10
        self.MINUTE = 60 # 5minutes (300)
        #self.MINUTE = 60 #

        self.HOUR = 3600
        #self.HOUR = 60


        # calibration that comes from GetXaxis()
        #self.xmin = 0
        #self.xmax = self.size

        #self.store_limit = 3600 # seconds
        self.store_limit = 3*3600 # seconds

        self.first_fetch = True # avoid 1st fetch diff
        #------------------------------------------------ init NumPy array
        self.h1np = np.zeros( self.size+2)
        self.h1np_prev = np.zeros( self.size+2)
        self.h1np_diff = np.zeros( self.size+2)

        #---------------------- store this got get()
        self.fflag = False # fetch flag
        now1 = dt.datetime.now() # fetch flag
        time.sleep(0.2)
        self.runtime = dt.datetime.now() - now1 # fetch flag
        # print("D... init end")
    #------------------------------------------------------------

    #i keep all the history histos here in this object
    def get_lenhistos(self):
        return len(self.histos)

    def get_limits_calib(self):
        return self.xmin,self.xmax

    def get_limits_bins(self):
        return 0,self.size


    def get_partial_time_histo(self, age):
        ele=None
        dist=999999
        #print(f"D... demanded age = {age}")
        for k in self.histos.keys():
            if ele is None: ele = k
            agedif = abs(self.histos[k][0] - age)
            #print(f"D... {k} - histo = {self.histos[k]}")
            if agedif < dist:
                ele = k
                dist = agedif
        #print(f"D... retuning closest distance  == {dist}")
        return self.histos[ele][1], dist


    # earlier set_runtime...
    def set_started_before(self, seconds, silent = False):
        if not silent:  print("i... started was=",self.started,"  calulating from ",seconds)
        self.started = dt.datetime.now() - dt.timedelta(seconds=seconds)
        # there was some worry aobut resistance to clear....
        # ... spectrum jumps...
        # self.runtime = dt.timedelta(seconds=seconds)
        if not silent:  print("i... newly       ",self.started, "runtime=",self.runtime )
        #self.runtime =


    def get_started(self):
        return self.started


    def get_runtime(self):
        #print( "D... get runtime:", self.runtime, type(self.runtime)  )
        # print(f"D... realtime in get_runtime  = {self.realtime}")
        if type(self.runtime) is dt.timedelta:
            if self.runtime.total_seconds()<=0:
                self.runtime = dt.timedelta(seconds=1)

        if self.realtime is not None: # TITLE is used .....
            #print( "D... realtime=", self.realtime  ,   self.runtime )
            if abs(self.realtime  -self.runtime.total_seconds() )>15: # DEIFFERENCE 15 seconds ........
                print(f"{fg.red}START TIME RESET !!!!!!!!!!{fg.default}")
                self.set_started_before( self.realtime ) # RESET RUNTIME, SINCE THERE IS A 15s difference
            return dt.timedelta( seconds=self.realtime ) # taken from TITLE
        else:
            return self.runtime
        return 1


    def get_h1np(self):
        return self.h1np

    def get_h1np_diff(self):
        return self.h1np_diff

    def get_deltat(self):
        return self.deltat


    def fetch_flag(self):
        """
        Let know ONLY ONCE that there was a fetch
        """
        if self.fflag:
            self.fflag = False
            return True
        return False



    def fetch_histo(self):
        """
        Every fetch, numpy arrays are filled /  TH1F content is set too
        h1np and h1np_prev and h1np_diff    are kept
        """


        #print(f"i... fetching ...{self.url}", end="\n")

        fstart = dt.datetime.now()
        ok = False
        try:
            with urllib.request.urlopen(self.url, timeout=5) as response:
                jhis = response.read().decode("utf8")
            ok = True
            #print("i... ok")
        except:
            ok = False
        self.tcp_fetch_time = (dt.datetime.now() - fstart).total_seconds()


        if not ok :
            print(f"!... no connection {self.url}")
            return False

        jhis = json.loads(jhis)
        # dict_keys(['_typename', 'fUniqueID', 'fBits', 'fName', 'fTitle', 'fLineColor', 'fLineStyle', 'fLineWidth', 'fFillColor', 'fFillStyle', 'fMarkerColor', 'fMarkerStyle', 'fMarkerSize', 'fNcells', 'fXaxis', 'fYaxis', 'fZaxis', 'fBarOffset', 'fBarWidth', 'fEntries', 'fTsumw', 'fTsumw2', 'fTsumwx', 'fTsumwx2', 'fMaximum', 'fMinimum', 'fNormFactor', 'fContour', 'fSumw2', 'fOption', 'fFunctions', 'fBufferSize', 'fBuffer', 'fBinStatErrOpt', 'fStatOverflows', 'fArray'])


        #print(jhis.keys() )

        # print( jhis["fTitle"])

        grp = re.search(r'rt=([\d\.]+)$',jhis["fTitle"])  # rt=3600 at the END of title ...
        # print(grp)
        if grp is not None and len(grp.groups())>0:
            self.realtime = float(grp.groups()[0].split("=")[-1])
            #print( f" realtime from title grp ={self.realtime}" )

        # THIS STEERS CALIBRATION ..... limits_calib
        self.xmin = jhis['fXaxis']['fXmin']
        self.xmax = jhis['fXaxis']['fXmax']

        #print( jhis.keys() )
        helem = jhis['fArray']

        # print("D... helem in fetch: len,0,1 ...", len(helem) , helem[0], helem[-1] )

        self.h1np_prev = 1.0*self.h1np # save  previous
        self.h1np = np.array( helem )

        #---------protection in case of  reset
        if self.h1np.sum()< self.h1np_prev.sum():
            print(f"i... {fg.red}RESET? I CLEAN THE PREV. HISTOGRAM{fg.default}")
            self.h1np_prev = self.h1np_prev*0
            self.histos = {} # !!!
            # BUG?
            self.set_started_before( 1 ) # BUG?

        if self.first_fetch:
            self.first_fetch = False
            self.h1np_diff = self.h1np*0
        else:
            self.h1np_diff = self.h1np - self.h1np_prev

            # print("D... diff after substract", self.h1np_diff)
            # print("D... h1np and prev@ substract",  self.h1np, self.h1np_prev)
            # underflow should be retained

        #sum = 0

        #self.maximum = max(helem)

        #print(f"D... end fetch {sumnow-sumprev}  {sumnow}, {sumprev}")
        return True




    def start2collect(self):
        """
        We reset histos DICT and start to collect all
        dict members = list [ deltat, histo ]
        ON RESTART - it resets the self.started
        """
        self.histos = {}

        # i think these are starting values---------------------

        deltas = np.zeros( 2 ) +0.2
        avgdeltat = 0.2
        avgoverhead = 0.02
        overheads = np.zeros(2) + 0.02
        lastnow = dt.datetime.now() # for the 1st

        #for i in range(20):
        self.thrmyself = threading.current_thread()

        #while True: THREAD WaTCHES the FLAG from INSIDE... it can be stopped from outside
        while getattr( self.thrmyself, "do_run", True ):
            # print( "getattr FETCH",  getattr(self.thrmyself, "do_run", True) )

            start = dt.datetime.now()
            self.fetch_histo()
            now = dt.datetime.now() # NOW = AFTER HISTO IS DELIVERED

            if (now-lastnow).total_seconds() > self.STEP:
                overheads = np.append( overheads,   (now-lastnow).total_seconds() - self.STEP )

            deltat = (now - start).total_seconds()
            deltas = np.append( deltas, deltat )

            avgdeltat = deltas.mean()

            sumnow = self.h1np.sum()
            sumprev = self.h1np_prev.sum()
            # -------- if no change or smaller SUM (clashes with fetch reset)
            #if (sumnow<=sumprev) or (sumnow==0) or (sumprev==0):
            if (sumnow<=sumprev) :
                # self.started=now # this doesnt reset really
                self.set_started_before( 1 ) # BUG?
                print("I... START TIME RESET")
            # -------- if no change or smaller SUM (clashes with fetch reset)
            if (sumnow<=sumprev) or (sumnow==0):
                self.histos = {}

            # ---------runtime, that is resistant to clear or no count
            #  HERE I PREPARE REALTIME AND RUNTIME (if no title info available)
            #   - this (together wth get_) can keep self.started  GOOD - TITLEvar works...

            if self.started is None:
                if self.tcp_fetch_time is not None:
                    if self.realtime is not None: # set from TITLE rt=
                        # print(f"D... {fg.yellow}1st tuning of starttime from title realtime{fg.default}")
                        self.set_started_before( self.realtime + self.tcp_fetch_time/2)
                    else:
                        # print(f"D... {fg.yellow}1st tuning of starttime from runtime{fg.default}")
                        self.set_started_before( self.runtime.total_seconds() + self.tcp_fetch_time/2 ) # guess

            if self.realtime is None: # do it from our time
                if self.started is not None:
                    self.runtime = now - self.started
            else: # DO IT FROM TITLE -
                self.runtime = dt.timedelta(seconds = self.realtime)
                # -nothing,,
            # if self.runtime < 0:
            #     if self.realtime is not None:
            #         self.runtime = now - self.started

            #print(self.started)
            #print(self.runtime)



            # print(f"i... {str(self.runtime)[:-4]} dt= {deltat:.2f} [avg={avgdeltat:.2f}], ovh~{overheads.mean():.2f} #={len(self.histos)}")

            self.histos[ now ] = [ 0, self.h1np ]



            # least_dist = 1000*1000
            # least_who = now
            # --------- set proper delta times
            removekeys = []
            for k,v in self.histos.items():
                age = (now - k).total_seconds()
                if age>self.store_limit:
                    #self.histos.pop(k)
                    removekeys.append(k)
                else:
                    self.histos[k][0] = age
            for key in removekeys:
                self.histos.pop(key)



            self.deltat = ( now - lastnow ).total_seconds()
            lastnow = now



            # ALL PREPARED.......... announce and sleep.......
            self.fflag = True


            # SLEEP WISELY----------------------------------------------------
            #--------------------------calculate deltas(web) and overhead(code)
            # and sleep.
            if avgdeltat/2<self.STEP:
                slp = self.STEP - avgdeltat/2 - overheads.mean()
                if slp<0.1: slp = 0.1
                time.sleep( slp )
            if len(overheads)>20:
                overheads = np.delete( overheads,0)
            if len(deltas)>20:
                deltas = np.delete( deltas,0) # delete 1st member






if __name__=="__main__":
    b0c01 = Histogram("192.168.250.60", "b0c01")
    b0c01.start2collect()
    print("__________________-")
