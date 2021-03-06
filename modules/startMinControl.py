#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------
# File Name: startMinControl.py
# Purpose:
# Creation Date: 21-12-2016
# Last Modified: Wed, Jan 25, 2017  2:40:53 PM
# Author(s): The DeepSEQ Team, University of Nottingham UK
# Copyright 2016 The Author(s) All Rights Reserved
# Credits:
# --------------------------------------------------

from sql import create_mincontrol_interaction_table, \
                    create_mincontrol_messages_table, \
                    create_mincontrol_barcode_control_table

import subprocess
import sys , os
import time
import socket
from exit_gracefully import terminate_mincontrol


def startMincontrol(args, cursor, dbcheckhash, \
                        minup_version, oper):

    dbname = None

    # -------- mincontrol --------
    # # get the IP address of the host

    ip = '127.0.0.1'
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception, err:
        err_string = 'Error obtaining upload IP adress'
        #print >> sys.stderr, err_string
        print err_string




    if args.pin is not False:
        if args.verbose == "high":
            print 'starting mincontrol'
            sys.stdout.flush()
        control_ip = ip
        if args.ip_address is not False:
            control_ip = args.ip_address

        # print "IP", control_ip
        # else the IP is the address of this machine

        '''
        create_mincontrol_interaction_table('interaction', cursor)
        create_mincontrol_messages_table('messages', cursor)
        create_mincontrol_barcode_control_table('barcode_control',
                cursor)
        '''

        try:
            terminate_mincontrol(args, dbcheckhash, oper, minup_version)
            time.sleep(2)
            if oper is 'linux':
                '''
                #  pre 16.11.16
                cmd = \
                    'python mincontrol.py -dbh %s -dbu %s -dbp %d -pw %s -db %s -pin %s -ip %s' \
                    % (
                    args.dbhost,
                    args.dbusername,
                    args.dbport,
                    args.dbpass,
                    dbname,
                    args.pin,
                    control_ip,
                    )
                '''
                cmd = \
                    'python mincontrol.py -ws %s -dbh %s -dbu %s -dbp %d -pw %s -pin %s -ip %s' \
                    % (
                    args.dbhost,
                    args.dbhost,
                    args.dbusername,
                    args.dbport,
                    args.dbpass,
                    args.pin,
                    control_ip,
                    )

                if args.verbose == "high": print "CMD", cmd

                subprocess.Popen(cmd, stdout=None, stderr=None,
                        stdin=None, shell=True)
            if oper is 'windows':
                '''
                # Pre 16.11.16
                cmd = \
                    '.\mincontrol.exe -dbh %s -dbu %s -dbp %d -pw %s -db %s -pin %s -ip %s' \
                    % (
                    args.dbhost,
                    args.dbusername,
                    args.dbport,
                    args.dbpass,
                    dbname,
                    args.pin,
                    control_ip,
                    )
                '''
                cmd = \
                    '.\mincontrol.exe -ws %s -dbh %s -dbu %s -dbp %d -pw %s -pin %s -ip %s' \
                    % (
                    args.dbhost,
                    args.dbhost,
                    args.dbusername,
                    args.dbport,
                   args.dbpass,
                    args.pin,
                    control_ip,
                    )
            else:
                cmd = \
                    'python mincontrol.py -ws %s -dbh %s -dbu %s -dbp %d -pw %s -pin %s -ip %s' \
                    % (
                    args.dbhost,
                    args.dbhost,
                    args.dbusername,
                    args.dbport,
                    args.dbpass,
                    args.pin,
                    control_ip,
                    )
                
            if args.verbose == "high": print "CMD", cmd

            subprocess.Popen(cmd, stdout=None, stderr=None,
                        stdin=None, shell=False)  # , creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception, err:
            err_string = 'Error starting mincontrol: %s ' % err
            print >> sys.stderr, err_string
            sys.stdout.flush()
            #with open(dbcheckhash['logfile'][dbname], 'a') as \
            #    logfilehandle:
            #    logfilehandle.write(err_string + os.linesep)
            #    logfilehandle.close()
    return ip
