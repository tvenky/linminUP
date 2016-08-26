#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------
# File Name: add_minoTour_meta_to_hdf.py
# Purpose:
# Creation Date: 08-06-2016
# Last Modified: Fri, Aug 26, 2016 12:25:43 PM
# Author(s): The DeepSEQ Team, University of Nottingham UK
# Copyright 2016 The Author(s) All Rights Reserved
# Credits: 
# --------------------------------------------------

import h5py, sys
from debug import debug
import string
printable = set(string.printable)

import re
comment = re.compile(r'#.+')

def fix(s): 
    return ' '.join(s.split())

def add_metadata_to_hdf(args, metadataFile, fast5file):
    
    print "Adding minoTour_meta to fast5 file... ", fast5file

    lines = filter(None, open(metadataFile, "r").read().splitlines())

    with h5py.File(fast5file, "a") as hdf:

        mainGroup = "/minoTour_meta"
        try: del(hdf["/minoTour_meta"])
        except: 
            if args.verbose == "high":
                print "No minoTour_meta group in fast5 file"
            pass

        try: 
            if args.verbose == "high":
                print "Adding Group: ", mainGroup
            hdf.create_group(mainGroup)
        except: 
            if args.verbose == "high":
                print "Adding Group: $s -- FAILED" % (mainGroup)
            pass


        for s in lines: 
          s = filter(lambda x: x in printable, s)
          s = re.sub(comment, '', s)
          s = fix(s)
          if s!='':
            if not ': ' in s: 
                if args.verbose == "high":
                    print "Adding Group:" , s
                try: grp = hdf.create_group(mainGroup+"/"+s)
                except: 
                    if args.verbose == "high":
                        print "Adding Group: %s -- FAILED" % (s)
                    pass
            else: 
                if args.verbose == "high":
                    print "Adding Att:" , s
                xs = s.split(': ')
                x = fix(xs[0])
                y = ': '.join(xs[1:])
                
                try:  grp.attrs[x] = y
                except: 
                    if args.verbose == "high":
                        print "Adding Att: %s -- FAILED" % (x)
                    pass

    print "... metadata added."
